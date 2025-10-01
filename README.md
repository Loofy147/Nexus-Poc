# NEXUS: Enterprise-Grade AI Orchestrator

This repository contains the implementation for NEXUS, a modular, enterprise-grade AI orchestrator. NEXUS is designed with a professional, high-tech microservices architecture to provide intelligent, secure, and scalable AI-driven workflows.

## Overview

NEXUS intelligently processes user queries by orchestrating a professional suite of microservices. It leverages a true Graph-RAG pipeline for deep, context-aware knowledge retrieval and a hardened, containerized sandbox for secure code execution, making it a cutting-edge platform for advanced AI applications.

The core enterprise-grade components are:
- **Orchestrator**: The central service that manages complex workflows.
- **Knowledge Retriever**: A true Graph-RAG service using Neo4j and FAISS for hybrid knowledge retrieval.
- **Execution Sandbox**: A hardened service that executes code in isolated, resource-limited Docker containers.
- **LLM Adapter**: Connects to OpenAI's GPT models to generate intelligent, context-aware responses.
- **Memory Layer**: A robust service using Redis for high-performance session memory.

## High-Tech Architecture

The system is designed as a set of communicating microservices containerized with Docker. This architecture includes:
- **Neo4j**: A graph database that stores interconnected knowledge.
- **Redis**: An in-memory data store for high-speed session management.
- **Docker-in-Docker**: The execution sandbox uses this pattern to provide breakthrough security, running all code in isolated containers.

For a detailed explanation of the original architectural principles, see the [ARCHITECTURE.md](docs/ARCHITECTURE.md) file.

## Getting Started

Follow these instructions to build and run the enterprise-grade NEXUS system.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
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

3.  **Build and run the services**:
    This command will build all service images and start the full NEXUS stack, including Neo4j and Redis.
    ```sh
    docker-compose -f infra/docker-compose.yml up --build
    ```
    *Note: The first time you run this, Docker will download the Neo4j and Redis images, which may take a few moments.*

### Testing the System

Once all services are running, you must first populate the knowledge base.

1.  **Populate the Knowledge Retriever**:
    Send a POST request to the `/populate` endpoint to load the sample data into Neo4j and FAISS.
    ```sh
    curl -X POST http://localhost:5003/populate
    ```

2.  **Query the Orchestrator**:
    Now, you can send a query to the main endpoint. Use a query that leverages the populated knowledge to see the Graph-RAG pipeline in action.
    ```sh
    curl -X POST http://localhost:5001/api/v1/query \
    -H "Content-Type: application/json" \
    -d '{
        "user_id": "enterprise-user",
        "session_id": "session-456",
        "query": "What is the relationship between the orchestrator and the memory layer?"
    }'
    ```
    You should receive a professional, context-aware response from the LLM, informed by the hybrid search results from the knowledge retriever.

## Services

| Service                 | Port  | Description                                                         |
| ----------------------- | ----- | ------------------------------------------------------------------- |
| **Orchestrator**        | 5001  | The main entry point and advanced workflow coordinator.             |
| **Knowledge Retriever** | 5003  | Enterprise Graph-RAG service with Neo4j and FAISS.                  |
| **Memory Layer**        | 5004  | High-performance session memory using Redis.                        |
| **Execution Sandbox**   | 5005  | Hardened, secure code execution using Docker-in-Docker.             |
| **LLM Adapter**         | 5006  | Connects to OpenAI to generate intelligent responses.               |
| **Neo4j**               | 7474  | Graph database for the knowledge retriever. (UI on port 7474)       |
| **Redis**               | 6379  | In-memory data store for the Memory Layer.                          |
| Agent Manager           | 5002  | Mock service, kept for structural consistency.                      |