FROM postgres:16

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip


COPY app/scripts /app/scripts

COPY requirements.txt /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt