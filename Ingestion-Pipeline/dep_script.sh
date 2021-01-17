
set -e


NUMBER=$1
pushd "Ingestion-Pipeline"
sam build

sam deploy --no-fail-on-empty-changeset --parameter-overrides "ParameterKey=Number,ParameterValue=${NUMBER}"

popd
