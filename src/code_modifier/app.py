import os
import json
from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# The root directory of the source code, which will be mounted as a volume.
SRC_CODE_PATH = "/app/src_code"

@app.route('/propose', methods=['POST'])
def propose_modification():
    """
    Receives a code modification proposal from the meta_controller.
    For this PoC, it appends a comment to the target file instead of modifying the code.
    """
    data = request.get_json()
    service = data.get('service')
    description = data.get('description')

    if not service or not description:
        return jsonify({"error": "A 'service' and 'description' are required."}), 400

    # Log the proposal for auditing
    print(f"Code Modifier: Received proposal for service '{service}': {description}")

    # For this professional PoC, we simulate the change by appending a comment.
    # This provides a safe, auditable way to demonstrate the self-modification principle.
    target_file_path = os.path.join(SRC_CODE_PATH, service, "app.py")

    if not os.path.exists(target_file_path):
        print(f"Code Modifier: Target file '{target_file_path}' does not exist.")
        return jsonify({"error": f"Target service '{service}' not found."}), 404

    try:
        with open(target_file_path, "a") as f:
            timestamp = datetime.utcnow().isoformat()
            comment = f"\n# [SELF-MODIFICATION PROPOSAL @ {timestamp}] - {description}\n"
            f.write(comment)

        print(f"Code Modifier: Successfully applied simulated modification to '{target_file_path}'.")
        return jsonify({
            "status": "success",
            "message": f"Simulated modification applied to {service}."
        }), 200

    except Exception as e:
        print(f"Code Modifier: Failed to apply modification: {e}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6001)