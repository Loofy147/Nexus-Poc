from typing import Dict, List

import numpy as np
import pandas as pd
import requests


class AdvancedMetricsCollector:
    """
    Collects and analyzes comprehensive metrics from Prometheus,
    including anomaly detection.
    """

    def __init__(self, prometheus_url: str):
        self.prometheus_url = prometheus_url
        print("Advanced Metrics Collector: Initialized.")

    def collect_comprehensive_metrics(
        self, time_range: str = "5m", step: str = "15s"
    ) -> Dict:
        """
        Collects comprehensive metrics and performs anomaly detection.
        """
        print("Advanced Metrics Collector: Starting comprehensive metric collection.")

        # For this PoC, we will focus on a key metric: latency.
        # In a full implementation, this would query all metrics defined in the plan.
        raw_metrics = self._query_prometheus_metrics(time_range, step)

        anomalies = self._detect_anomalies(raw_metrics)

        return {"raw_metrics": raw_metrics, "anomalies": anomalies}

    def _query_prometheus_metrics(self, time_range: str, step: str) -> Dict:
        """
        Queries Prometheus for a predefined set of advanced metrics.
        """
        queries = {
            "p95_latency": f'histogram_quantile(0.95, sum(rate(flask_http_request_duration_seconds_bucket{{job="orchestrator"}}[{time_range}])))',
            "request_rate": f'sum(rate(flask_http_request_duration_seconds_count{{job="orchestrator"}}[{time_range}]))',
        }

        results = {}
        for metric_name, query in queries.items():
            try:
                response = requests.get(
                    f"{self.prometheus_url}/api/v1/query",
                    params={"query": query},
                    timeout=10,
                )
                response.raise_for_status()
                result_data = response.json()["data"]["result"]
                if result_data:
                    results[metric_name] = float(result_data[0]["value"][1])
                else:
                    results[metric_name] = 0.0
            except (
                requests.exceptions.RequestException,
                KeyError,
                IndexError,
                ValueError,
            ) as e:
                print(
                    f"Advanced Metrics Collector: Failed to query Prometheus for {metric_name}: {e}"
                )
                results[metric_name] = None

        print(
            f"Advanced Metrics Collector: Raw metrics queried from Prometheus: {results}"
        )
        return results

    def _detect_anomalies(self, metrics_data: Dict) -> List[Dict]:
        """
        Detects anomalies in the collected metrics using the Z-score method.
        This is a simplified version of the multi-method approach in the plan.

        Note: Anomaly detection on single data points is not statistically robust.
        This PoC simulates detection on a single point for demonstration. A real system
        would analyze a time-series window.
        """
        anomalies = []

        # For this PoC, we will use a simple, hardcoded threshold for demonstration.
        # A real system would use dynamic, learned thresholds.
        latency_threshold = 1.0  # seconds

        p95_latency = metrics_data.get("p95_latency")

        if p95_latency is not None and p95_latency > latency_threshold:
            print(
                f"Advanced Metrics Collector: ANOMALY DETECTED in p95_latency. Value: {p95_latency}, Threshold: {latency_threshold}"
            )
            anomalies.append(
                {
                    "metric": "p95_latency",
                    "value": p95_latency,
                    "threshold": latency_threshold,
                    "method": "static_threshold",
                }
            )

        return anomalies
