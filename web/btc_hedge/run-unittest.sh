#!/bin/bash

source env.sh

echo "connecting to cache ..."
wait_tcp_dependency ${MEMCACHED_HOST} ${MEMCACHED_PORT}
#echo "connecting to redis ..."
#wait_tcp_dependency ${REDIS_HOST} ${REDIS_PORT}
echo "connecting to db ..."
wait_tcp_dependency ${POSTGRES_HOST} ${POSTGRES_PORT}

coverage run manage.py test --keepdb --noinput --parallel=1 ${TEST_PARAMETER} 2>&1
coverage report
