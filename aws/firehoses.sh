#!/bin/bash

AWS_PROFILE=$1
ENV=$2

usage() {
  echo "USAGE: firehoses.sh <AWS_PROFILE> <sbx|prd>"
  echo "This script recreates PRIO-API AWS Firehoses from either SBX or PRD AIP envs"
  exit 1
}

if [[ "sbx" != "$ENV" && "prd" != "$ENV" ]]; then
  usage
fi

aws --profile=$AWS_PROFILE firehose delete-delivery-stream --delivery-stream-name ibr-prio-request-confirm-$ENV
aws --profile=$AWS_PROFILE firehose delete-delivery-stream --delivery-stream-name ibr-prio-response-confirm-$ENV
echo "Waiting 60 seconds until firehoses are effectively deleted..."
sleep 60;

aws --profile=$AWS_PROFILE firehose create-delivery-stream --delivery-stream-name ibr-prio-request-confirm-$ENV --extended-s3-destination-configuration file://ibr-prio-request-confirm-$ENV.json
aws --profile=$AWS_PROFILE firehose create-delivery-stream --delivery-stream-name ibr-prio-response-confirm-$ENV --extended-s3-destination-configuration file://ibr-prio-response-confirm-$ENV.json

echo "Firehoses successfully recreated"


