#!/bin/bash
set -e

echo "$(date '+%Y-%m-%d %H:%M:%S,%3N') - INFO - migration.sh - run postgres"
docker-entrypoint.sh postgres &

until pg_isready -h localhost -p 5432 -U "$POSTGRES_USER"; do
  sleep 1
done

python3 migrations.py

echo "$(date '+%Y-%m-%d %H:%M:%S,%3N') - INFO - migration.sh - run crontab"
cron && tail -f /var/log/cron.log

wait -n