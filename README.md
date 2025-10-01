# NEXUS: An Enterprise-Grade, Self-Improving AI Architecture

This repository contains the implementation for NEXUS, a high-tech, self-improving AI architecture. NEXUS is designed to autonomously observe, analyze, and evolve its own software components to achieve high-level strategic goals, built on a foundation of mathematical guarantees for stability and rational decision-making.

## The NEXUS Architecture: A Layered Approach

NEXUS is built on a professional, layered architecture to separate concerns and ensure enterprise-grade stability and intelligence.

### Layer 1: The Intelligence Layer (The Mind)

This is the core of the system's autonomy. It is responsible for high-level reasoning and decision-making. It consists of:
-   **Meta-Controller**: The primary agent that orchestrates the self-improvement loop.
-   **Enterprise Causal Engine**: A sophisticated component that uses causal inference libraries (`dowhy`, `causalnex`) to discover the root causes of system behavior and predict the impact of potential changes. This allows NEXUS to move beyond simple correlation to understand true causation.
-   **Enterprise Risk Assessor**: A professional risk management component that uses statistical and time-series analysis (`statsmodels`) to assess the stability of the system and the risks associated with any proposed change.

The Intelligence Layer operates on a continuous **Observe-Orient-Decide-Act (OODA)** loop:
1.  **Observe**: It queries the Observability Layer (Prometheus) to gather real-time and historical performance data.
2.  **Orient**: It uses the `EnterpriseRiskAssessor` to analyze the data, assessing system stability and quantifying risks.
3.  **Decide**: It uses the `EnterpriseCausalEngine` to perform a rigorous causal analysis, identifying the optimal action to achieve its strategic goals while minimizing risk.
4.  **Act**: It formulates a formal change proposal and dispatches it to the Execution Layer.

### Other Layers

-   **Layer 0 (Strategic Control)**: The human interface for setting high-level goals.
-   **Layer 2 (Execution)**: The `code_modifier` service that safely applies changes.
-   **Layer 3 (Service Mesh)**: The core NEXUS services (`orchestrator`, `knowledge_retriever`, etc.).
-   **Layer 4 (Observability)**: Prometheus and Grafana, the system's "senses."
-   **Layer 5 (Data)**: The underlying data stores (Neo4j, Redis).

## Getting Started

Follow these instructions to run the full self-improving NEXUS ecosystem.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- An [OpenAI API Key](https://platform.openai.com/api-keys)

### Running the Application

1.  **Set your OpenAI API Key**: Create a `.env` file: `OPENAI_API_KEY=your_key_here`
2.  **Build and run**: `docker-compose -f infra/docker-compose.yml up --build`

### Testing the Intelligence Layer

1.  **Populate Knowledge Base**: `curl -X POST http://localhost:5003/populate`
2.  **Generate Performance Data**: Run a few sample queries to generate metrics for Prometheus.
    ```sh
    curl -X POST http://localhost:5001/api/v1/query -H "Content-Type: application/json" -d '{"user_id": "test", "session_id": "1", "query": "test"}'
    ```
3.  **Give the System a Strategic Goal**:
    Instruct the Intelligence Layer to achieve an objective. Note the new `affected_metrics` field, which is used by the `EnterpriseRiskAssessor`.
    ```sh
    curl -X POST http://localhost:6000/api/v1/objective \
    -H "Content-Type: application/json" \
    -d '{
        "goal": "reduce_latency",
        "target_metric": "latency",
        "intervention": "enable_caching",
        "affected_metrics": ["latency", "error_rate"]
    }'
    ```
4.  **Observe the System's Response**:
    Check the Docker logs (`docker-compose -f infra/docker-compose.yml logs -f meta_controller`). You will see the full OODA loop in action: data fetching, risk assessment, causal analysis, and the final decision to act.

## Services

| Service                 | Port  | Description                                                         |
| ----------------------- | ----- | ------------------------------------------------------------------- |
| **Meta-Controller**     | 6000  | **The Intelligence Layer.** Orchestrates the OODA loop.             |
| **Code Modifier**       | 6001  | **The Execution Layer.** Safely applies code changes.               |
| **Orchestrator**        | 5001  | The core workflow engine, instrumented for observability.           |
| **Knowledge Retriever** | 5003  | Enterprise Graph-RAG service with Neo4j and FAISS.                  |
| **Execution Sandbox**   | 5005  | Hardened, secure code execution using Docker-in-Docker.             |
| **LLM Adapter**         | 5006  | Connects to OpenAI to generate intelligent responses.               |
| **Prometheus**          | 9090  | **The Observability Layer.** Collects performance metrics.          |
| **Grafana**             | 3000  | Visualizes system performance.                                      |
| **Neo4j**               | 7474  | Graph database for the knowledge retriever.                         |
| **Redis**               | 6379  | In-memory data store for the Memory Layer.                          |