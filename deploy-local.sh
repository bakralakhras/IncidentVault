#!/bin/bash

CHART_PATH=./helm/incidentvault
RELEASE_NAME=incidentvault
DOCKER_USER=bakrferas
IMAGE_NAME=incidentvault

echo "📥 Pulling latest code from GitHub..."
git pull origin main

SHA=$(git rev-parse --short HEAD)
echo "🔖 Using image tag: ${SHA}"

echo "📥 Pulling Docker image ${DOCKER_USER}/${IMAGE_NAME}:${SHA} from Docker Hub..."
docker pull ${DOCKER_USER}/${IMAGE_NAME}:${SHA}

echo "📦 Loading image into Minikube..."
minikube image load ${DOCKER_USER}/${IMAGE_NAME}:${SHA}

echo "🚀 Deploying via Helm..."
helm upgrade --install ${RELEASE_NAME} ${CHART_PATH} \
  --set image.repository=${DOCKER_USER}/${IMAGE_NAME} \
  --set image.tag=${SHA} \
  --set image.pullPolicy=IfNotPresent

echo "🔌 Port forwarding 8000 -> service/${RELEASE_NAME}"
kubectl port-forward svc/${RELEASE_NAME} 8000:8000
