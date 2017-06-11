FROM python:2.7-slim
MAINTAINER "Bijia Lan <lbj.world@gmail.com>"

# add user
ENV SERVICE_USER btc_hedge
RUN useradd -ms /bin/bash $SERVICE_USER

# install libs
COPY ./btc_hedge/requirements.txt /
ADD ./jessie-sources.list /etc/apt/sources.list
RUN apt-get update \
    && apt-get install -y build-essential \
                          libpq-dev \
                          gettext \
                          git \
                          libffi-dev \
    && pip install -r /requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com \
    && apt-get purge -y build-essential git \
    && apt-get autoremove -y \
    && apt-get remove -y libpq-dev libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# setup env
ENV SERVICE_PORT 8000
EXPOSE $SERVICE_PORT

ADD ./btc_hedge /code
WORKDIR /code

# change dir owner
RUN chown -R $SERVICE_USER /code
USER $SERVICE_USER

# run task
CMD ./run-site.sh
