import os
from flask import Flask, jsonify, request
from enterprise_graph_rag import EnterpriseGraphRAG

app = Flask(__name__)

# --- Configuration & Initialization ---
config = {
    "neo4j_uri": os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
    "neo4j_user": os.environ.get("NEO4J_USER", "neo4j"),
    "neo4j_password": os.environ.get("NEO4J_PASSWORD", "password"),
}
graph_rag_engine = EnterpriseGraphRAG(config)

# --- Data Population Endpoint ---
@app.route('/populate', methods=['POST'])
def populate_knowledge():
    """
    Populates the knowledge graph using the advanced ingestion pipeline.
    Expects a JSON payload: {"documents": ["text1", "text2"]}
    """
    data = request.get_json()
    documents = data.get('documents')

    if not documents or not isinstance(documents, list):
        return jsonify({"error": "Request must include a 'documents' list."}), 400

    try:
        graph_rag_engine.populate_knowledge_graph(documents)
        return jsonify({"status": "success", "message": f"{len(documents)} documents are being processed."}), 202
    except Exception as e:
        print(f"Knowledge Retriever Service: Error during population: {e}")
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500


# --- Advanced Query Endpoint ---
@app.route('/query', methods=['POST'])
def query():
    """
    Performs an advanced query using the EnterpriseGraphRAG engine.
    Expects a JSON payload: {"query": "Your question here"}
    """
    data = request.get_json()
    question = data.get('query')

    if not question:
        return jsonify({"error": "Request must include a 'query'."}), 400

    try:
        result = graph_rag_engine.query(question)
        return jsonify(result), 200
    except Exception as e:
        print(f"Knowledge Retriever Service: Error during query: {e}")
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

if __name__ == '__main__':
    # For standalone testing, you might want to populate some data first.
    # To do this, send a POST request to /populate.
    app.run(host='0.0.0.0', port=5003)