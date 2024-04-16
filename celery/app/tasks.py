from config import config
from worker import celery
# from celery import Celery
from celery.schedules import crontab
import time
import glob
from datetime import datetime, timezone, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
# from celery.task.control import inspect
import logging
import pytz

# Tạo logger
logger = logging.getLogger(__name__)


engine = create_engine((f'postgresql+psycopg2://{config["POSTGRES_USER"]}:'
            f'{config["POSTGRES_PASSWORD"]}@{config["POSTGRES_HOST"]}:'
            f'{config["POSTGRES_PORT"]}/{config["POSTGRES_DB"]}'))

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# app = Celery('tasks',
#              broker='amqp://admin:mypass@rabbit:5672',
#              backend='rpc://')

tts_api = "http://tts_service:3000/tts"

@celery.task(name=config["CELERY_TASK"], queue='tasks', bind=True)
def tts(self, title, url, category, published, content):
    pass