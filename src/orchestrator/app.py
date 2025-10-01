import os
import requests
import re
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

# --- Service URLs ---
# Updated to reflect the new enterprise-grade services
AGENT_MANAGER_URL = os.environ.get("AGENT_MANAGER_URL", "http://localhost:5002")
KNOWLEDGE_RETRIEVER_URL = os.environ.get("KNOWLEDGE_RETRIEVER_URL", "http://localhost:5003")
MEMORY_LAYER_URL = os.environ.get("MEMORY_LAYER_URL", "http://localhost:5004")
EXECUTION_SANDBOX_URL = os.environ.get("EXECUTION_SANDBOX_URL", "http://localhost:5005")
LLM_ADAPTER_URL = os.environ.get("LLM_ADAPTER_URL", "http://localhost:5006")

def extract_code(text):
    """Extracts python code from a markdown code block."""
    match = re.search(r"```python\n(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1)
    return None

def format_knowledge_for_prompt(knowledge_context):
    """Formats the rich context from the knowledge retriever for the LLM."""
    prompt_context = "Relevant Documents (from vector search):\n"
    for hit in knowledge_context.get('document_hits', []):
        prompt_context += f"- ID: {hit.get('id')}, Score: {hit.get('score')}\n"

    prompt_context += "\nRelated Concepts (from graph expansion):\n"
    for expansion in knowledge_context.get('graph_expansions', []):
        prompt_context += f"- {expansion.get('source')} -> {expansion.get('relationship')} -> {expansion.get('target')}\n"

    return prompt_context

@app.route('/api/v1/query', methods=['POST'])
def query_handler():
    data = request.get_json()
    user_id = data.get('user_id')
    session_id = data.get('session_id')
    query = data.get('query')

    if not all([user_id, session_id, query]):
        return jsonify({"error": "user_id, session_id, and query are required"}), 400

    print(f"Orchestrator: Received query: '{query}' for user '{user_id}'")

    # 1. Retrieve memory
    try:
        memory_payload = {'user_id': user_id, 'session_id': session_id}
        memory_response = requests.post(f"{MEMORY_LAYER_URL}/memory/retrieve", json=memory_payload)
        session_history = memory_response.json()
        print(f"Orchestrator: Retrieved {len(session_history)} events from memory.")
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to Memory Layer: {e}"}), 503

    # 2. Retrieve knowledge from the new enterprise-grade retriever
    try:
        knowledge_payload = {'query': query}
        knowledge_response = requests.post(f"{KNOWLEDGE_RETRIEVER_URL}/hybrid_search", json=knowledge_payload)
        knowledge_context = knowledge_response.json()
        print("Orchestrator: Retrieved rich context from Knowledge Retriever.")
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to Knowledge Retriever: {e}"}), 503

    # 3. Interact with LLM, providing the rich, formatted context
    try:
        formatted_context = format_knowledge_for_prompt(knowledge_context)
        llm_prompt = f"You are an expert assistant. Use the following context to answer the user's query.\n\n--- Context ---\n{formatted_context}\n--- History ---\n{session_history}\n\n--- Query ---\n{query}\n\nBased on the query, if a user asks to run code, provide a Python script in a markdown block. Otherwise, provide a helpful and context-aware answer."
        llm_payload = {'prompt': llm_prompt}
        llm_response = requests.post(f"{LLM_ADAPTER_URL}/llm/generate", json=llm_payload)
        llm_result = llm_response.json()
        llm_answer = llm_result.get('answer')
        print("Orchestrator: Received intelligent response from LLM Adapter.")
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to connect to LLM Adapter: {e}"}), 503

    # 4. Execute code if a script is present in the LLM's response
    execution_result = None
    code_to_execute = extract_code(llm_answer)

    if code_to_execute:
        try:
            print("Orchestrator: Code found. Dispatching to hardened Execution Sandbox.")
            execution_payload = {"language": "python", "code": code_to_execute}
            exec_response = requests.post(f"{EXECUTION_SANDBOX_URL}/execute", json=execution_payload)
            execution_result = exec_response.json()
            print("Orchestrator: Received result from hardened Execution Sandbox.")
        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Failed to connect to Execution Sandbox: {e}"}), 503

    # 5. Store event in memory
    try:
        event_payload = {'user_id': user_id, 'session_id': session_id, 'event': {'query': query, 'response': llm_result, 'execution': execution_result}}
        requests.post(f"{MEMORY_LAYER_URL}/memory/store", json=event_payload)
        print("Orchestrator: Stored event in memory.")
    except requests.exceptions.RequestException as e:
        print(f"Orchestrator: Could not store event in Memory Layer: {e}")

    # 6. Consolidate and return response
    final_response = {
        "query": query,
        "llm_answer": llm_answer,
        "execution_result": execution_result,
        "knowledge_source": "Enterprise Graph-RAG Retriever"
    }

    return jsonify(final_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)