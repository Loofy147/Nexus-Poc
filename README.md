# NEXUS Proof of Concept (PoC)

This repository contains the Proof of Concept (PoC) implementation for NEXUS, a modular, microservices-based adaptive knowledge-driven AI orchestrator. This PoC is built according to the specifications outlined in the [ARCHITECTURE.md](docs/ARCHITECTURE.md) document.

## Overview

The NEXUS PoC demonstrates a service-oriented architecture for an AI system. It orchestrates interactions between specialized components to intelligently process user queries by combining knowledge retrieval, memory management, and safe code execution.

The core components implemented in this PoC are:
- **Orchestrator**: The central service that coordinates the entire workflow.
- **Agent Manager**: A mock service for selecting processing agents.
- **Knowledge Graph (Mock)**: A mock service simulating Graph-RAG hybrid search.
- **Memory Layer (Mock)**: A mock service for persistent, file-based memory.
- **Execution Sandbox**: A mock service for controlled code execution.
- **LLM Abstraction Layer (Mock)**: A mock service that simulates LLM interactions.

## Architecture

The system is designed as a set of communicating microservices, containerized with Docker. The `orchestrator` service acts as the brain, receiving user queries and coordinating calls to the other services to generate a response.

For a detailed explanation of the architecture, data flow, and design decisions, please see the [ARCHITECTURE.md](docs/ARCHITECTURE.md) file.

## Getting Started

Follow these instructions to build and run the NEXUS PoC on your local machine.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running the Application

1.  **Clone the repository** (if you haven't already):
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Build and run the services** using Docker Compose:
    ```sh
    docker-compose -f infra/docker-compose.yml up --build
    ```
    This command will build the Docker image for each service and start all the containers. The services will be available on their respective ports (5001-5006).

### Testing the Endpoint

Once the services are running, you can test the main query endpoint of the orchestrator using `curl` or any API client.

```sh
curl -X POST http://localhost:5001/api/v1/query \
-H "Content-Type: application/json" \
-d '{
    "user_id": "test-user",
    "session_id": "session-123",
    "query": "Please execute a simple python script to print hello."
}'
```

You should receive a JSON response from the orchestrator that includes the LLM's answer and the result from the execution sandbox.

## Services

The following services are included in this PoC:

| Service                | Port | Description                                             |
| ---------------------- | ---- | ------------------------------------------------------- |
| **Orchestrator**       | 5001 | The main entry point and workflow coordinator.          |
| Agent Manager          | 5002 | Selects agents based on the query.                      |
| Knowledge Graph Mock   | 5003 | Simulates hybrid knowledge retrieval.                   |
| Memory Layer Mock      | 5004 | Stores and retrieves session history.                   |
| Execution Sandbox      | 5005 | Executes code in a controlled environment.              |
| LLM Adapter Mock       | 5006 | Simulates responses from a Large Language Model.        |