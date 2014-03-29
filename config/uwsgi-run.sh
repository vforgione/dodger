#!/bin/bash

echo "killing wsgi processes"
ps -ef | grep wsgi | awk '{print $2}' | xargs kill -9

echo "starting mew wsgi processes"
NEW_RELIC_CONFIG_FILE=/home/deploy/dodger-env/dodger/config/newrelic.ini newrelic-admin run-program uwsgi --ini /home/deploy/dodger-env/dodger/config/uwsgi.ini --single-interpreter --enable-threads
