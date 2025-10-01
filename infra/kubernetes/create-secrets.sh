#!/bin/bash

# This script provides a secure way to create the Kubernetes secret
# required by the NEXUS application. It prompts for sensitive values
# and creates the secret directly in the cluster without storing
# the values in a file.

set -e

# Ensure the user has kubectl installed and configured.
if ! command -v kubectl &> /dev/null
then
    echo "ERROR: kubectl could not be found. Please install it and configure access to your cluster."
    exit 1
fi

echo "This script will create the 'nexus-secrets' Kubernetes secret in the 'nexus-production' namespace."
echo "You will be prompted for the required secret values."
echo

# Prompt for OpenAI API Key
read -sp "Enter your OpenAI API Key: " OPENAI_KEY
echo

# Prompt for Neo4j Password
read -sp "Enter the password for the Neo4j database: " NEO4J_PASS
echo

if [ -z "$OPENAI_KEY" ] || [ -z "$NEO4J_PASS" ]; then
    echo "ERROR: Both OpenAI API Key and Neo4j password are required."
    exit 1
fi

# Check if the namespace exists, create if it doesn't.
# This makes the script more robust.
if ! kubectl get namespace nexus-production > /dev/null 2>&1; then
  echo "Namespace 'nexus-production' not found. Creating it..."
  kubectl create namespace nexus-production
fi

# Create the secret using kubectl.
# Using --dry-run=client -o yaml | kubectl apply -f - makes the command idempotent.
# It will create the secret if it doesn't exist, or update it if it does.
echo "Creating/updating secret 'nexus-secrets'..."
kubectl create secret generic nexus-secrets \
  --namespace=nexus-production \
  --from-literal=OPENAI_API_KEY="$OPENAI_KEY" \
  --from-literal=NEO4J_PASSWORD="$NEO4J_PASS" \
  --dry-run=client -o yaml | kubectl apply -f -

echo
echo "✅ Secret 'nexus-secrets' created/updated successfully in namespace 'nexus-production'."