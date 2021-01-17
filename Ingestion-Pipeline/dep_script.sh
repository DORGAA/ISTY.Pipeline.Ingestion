#!/usr/bin/bash

NUMBER=$1

sam build

sam deploy --no-fail-on-empty-changeset --parameter-overrides "ParameterKey=Number,ParameterValue=${NUMBER}"
