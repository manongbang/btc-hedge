#!/bin/bash

source env.sh

echo "connecting to cache ..."
wait_tcp_dependency ${MEMCACHED_HOST} ${MEMCACHED_PORT}
echo "connecting to redis ..."
wait_tcp_dependency ${REDIS_HOST} ${REDIS_PORT}
echo "connecting to db ..."
wait_tcp_dependency ${POSTGRES_HOST} ${POSTGRES_PORT}

# do database migration
python manage.py makemigrations
python manage.py migrate
# do translation
python manage.py compilemessages
# collect static files
python manage.py collectstatic --noinput
# run server
export CELERY_BROKER_URL=redis://${REDIS_HOST}:${REDIS_PORT}
# python manage.py runserver 0.0.0.0:${SERVICE_PORT}
uwsgi --ini uwsgi.ini
