FROM python:3.11-slim


RUN apt-get update && apt-get install -y \
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
RUN apt-get update && \
    apt-get install -y cron gettext-base && \
    rm -rf /var/lib/apt/lists/*

COPY app/crons/crontab.template .


RUN chmod +x crontab.template

RUN touch /var/log/cron.log

WORKDIR /root/app/scripts
COPY app/bash_scripts/migration.sh .
RUN chmod +x migration.sh

CMD ["./migration.sh"]
