from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager

from fastapi_pagination import Page, add_pagination, paginate

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
    articles = sql_session["session"].query(Article.id, Article.title, Article.link_source, Article.image_url, Article.description, Article.slug_url, Article.written_at) \
                                    .all().order_by(Article.id.desc())

    news = []
    for id, title, link_source, image_url, description, slug_url, written_at in articles:
        news.append({"id": id, "title": title, "link_source": link_source,
                     "image_url": image_url, "description": description,
                     "slug_url": slug_url,
                     "written_at": written_at.strftime("%m/%d/%Y, %H:%M:%S")})

    return {"message": paginate(news)}

@app.get("/api/news/category/{category}")
async def get_all_category(category: str):
    articles = sql_session["session"].query(Article.id, Article.title, Article.link_source, Article.image_url, Article.description, Article.slug_url, Article.written_at) \
                                    .filter(Article.category == category).all().order_by(Article.id.desc())

    news = []
    for id, title, link_source, image_url, description, slug_url, written_at in articles:
        news.append({"id": id, "title": title, "link_source": link_source,
                     "image_url": image_url, "description": description,
                     "slug_url": slug_url,
                     "written_at": written_at.strftime("%m/%d/%Y, %H:%M:%S")})

    return {"message": paginate(news)}

@app.get("/api/news/{slug_url}")
async def get_one(slug_url: str):
    articles = sql_session["session"].query(Article.id, Article.title, Article.link_source, Article.content, Article.slug_url, Article.written_at) \
                                    .filter(Article.slug_url == slug_url).all().order_by(Article.id.desc())

    news = []
    for id, title, link_source, content, slug, written_at in articles:
        news.append({"id": id, "title": title, "link_source": link_source, "content": content, "slug_url": slug,
                     "audio_male-north": f"/api/news/audio/{id}/male-north",
                     "audio_female-north": f"/api/news/audio/{id}/female-north",
                     "audio_male-south": f"/api/news/audio/{id}/male-south",
                     "audio_female-south": f"/api/news/audio/{id}/female-south",
                     "audio_female-central": f"/api/news/audio/{id}/female-central",
                     "written_at": written_at.strftime("%m/%d/%Y, %H:%M:%S")})

    return {"message": paginate(news)}

@app.get("/api/news/audio/{id}/{voice}")
async def get_audio(id: int, voice: Literal["male-north", "female-north", "male-south", "female-south", "female-central"]):
    folder_path = sql_session["session"].query(Article.path_audio).filter(Article.id == id).first()
    file_name = voice + ".wav"
    audio_path = os.path.join("audio", folder_path[0], file_name)

    return FileResponse(audio_path)

add_pagination(app)
