#!/usr/bin/env bash 

set -e

if [[ -z "${GITHUB_ACTIONS}" ]]; then
    cd "$(dirname "$0")"
fi

if [ "${LOCAL_IMAGE_NAME}" == "" ]; then
    LOCAL_TAG=`date "+%Y-%m-%d-%H-%M"`
    export LOCAL_IMAGE_NAME="stream-model-duration:${LOCAL_TAG}"
    export PREDICTIONS_STREAM_NAME="ride_predictions"
    docker build -t ${LOCAL_IMAGE_NAME} ../
else
    echo "Using image ${LOCAL_IMAGE_NAME}"
fi

export PREDICTIONS_STREAM_NAME="ride_predictions"

docker compose up -d

sleep 1

aws --endpoint-url=http://localhost:4566 \
	kinesis create-stream \
	--stream-name ${PREDICTIONS_STREAM_NAME} \
	--shard-count 1

pipenv run python test_docker.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker compose logs
    docker compose down
    exit ${ERROR_CODE}
fi

pipenv run python test_kinesis.py

ERROR_CODE=$?

if [ ${ERROR_CODE} != 0 ]; then
    docker compose logs
    docker compose down
    exit ${ERROR_CODE}
fi

docker compose down

