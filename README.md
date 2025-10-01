# NEXUS: An Enterprise-Grade, Self-Improving AI Architecture

This repository contains the implementation for NEXUS, a high-tech, self-improving AI architecture. NEXUS is designed to autonomously observe, analyze, and evolve its own software components to achieve high-level strategic goals, built on a foundation of professional, cloud-native principles.

## The NEXUS Architecture: A Layered Approach

NEXUS is built on a professional, layered architecture to separate concerns and ensure enterprise-grade stability, observability, and intelligence.

-   **Layer 0: API Gateway (The Front Door)**: A Kong gateway manages all ingress traffic, providing routing, authentication, and resilience.
-   **Layer 1: Intelligence (The Mind)**: The `meta_controller` orchestrates an OODA loop, using advanced engines for anomaly detection, causal inference, and risk assessment to make rational, data-driven decisions.
-   **Layer 2: Execution (The Hands)**: The `code_modifier` provides a secure pipeline to apply, validate, and version-control autonomous code changes.
-   **Layer 3: Service Mesh**: The core application services (`orchestrator`, `knowledge_retriever`, etc.) that perform the primary business logic.
-   **Layer 4: Observability (The Senses)**: A comprehensive stack including Prometheus, Grafana, Jaeger, and Pyroscope provides deep, real-time insight into the system's behavior.
-   **Layer 5: Data**: A robust data layer with Neo4j for graph data and Redis for caching and messaging.
-   **Layer 6: Infrastructure**: The entire system is containerized with Docker and designed for a production deployment on Kubernetes with ArgoCD.

## Getting Started

NEXUS can be run in two modes: `local` for lightweight development and `enterprise` for the full, high-tech experience.

### Option 1: Local Development (Recommended for a quick start)

This mode runs only the core application services without the advanced observability, security, or CI/CD components.

1.  **Set API Key**: Create a `.env` file: `OPENAI_API_KEY=your_key_here`
2.  **Build and run**:
    ```sh
    docker-compose -f infra/docker-compose.local.yml up --build
    ```

### Option 2: Full Enterprise Stack

This mode runs the entire NEXUS ecosystem, including the full data, observability, and security layers as defined in the enterprise manifest.

1.  **Set Environment Variables**: Create a `.env` file with your OpenAI API key and any other necessary credentials:
    ```
    OPENAI_API_KEY=your_key_here
    # Add other variables like NEO4J_PASSWORD, VAULT_ROOT_TOKEN, etc. as needed.
    ```
2.  **Build and run the full stack**:
    ```sh
    docker-compose -f infra/docker-compose.enterprise.yaml up --build
    ```
    *Note: This will download and start many services and may require significant system resources (e.g., 16GB+ of RAM is recommended).*

### Developer Setup: Code Quality Hooks

To ensure consistent code quality and automatically format code, this project uses `pre-commit`.

1.  **Install pre-commit**:
    ```sh
    pip install -r requirements.txt
    ```

2.  **Install the Git hooks**:
    ```sh
    pre-commit install
    ```

Now, `black`, `isort`, `pylint`, and `bandit` will run automatically on every commit.

### Testing the Full OODA Loop

Once the **enterprise stack** is running, you can test the full self-improving loop:

1.  **Generate an API Key via Kong**:
    ```sh
    # Create a consumer
    curl -i -X POST http://localhost:8001/consumers/ --data username=nexus-developer
    # Provision an API key
    curl -i -X POST http://localhost:8001/consumers/nexus-developer/key-auth --data key=my-secret-apikey
    ```

2.  **Populate the Knowledge Base**:
    ```sh
    curl -X POST http://localhost:8000/orchestrator/populate -H "apikey: my-secret-apikey" -H "Content-Type: application/json" -d '{"documents": ["The orchestrator is the core of NEXUS."]}'
    ```

3.  **Give the System a Strategic Goal**:
    ```sh
    curl -X POST http://localhost:8000/meta-controller/api/v1/objective -H "apikey: my-secret-apikey" -H "Content-Type: application/json" -d '{"goal": "reduce_latency", "target_metric": "latency", "intervention": "enable_caching", "affected_metrics": ["latency", "error_rate"]}'
    ```

4.  **Observe the System's Response**:
    -   **Logs**: `docker-compose -f infra/docker-compose.enterprise.yaml logs -f meta_controller code_modifier`
    -   **Git**: `git log --oneline --graph --all` (to see the new commit)
    -   **Jaeger UI**: `http://localhost:16686`
    -   **Pyroscope UI**: `http://localhost:4040`
    -   **Prometheus UI**: `http://localhost:9090` (query `nexus_decisions_total`)
    -   **Alertmanager UI**: `http://localhost:9093`

## Enterprise Alerting

The enterprise stack is pre-configured with a robust alerting pipeline. Prometheus monitors system metrics and fires alerts to Alertmanager based on predefined rules.

-   **Alerting Rules**: Defined in `infra/config/prometheus/rules/alert.rules.yml`. You can add your own custom alerts here.
-   **Alertmanager**: Receives alerts from Prometheus, deduplicates them, groups them, and routes them to the correct receiver (e.g., email, Slack, PagerDuty). The default configuration is in `infra/config/alertmanager/config.yml`.
-   **Viewing Alerts**: Access the Alertmanager UI at `http://localhost:9093` to see currently firing alerts.

## Future Work

This implementation is a functional proof-of-concept. The `README.md` and `docs/ARCHITECTURE.md` outline a clear roadmap for future work, including implementing the more advanced statistical models, LLM-powered code generation, and a full CI/CD pipeline with Argo Rollouts for automated canary deployments.