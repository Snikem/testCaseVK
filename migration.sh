#!/bin/bash
set -e

# Запускаем Postgres в фоне
docker-entrypoint.sh postgres &

# Ждём пока база будет доступна
until pg_isready -h localhost -p 5432 -U "$POSTGRES_USER"; do
  sleep 1
done

python3 migrations.py
cron && tail -f /var/log/cron.log
# Чтобы контейнер не завершился сразу, держим postgres в переднем плане
wait -n