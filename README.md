# NEXUS: A Self-Improving AI Architecture

This repository contains the implementation for NEXUS, a high-tech, self-improving AI architecture. NEXUS is designed to autonomously observe, analyze, and evolve its own software components to achieve high-level strategic goals, built on a foundation of mathematical guarantees for stability and rational decision-making.

## Core Principles: Autonomous Evolution

NEXUS operates on a dynamic observe-orient-decide-act (OODA) loop, enabling it to evolve without human intervention. This is achieved through a professional, multi-ecosystem architecture:

-   **The Central Nervous System (Observability)**: An integrated Prometheus and Grafana stack allows the system to observe its own performance metrics in real-time, providing a quantitative "feeling" of its state.
-   **The Mind (Meta-Controller)**: A high-level agent that receives strategic goals from operators. It analyzes the system's performance data from the nervous system to make rational, goal-oriented decisions about how the system should evolve.
-   **The Hands (Code Modifier)**: A secure, privileged service that acts on the decisions of the Mind. It has the ability to safely modify the source code of other components, completing the self-evolutionary loop.

This architecture transforms NEXUS from a static application into a dynamic, goal-driven system capable of autonomous improvement.

## High-Tech Components

The system is composed of a suite of professional microservices:
- **Meta-Controller**: The "Mind." Analyzes performance and decides on code changes.
- **Code Modifier**: The "Hands." Safely applies proposed code changes.
- **Orchestrator**: The core workflow engine, now fully observable by the meta-controller.
- **Knowledge Retriever**: A true Graph-RAG service using Neo4j and FAISS.
- **Execution Sandbox**: A hardened, containerized sandbox for secure code execution.
- **Observability Stack**: Prometheus and Grafana provide the system's "senses."

## Getting Started

Follow these instructions to run the full self-improving NEXUS ecosystem.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- An [OpenAI API Key](https://platform.openai.com/api-keys)

### Running the Application

1.  **Set your OpenAI API Key**: Create a `.env` file in the root of the project:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```

2.  **Build and run the full ecosystem**:
    ```sh
    docker-compose -f infra/docker-compose.yml up --build
    ```
    This will start all NEXUS services, including the new meta-controller and observability stack.

### Testing the Self-Improving Loop

1.  **Populate the Knowledge Base**:
    (In a new terminal) First, load the sample data into the knowledge retriever.
    ```sh
    curl -X POST http://localhost:5003/populate
    ```

2.  **Run a Sample Query**:
    Generate some performance data by sending a normal query to the orchestrator.
    ```sh
    curl -X POST http://localhost:5001/api/v1/query -H "Content-Type: application/json" -d '{"user_id": "test-user", "session_id": "session-1", "query": "hello"}'
    ```

3.  **Give the System a Strategic Goal**:
    Now, instruct the "Mind" to improve the system. Set a strategic objective for the p95 latency to be under 0.1 seconds.
    ```sh
    curl -X POST http://localhost:6000/api/v1/objective \
    -H "Content-Type: application/json" \
    -d '{
        "goal": "reduce_p95_latency",
        "target": 0.1
    }'
    ```

4.  **Observe the System's Response**:
    Check the Docker logs for the `meta_controller` and `code_modifier` services (`docker-compose -f infra/docker-compose.yml logs -f meta_controller code_modifier`). You will see the meta-controller analyze the Prometheus data, decide that the latency target is missed, and send a modification proposal to the code modifier. The code modifier will then apply a simulated change to the orchestrator's source code.

## Services

| Service                 | Port  | Description                                                         |
| ----------------------- | ----- | ------------------------------------------------------------------- |
| **Meta-Controller**     | 6000  | The "Mind" of the system. Receives goals and makes decisions.       |
| **Code Modifier**       | 6001  | The "Hands" of the system. Safely applies code changes.             |
| **Orchestrator**        | 5001  | The core workflow engine, instrumented for observability.           |
| **Knowledge Retriever** | 5003  | Enterprise Graph-RAG service with Neo4j and FAISS.                  |
| **Execution Sandbox**   | 5005  | Hardened, secure code execution using Docker-in-Docker.             |
| **LLM Adapter**         | 5006  | Connects to OpenAI to generate intelligent responses.               |
| **Prometheus**          | 9090  | The "Nervous System." Collects performance metrics.                 |
| **Grafana**             | 3000  | Visualizes system performance. (Default login: admin/admin)         |
| **Neo4j**               | 7474  | Graph database for the knowledge retriever. (UI on port 7474)       |
| **Redis**               | 6379  | In-memory data store for the Memory Layer.                          |