#!/bin/sh
set -e

apk add --no-cache python3 py3-pip py3-wheel py3-greenlet py3-psycopg2 py3-pillow
grep -ivE "^#|psycopg2|Pillow" /app/requirements.txt > /tmp/requirements.txt
pip install -r /tmp/requirements.txt

sleep 5
exec python3 -m $START_COMMAND
