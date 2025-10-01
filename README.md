# NEXUS Proof of Concept (PoC)

This repository contains the Proof of Concept (PoC) implementation for NEXUS, a modular, microservices-based adaptive knowledge-driven AI orchestrator. This PoC is built according to the specifications outlined in the [ARCHITECTURE.md](docs/ARCHITECTURE.md) document and has been enhanced with professional-grade components.

## Overview

The NEXUS PoC demonstrates a service-oriented architecture for an AI system. It orchestrates interactions between specialized components to intelligently process user queries by combining knowledge retrieval, memory management, and safe code execution.

The core components are:
- **Orchestrator**: The central service that coordinates the entire workflow.
- **LLM Adapter**: Connects to a real LLM provider (OpenAI) to generate intelligent responses.
- **Memory Layer**: A robust service using Redis for persistent session memory.
- **Execution Sandbox**: A mock service for controlled code execution.
- **Agent Manager**: A mock service for selecting processing agents.
- **Knowledge Graph (Mock)**: A mock service simulating Graph-RAG hybrid search.

## Architecture

The system is designed as a set of communicating microservices, containerized with Docker. The `orchestrator` service acts as the brain, receiving user queries and coordinating calls to the other services to generate a response. The `memory_layer` now uses Redis for improved performance and scalability, and the `llm_adapter` connects to OpenAI's GPT models.

For a detailed explanation of the original architecture, see the [ARCHITECTURE.md](docs/ARCHITECTURE.md) file.

## Getting Started

Follow these instructions to build and run the NEXUS PoC on your local machine.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- An [OpenAI API Key](https://platform.openai.com/api-keys)

### Running the Application

1.  **Clone the repository** (if you haven't already):
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Set your OpenAI API Key**:
    Create a `.env` file in the root of the project and add your API key to it:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```
    The `docker-compose.yml` file is configured to read this variable and pass it to the LLM adapter service.

3.  **Build and run the services** using Docker Compose:
    ```sh
    docker-compose -f infra/docker-compose.yml up --build
    ```
    This command will build the Docker image for each service and start all the containers.

### Testing the Endpoint

Once the services are running, you can test the main query endpoint. Use a query that prompts the LLM to generate code to see the full workflow in action.

```sh
curl -X POST http://localhost:5001/api/v1/query \
-H "Content-Type: application/json" \
-d '{
    "user_id": "test-user",
    "session_id": "session-123",
    "query": "Can you write a python script that prints the first 5 prime numbers?"
}'
```

You should receive a JSON response from the orchestrator that includes the LLM's answer and the result from the execution sandbox.

## Services

The following services are included in this PoC:

| Service                | Port | Description                                             |
| ---------------------- | ---- | ------------------------------------------------------- |
| **Orchestrator**       | 5001 | The main entry point and workflow coordinator.          |
| Agent Manager          | 5002 | Selects agents based on the query. (Mock)               |
| Knowledge Graph Mock   | 5003 | Simulates hybrid knowledge retrieval. (Mock)            |
| Memory Layer           | 5004 | Stores and retrieves session history using Redis.       |
| Execution Sandbox      | 5005 | Executes code in a controlled environment. (Mock)       |
| LLM Adapter            | 5006 | Connects to OpenAI to generate responses.               |
| **Redis**              | 6379 | In-memory data store for the Memory Layer.              |