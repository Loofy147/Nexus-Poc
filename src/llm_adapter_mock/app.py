from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/llm/generate', methods=['POST'])
def generate():
    data = request.get_json()
    prompt = data.get('prompt')

    print(f"LLM Adapter Mock: Received prompt: {prompt[:100]}...") # Log first 100 chars

    # Mocked LLM response
    mock_response = {
        "answer": "Based on the retrieved context, the recommended next step is to execute a code snippet to verify the information.",
        "action_plan": {
            "agent": "execution_agent",
            "payload": {
                "language": "python",
                "code": "print('Verifying information...')"
            }
        }
    }

    return jsonify(mock_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)