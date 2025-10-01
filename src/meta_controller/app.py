import json
import os

import numpy as np
import pandas as pd
import requests
from advanced_metrics import AdvancedMetricsCollector

# Import the new enterprise-grade modules
# from causal_engine import EnterpriseCausalEngine # MOCKED
from flask import Flask, jsonify, request
from prometheus_flask_exporter import Counter, PrometheusMetrics
from risk_assessor import EnterpriseRiskAssessor

app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Define a custom business metric to track meta-controller decisions
decisions_total = Counter(
    "nexus_decisions_total",
    "Total decisions made by the meta-controller",
    ["decision_type", "outcome"],
)

PROMETHEUS_URL = os.environ.get("PROMETHEUS_URL", "http://prometheus:9090")
CODE_MODIFIER_URL = os.environ.get("CODE_MODIFIER_URL", "http://code_modifier:6001")

# Instantiate the core intelligence engines
# causal_engine = EnterpriseCausalEngine() # MOCKED
metrics_collector = AdvancedMetricsCollector(prometheus_url=PROMETHEUS_URL)

# In-memory storage for the current objective
current_objective = {}


@app.route("/api/v1/objective", methods=["POST"])
def set_objective():
    """
    Sets a high-level strategic goal for the system.
    Example: {"goal": "reduce_latency", "target_metric": "latency", "intervention": "enable_caching", "affected_metrics": ["latency", "error_rate"]}
    """
    global current_objective
    data = request.get_json()

    if not all(
        k in data for k in ["goal", "target_metric", "intervention", "affected_metrics"]
    ):
        return (
            jsonify(
                {
                    "error": "A 'goal', 'target_metric', 'intervention', and 'affected_metrics' list are required."
                }
            ),
            400,
        )

    current_objective = data
    print(f"Meta Controller: New objective set -> {json.dumps(current_objective)}")

    analyze_and_act()
    return jsonify({"status": "Objective set and analysis triggered."}), 200


def analyze_and_act():
    """
    The core OODA loop, orchestrating the advanced engines.
    """
    if not current_objective:
        print("Meta Controller: No objective set. Standing by.")
        return

    print("\n--- META-CONTROLLER: STARTING ANALYSIS & DECISION CYCLE ---")

    # 1. OBSERVE: Use the AdvancedMetricsCollector - MOCKED
    metrics_report = {
        "raw_metrics": {"p95_latency": 0.15, "request_rate": 10},
        "anomalies": [],
    }

    # 2. ORIENT (Anomaly Detection & Risk Assessment)
    if metrics_report["anomalies"]:
        print(
            f"Meta Controller: DECISION - Critical anomalies detected. Aborting modification cycle. Anomalies: {json.dumps(metrics_report['anomalies'])}"
        )
        decisions_total.labels(
            decision_type=current_objective.get("goal"), outcome="ABORTED_ANOMALY"
        ).inc()
        print("--- META-CONTROLLER: CYCLE END ---\n")
        return

    # For this PoC, we will create a simulated DataFrame for the next steps
    # based on the collected metrics. A full implementation would use a proper
    # time-series dataset from a database like TimescaleDB.
    simulated_historical_data = pd.DataFrame(
        {
            "latency": np.random.normal(
                loc=metrics_report["raw_metrics"].get("p95_latency", 0.1),
                scale=0.05,
                size=100,
            ),
            "error_rate": np.random.normal(loc=0.01, scale=0.005, size=100).clip(0),
            "enable_caching": np.random.randint(0, 2, size=100),
        }
    )

    risk_assessor = EnterpriseRiskAssessor(simulated_historical_data)
    stability_assessment = risk_assessor.assess_stability_risk(
        current_objective.get("affected_metrics", [])
    )

    print(
        f"Meta Controller: Risk assessment complete. Result: {json.dumps(stability_assessment)}"
    )
    if stability_assessment.get("overall_risk_level") == "HIGH":
        print(
            "Meta Controller: DECISION - High stability risk detected. Aborting modification cycle."
        )
        decisions_total.labels(
            decision_type=current_objective.get("goal"), outcome="ABORTED_RISK"
        ).inc()
        print("--- META-CONTROLLER: CYCLE END ---\n")
        return

    # 3. DECIDE (Causal Inference) - MOCKED
    causal_decision = {
        "action": "APPLY_INTERVENTION",
        "intervention": current_objective.get("intervention"),
        "target_metric": current_objective.get("target_metric"),
        "expected_effect": 0.15,  # Dummy value
    }

    print(
        f"Meta Controller: Causal analysis complete. Decision: {json.dumps(causal_decision)}"
    )

    # 4. ACT: Propose modification if intervention is recommended
    action = causal_decision.get("action", "UNKNOWN")
    decisions_total.labels(
        decision_type=current_objective.get("goal"), outcome=action
    ).inc()

    if action == "APPLY_INTERVENTION":
        print("Meta Controller: ACTING on decision. Proposing code modification.")
        proposal = {
            "service": "orchestrator",
            "type": current_objective.get("intervention"),
            "description": f"Causal engine recommends applying intervention '{causal_decision.get('intervention')}' to affect '{causal_decision.get('target_metric')}' with an expected effect of {causal_decision.get('expected_effect'):.4f}.",
        }
        propose_modification(proposal)
    else:
        print(
            f"Meta Controller: ACTING on decision. Outcome is '{action}'. No intervention required."
        )

    print("--- META-CONTROLLER: ANALYSIS & DECISION CYCLE COMPLETE ---\n")


def propose_modification(proposal):
    """
    Sends a modification proposal to the code_modifier service.
    """
    print(
        f"Meta Controller: Sending proposal to Code Modifier -> {json.dumps(proposal)}"
    )
    try:
        response = requests.post(
            f"{CODE_MODIFIER_URL}/propose", json=proposal, timeout=30
        )
        response.raise_for_status()
        print("Meta Controller: Proposal sent successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Meta Controller: Failed to send proposal to Code Modifier: {e}")


if __name__ == "__main__":
    # Note: Binding to 0.0.0.0 is for containerized environments.
    app.run(host="0.0.0.0", port=6000)  # nosec
