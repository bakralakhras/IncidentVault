#!/bin/bash
CHART_PATH=./helm/incidentvault
RELEASE_NAME=incidentvault
IMAGE_NAME=incidentvault
SHA=$(git rev-parse --short HEAD)
echo "👉 Using image tag: $SHA"
minikube image load ${IMAGE_NAME}:${SHA}
helm upgrade --install ${RELEASE_NAME} ${CHART_PATH} --set image.repository=${IMAGE_NAME} --set image.tag=${SHA}
kubectl port-forward svc/${RELEASE_NAME} 8000:8000
