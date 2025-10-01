import os

from flask import Flask, jsonify, request

# Import the new enterprise-grade engine
from safe_code_modifier import EnterpriseCodeModifier

app = Flask(__name__)

# Instantiate the code modifier engine
# This can be configured via a file, but for now, we use defaults.
config = {
    "pylint_threshold": 8.0,
    "min_security_score": 95.0,  # Placeholder for a more complex scoring system
}
code_modifier_engine = EnterpriseCodeModifier(config=config)


@app.route("/propose", methods=["POST"])
def propose_modification():
    """
    Receives a code modification proposal from the meta_controller
    and triggers the full enterprise modification pipeline.
    """
    modification_request = request.get_json()

    if not modification_request:
        return jsonify({"error": "Invalid JSON payload."}), 400

    print(f"Code Modifier Service: Received request -> {modification_request}")

    # Trigger the full pipeline
    result = code_modifier_engine.apply_modification(modification_request)

    print(
        f"Code Modifier Service: Pipeline finished with status: {result.get('status')}"
    )

    if result.get("status") == "SUCCESS":
        return jsonify(result), 200
    else:
        # Return a server error if the modification pipeline failed
        return jsonify(result), 500


if __name__ == "__main__":
    # Note: Binding to 0.0.0.0 is for containerized environments.
    # In a production deployment, this should be a configurable, specific interface.
    app.run(host="0.0.0.0", port=6001)  # nosec
