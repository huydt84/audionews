from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager

import os
from typing import Literal

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config
from models import Article

sql_session = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_engine((f'postgresql+psycopg2://{config["POSTGRES_USER"]}:'
                f'{config["POSTGRES_PASSWORD"]}@{config["POSTGRES_HOST"]}:'
                f'{config["POSTGRES_PORT"]}/{config["POSTGRES_DB"]}'))

    Session = sessionmaker()
    Session.configure(bind=engine)
    sql_session["session"] = Session()
    yield
    sql_session.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/api/news")
async def get_all():
    articles = sql_session["session"].query(Article.id, Article.title, Article.link_source, Article.image_url, Article.description, Article.written_at).all()

    news = []
    for id, title, link_source, image_url, description, written_at in articles:
        news.append({"id": id, "title": title, "link_source": link_source,
                     "image_url": image_url, "description": description,
                     "written_at": written_at.strftime("%m/%d/%Y, %H:%M:%S")})

    return {"message": news}

@app.get("/api/news/category/{category}")
async def get_all_category(category: str):
    articles = sql_session["session"].query(Article.id, Article.title, Article.link_source, Article.image_url, Article.description, Article.written_at).filter(Article.category == category).all()

    news = []
    for id, title, link_source, image_url, description, written_at in articles:
        news.append({"id": id, "title": title, "link_source": link_source,
                     "image_url": image_url, "description": description,
                     "written_at": written_at.strftime("%m/%d/%Y, %H:%M:%S")})

    return {"message": news}

@app.get("/api/news/{id}")
async def get_one(id: int):
    articles = sql_session["session"].query(Article.id, Article.title, Article.link_source, Article.content, Article.written_at) \
                                    .filter(Article.id == id).all()

    news = []
    for id, title, link_source, content, written_at in articles:
        news.append({"id": id, "title": title, "link_source": link_source, "content": content,
                        "written_at": written_at.strftime("%m/%d/%Y, %H:%M:%S")})

    return {"message": news}

@app.get("/api/news/audio/{id}/{voice}")
async def get_audio(id: int, voice: Literal["male-north", "female-north", "male-south", "female-south"]):
    folder_path = sql_session["session"].query(Article.path_audio).filter(Article.id == id).first()
    file_name = voice + ".wav"
    audio_path = os.path.join("audio", folder_path[0], file_name)

    return FileResponse(audio_path)
