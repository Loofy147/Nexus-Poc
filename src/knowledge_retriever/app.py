import os
import numpy as np
import faiss
from flask import Flask, jsonify, request
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

# --- Configuration & Initialization ---
NEO4J_URI = os.environ.get("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.environ.get("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.environ.get("NEO4J_PASSWORD", "password")

try:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    driver.verify_connectivity()
    print("Knowledge Retriever: Successfully connected to Neo4j.")
except Exception as e:
    print(f"Knowledge Retriever: Could not connect to Neo4j: {e}")
    driver = None

# Load a pre-trained model for generating embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
embedding_dim = model.get_sentence_embedding_dimension()

# Initialize a FAISS index
faiss_index = faiss.IndexFlatL2(embedding_dim)
# In-memory mapping from FAISS index ID to Neo4j node ID
index_to_doc_id = {}
doc_id_counter = 0

# --- Data Population Endpoint ---
@app.route('/populate', methods=['POST'])
def populate_knowledge():
    global doc_id_counter
    if not driver:
        return jsonify({"error": "Database connection is not available."}), 503

    # Sample data representing interconnected concepts
    documents = [
        {"id": "doc1", "text": "The orchestrator is the central component of the NEXUS system."},
        {"id": "doc2", "text": "NEXUS uses a microservices architecture for modularity and scalability."},
        {"id": "doc3", "text": "Redis is used for the memory layer to ensure high performance."},
        {"id": "doc4", "text": "The execution sandbox provides a secure environment for running code."},
    ]
    relationships = [
        ("doc1", "RELATES_TO", "doc2"),
        ("doc3", "IS_COMPONENT_OF", "doc2"),
        ("doc4", "IS_COMPONENT_OF", "doc2"),
    ]

    # Create embeddings and add to FAISS
    doc_texts = [doc['text'] for doc in documents]
    embeddings = model.encode(doc_texts, convert_to_tensor=False)
    faiss_index.add(np.array(embeddings))

    # Store mappings
    for doc in documents:
        index_to_doc_id[doc_id_counter] = doc['id']
        doc_id_counter += 1

    # Add data to Neo4j
    with driver.session() as session:
        # Clear old data
        session.run("MATCH (n) DETACH DELETE n")
        # Add documents as nodes
        for doc in documents:
            session.run("CREATE (d:Document {id: $id, text: $text})", id=doc['id'], text=doc['text'])
        # Add relationships
        for rel in relationships:
            session.run("""
                MATCH (a:Document {id: $start_node})
                MATCH (b:Document {id: $end_node})
                CREATE (a)-[:""" + rel[1] + """]->(b)
            """, start_node=rel[0], end_node=rel[2])

    print(f"Knowledge Retriever: Populated database with {len(documents)} documents and {len(relationships)} relationships.")
    return jsonify({"status": "success", "documents_added": len(documents)}), 201

# --- Hybrid Search Endpoint ---
@app.route('/hybrid_search', methods=['POST'])
def hybrid_search():
    if not driver:
        return jsonify({"error": "Database connection is not available."}), 503

    data = request.get_json()
    query = data.get('query')
    k = data.get('k', 3) # Number of results to return

    # 1. Vector Search (FAISS)
    query_embedding = model.encode([query])
    distances, indices = faiss_index.search(np.array(query_embedding), k)

    vector_hits = []
    hit_ids = []
    for i, idx in enumerate(indices[0]):
        doc_id = index_to_doc_id.get(idx)
        if doc_id:
            vector_hits.append({"id": doc_id, "score": float(distances[0][i])})
            hit_ids.append(doc_id)

    # 2. Graph Expansion (Neo4j)
    graph_expansions = []
    if hit_ids:
        with driver.session() as session:
            result = session.run("""
                MATCH (d:Document)-[r]-(related:Document)
                WHERE d.id IN $ids
                RETURN d.id AS source, type(r) AS relationship, related.id AS target
            """, ids=hit_ids)
            for record in result:
                graph_expansions.append({
                    "source": record["source"],
                    "relationship": record["relationship"],
                    "target": record["target"]
                })

    response = {
        "document_hits": vector_hits,
        "graph_expansions": graph_expansions
    }

    print(f"Knowledge Retriever: Performed hybrid search for query '{query}'. Found {len(vector_hits)} vector hits and {len(graph_expansions)} graph expansions.")
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)