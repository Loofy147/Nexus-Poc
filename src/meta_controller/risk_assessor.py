from typing import Dict, List

import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss


class EnterpriseRiskAssessor:
    """
    Provides multi-dimensional risk assessment for decisions made by the meta-controller.
    This initial version focuses on assessing the stability risk of affected metrics.
    """

    def __init__(self, historical_data: pd.DataFrame):
        """
        Initializes the risk assessor with historical performance data.
        """
        self.historical_data = historical_data
        print("Enterprise Risk Assessor: Initialized.")

    def assess_stability_risk(self, affected_metrics: List[str]) -> Dict:
        """
        Assesses the stability risk of a set of metrics using time-series analysis.
        A non-stationary metric (e.g., one with a trend) is considered less stable.
        """
        print(
            f"Enterprise Risk Assessor: Assessing stability risk for metrics: {affected_metrics}"
        )
        stability_scores = {}
        overall_risk_level = "LOW"

        for metric in affected_metrics:
            if metric not in self.historical_data.columns:
                stability_scores[metric] = {
                    "error": "Metric not found in historical data."
                }
                continue

            metric_series = self.historical_data[metric].dropna()

            if len(metric_series) < 20:  # Need enough data for meaningful tests
                stability_scores[metric] = {
                    "error": "Not enough data points for stability analysis."
                }
                continue

            # Perform Augmented Dickey-Fuller test (H0: unit root is present, i.e., non-stationary)
            adf_result = adfuller(metric_series)
            adf_pvalue = adf_result[1]

            # Perform KPSS test (H0: series is stationary)
            # We suppress a warning that can occur with low p-values
            import warnings

            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                kpss_result = kpss(metric_series, regression="c", nlags="auto")
            kpss_pvalue = kpss_result[1]

            # A series is considered stable (stationary) if it rejects the ADF null
            # and fails to reject the KPSS null.
            is_stationary = adf_pvalue < 0.05 and kpss_pvalue > 0.05

            if not is_stationary:
                overall_risk_level = "HIGH"

            stability_scores[metric] = {
                "adf_pvalue": adf_pvalue,
                "kpss_pvalue": kpss_pvalue,
                "is_stationary": is_stationary,
            }

        print(
            f"Enterprise Risk Assessor: Stability assessment complete. Overall risk level: {overall_risk_level}"
        )
        return {
            "overall_risk_level": overall_risk_level,
            "metric_stability": stability_scores,
        }
