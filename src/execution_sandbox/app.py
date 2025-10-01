from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)

# Basic security: prevent dangerous keywords
DANGEROUS_KEYWORDS = ['os', 'subprocess', 'shutil', 'requests', 'urllib', 'socket']

@app.route('/execute', methods=['POST'])
def execute_code():
    data = request.get_json()
    language = data.get('language')
    code = data.get('code')

    if language != 'python':
        return jsonify({"error": "Unsupported language"}), 400

    # PoC-level security check
    for keyword in DANGEROUS_KEYWORDS:
        if keyword in code:
            return jsonify({"error": f"Disallowed keyword '{keyword}' found in code."}), 400

    try:
        print(f"Execution Sandbox: Executing code:\n{code}")
        # Execute the code in a separate process with a timeout
        result = subprocess.run(
            ['python', '-c', code],
            capture_output=True,
            text=True,
            timeout=5 # 5-second timeout
        )

        if result.returncode == 0:
            print(f"Execution Sandbox: Execution successful.")
            return jsonify({
                "status": "success",
                "stdout": result.stdout,
                "stderr": result.stderr
            }), 200
        else:
            print(f"Execution Sandbox: Execution failed.")
            return jsonify({
                "status": "error",
                "stdout": result.stdout,
                "stderr": result.stderr
            }), 400

    except subprocess.TimeoutExpired:
        print(f"Execution Sandbox: Execution timed out.")
        return jsonify({"error": "Execution timed out"}), 408
    except Exception as e:
        print(f"Execution Sandbox: An unexpected error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)