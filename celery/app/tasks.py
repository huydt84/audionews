import time
import glob
from datetime import datetime, timezone, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import logging
import pytz
import uuid
import requests

from config import config
from worker import celery
from models import Article
from utils import slug

# Tạo logger
logger = logging.getLogger(__name__)


engine = create_engine((f'postgresql+psycopg2://{config["POSTGRES_USER"]}:'
            f'{config["POSTGRES_PASSWORD"]}@{config["POSTGRES_HOST"]}:'
            f'{config["POSTGRES_PORT"]}/{config["POSTGRES_DB"]}'))

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


tts_api = "http://tts_service:3000/tts"

@celery.task(name=config["CELERY_TASK"], queue='tasks', bind=True)
def tts(self, title, url, category, published, content, image_url, description):
    # Create folder
    folder_name = str(uuid.uuid4())
    # os.mkdir(f"audio/{folder_name}")

    # Save to database
    data = Article(
        link_source=url,
        title=title,
        category=category,
        content=content,
        image_url=image_url,
        description=description,
        slug_url=slug(title),
        path_audio=folder_name,
        written_at = published
    )

    session.add(data)
    session.commit()

    # Get audio
    response = requests.post(url=tts_api, json={"content": content, "folder_name": folder_name})
    while response.status_code != 200:
        response = requests.post(url=tts_api, json={"content": content, "folder_name": folder_name})
    # print(len(response.content))
    # if response.status_code == 200:
    #     with open(f"audio/{folder_name}/male-north.wav", "wb") as f:
    #         f.write(response.content)

    # response = requests.post(url=f"{tts_api}/female-north", json={"content": content}, timeout=20)
    # if response.status_code == 200:
    #     with open(f"audio/{folder_name}/female-north.wav", "wb") as f:
    #         f.write(response.content)

    # response = requests.post(url=f"{tts_api}/male-south", json={"content": content}, timeout=20)
    # if response.status_code == 200:
    #     with open(f"audio/{folder_name}/male-south.wav", "wb") as f:
    #         f.write(response.content)

    # response = requests.post(url=f"{tts_api}/female-south", json={"content": content}, timeout=20)
    # if response.status_code == 200:
    #     with open(f"audio/{folder_name}/female-south.wav", "wb") as f:
    #         f.write(response.content)

