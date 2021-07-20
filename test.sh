#!/bin/bash

USAGE(){
  echo "USAGE: ./test.sh <local|sbx|prd>" &> /dev/stderr
  exit 1
}

if [[ -z "$1" ]]; then
  USAGE
fi

ENV=$1

if [[ "local" != "$ENV" && "sbx" != "$ENV" && "prd" != "$ENV" ]]; then
  USAGE
fi

set -o allexport
source ${ENV}.properties
source ${ENV}.secrets
set +o allexport

curl "${API_ENDPOINT}/health" -H "user-agent: x" -H "accept: application/json" -H "x-api-key: ${X_API_KEY}" -H "Content-Type: application/json"
