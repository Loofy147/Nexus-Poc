import os
import json
import redis
from flask import Flask, jsonify, request

app = Flask(__name__)

# Connect to Redis
# The host is provided by Docker Compose.
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
try:
    redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)
    redis_client.ping()
    print("Memory Layer: Successfully connected to Redis.")
except redis.exceptions.ConnectionError as e:
    print(f"Memory Layer: Could not connect to Redis: {e}")
    redis_client = None

@app.route('/memory/store', methods=['POST'])
def store_memory():
    if not redis_client:
        return jsonify({"error": "Memory service is not available."}), 503

    data = request.get_json()
    user_id = data.get('user_id')
    session_id = data.get('session_id')
    event = data.get('event')

    if not all([user_id, session_id, event]):
        return jsonify({"error": "Missing required fields"}), 400

    # Use a Redis list to store session events
    session_key = f"session:{user_id}:{session_id}"
    redis_client.rpush(session_key, json.dumps(event))

    print(f"Memory Layer: Stored event for session '{session_key}' in Redis.")
    return jsonify({"status": "success"}), 201

@app.route('/memory/retrieve', methods=['POST'])
def retrieve_memory():
    if not redis_client:
        return jsonify({"error": "Memory service is not available."}), 503

    data = request.get_json()
    user_id = data.get('user_id')
    session_id = data.get('session_id')

    if not all([user_id, session_id]):
        return jsonify({"error": "Missing required fields"}), 400

    session_key = f"session:{user_id}:{session_id}"

    # Retrieve all events from the list
    events_raw = redis_client.lrange(session_key, 0, -1)
    events = [json.loads(event) for event in events_raw]

    print(f"Memory Layer: Retrieved {len(events)} events for session '{session_key}' from Redis.")
    return jsonify(events), 200

if __name__ == '__main__':
    # Rename the service to reflect its new implementation
    app.run(host='0.0.0.0', port=5004)