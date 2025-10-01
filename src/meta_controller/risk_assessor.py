import warnings
import json
from typing import Dict, List

import pandas as pd
from arch import arch_model
from statsmodels.tsa.stattools import adfuller, kpss, zivot_andrews


class EnterpriseRiskAssessor:
    """
    Provides multi-dimensional risk assessment for decisions made by the meta-controller.
    This enhanced version uses a multi-test approach for stability assessment
    and includes volatility analysis.
    """

    def __init__(self, historical_data: pd.DataFrame):
        """
        Initializes the risk assessor with historical performance data.
        """
        self.historical_data = historical_data
        self.tests = {
            "adf": self._augmented_dickey_fuller,
            "kpss": self._kwiatkowski_phillips,
            "zivot_andrews": self._zivot_andrews_test,
        }
        print("Enhanced Enterprise Risk Assessor: Initialized.")

    def assess_stability_risk(self, affected_metrics: List[str]) -> Dict:
        """
        Assesses the stability risk of a set of metrics using a consensus-based
        multi-test approach and GARCH volatility modeling.
        """
        print(f"Enterprise Risk Assessor: Assessing stability for metrics: {affected_metrics}")
        assessment_results = {}
        high_risk_metrics = []

        for metric in affected_metrics:
            if metric not in self.historical_data.columns:
                assessment_results[metric] = {"error": "Metric not found"}
                continue

            series = self.historical_data[metric].dropna()
            if len(series) < 30:  # Increased requirement for more advanced tests
                assessment_results[metric] = {"error": "Not enough data"}
                continue

            # Run all stability tests
            test_results = {}
            for test_name, test_func in self.tests.items():
                try:
                    test_results[test_name] = test_func(series)
                except Exception as e:
                    test_results[test_name] = {"error": str(e)}

            # Get consensus on stationarity
            consensus = self._get_consensus(test_results)

            # Model volatility with GARCH
            volatility_result = self._garch_volatility(series)

            assessment_results[metric] = {
                "consensus_stationary": consensus["is_stationary"],
                "confidence": consensus["confidence"],
                "volatility": volatility_result.get('volatility'),
                "individual_tests": test_results,
            }

            if not consensus["is_stationary"] or (volatility_result.get('volatility') is not None and volatility_result.get('volatility', 0) > 0.5):
                high_risk_metrics.append(metric)

        overall_risk_level = "HIGH" if high_risk_metrics else "LOW"
        print(f"Enterprise Risk Assessor: Assessment complete. Overall risk: {overall_risk_level}")

        return {
            "overall_risk_level": overall_risk_level,
            "high_risk_metrics": high_risk_metrics,
            "metric_assessments": assessment_results,
        }

    def _get_consensus(self, results: Dict) -> Dict:
        """Aggregates results from multiple tests to form a consensus."""
        votes_for_stationary = 0
        valid_tests = 0

        # ADF: p-value < 0.05 indicates stationarity
        if "adf" in results and "is_stationary" in results["adf"]:
            valid_tests += 1
            if results["adf"]["is_stationary"]:
                votes_for_stationary += 1

        # KPSS: p-value > 0.05 indicates stationarity
        if "kpss" in results and "is_stationary" in results["kpss"]:
            valid_tests += 1
            if results["kpss"]["is_stationary"]:
                votes_for_stationary += 1

        # Zivot-Andrews: p-value < 0.05 indicates stationarity (rejecting null of unit root)
        if "zivot_andrews" in results and "is_stationary" in results["zivot_andrews"]:
            valid_tests += 1
            if results["zivot_andrews"]["is_stationary"]:
                votes_for_stationary += 1

        if valid_tests == 0:
            return {"is_stationary": False, "confidence": 0.0}

        # Consensus requires a majority vote
        is_stationary = (votes_for_stationary / valid_tests) > 0.5
        confidence = votes_for_stationary / valid_tests

        return {"is_stationary": is_stationary, "confidence": confidence}


    def _augmented_dickey_fuller(self, series: pd.Series) -> Dict:
        """ADF test with auto lag selection."""
        # Use 'c' for regression to correctly identify trends as non-stationary
        result = adfuller(series, autolag='AIC', regression='c')
        p_value = result[1]
        return {
            "statistic": result[0],
            "p_value": p_value,
            "is_stationary": bool(p_value < 0.05),
        }

    def _kwiatkowski_phillips(self, series: pd.Series) -> Dict:
        """KPSS test with auto lag selection."""
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            result = kpss(series, regression="c", nlags="auto")
        p_value = result[1]
        return {
            "statistic": result[0],
            "p_value": p_value,
            "is_stationary": bool(p_value > 0.05),
        }

    def _zivot_andrews_test(self, series: pd.Series) -> Dict:
        """Zivot-Andrews test for structural breaks."""
        # The default regression is 'c', which is appropriate for this test
        result = zivot_andrews(series, trim=0.15, autolag='AIC')
        p_value = result[1]
        return {
            "statistic": result[0],
            "p_value": p_value,
            "is_stationary": bool(p_value < 0.05),
        }

    def _garch_volatility(self, series: pd.Series) -> Dict:
        """GARCH model for volatility analysis."""
        try:
            # Do not standardize the series, as it can mask the true volatility
            model = arch_model(series, vol='Garch', p=1, q=1, dist='Normal')
            fitted = model.fit(disp='off', show_warning=False)

            # Return the standard deviation of the conditional volatility as a measure of risk
            return {
                'volatility': float(fitted.conditional_volatility.std()),
                'aic': fitted.aic,
                'bic': fitted.bic
            }
        except Exception as e:
            # GARCH can fail on some data, handle this gracefully
            return {'volatility': None, 'error': str(e)}