#!/bin/bash

REGISTRY="btc-hedge/"
IMAGE_NAME="openresty"
VERSION="1.9-dns"

IMAGE="${REGISTRY}${IMAGE_NAME}:${VERSION}"

docker build -t ${IMAGE} .
if [ "$?" != "0" ]; then
    echo "${IMAGE} build fail"
    exit 1
fi

if [ "$1" == "push" ]; then
    docker push ${IMAGE}
    if [ "$?" != "0" ]; then
        echo "${IMAGE} push fail"
        exit 1
    fi
fi
