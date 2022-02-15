#!/bin/sh

set -e

. /venv/bin/activate

while ! flask db upgrade
do
     echo "Retry..."
     sleep 1
done

exec gunicorn --bind 0.0.0.0:5000 --forwarded-allow-ips='*' wsgi:app