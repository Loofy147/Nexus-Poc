import os
import requests
import json
import pandas as pd
import numpy as np
from flask import Flask, jsonify, request

# Import the new enterprise-grade modules
from causal_engine import EnterpriseCausalEngine
from risk_assessor import EnterpriseRiskAssessor

app = Flask(__name__)

PROMETHEUS_URL = os.environ.get("PROMETHEUS_URL", "http://prometheus:9090")
CODE_MODIFIER_URL = os.environ.get("CODE_MODIFIER_URL", "http://code_modifier:6001")

# Instantiate the core intelligence engines
causal_engine = EnterpriseCausalEngine()

# In-memory storage for the current objective
current_objective = {}

@app.route('/api/v1/objective', methods=['POST'])
def set_objective():
    """
    Sets a high-level strategic goal for the system.
    Example: {"goal": "reduce_latency", "target_metric": "latency", "intervention": "enable_caching", "affected_metrics": ["latency", "error_rate"]}
    """
    global current_objective
    data = request.get_json()

    if not all(k in data for k in ["goal", "target_metric", "intervention", "affected_metrics"]):
        return jsonify({"error": "A 'goal', 'target_metric', 'intervention', and 'affected_metrics' list are required."}), 400

    current_objective = data
    print(f"Meta Controller: New objective set -> {json.dumps(current_objective)}")

    analyze_and_act()
    return jsonify({"status": "Objective set and analysis triggered."}), 200

def fetch_metrics_data(metrics: list, duration: str = '5m', step: str = '15s') -> pd.DataFrame:
    """
    Fetches time-series data from Prometheus for a list of metrics.
    """
    print(f"Meta Controller: Fetching historical data for {metrics} from Prometheus.")
    try:
        # Use a simple query for the PoC; a real system would have more complex queries.
        query = 'rate(flask_http_request_duration_seconds_sum{job="orchestrator"}[1m])'
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/query_range", params={'query': query, 'start': f'now()-{duration}', 'end': 'now()', 'step': step})
        response.raise_for_status()
        latency_data = response.json()['data']['result']

        if not latency_data or not latency_data[0]['values']:
            print("Meta Controller: No data returned from Prometheus.")
            return pd.DataFrame()

        values = latency_data[0]['values']
        df = pd.DataFrame(values, columns=['timestamp', 'latency'])
        df['latency'] = pd.to_numeric(df['latency'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df = df.set_index('timestamp')

        # Simulate other metrics for analysis purposes
        df['error_rate'] = (df['latency'] * np.random.uniform(0.1, 0.5) + np.random.rand(len(df)) * 0.05).clip(0, 1)
        df['enable_caching'] = np.random.randint(0, 2, size=len(df))

        print(f"Meta Controller: Successfully fetched and processed {len(df)} data points.")
        return df
    except (requests.exceptions.RequestException, KeyError, IndexError) as e:
        print(f"Meta Controller: Could not fetch or process data from Prometheus: {e}")
        return pd.DataFrame()

def analyze_and_act():
    """
    The core OODA loop, orchestrating the advanced engines.
    """
    if not current_objective:
        print("Meta Controller: No objective set. Standing by.")
        return

    print("\n--- META-CONTROLLER: STARTING ANALYSIS & DECISION CYCLE ---")

    # 1. OBSERVE: Fetch historical data
    affected_metrics = current_objective.get("affected_metrics", [])
    historical_data = fetch_metrics_data(affected_metrics)

    if historical_data.empty:
        print("Meta Controller: Analysis aborted. No data available.")
        print("--- META-CONTROLLER: CYCLE END ---\n")
        return

    # 2. ORIENT (Risk Assessment)
    risk_assessor = EnterpriseRiskAssessor(historical_data)
    stability_assessment = risk_assessor.assess_stability_risk(affected_metrics)

    print(f"Meta Controller: Risk assessment complete. Result: {json.dumps(stability_assessment)}")
    if stability_assessment['overall_risk_level'] == 'HIGH':
        print("Meta Controller: DECISION - High stability risk detected. Aborting modification cycle to ensure system integrity.")
        print("--- META-CONTROLLER: CYCLE END ---\n")
        return

    # 3. DECIDE (Causal Inference)
    causal_decision = causal_engine.analyze_and_decide(
        metrics_data=historical_data,
        strategic_goal=current_objective
    )

    print(f"Meta Controller: Causal analysis complete. Decision: {json.dumps(causal_decision)}")

    # 4. ACT: Propose modification if intervention is recommended
    if causal_decision.get("action") == "APPLY_INTERVENTION":
        print("Meta Controller: ACTING on decision. Proposing code modification.")
        proposal = {
            "service": "orchestrator",
            "type": "causal_optimization",
            "description": f"Causal engine recommends applying intervention '{causal_decision.get('intervention')}' to affect '{causal_decision.get('target_metric')}' with an expected effect of {causal_decision.get('expected_effect'):.4f}."
        }
        propose_modification(proposal)
    else:
        print("Meta Controller: ACTING on decision. No intervention required.")

    print("--- META-CONTROLLER: ANALYSIS & DECISION CYCLE COMPLETE ---\n")

def propose_modification(proposal):
    """
    Sends a modification proposal to the code_modifier service.
    """
    print(f"Meta Controller: Sending proposal to Code Modifier -> {json.dumps(proposal)}")
    try:
        response = requests.post(f"{CODE_MODIFIER_URL}/propose", json=proposal)
        response.raise_for_status()
        print("Meta Controller: Proposal sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Meta Controller: Failed to send proposal to Code Modifier: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)