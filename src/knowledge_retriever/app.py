import os
import sys
from enterprise_graph_rag import EnterpriseGraphRAG
from flask import Flask, jsonify, request

# Add src to path to allow direct import of security module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from security.vault_client import VaultClient

app = Flask(__name__)

# --- Configuration & Initialization ---
def get_database_credentials():
    """
    Fetches database credentials, prioritizing Vault over environment variables.
    """
    # Try to fetch from Vault first
    if os.getenv("VAULT_ADDR") and os.getenv("VAULT_TOKEN"):
        try:
            vault_client = VaultClient()
            secrets = vault_client.get_secret("knowledge-retriever/neo4j")
            if secrets and 'username' in secrets and 'password' in secrets:
                print("Knowledge Retriever: Successfully fetched credentials from Vault.")
                return secrets['username'], secrets['password']
        except Exception as e:
            print(f"Knowledge Retriever: Failed to fetch credentials from Vault: {e}. Falling back to env vars.")

    # Fallback to environment variables
    print("Knowledge Retriever: Using environment variables for credentials.")
    return os.environ.get("NEO4J_USER", "neo4j"), os.environ.get("NEO4J_PASSWORD", "password")

neo4j_user, neo4j_password = get_database_credentials()

config = {
    "neo4j_uri": os.environ.get("NEO4J_URI", "bolt://localhost:7687"),
    "neo4j_user": neo4j_user,
    "neo4j_password": neo4j_password,
}
graph_rag_engine = EnterpriseGraphRAG(config)


# --- Data Population Endpoint ---
@app.route("/populate", methods=["POST"])
def populate_knowledge():
    """
    Populates the knowledge graph using the advanced ingestion pipeline.
    Expects a JSON payload: {"documents": ["text1", "text2"]}
    """
    data = request.get_json()
    documents = data.get("documents")

    if not documents or not isinstance(documents, list):
        return jsonify({"error": "Request must include a 'documents' list."}), 400

    try:
        graph_rag_engine.populate_knowledge_graph(documents)
        return (
            jsonify(
                {
                    "status": "success",
                    "message": f"{len(documents)} documents are being processed.",
                }
            ),
            202,
        )
    except Exception as e:
        print(f"Knowledge Retriever Service: Error during population: {e}")
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500


# --- Advanced Query Endpoint ---
@app.route("/query", methods=["POST"])
def query():
    """
    Performs an advanced query using the EnterpriseGraphRAG engine.
    Expects a JSON payload: {"query": "Your question here"}
    """
    data = request.get_json()
    question = data.get("query")

    if not question:
        return jsonify({"error": "Request must include a 'query'."}), 400

    try:
        result = graph_rag_engine.query(question)
        return jsonify(result), 200
    except Exception as e:
        print(f"Knowledge Retriever Service: Error during query: {e}")
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500


if __name__ == "__main__":
    # For standalone testing, you might want to populate some data first.
    # To do this, send a POST request to /populate.
    # Note: Binding to 0.0.0.0 is for containerized environments.
    app.run(host="0.0.0.0", port=5003)  # nosec
