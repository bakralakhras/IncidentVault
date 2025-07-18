#!/bin/bash
CHART_PATH=./helm/incidentvault
RELEASE_NAME=incidentvault
IMAGE_NAME=incidentvault
SHA=$(git rev-parse --short HEAD)

echo "Building Docker image: ${IMAGE_NAME}:${SHA}"
docker build -f docker/Dockerfile -t ${IMAGE_NAME}:${SHA} .

echo "Loading image into Minikube..."
minikube image load ${IMAGE_NAME}:${SHA}

echo "Deploying with Helm..."
helm upgrade --install ${RELEASE_NAME} ${CHART_PATH} \
  --set image.repository=${IMAGE_NAME} \
  --set image.tag=${SHA}

echo "Forwarding port 8000 to service/${RELEASE_NAME}"
kubectl port-forward svc/${RELEASE_NAME} 8000:8000
