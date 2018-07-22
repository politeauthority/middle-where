#!/bin/sh
env | egrep '^ENV_' | cat - /tmp/crontab > /etc/crontabs/root
crond -L /var/log/cron/cron.log "$@" && tail -f /var/log/cron/cron.log
