FROM python:3.11-slim

# установка крона и билдера для psycopg2
RUN apt-get update && apt-get install -y \
    cron \
    cron gettext-base \
    build-essential libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*


COPY . /root 
WORKDIR /root

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip3 install --no-cache-dir -r requirements.txt

RUN chmod +x init_project/_run_init.sh
RUN chmod +x app/workers/_run_workers.sh
WORKDIR /root/init_project
CMD ["./_run_init.sh"]
