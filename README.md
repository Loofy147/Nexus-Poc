# NEXUS: An Enterprise-Grade, Self-Improving AI Architecture

This repository contains the implementation for NEXUS, a high-tech, self-improving AI architecture. NEXUS is designed to autonomously observe, analyze, and evolve its own software components to achieve high-level strategic goals, built on a foundation of mathematical guarantees for stability and rational decision-making.

## The NEXUS Architecture: A Layered Approach

NEXUS is built on a professional, layered architecture to separate concerns and ensure enterprise-grade stability and intelligence.

### Layer 1: The Intelligence Layer (The Mind)

This is the core of the system's autonomy, responsible for high-level reasoning. The `meta_controller` service orchestrates an **Observe-Orient-Decide-Act (OODA)** loop, using its `EnterpriseCausalEngine` and `EnterpriseRiskAssessor` to make rational, data-driven decisions.

### Layer 2: The Execution Layer (The Hands)

This layer is responsible for safely and reliably acting on the decisions made by the Intelligence Layer. It is powered by the `code_modifier` service, which contains the `EnterpriseCodeModifier` engine. This engine provides enterprise-grade guarantees for every autonomous code change by enforcing a professional, multi-stage pipeline:
1.  **Code Generation**: It receives a high-level directive and generates a precise, deterministic code change.
2.  **Security Scanning**: It uses `bandit` to perform a static analysis security test (SAST), rejecting any change with potential vulnerabilities.
3.  **Quality Gates**: It uses `pylint` to analyze the code against enterprise-grade quality standards, rejecting any change that does not meet the required threshold.
4.  **Version Control**: Upon passing all gates, it automatically creates a new feature branch, and commits the change with a detailed, auditable message using `GitPython`.

### Other Layers

-   **Layer 0 (Strategic Control)**: The human interface for setting high-level goals.
-   **Layer 3 (Service Mesh)**: The core NEXUS application services.
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

### Testing the Full OODA Loop

1.  **Populate Knowledge Base**: `curl -X POST http://localhost:5003/populate`
2.  **Generate Performance Data**: Run a few sample queries to generate metrics.
    ```sh
    curl -X POST http://localhost:5001/api/v1/query -H "Content-Type: application/json" -d '{"user_id": "test", "session_id": "1", "query": "test"}'
    ```
3.  **Give the System a Strategic Goal**:
    Instruct the Intelligence Layer to achieve an objective.
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
    - **Check the logs**: In your first terminal, watch the logs (`docker-compose -f infra/docker-compose.yml logs -f meta_controller code_modifier`). You will see the `meta_controller` make a decision and the `code_modifier` run its security and quality pipeline.
    - **Check the Git repository**: In a new terminal, check the git log to see the new, autonomous commit on its own feature branch: `git log --oneline --graph --all`.

## Services

| Service                 | Port  | Description                                                         |
| ----------------------- | ----- | ------------------------------------------------------------------- |
| **Meta-Controller**     | 6000  | **The Intelligence Layer.** Orchestrates the OODA loop.             |
| **Code Modifier**       | 6001  | **The Execution Layer.** Applies safe, validated, versioned changes.|
| **Orchestrator**        | 5001  | The core workflow engine, instrumented for observability.           |
| **Knowledge Retriever** | 5003  | Enterprise Graph-RAG service with Neo4j and FAISS.                  |
| **Execution Sandbox**   | 5005  | Hardened, secure code execution using Docker-in-Docker.             |
| **LLM Adapter**         | 5006  | Connects to OpenAI to generate intelligent responses.               |
| **Prometheus**          | 9090  | **The Observability Layer.** Collects performance metrics.          |
| **Grafana**             | 3000  | Visualizes system performance.                                      |
| **Neo4j**               | 7474  | Graph database for the knowledge retriever.                         |
| **Redis**               | 6379  | In-memory data store for the Memory Layer.                          |