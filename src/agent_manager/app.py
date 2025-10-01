from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/agent/select', methods=['POST'])
def select_agent():
    data = request.get_json()
    query = data.get('query', '').lower()

    print(f"Agent Manager: Received query: {query}")

    # Mocked agent selection logic
    if 'execute' in query or 'run' in query or 'code' in query:
        agent = 'execution_agent'
    elif 'knowledge' in query or 'graph' in query:
        agent = 'knowledge_agent'
    else:
        agent = 'default_agent'

    mock_response = {
        "agent": agent,
        "confidence": 0.95
    }

    print(f"Agent Manager: Selected agent: {agent}")
    return jsonify(mock_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)