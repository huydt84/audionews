#!/bin/sh

# Spawn celery workers
echo "Spawn celery workers"
celery -A tasks worker \
    --concurrency=3 \
    --loglevel=INFO \
    -B