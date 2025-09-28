#!/bin/sh
set -e  
#тянем переменные окружения из .env
set -o allexport
if [ -f /root/.env ]; then
  . /root/.env
fi
set +o allexport
#запуск extract и transform
echo "$(date '+%Y-%m-%d %H:%M:%S,%3N') -  INFO - run_refresh_db.sh - run extract.py..."
/opt/venv/bin/python3 /root/app/workers/extract.py

echo "$(date '+%Y-%m-%d %H:%M:%S,%3N') -  INFO - run_refresh_db.sh -  run transform.py..."
/opt/venv/bin/python3 /root/app/workers/transform.py