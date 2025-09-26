#!/bin/sh
set -e  # если какая-то команда упадёт — скрипт завершится
set -o allexport
if [ -f /root/app/.env ]; then
  . /root/app/.env
fi
set +o allexport
echo "run extract.py..."
/opt/venv/bin/python3 /root/app/scripts/extract.py

echo "run transform.py..."
/opt/venv/bin/python3 /root/app/scripts/transform.py