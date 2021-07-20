#!/bin/bash

ENV=$1

function USAGE() {
  echo "USAGE: ./run-docker.sh <sbx|prd> <VERSION>" &>/dev/stderr
  exit 1
}

if [[ -z "$2" ]]; then
  USAGE
fi

if [[ "sbx" != "$ENV" && "prd" != "$ENV" ]]; then
  USAGE
fi

docker run \
  --env-file="$ENV".properties \
  --env-file="$ENV".secrets \
  -p 8000:80 iberia-dataprep/prio-api:${VERSION}
