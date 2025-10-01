import os
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# Service URLs from environment variables or defaults
AGENT_MANAGER_URL = os.environ.get("AGENT_MANAGER_URL", "http://localhost:5002")
KNOWLEDGE_GRAPH_URL = os.environ.get("KNOWLEDGE_GRAPH_URL", "http://localhost:5003")
MEMORY_LAYER_URL = os.environ.get("MEMORY_LAYER_URL", "http://localhost:5004")
EXECUTION_SANDBOX_URL = os.environ.get("EXECUTION_SANDBOX_URL", "http://localhost:5005")
LLM_ADAPTER_URL = os.environ.get("LLM_ADAPTER_URL", "http://localhost:5006")

@app.route('/api/v1/query', methods=['POST'])
def query_handler():
    data = request.get_json()
    user_id = data.get('user_id')
    session_id = data.get('session_id')
    query = data.get('query')

    if not all([user_id, session_id, query]):
        return jsonify({"error": "user_id, session_id, and query are required"}), 400

    print(f"Orchestrator: Received query: '{query}' for user '{user_id}'")

    # 1. Retrieve memory (simulated for PoC)
    try:
        memory_payload = {'user_id': user_id, 'session_id': session_id}
        memory_response = requests.post(f"{MEMORY_LAYER_URL}/memory/retrieve", json=memory_payload)
        session_history = memory_response.json()
        print(f"Orchestrator: Retrieved {len(session_history)} events from memory.")
    except requests.exceptions.RequestException as e:
        print(f"Orchestrator: Could not connect to Memory Layer: {e}")
        return jsonify({"error": "Failed to connect to Memory Layer"}), 503

    # 2. Select agent
    try:
        agent_payload = {'query': query}
        agent_response = requests.post(f"{AGENT_MANAGER_URL}/agent/select", json=agent_payload)
        agent = agent_response.json().get('agent')
        print(f"Orchestrator: Selected agent '{agent}'.")
    except requests.exceptions.RequestException as e:
        print(f"Orchestrator: Could not connect to Agent Manager: {e}")
        return jsonify({"error": "Failed to connect to Agent Manager"}), 503

    # 3. Retrieve knowledge
    try:
        knowledge_payload = {'query': query}
        knowledge_response = requests.post(f"{KNOWLEDGE_GRAPH_URL}/hybrid_search", json=knowledge_payload)
        knowledge_context = knowledge_response.json()
        print("Orchestrator: Retrieved knowledge context.")
    except requests.exceptions.RequestException as e:
        print(f"Orchestrator: Could not connect to Knowledge Graph: {e}")
        return jsonify({"error": "Failed to connect to Knowledge Graph"}), 503

    # 4. Interact with LLM
    try:
        llm_prompt = f"Context: {knowledge_context}\n\nHistory: {session_history}\n\nQuery: {query}\n\nRespond now."
        llm_payload = {'prompt': llm_prompt}
        llm_response = requests.post(f"{LLM_ADAPTER_URL}/llm/generate", json=llm_payload)
        llm_result = llm_response.json()
        print("Orchestrator: Received response from LLM Adapter.")
    except requests.exceptions.RequestException as e:
        print(f"Orchestrator: Could not connect to LLM Adapter: {e}")
        return jsonify({"error": "Failed to connect to LLM Adapter"}), 503

    # 5. Execute code if needed
    execution_result = None
    if llm_result.get('action_plan') and llm_result['action_plan']['agent'] == 'execution_agent':
        try:
            print("Orchestrator: Dispatching code to Execution Sandbox.")
            execution_payload = llm_result['action_plan']['payload']
            exec_response = requests.post(f"{EXECUTION_SANDBOX_URL}/execute", json=execution_payload)
            execution_result = exec_response.json()
            print("Orchestrator: Received result from Execution Sandbox.")
        except requests.exceptions.RequestException as e:
            print(f"Orchestrator: Could not connect to Execution Sandbox: {e}")
            return jsonify({"error": "Failed to connect to Execution Sandbox"}), 503

    # 6. Store event in memory
    try:
        event_payload = {
            'user_id': user_id,
            'session_id': session_id,
            'event': {'query': query, 'response': llm_result, 'execution': execution_result}
        }
        requests.post(f"{MEMORY_LAYER_URL}/memory/store", json=event_payload)
        print("Orchestrator: Stored event in memory.")
    except requests.exceptions.RequestException as e:
        # Non-critical error, log and continue
        print(f"Orchestrator: Could not store event in Memory Layer: {e}")

    # 7. Consolidate and return response
    final_response = {
        "query": query,
        "llm_answer": llm_result.get('answer'),
        "execution_result": execution_result,
        "knowledge_source": "Graph-RAG Mock"
    }

    return jsonify(final_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)