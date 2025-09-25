#!/bin/sh
set -e  # если какая-то команда упадёт — скрипт завершится

echo "🚀 Запускаю extract.py..."
python3 scripts/extract.py

echo "🚀 Запускаю transform.py..."
python3 scripts/transform.py