#!/bin/bash

if [[ -z "$1" ]]; then
  echo "USAGE: ./build.sh <VERSION>" &> /dev/stderr
  exit 1
fi

if [[ -z "$AWS_PROFILE" ]]; then
  echo "ERROR: AWS_PROFILE environment variable must be defined" &> /dev/stderr
  exit 1
fi

VERSION="$1"

docker build --network=host . -t 077156906314.dkr.ecr.eu-west-1.amazonaws.com/prio-api:"${VERSION}"

if [[ $? != 0 ]]; then
  echo "ERROR: Unable to build the image" &> /dev/stderr
  exit 1
fi

aws --profile="$AWS_PROFILE" ecr get-login-password | docker login --username AWS --password-stdin 077156906314.dkr.ecr.eu-west-1.amazonaws.com

if [[ "$?" != "0" ]]; then
  exit 1
fi

docker push 077156906314.dkr.ecr.eu-west-1.amazonaws.com/prio-api:"$VERSION"
