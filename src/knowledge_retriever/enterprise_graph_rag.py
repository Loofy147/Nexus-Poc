import json
import os
from typing import Dict, List

import faiss
import numpy as np
import spacy
from kg_reasoner import KnowledgeGraphReasoner
from langchain.text_splitter import RecursiveCharacterTextSplitter
from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer


class EnterpriseGraphRAG:
    """
    Enterprise-grade Graph-RAG engine.
    This implementation focuses on the knowledge ingestion pipeline.
    """

    def __init__(self, config: Dict):
        self.config = config
        self.neo4j_driver = GraphDatabase.driver(
            config["neo4j_uri"], auth=(config["neo4j_user"], config["neo4j_password"])
        )
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
        self.vector_dimension = self.embedding_model.get_sentence_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.vector_dimension)
        self.index_to_chunk_id = {}
        self.chunk_id_counter = 0

        try:
            self.nlp = spacy.load("en_core_web_sm")
            print("Enterprise Graph RAG: Spacy model loaded successfully.")
        except IOError:
            print(
                "Enterprise Graph RAG: Spacy model not found. Please run 'python -m spacy download en_core_web_sm'"
            )
            self.nlp = None

        self.kg_reasoner = KnowledgeGraphReasoner(self.neo4j_driver)
        print("Enterprise Graph RAG: Initialized.")

    def populate_knowledge_graph(
        self, documents: List[str], metadata: List[Dict] = None
    ):
        """
        Populates the knowledge graph from documents with entity extraction.
        """
        if not self.nlp:
            print(
                "Enterprise Graph RAG: Cannot populate knowledge graph, Spacy model not loaded."
            )
            return

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n", ". ", " ", ""]
        )

        if metadata is None:
            metadata = [{}] * len(documents)

        for i, doc_text in enumerate(documents):
            chunks = text_splitter.split(doc_text)
            for chunk in chunks:
                doc_nlp = self.nlp(chunk)
                entities = [
                    {"text": ent.text, "label": ent.label_} for ent in doc_nlp.ents
                ]

                doc_id = self._store_chunk_in_neo4j(chunk, entities, metadata[i])

                embedding = self.embedding_model.encode([chunk])
                self.index.add(np.array(embedding))
                self.index_to_chunk_id[self.chunk_id_counter] = doc_id
                self.chunk_id_counter += 1

        print(
            f"Enterprise Graph RAG: Knowledge graph populated with {len(documents)} documents, resulting in {self.chunk_id_counter} chunks."
        )

    def _store_chunk_in_neo4j(
        self, chunk: str, entities: List[Dict], metadata: Dict
    ) -> int:
        """Stores a text chunk and its extracted entities in Neo4j."""
        with self.neo4j_driver.session() as session:
            result = session.run(
                "CREATE (c:Chunk {text: $text, metadata: $metadata}) RETURN id(c)",
                text=chunk,
                metadata=json.dumps(metadata),
            )
            chunk_id = result.single()[0]

            for entity in entities:
                session.run(
                    """
                    MATCH (c:Chunk) WHERE id(c) = $chunk_id
                    MERGE (e:Entity {name: $name, type: $type})
                    MERGE (c)-[:CONTAINS_ENTITY]->(e)
                    """,
                    chunk_id=chunk_id,
                    name=entity["text"],
                    type=entity["label"],
                )
        return chunk_id

    def query(self, question: str, k: int = 5) -> Dict:
        """
        Performs an advanced query using the full Graph-RAG pipeline.
        """
        print(f"Enterprise Graph RAG: Starting advanced query for: '{question}'")
        if not self.nlp:
            return {"error": "NLP model not loaded."}

        # 1. Entity Extraction
        doc_nlp = self.nlp(question)
        entities = [{"text": ent.text, "label": ent.label_} for ent in doc_nlp.ents]
        print(f"Enterprise Graph RAG: Extracted entities: {entities}")

        # 2. Vector Search
        query_embedding = self.embedding_model.encode([question])
        distances, indices = self.index.search(np.array(query_embedding), k)

        vector_hits = []
        for i, idx in enumerate(indices[0]):
            chunk_id = self.index_to_chunk_id.get(idx)
            if chunk_id:
                vector_hits.append(
                    {"chunk_id": chunk_id, "score": float(distances[0][i])}
                )

        print(f"Enterprise Graph RAG: Found {len(vector_hits)} vector hits.")

        # 3. Multi-hop Reasoning
        reasoning_chain = self.kg_reasoner.multi_hop_reasoning(entities)

        # 4. Combine and return results
        response = {
            "question": question,
            "extracted_entities": entities,
            "vector_search_results": vector_hits,
            "graph_reasoning_results": reasoning_chain,
            "answer": "Combined results from vector and graph search. Ready for LLM synthesis.",
        }

        print("Enterprise Graph RAG: Advanced query pipeline complete.")
        return response
