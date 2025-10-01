# NEXUS: An Enterprise-Grade, Self-Improving AI Architecture

This repository contains the implementation for NEXUS, a high-tech, self-improving AI architecture. NEXUS is designed to autonomously observe, analyze, and evolve its own software components to achieve high-level strategic goals.

## The NEXUS Architecture: A Layered Approach

NEXUS is built on a professional, layered architecture to separate concerns and ensure enterprise-grade stability and intelligence.

### Layer 0: The API Gateway (The Front Door)
All traffic into the NEXUS ecosystem is managed by an enterprise-grade API Gateway powered by Kong. This provides a single, secure, and manageable entry point for all services. Key features include:
-   **Centralized Routing**: Maps public API endpoints (e.g., `/orchestrator`) to the appropriate internal microservices.
-   **Security**: Enforces authentication (e.g., API keys) on all incoming requests.
-   **Resilience**: Provides rate-limiting and circuit-breaking to protect services from overload.
-   **Observability**: Automatically generates metrics for all API traffic, which are scraped by Prometheus.

### Layer 1: The Intelligence Layer (The Mind)
The `meta_controller` service orchestrates an **Observe-Orient-Decide-Act (OODA)** loop, using its advanced engines to make rational, data-driven decisions.

### Layer 2: The Execution Layer (The Hands)
The `code_modifier` service uses its `EnterpriseCodeModifier` engine to provide guarantees for every autonomous code change by enforcing a professional pipeline of security scanning, quality checks, and version control.

### Layer 4: The Observability Layer (The Senses)
This layer provides deep, real-time insight into the system's behavior and performance, with components like Prometheus, Jaeger, and Pyroscope.

## Getting Started

Follow these instructions to run the full self-improving NEXUS ecosystem.

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/install/)
- An [OpenAI API Key](https://platform.openai.com/api-keys)

### Running the Application
1.  **Set API Key**: Create a `.env` file: `OPENAI_API_KEY=your_key_here`
2.  **Build and run**: `docker-compose -f infra/docker-compose.yml up --build`

### Testing the Full OODA Loop through the API Gateway

1.  **Generate an API Key**:
    For this PoC, we will manually create a "consumer" and an API key for them by calling the Kong Admin API.
    ```sh
    # Step 1: Create a consumer
    curl -i -X POST http://localhost:8001/consumers/ \
      --data username=nexus-developer

    # Step 2: Provision an API key for the consumer
    curl -i -X POST http://localhost:8001/consumers/nexus-developer/key-auth \
      --data key=my-secret-apikey
    ```

2.  **Populate Knowledge Base via the Gateway**:
    All requests now go through the Kong proxy port (8000) and require the API key.
    ```sh
    curl -X POST http://localhost:8000/orchestrator/populate \
    -H "apikey: my-secret-apikey" \
    -H "Content-Type: application/json" \
    -d '{
        "documents": [
            "The NEXUS orchestrator is the core of the system.",
            "The orchestrator communicates with the knowledge retriever to get context."
        ]
    }'
    ```

3.  **Give the System a Strategic Goal via the Gateway**:
    ```sh
    curl -X POST http://localhost:8000/meta-controller/api/v1/objective \
    -H "apikey: my-secret-apikey" \
    -H "Content-Type: application/json" \
    -d '{
        "goal": "reduce_latency",
        "target_metric": "latency",
        "intervention": "enable_caching",
        "affected_metrics": ["latency", "error_rate"]
    }'
    ```

4.  **Observe the System's Response**:
    -   **Logs**: Watch the `meta_controller` and `code_modifier` logs. You will see the `meta_controller` first perform anomaly detection before proceeding with risk assessment and causal analysis.
    -   **Git**: Check the git log for the new autonomous commit: `git log --oneline --graph --all`.
    -   **Jaeger UI**: Open `http://localhost:16686` to view the distributed traces for the query request. Select the "orchestrator" service and find the most recent trace.
    -   **Pyroscope UI**: Open `http://localhost:4040` to view the continuous performance profiles of the `orchestrator` service.
    -   **Prometheus UI**: Open `http://localhost:9090` and query the custom metric `nexus_decisions_total` to see the `meta_controller`'s decision recorded in real-time.

## Future Work and Enterprise-Grade Roadmap

This implementation provides a strong foundation and a functional proof-of-concept for the NEXUS self-improving architecture. It successfully demonstrates the core principles of the layered design and the OODA loop for autonomous decision-making.

To fully realize the enterprise-grade vision outlined in the initial plan, the following areas represent the next steps for development:

-   **Advanced Causal and Risk Engines**: Enhance the `EnterpriseCausalEngine` and `EnterpriseRiskAssessor` to move from simplified models to the more advanced statistical methods outlined in the plan, such as Doubly Robust Estimation, formal verification with Z3, and multi-dimensional risk analysis.
-   **LLM-Powered Code Generation**: Upgrade the `EnterpriseCodeModifier` to use a Large Language Model (LLM) for dynamic, intelligent code generation, rather than the current deterministic simulation. This would involve advanced prompting techniques and validation of the LLM's output.
-   **Automated Testing and Gradual Deployment**: Implement the `AutomatedTestRunner` and `GradualDeploymentEngine` to create a full, enterprise-grade CI/CD pipeline for autonomous changes, including canary deployments and automated rollbacks.
-   **Comprehensive SLO and Governance Layer**: Build out the Strategic Control Layer (Layer 0) with a formal Policy Engine and SLO monitoring to provide robust governance and oversight for the system's autonomous actions.

### Layer-N: Performance Optimization
To ensure the system is scalable and responsive, NEXUS employs an enterprise-grade performance optimization strategy.
-   **Intelligent Caching**: The `orchestrator` service includes a professional, reusable caching system (`caching.py`) that uses Redis as a backend. The `@cached` decorator provides a simple and powerful way to apply a cache-aside pattern to any function, drastically reducing latency for repeated operations. The high-latency calls to the `knowledge_retriever` are now cached, significantly improving query performance.

## Services

| Service                 | Port   | Description                                                         |
| ----------------------- | ------ | ------------------------------------------------------------------- |
| **Kong API Gateway**    | 8000   | **The API Gateway Layer.** The single entry point for all services. |
| **Meta-Controller**     | (internal) | **The Intelligence Layer.** Orchestrates the OODA loop.             |
| **Code Modifier**       | (internal) | **The Execution Layer.** Applies safe, validated, versioned changes.|
| **Orchestrator**        | (internal) | The core workflow engine, instrumented for observability.           |
| **Knowledge Retriever** | (internal) | **Knowledge Layer.** High-tech Graph-RAG with dynamic ingestion.    |
| **Execution Sandbox**   | (internal) | Hardened, secure code execution using Docker-in-Docker.             |
| **LLM Adapter**         | (internal) | Connects to OpenAI to generate intelligent responses.               |
| **Prometheus**          | 9090   | **The Observability Layer.** Collects performance metrics.          |
| **Grafana**             | 3000   | Visualizes system performance.                                      |
| **Jaeger**              | 16686  | **The Observability Layer.** Provides distributed tracing.          |
| **Pyroscope**           | 4040   | **The Observability Layer.** Provides continuous profiling.         |
| **Neo4j**               | (internal) | Graph database for the knowledge retriever.                         |
| **Redis**               | (internal) | In-memory data store for the Memory Layer.                          |

---

## Enterprise-Grade Deployment (Kubernetes)

While `docker-compose` is excellent for local development, a professional, enterprise-grade deployment requires a robust container orchestrator like Kubernetes. This section provides the foundation for deploying NEXUS to a production environment.

### Prerequisites

*   A running Kubernetes cluster.
*   `kubectl` configured to connect to your cluster.
*   [Istio](https://istio.io/latest/docs/setup/getting-started/) installed on your cluster for service mesh capabilities.

### Deployment Steps

1.  **Create the `nexus-secrets` Secret**:
    The Kubernetes manifests reference a secret named `nexus-secrets` for sensitive data like API keys. To create this securely, use the provided helper script. This script will prompt you for the values and will not store them in your shell history.
    ```sh
    chmod +x infra/kubernetes/create-secrets.sh
    ./infra/kubernetes/create-secrets.sh
    ```

2.  **Apply the Kubernetes Manifests**:
    Apply the production configuration for the NEXUS system. This will create the `nexus-production` namespace and deploy the `meta-controller` with all its associated resources (HPA, Service, Network Policies, etc.).
    ```sh
    kubectl apply -f infra/kubernetes/nexus-production.yaml
    ```

3.  **Verify the Deployment**:
    Check the status of the pods in the `nexus-production` namespace.
    ```sh
    kubectl get pods -n nexus-production
    ```
    You should see the `meta-controller` pods running.

### Note on Full Deployment

The provided `nexus-production.yaml` file is a professional, production-ready template for the `meta-controller` service. For a full production deployment of the entire NEXUS system, you would need to create similar high-quality, robust manifest files for all other services (`orchestrator`, `code_modifier`, `knowledge_retriever`, etc.), following the best practices established in this template.

---

## Enterprise-Grade CI/CD with Argo

This project is designed to be managed using a professional, enterprise-grade GitOps and Progressive Delivery pipeline powered by the Argo ecosystem.

### Core Components

-   **ArgoCD**: The `infra/argocd/nexus-application.yaml` file defines the NEXUS system as an `Application` resource. This tells ArgoCD to continuously monitor the `infra/kubernetes` directory in this Git repository and ensure that the live state of the Kubernetes cluster matches the state defined in these manifests. This provides a single source of truth and automated, auditable deployments.
-   **Argo Rollouts**: The `infra/kubernetes/rollouts/meta-controller-rollout.yaml` file defines a `Rollout` resource, which replaces the standard `Deployment`. This custom resource orchestrates a sophisticated canary release strategy.
-   **Analysis Templates**: The `infra/kubernetes/rollouts/analysis-templates.yaml` file defines automated health checks. The `Rollout` uses these templates to query Prometheus and verify that key SLOs (like success rate and latency) are met before promoting a new version, automatically rolling back if they are not.

### Deployment Steps

1.  **Install ArgoCD and Argo Rollouts**: Follow their official documentation to install these tools into your Kubernetes cluster.
2.  **Apply the ArgoCD Application**:
    ```sh
    # This only needs to be done once.
    kubectl apply -f infra/argocd/nexus-application.yaml
    ```
    ArgoCD will now automatically detect and deploy all the manifests in the `infra/kubernetes` directory, including the new `Rollout` resources.
3.  **Triggering a New Release**:
    To deploy a new version of the `meta-controller`, simply update the `image:` tag in the `infra/kubernetes/rollouts/meta-controller-rollout.yaml` file and commit the change to the `main` branch. ArgoCD will detect the change and automatically begin the canary release process defined in the `Rollout` resource. You can observe the entire process in the ArgoCD UI.