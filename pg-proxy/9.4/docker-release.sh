#!/bin/bash

REGISTRY="btc-hedge/"
IMAGE_NAME="postgres-proxy"
VERSION="9.4"

IMAGE="${REGISTRY}${IMAGE_NAME}:${VERSION}"

docker build -t ${IMAGE} .
if [ "$?" != "0" ]; then
    echo "${IMAGE} build fail"
    exit 1
fi

docker tag ${REGISTRY}${IMAGE_NAME}:${VERSION} ${REGISTRY}${IMAGE_NAME}:latest

if [ "$1" == "push" ]; then
    docker push ${IMAGE}
    if [ "$?" != "0" ]; then
        echo "${IMAGE} push fail"
        exit 1
    fi
fi
