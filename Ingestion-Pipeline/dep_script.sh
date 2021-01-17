#!/bin/bash
set -e
AWS_ACCESS_KEY_ID=${KEY_ID}
AWS_SECRET_ACCESS_KEY=${SECRET_KEY}

NMBR=$1
pushd "Ingestion-Pipeline"
sam build

sam deploy --no-fail-on-empty-changeset --parameter-overrides "ParameterKey=Number,ParameterValue=${NMBR}"

popd
