import os

config = {
    "CELERY_TASK": os.environ.get("CELERY_TASK") or "tasks.convert",
    "CELERY_BROKER_URL": os.environ.get("CELERY_BROKER_URL", "amqp://guest:**@localhost:5672//"),
    "CELERY_RESULT_BACKEND": os.environ.get("CELERY_RESULT_BACKEND", "amqp://guest:**@localhost:5672//"),
    "CELERY_ACKS_LATE": os.environ.get("CELERY_ACKS_LATE", None),
    "CELERYD_PREFETCH_MULTIPLIER": os.environ.get("CELERYD_PREFETCH_MULTIPLIER", None),
    "X_MAX_PRIORITY": os.environ.get("X_MAX_PRIORITY", None),
}
