# Vote App — Kubernetes

Short description
A sample containerized "vote" application composed of a frontend, backend, worker, and supporting infrastructure. This repository contains Docker Compose files for local testing and Kubernetes manifests for deploying to a cluster.

Table of Contents
- Project overview
- Repository layout
- Prerequisites
- Local development (Docker Compose)
- Kubernetes deployment
- Building and publishing images
- Environment variables
- Debugging & logs
- Contributing
- License
- Contact

Project overview
This project demonstrates a small microservices stack for a voting app:
- Frontend: Single-page app for users to vote.
- Backend: API service that accepts votes and serves results.
- Worker: Background processor (e.g., tallying or post-processing).
- Result: Service or store responsible for aggregated results (may be a service or DB).
- NGINX: Reverse proxy / gateway configuration for routing.

Repository layout
Top-level
- docker-compose.yml — docker-compose configuration for local testing
- backend/ — backend service source and Dockerfile
- frontend/ — frontend app source and Dockerfile
- worker/ — worker service source and Dockerfile
- result/ — result service or configuration
- nginx/ — nginx config and Dockerfile (if used as reverse proxy)
- k8s/ — Kubernetes manifests (Deployments, Services, ConfigMaps, possibly Ingress)

Prerequisites
- Docker (for local builds and docker-compose)
- Docker Compose (v1.27+ or compatible)
- kubectl (for Kubernetes operations)
- A Kubernetes cluster (minikube, kind, or a cloud cluster) if deploying to k8s
- (Optional) A container registry (Docker Hub, GitHub Container Registry, etc.) to push images for use in a remote cluster

Local development (Docker Compose)
1. Inspect or create an env file:
   - Check for env examples in each service folder (e.g., `backend/.env.example` or `frontend/.env.example`) and copy them to `.env` or service-specific .env files.
2. Build and start services:
   - docker-compose up --build
3. Access the application:
   - The docker-compose.yml in the repository defines service ports — open the configured port on localhost (check the compose file).
4. Useful commands:
   - docker-compose up --build
   - docker-compose up -d
   - docker-compose logs -f <service-name>
   - docker-compose down

Kubernetes deployment
Note: Kubernetes manifests live in the `k8s/` directory. Before applying them, ensure container images referenced in manifests are available to your cluster (either by pushing to a registry or by loading into local cluster).

1. (Optional) Build and push images
   - docker build -t <registry>/<repo>-frontend:tag ./frontend
   - docker push <registry>/<repo>-frontend:tag
   - Repeat for backend, worker, result, nginx as needed.

2. Apply manifests
   - kubectl apply -f k8s/
   - Verify:
     - kubectl get namespaces
     - kubectl get pods -A
     - kubectl get svc -A

3. If using an Ingress, ensure your cluster has an ingress controller and that DNS/hosts are configured appropriately.

Building and publishing images (examples)
- docker build -t my-registry/vote-frontend:latest ./frontend
- docker push my-registry/vote-frontend:latest
- docker build -t my-registry/vote-backend:latest ./backend
- docker push my-registry/vote-backend:latest

If using minikube:
- eval $(minikube docker-env)
- docker build -t vote-backend:local ./backend
- kubectl apply -f k8s/

If using kind:
- kind load docker-image vote-backend:local --name <cluster-name>

Environment variables
- Each service may require environment variables (ports, DB connection strings, credentials). Check service directories (`backend/`, `frontend/`, etc.) for `.env` or configuration files.
- Typical envs to verify:
  - BACKEND_PORT, DATABASE_URL, REDIS_URL, FRONTEND_API_URL, etc.
- Do not commit secrets to the repository. Use Kubernetes Secrets or a secrets manager for production deployments.

Debugging & logs
- Docker Compose:
  - docker-compose logs -f backend
  - docker-compose logs --tail=200
- Kubernetes:
  - kubectl logs deployment/<deployment-name>
  - kubectl logs -l app=<label-selector>
  - kubectl describe pod <pod-name> — to inspect events

Tips & common issues
- Images not found in k8s: ensure images are pushed to a registry or loaded into the cluster.
- Ports conflict locally: check docker-compose.yml and change host ports if needed.
- DB/Redis connections: confirm environment variables and that dependent services are reachable.

Contributing
- Feel free to open issues or pull requests.

Contact
- Repository owner: @usmanfarooq317

Acknowledgements
- This README is a generic template tailored to the repository structure found in the project. Update any service-specific details (ports, image names, env vars) using the actual files in each service folder.
