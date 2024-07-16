# Kubernetes Project

The project includes configurations and resources to deploy and manage applications on Kubernetes.

## Overview

This project is designed to demonstrate Kubernetes deployment practices and configurations for scalable and manageable application deployments.

## Features

- **Deployment Configurations**: Includes YAML files for deploying applications on Kubernetes clusters.
- **Service Definitions**: Configurations for defining services to expose applications internally or externally.
- **Usage Examples**: Sample applications or configurations to illustrate deployment scenarios.

## Getting Started

To get started with this project, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/rapkeb/k8s_project.git
   cd k8s_project
2. **run the commands**:
   ```bash
   cd kubernetes
   kubectl apply -f mongo.yaml
   *make sure to wait until the mongo pod is running before continue to the next command*
   kubectl apply -f data-loader.yaml
   kubectl create configmap nginx-config --from-file=frontend.conf
   kubectl apply -f frontend.yaml
   kubectl apply -f backend.yaml
   kubectl apply -f ingress.yaml
   minikube addons enable ingress
   minikube tunnel
