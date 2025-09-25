FROM postgres:16


RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-venv \
    build-essential libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY requirements.txt .
COPY app/scripts scripts
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip3 install --no-cache-dir -r requirements.txt