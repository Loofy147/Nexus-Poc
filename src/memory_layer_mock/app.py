from flask import Flask, jsonify, request
import os
import json

app = Flask(__name__)
MEMORY_DIR = "/tmp/nexus_memory"

if not os.path.exists(MEMORY_DIR):
    os.makedirs(MEMORY_DIR)

@app.route('/memory/store', methods=['POST'])
def store_memory():
    data = request.get_json()
    user_id = data.get('user_id')
    session_id = data.get('session_id')
    event = data.get('event')

    if not user_id or not session_id or not event:
        return jsonify({"error": "Missing required fields"}), 400

    session_file = os.path.join(MEMORY_DIR, f"{user_id}_{session_id}.json")

    with open(session_file, 'a') as f:
        f.write(json.dumps(event) + '\n')

    print(f"Memory Layer Mock: Stored event for user {user_id}, session {session_id}")
    return jsonify({"status": "success"}), 201

@app.route('/memory/retrieve', methods=['POST'])
def retrieve_memory():
    data = request.get_json()
    user_id = data.get('user_id')
    session_id = data.get('session_id')

    if not user_id or not session_id:
        return jsonify({"error": "Missing required fields"}), 400

    session_file = os.path.join(MEMORY_DIR, f"{user_id}_{session_id}.json")

    if os.path.exists(session_file):
        with open(session_file, 'r') as f:
            events = [json.loads(line) for line in f]
        print(f"Memory Layer Mock: Retrieved {len(events)} events for user {user_id}, session {session_id}")
        return jsonify(events), 200
    else:
        return jsonify([]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)