#!/bin/bash

for pid in $(ps -ef | grep uwsgi | grep -v grep | cut -c 10-15); do
    echo $pid
    kill -9 $pid
done

for pid in $(ps -ef | grep nginx| grep -v grep | cut -c 10-15); do
    echo $pid
    kill -9 $pid
done