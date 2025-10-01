import os
import tempfile

import docker
from flask import Flask, jsonify, request

app = Flask(__name__)

# Connect to the Docker daemon
# Assumes the Docker socket is mounted into the container.
try:
    client = docker.from_env()
    client.ping()
    print("Execution Sandbox: Successfully connected to Docker daemon.")
except Exception as e:
    print(f"Execution Sandbox: Could not connect to Docker daemon: {e}")
    client = None


@app.route("/execute", methods=["POST"])
def execute_code():
    if not client:
        return jsonify({"error": "Execution service is not configured."}), 503

    data = request.get_json()
    language = data.get("language")
    code = data.get("code")

    if language != "python":
        return jsonify({"error": "Unsupported language"}), 400

    if not code:
        return jsonify({"error": "No code provided"}), 400

    # Create a temporary file to hold the user's code
    with tempfile.NamedTemporaryFile(
        mode="w+", suffix=".py", delete=False
    ) as tmp_code_file:
        tmp_code_file.write(code)
        tmp_file_name = tmp_code_file.name
        host_file_path = os.path.abspath(tmp_file_name)
        container_file_path = f"/app/{os.path.basename(tmp_file_name)}"

    try:
        print(f"Execution Sandbox: Running code in isolated container.")
        # Run the code in a new, isolated Docker container
        container = client.containers.run(
            image="python:3.9-slim",
            command=["python", container_file_path],
            volumes={host_file_path: {"bind": container_file_path, "mode": "ro"}},
            mem_limit="64m",  # Strict memory limit
            cpu_shares=512,  # Limit CPU usage (relative weight)
            network_disabled=True,  # Disable networking for security
            remove=True,  # Automatically remove the container when it exits
            detach=False,
            stdout=True,
            stderr=True,
        )

        stdout = container.decode("utf-8")
        stderr = ""  # Stderr is mixed with stdout in this mode, would need different handling for separation

        print("Execution Sandbox: Execution successful.")
        return jsonify({"status": "success", "stdout": stdout, "stderr": stderr}), 200

    except docker.errors.ContainerError as e:
        print(f"Execution Sandbox: Execution failed in container: {e}")
        return (
            jsonify(
                {
                    "status": "error",
                    "stdout": e.container.logs(stdout=True).decode("utf-8"),
                    "stderr": e.container.logs(stderr=True).decode("utf-8"),
                }
            ),
            400,
        )
    except Exception as e:
        print(f"Execution Sandbox: An unexpected error occurred: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up the temporary file
        if os.path.exists(host_file_path):
            os.remove(host_file_path)


if __name__ == "__main__":
    # Note: Binding to 0.0.0.0 is for containerized environments.
    app.run(host="0.0.0.0", port=5005)  # nosec
