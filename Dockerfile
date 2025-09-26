FROM postgres:16


RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    build-essential libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /root/app


COPY app/python_scripts/requirements.txt .
COPY app/python_scripts scripts
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip3 install --no-cache-dir -r requirements.txt

COPY .env .

RUN chmod +x .env

COPY app/bash_scripts/run_refresh_db.sh .

RUN chmod +x run_refresh_db.sh

# Устанавливаем cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Копируем cron-файл
COPY crontab /etc/cron.d/app-cron

# Даем права
RUN chmod +x /etc/cron.d/app-cron

# Загружаем крон-задачи
RUN crontab /etc/cron.d/app-cron
RUN touch /var/log/cron.log

WORKDIR /root/app/scripts
COPY app/bash_scripts/migration.sh .
RUN chmod +x migration.sh

CMD ["./migration.sh"]
