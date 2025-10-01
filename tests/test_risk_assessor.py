import numpy as np
import pandas as pd
import pytest

# Add src to path to allow direct import
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.meta_controller.risk_assessor import EnterpriseRiskAssessor

@pytest.fixture
def stationary_data():
    """Fixture for stationary, low-volatility time series data."""
    np.random.seed(42)
    return pd.DataFrame({
        'metric1': np.random.randn(200),
        'metric2': np.random.randn(200) * 0.1, # Even lower volatility
    })

@pytest.fixture
def non_stationary_data():
    """Fixture for non-stationary (trend) time series data."""
    np.random.seed(42)
    return pd.DataFrame({
        'metric1': np.arange(200) + np.random.randn(200) * 0.5,
    })

@pytest.fixture
def high_volatility_data():
    """Fixture for stationary but high-volatility data."""
    np.random.seed(42)
    # Create a series with changing variance
    volatility = np.ones(200)
    volatility[100:] = 3
    return pd.DataFrame({
        'metric1': np.random.randn(200) * volatility,
    })


def test_stationary_low_volatility_series(stationary_data):
    """
    Test that a stationary series with low volatility is assessed as LOW risk.
    """
    assessor = EnterpriseRiskAssessor(stationary_data)
    result = assessor.assess_stability_risk(['metric1', 'metric2'])

    assert result['overall_risk_level'] == 'LOW'
    assert not result['high_risk_metrics']

    # Check metric1 assessment
    metric1_assessment = result['metric_assessments']['metric1']
    assert metric1_assessment['consensus_stationary'] is True
    assert metric1_assessment['confidence'] > 0.5
    assert 'volatility' in metric1_assessment
    assert metric1_assessment['volatility'] is not None

def test_non_stationary_series(non_stationary_data):
    """
    Test that a non-stationary series is assessed as HIGH risk.
    """
    assessor = EnterpriseRiskAssessor(non_stationary_data)
    result = assessor.assess_stability_risk(['metric1'])

    assert result['overall_risk_level'] == 'HIGH'
    assert 'metric1' in result['high_risk_metrics']

    metric1_assessment = result['metric_assessments']['metric1']
    assert metric1_assessment['consensus_stationary'] is False
    assert metric1_assessment['confidence'] < 0.5

def test_high_volatility_series(high_volatility_data):
    """
    Test that a high-volatility series is assessed as HIGH risk, even if stationary.
    """
    assessor = EnterpriseRiskAssessor(high_volatility_data)
    result = assessor.assess_stability_risk(['metric1'])

    assert result['overall_risk_level'] == 'HIGH'
    assert 'metric1' in result['high_risk_metrics']

    metric1_assessment = result['metric_assessments']['metric1']
    # It might be stationary, but the volatility is the key risk factor here
    assert 'volatility' in metric1_assessment
    assert metric1_assessment['volatility'] > 0.5

def test_consensus_logic():
    """
    Directly test the consensus logic of the risk assessor.
    """
    # Dummy assessor, data doesn't matter for this test
    assessor = EnterpriseRiskAssessor(pd.DataFrame())

    # Case 1: All agree on stationary
    all_stationary = {
        'adf': {'is_stationary': True},
        'kpss': {'is_stationary': True},
        'zivot_andrews': {'is_stationary': True}
    }
    consensus = assessor._get_consensus(all_stationary)
    assert consensus['is_stationary'] is True
    assert consensus['confidence'] == 1.0

    # Case 2: Majority agree on stationary
    majority_stationary = {
        'adf': {'is_stationary': True},
        'kpss': {'is_stationary': False},
        'zivot_andrews': {'is_stationary': True}
    }
    consensus = assessor._get_consensus(majority_stationary)
    assert consensus['is_stationary'] is True
    assert consensus['confidence'] == 2/3

    # Case 3: Majority agree on non-stationary
    majority_non_stationary = {
        'adf': {'is_stationary': True},
        'kpss': {'is_stationary': False},
        'zivot_andrews': {'is_stationary': False}
    }
    consensus = assessor._get_consensus(majority_non_stationary)
    assert consensus['is_stationary'] is False
    assert consensus['confidence'] == 1/3

    # Case 4: One test fails
    one_fails = {
        'adf': {'is_stationary': True},
        'kpss': {'error': 'test failed'},
        'zivot_andrews': {'is_stationary': True}
    }
    consensus = assessor._get_consensus(one_fails)
    assert consensus['is_stationary'] is True
    assert consensus['confidence'] == 1.0 # 2 votes out of 2 valid tests