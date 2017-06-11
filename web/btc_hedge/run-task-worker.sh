#!/bin/bash

source env.sh

echo "connecting to cache ..."
wait_tcp_dependency ${MEMCACHED_HOST} ${MEMCACHED_PORT}
echo "connecting to redis ..."
wait_tcp_dependency ${REDIS_HOST} ${REDIS_PORT}
echo "connecting to db ..."
wait_tcp_dependency ${POSTGRES_HOST} ${POSTGRES_PORT}

echo "run celery worker ..."
export CELERY_BROKER_URL=redis://${REDIS_HOST}:${REDIS_PORT}
rm celerybeat.pid
celery --app=btc_hedge.celery:app worker --loglevel=DEBUG --autoreload &
celery --app=btc_hedge.celery:app beat -S djcelery.schedulers.DatabaseScheduler
