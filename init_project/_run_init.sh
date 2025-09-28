#!/bin/bash
set -e

#запуск миграций закомментить, если не нужны
echo "$(date '+%Y-%m-%d %H:%M:%S,%3N') -  INFO - migration.sh - run db migration"
python3 db_migration/migration.py

#запуск крона
echo "$(date '+%Y-%m-%d %H:%M:%S,%3N') -  INFO - migration.sh - run crontab"
envsubst < crons/crontab.template > /etc/cron.d/app-cron
chmod 0644 /etc/cron.d/app-cron
crontab /etc/cron.d/app-cron
cron 

#запуск api
echo "$(date '+%Y-%m-%d %H:%M:%S,%3N') -  INFO - migration.sh - run flask api"
python3 /root/app/api/router.py &
wait -n