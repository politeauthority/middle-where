FROM frolvlad/alpine-python3
RUN apk update && apk add --no-cache \
    bash \
    openssh \
    curl \
    rsync \
    py-gunicorn
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev openssl openssl-dev
WORKDIR /opt/middle-where

VOLUME /data
VOLUME /root/.ssh/
VOLUME /opt/middle-where

COPY ./ /opt/middle-where
COPY crontab /tmp/crontab
COPY run-crond.sh /run-crond.sh
RUN pip3 install -r /opt/middle-where/requirements.txt
RUN mkdir -p /var/log/cron && touch /var/log/cron/cron.log

CMD ["/run-crond.sh", "gunicorn -b 0.0.0.0:13203 app:app"]
