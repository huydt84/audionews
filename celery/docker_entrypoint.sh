#!/bin/sh

# Init database
echo "Create database"
python create_db.py

# Spawn celery workers
echo "Spawn celery workers"
celery -A tasks worker \
    --concurrency=3 \
    --loglevel=INFO \
    -B