import logging
import requests

from config import config
from worker import celery

# Tạo logger
logger = logging.getLogger(__name__)

tts_api = "http://tts_service:3000/tts"

requests.adapters.DEFAULT_RETRIES = 5

@celery.task(name=config["CELERY_TASK"], queue='tasks', bind=True)
def tts(self, folder_name, content):
    # Get audio
    response = requests.post(url=tts_api, json={"content": content, "folder_name": folder_name}, timeout=120)

    return response.json()

