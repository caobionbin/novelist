#!/bin/bash
set -e
LOGFILE=/root/django-git/logs/novel.log

LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=2

# user/group to run as
USER=root
GROUP=root
cd /root/django-git/novelist/novelget

test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn -w $NUM_WORKERS -b 0.0.0.0:8000 novelget.wsgi:application --user=$USER --group=$GROUP
