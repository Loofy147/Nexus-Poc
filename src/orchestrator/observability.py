import os

import pyroscope
from opentelemetry.distro import OpenTelemetryDistro
from opentelemetry.instrumentation.auto_instrumentation import get_distro


def setup_observability(service_name="orchestrator"):
    """
    Initializes and configures the observability stack for a service,
    including OpenTelemetry for tracing and Pyroscope for profiling.
    """
    print(f"[{service_name}] Initializing observability stack...")

    # --- Configure OpenTelemetry for Distributed Tracing ---
    # The OpenTelemetry Distro will automatically configure the exporter
    # based on environment variables like OTEL_EXPORTER_OTLP_ENDPOINT.
    # It also auto-instruments popular libraries like Flask and Requests.
    try:
        get_distro().configure()
        print(f"[{service_name}] OpenTelemetry configured successfully.")
    except Exception as e:
        print(f"[{service_name}] Failed to configure OpenTelemetry: {e}")

    # --- Configure Pyroscope for Continuous Profiling ---
    # The server address is read from the PYROSCOPE_SERVER_ADDRESS env var.
    try:
        pyroscope.configure(
            application_name=f"nexus.{service_name}",
            server_address=os.environ.get(
                "PYROSCOPE_SERVER_ADDRESS", "http://pyroscope:4040"
            ),
            tags={
                "service": service_name,
            },
            enable_logging=True,
        )
        print(f"[{service_name}] Pyroscope configured successfully.")
    except Exception as e:
        print(f"[{service_name}] Failed to configure Pyroscope: {e}")
