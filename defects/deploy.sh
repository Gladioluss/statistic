#!/bin/bash

echo "Creating the volume..."
kubectl apply -f ./kubernetes/persistent-volume.yaml
kubectl apply -f ./kubernetes/persistent-volume-claim.yaml
echo ""

echo "Creating the database credentials..."
kubectl apply -f ./kubernetes/database/db-secret.yaml
echo ""

echo "Creating the api server credentials..."
kubectl apply -f ./kubernetes/app/app-secret.yaml
echo ""

echo "Creating the Postgres deployment and service..."
kubectl apply -f ./kubernetes/database/db-deployment.yaml
kubectl apply -f ./kubernetes/database/db-service.yaml
echo ""

echo "Creating the FastAPI deployment and service..."
kubectl apply -f ./kubernetes/app/app-deployment.yaml
kubectl apply -f ./kubernetes/app/app-service.yaml
echo ""


#watch kubectl get pods -A

