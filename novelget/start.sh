#!/bin/bash
set -e
LOGFILE=/root/django-git/logs/novel.log
# log路径
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=5
#下面有解释
# user/group to run as
USER=root
GROUP=root
cd /root/django-git/novelist/novelget
#web的路径
test -d $LOGDIR || mkdir -p $LOGDIR
exec gunicorn -w $NUM_WORKERS -b 0.0.0.0:8000 novelget.wsgi:application --user=$USER --group=$GROUP
#8000是端口 可随意修改
