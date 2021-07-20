#!/bin/bash

export ENV=$1
export VERSION=$2

declare -A EKS_CLUSTER
EKS_CLUSTER['sbx']='sbxeu-ibr-cluster-eks'
EKS_CLUSTER['prd']='prdeu-ibr-cluster-eks'

declare -A REPLICAS
REPLICAS['sbx']=1
REPLICAS['prd']=2
export REPLICAS

function USAGE() {
  echo "USAGE: ./deploy.sh <sbx|prd> <VERSION>" &>/dev/stderr
  echo "EXAMPLE: ./deploy.sh prd 0.0.1"
  exit 1
}

if [[ -z "$2" ]]; then
  USAGE
fi

if [[ "sbx" != "$ENV" && "prd" != "$ENV" ]]; then
  USAGE
fi

if [[ -z "$AWS_PROFILE" ]]; then
  echo "ERROR: AWS_PROFILE environment variable must be defined" &> /dev/stderr
  exit 1
fi

# EKS login
aws --profile="$AWS_PROFILE" eks --region eu-west-1 update-kubeconfig --name "${EKS_CLUSTER[$ENV]}"

# Re-create configmaps
kubectl --cluster=arn:aws:eks:eu-west-1:077156906314:cluster/${EKS_CLUSTER[$ENV]} delete configmap prio-api-configmap
kubectl --cluster=arn:aws:eks:eu-west-1:077156906314:cluster/${EKS_CLUSTER[$ENV]} create configmap prio-api-configmap --from-env-file=${ENV}.properties 

# Re-create secrets
kubectl --cluster=arn:aws:eks:eu-west-1:077156906314:cluster/${EKS_CLUSTER[$ENV]} delete secret prio-api-secrets
kubectl --cluster=arn:aws:eks:eu-west-1:077156906314:cluster/${EKS_CLUSTER[$ENV]} create secret generic prio-api-secrets --from-env-file="${ENV}".secrets

envsubst < k8s/deployment.yml.tpl | kubectl --cluster=arn:aws:eks:eu-west-1:077156906314:cluster/${EKS_CLUSTER[$ENV]} apply -f -

kubectl --cluster=arn:aws:eks:eu-west-1:077156906314:cluster/${EKS_CLUSTER[$ENV]} rollout restart deployment prio-api-deployment
