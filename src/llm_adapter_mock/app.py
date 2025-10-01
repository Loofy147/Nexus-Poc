import os
import openai
from flask import Flask, jsonify, request

app = Flask(__name__)

# Get OpenAI API key from environment variable
# The user will need to set this.
api_key = os.environ.get("OPENAI_API_KEY")
if api_key:
    openai.api_key = api_key
else:
    print("Warning: OPENAI_API_KEY environment variable not set. LLM Adapter will not function.")

@app.route('/llm/generate', methods=['POST'])
def generate():
    if not openai.api_key:
        return jsonify({"error": "OpenAI API key is not configured on the server."}), 500

    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "A prompt is required."}), 400

    print(f"LLM Adapter: Received prompt, sending to OpenAI...")

    try:
        # Use the ChatCompletion endpoint
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Based on the provided context, answer the user's query. If the query implies a need for a specific action (like running code), suggest that action clearly."},
                {"role": "user", "content": prompt}
            ]
        )

        message_content = response.choices[0].message['content']

        # NOTE: For this version, we will not be generating a structured action plan.
        # The orchestrator will need to be updated to handle this simpler response.
        # A future improvement would be to use function calling to generate structured plans.
        llm_result = {
            "answer": message_content,
            "action_plan": None
        }

        print("LLM Adapter: Successfully received response from OpenAI.")
        return jsonify(llm_result)

    except openai.error.OpenAIError as e:
        print(f"LLM Adapter: OpenAI API error: {e}")
        return jsonify({"error": f"An OpenAI API error occurred: {str(e)}"}), 503
    except Exception as e:
        print(f"LLM Adapter: An unexpected error occurred: {e}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)