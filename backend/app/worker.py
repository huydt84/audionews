from celery import Celery
from kombu import Exchange, Queue
from config import config

celery = Celery(
    "celery",
    backend=config["CELERY_BROKER_URL"],
    broker=config["CELERY_RESULT_BACKEND"],
)
celery.conf.task_queues = [
    Queue(
        "tasks",
        Exchange("tasks"),
        routing_key="tasks",
        queue_arguments={"x-max-priority": int(config["X_MAX_PRIORITY"])},
    )

]
celery.conf.task_queue_max_priority = int(config["X_MAX_PRIORITY"])
celery.conf["worker_prefetch_multiplier"] = config["CELERYD_PREFETCH_MULTIPLIER"]
celery.conf["task_acks_late"] = config["CELERY_ACKS_LATE"]