#!/bin/bash

ENV=$1
USERS=$2
SPAWN_RATE=$3
RUN_TIME=$4

function USAGE() {
  echo "USAGE: ./stress-test.sh <sbx|prd> <users> <spawn_rate> <run_time>" &>/dev/stderr
  echo "EXAMPLE: ./stress-test.sh sbx 1000 100 1h10m"
  echo "'users' are the number of users to spawn."
  echo "'spawn_rate' is the number of users to start per second."
  echo "'run_time' is total run time for the test."
  exit 1
}

if [[ -z "$4" ]]; then
  USAGE
fi

if [[ -z "$X_API_KEY" ]]; then
  echo "X_API_KEY must be defined."
fi

if [[ "sbx" != "$ENV" && "prd" != "$ENV" ]]; then
  USAGE
fi

HOST="https://prio-api-$ENV.iberia.accentureanalytics.com"

locust --host $HOST -f app/flex/tests/locustfile.py --headless -u $USERS -r $SPAWN_RATE --run-time $RUN_TIME