import numpy as np
import pandas as pd
import pytest

# Add src to path to allow direct import
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.meta_controller.causal_engine import EnterpriseCausalEngine


@pytest.fixture
def causal_engine():
    """Fixture for the EnterpriseCausalEngine."""
    return EnterpriseCausalEngine()


def test_analyze_and_decide_runs_successfully(causal_engine):
    """
    Test that the main analysis pipeline runs without critical errors using
    an assumed causal structure.
    """
    # Create a realistic, but simulated, DataFrame
    data = pd.DataFrame(
        {
            "latency": np.random.normal(loc=0.2, scale=0.05, size=100),
            "error_rate": np.random.uniform(0.01, 0.05, size=100),
            "cpu_utilization": np.random.normal(loc=50, scale=10, size=100),
            "enable_caching": np.random.randint(0, 2, size=100),
        }
    )

    # Define a strategic goal with assumed confounders
    strategic_goal = {
        "goal": "reduce_latency",
        "target_metric": "latency",
        "intervention": "enable_caching",
        "confounders": ["cpu_utilization", "error_rate"],
    }

    # Run the analysis
    decision = causal_engine.analyze_and_decide(data, strategic_goal)

    # Assertions to ensure the output is as expected
    assert isinstance(decision, dict)
    assert "action" in decision
    assert "expected_effect" in decision
    assert "formally_verified" in decision
    assert "error" not in decision

def test_formal_verification(causal_engine):
    """
    Test the formal verification logic.
    """
    # A decision that should pass verification
    safe_decision = {"expected_effect": 0.1}
    verification = causal_engine.formal_verification(safe_decision)
    assert verification["verified"] is True

    # A decision that should fail verification
    unsafe_decision = {"expected_effect": 1.5}
    verification = causal_engine.formal_verification(unsafe_decision)
    assert verification["verified"] is False

def test_missing_confounder_in_data(causal_engine):
    """
    Test that the engine handles cases where a confounder is missing from the data.
    """
    data = pd.DataFrame({
        "latency": np.random.normal(0.2, 0.05, 100),
        "enable_caching": np.random.randint(0, 2, 100),
    })

    strategic_goal = {
        "goal": "reduce_latency",
        "target_metric": "latency",
        "intervention": "enable_caching",
        "confounders": ["cpu_utilization"], # This column is missing
    }

    decision = causal_engine.analyze_and_decide(data, strategic_goal)

    # Expect the estimation to fail gracefully and return a 0.0 effect
    assert decision["expected_effect"] == 0.0
    # The action should likely be "DO_NOT_APPLY" if the effect is 0
    assert decision["action"] == "DO_NOT_APPLY"