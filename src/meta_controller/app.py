import os
import requests
import json
from flask import Flask, jsonify, request

app = Flask(__name__)

PROMETHEUS_URL = os.environ.get("PROMETHEUS_URL", "http://localhost:9090")
CODE_MODIFIER_URL = os.environ.get("CODE_MODIFIER_URL", "http://localhost:6001") # Port for the new service

# In-memory storage for the current objective
current_objective = {}

@app.route('/api/v1/objective', methods=['POST'])
def set_objective():
    """
    Sets a high-level strategic goal for the system.
    Example: {"goal": "reduce_p95_latency", "target": 0.5}
    """
    global current_objective
    data = request.get_json()
    goal = data.get('goal')
    target = data.get('target')

    if not goal or not target:
        return jsonify({"error": "A 'goal' and 'target' are required."}), 400

    current_objective = {"goal": goal, "target": float(target)}
    print(f"Meta Controller: New objective set -> Goal: {goal}, Target: {target}")

    # Trigger an immediate analysis based on the new goal
    analyze_and_act()

    return jsonify({"status": "Objective set successfully."}), 200

def analyze_and_act():
    """
    The core loop for the meta-controller. It observes, analyzes, and decides.
    """
    if not current_objective:
        print("Meta Controller: No objective set. Standing by.")
        return

    print("Meta Controller: Analyzing system performance against objective.")

    if current_objective.get('goal') == 'reduce_p95_latency':
        try:
            # Query Prometheus for the orchestrator's request latency histogram
            query = 'histogram_quantile(0.95, sum(rate(flask_http_request_duration_seconds_bucket{job="orchestrator"}[5m])) by (le))'
            response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={'query': query})
            response.raise_for_status()
            result = response.json()['data']['result']

            if not result:
                print("Meta Controller: No performance data available from Prometheus yet.")
                return

            current_latency = float(result[0]['value'][1])
            target_latency = current_objective.get('target')

            print(f"Meta Controller: Current p95 latency is {current_latency:.4f}s. Target is {target_latency}s.")

            # Decision-making logic
            if current_latency > target_latency:
                print(f"Meta Controller: DECISION - Performance target missed. Proposing action.")
                # In a full implementation, this would trigger a call to the code_modifier
                # For now, we will just log the intended action.
                propose_modification({
                    "service": "orchestrator",
                    "type": "performance_optimization",
                    "description": f"Current p95 latency {current_latency:.4f}s exceeds target of {target_latency}s. Suggest caching or query optimization."
                })
            else:
                print("Meta Controller: DECISION - Performance target met. No action needed.")

        except requests.exceptions.RequestException as e:
            print(f"Meta Controller: Could not connect to Prometheus: {e}")
        except Exception as e:
            print(f"Meta Controller: An error occurred during analysis: {e}")

def propose_modification(proposal):
    """
    A placeholder function to simulate calling the code_modifier service.
    """
    print(f"Meta Controller: Proposing code modification -> {json.dumps(proposal)}")
    # try:
    #     response = requests.post(f"{CODE_MODIFIER_URL}/propose", json=proposal)
    #     response.raise_for_status()
    #     print("Meta Controller: Proposal sent to Code Modifier successfully.")
    # except requests.exceptions.RequestException as e:
    #     print(f"Meta Controller: Failed to send proposal to Code Modifier: {e}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)