#!/bin/bash

# input: tcp_addr, tcp_port
wait_tcp_dependency()
{
    local tcp_addr=$1;
    local tcp_port=$2;
    local testing_url="tcp://${tcp_addr}:${tcp_port}"

    # assign fd automatically
    # refer to http://stackoverflow.com/questions/8295908/how-to-use-a-variable-to-indicate-a-file-descriptor-in-bash
    while ! exec {id}<>/dev/tcp/${tcp_addr}/${tcp_port}; do
        echo "$(date) - trying to connect to ${testing_url}"
        sleep 1
    done
}

resolve_service()
{
    local service=$1;
    echo "querying "$service" service ..."
    is_local=$(echo $service | grep ':')
    if [ "$is_local" != "" ]; then
        # resolve local service
        raw_ip=$(echo $service | awk -F: '{print $1}')
        raw_port=$(echo $service | awk -F: '{print $2}')
        RESOLVE_IP=${raw_ip//\"/}
        RESOLVE_PORT=${raw_port//\"/}
    else
        # resolve remote service
        if [ "${DNS_SERVICE}" == "" ]; then
            echo "no DNS service found"
            exit 1
        fi
        result=`curl http://${DNS_SERVICE}/v1/services/${service}`
        raw_ip=$(echo $result | awk -F, '{print $3}' | awk -F: '{print $2}')
        RESOLVE_IP=${raw_ip//\"/}
        RESOLVE_IP=${RESOLVE_IP// /}
        raw_port=$(echo $result | awk -F, '{print $4}' | awk -F: '{print $2}' | awk -F} '{print $1}' )
        RESOLVE_PORT=${raw_port//\"/}
        RESOLVE_PORT=${RESOLVE_PORT// /}
    fi
    echo "query result (ip:"$RESOLVE_IP", port:"$RESOLVE_PORT")"
}

if [ "${DB_SERVICE}" != "" ]; then
    echo "setting DB service ..."
    resolve_service ${DB_SERVICE}
    export POSTGRES_HOST=$RESOLVE_IP
    export POSTGRES_PORT=$RESOLVE_PORT
fi
if [ "${REDIS_SERVICE}" != "" ]; then
    echo "setting redis service ..."
    resolve_service ${REDIS_SERVICE}
    export REDIS_HOST=$RESOLVE_IP
    export REDIS_PORT=$RESOLVE_PORT
fi
if [ "${CACHE_SERVICE}" != "" ]; then
    echo "setting cache redis service ..."
    resolve_service ${CACHE_SERVICE}
    export MEMCACHED_HOST=$RESOLVE_IP
    export MEMCACHED_PORT=$RESOLVE_PORT
fi
