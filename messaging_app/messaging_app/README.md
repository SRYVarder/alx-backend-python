# messaging_app - Kubernetes exercises (alx-backend-python)

This repository contains Kubernetes manifests and helper scripts to complete the 'Basics of container orchestration with Kubernetes' project.

## Files added
- kurbeScript             - starts minikube and verifies cluster
- deployment.yaml         - Django deployment + ClusterIP service (v1.0)
- kubctl-0x01             - scales deployment to 3 replicas and runs checks
- ingress.yaml            - Ingress resource for nginx ingress controller
- commands.txt            - commands used to apply ingress
- blue_deployment.yaml    - blue deployment (v1)
- green_deployment.yaml   - green deployment (v2)
- kubeservice.yaml        - service used to switch traffic between blue/green
- kubctl-0x02             - script to apply blue/green and check logs
- kubctl-0x03             - perform rolling update and test for downtime
- Dockerfile              - example dockerfile for the Django app
- requirements.txt

## Usage notes
- Replace `docker.io/yourusername/messaging_app:1.0` and `2.0` with your real image names.
- Minikube (or any Kubernetes cluster) and kubectl must be installed.
- For ingress on minikube: `minikube addons enable ingress`
- Metrics-server may be required for `kubectl top`.
- Scripts are idempotent and include helpful echo lines.
