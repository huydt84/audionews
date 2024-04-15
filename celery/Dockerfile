# syntax=docker/dockerfile:1

FROM python:3.8-slim

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt --no-cache-dir

COPY ./app /app/

WORKDIR /app

CMD celery -A tasks worker \
    --concurrency=3 \
    --loglevel=INFO \
    -B