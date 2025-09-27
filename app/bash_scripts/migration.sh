#!/bin/bash
set -e

python3 migration.py

echo "$(date '+%Y-%m-%d %H:%M:%S,%3N') -  INFO - migration.sh - run crontab"

#запуск крона
cd ..
envsubst < crontab.template > /etc/cron.d/app-cron
chmod 0644 /etc/cron.d/app-cron

crontab /etc/cron.d/app-cron
cron 
python3 scripts/api/router.py &
wait -n