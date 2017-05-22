#!/bin/bash

echo "building pg-proxy ..."
cd pg-proxy/9.4/
./docker-release.sh
cd -
echo "build pg-proxy done"

echo "building web ..."
cd web/
./docker-release.sh
cd -
echo "build web done"

echo "building rproxy ..."
cd rproxy/openresty_dns/
./docker-release.sh
cd -
echo "build rproxy done"
