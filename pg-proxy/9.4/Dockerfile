FROM postgres:9.4
MAINTAINER "Bijia Lan <lbj.world@gmail.com>"

ADD ./jessie-sources.list /etc/apt/sources.list
RUN apt-get update && apt-get -y install wget ca-certificates python-psycopg2 && rm -rf /var/lib/apt/lists/*
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
    && apt-get update && apt-get install -y pgbouncer \
    && rm -rf /var/lib/apt/lists/*

ENV POSTGRES_MAX_CLIENT_CONN 10000
ENV POSTGRES_DEFAULT_POOL_SIZE 400
ENV POSTGRES_SERVER_LIFETIME 300
ENV POSTGRES_SERVER_IDLE_TIMEOUT 240
ENV POSTGRES_SERVER_CONNECT_TIMEOUT 15

COPY docker-entrypoint.sh /

EXPOSE 5433
ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["postgres"]
