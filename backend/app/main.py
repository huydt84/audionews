from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager

import os
from typing import Literal

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import config
from models import Article

def get_site_logo(link_source):
    if "https://vnexpress.net" in link_source:
        site_name = "VnExpress"
        logo_url = os.environ.get("VNEXPRESS_LOGO_URL", "")
    elif "https://dantri.com.vn" in link_source:
        site_name = "Dân trí"
        logo_url = os.environ.get("DANTRI_LOGO_URL", "")
    elif "https://tienphong.vn" in link_source:
        site_name = "Tiền Phong"
        logo_url = os.environ.get("TIENPHONG_LOGO_URL", "")
    elif "https://thanhnien.vn" in link_source:
        site_name = "Thanh Niên"
        logo_url = os.environ.get("THANHNIEN_LOGO_URL", "")
    else: 
        site_name = ""
        logo_url = ""

    return site_name, logo_url

def get_pagination(items, page_number=1, page_size=50):
    start_idx = (page_number - 1) * page_size
    if start_idx >= len(items):
        start_idx = 0
    end_idx = start_idx + page_size
    if end_idx > len(items):
        end_idx = len(items)
    return items[start_idx:end_idx]
    

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
async def get_all(page: int = 1, offset: int = 40):
    articles = sql_session["session"].query(Article.id, Article.title, Article.link_source, Article.image_url, Article.description, Article.slug_url, Article.written_at) \
                                    .order_by(Article.id.desc()).all()

    news = []
    for id, title, link_source, image_url, description, slug_url, written_at in articles:
        site_name, logo_url = get_site_logo(link_source)
        news.append({"id": id, "title": title, "link_source": link_source,
                     "image_url": image_url, "description": description,
                     "slug_url": slug_url,
                     "site_name": site_name, "logo_url": logo_url,
                     "written_at": written_at.strftime("%m/%d/%Y, %H:%M:%S")})

    return {"message": "Get all news successfully",
            "data": get_pagination(news),
            "pagination": {
                "totalPages": (len(news) - 1) // offset + 1,
                "currentPage": 1,
                "total": len(news)
            }}


@app.get("/api/news/category/{category}")
async def get_all_category(category: str, page: int = 1, offset: int = 40):
    articles = sql_session["session"].query(Article.id, Article.title, Article.link_source, Article.image_url, Article.description, Article.slug_url, Article.written_at) \
                                    .filter(Article.category == category).order_by(Article.id.desc()).all()

    news = []
    for id, title, link_source, image_url, description, slug_url, written_at in articles:
        site_name, logo_url = get_site_logo(link_source)
        news.append({"id": id, "title": title, "link_source": link_source,
                     "image_url": image_url, "description": description,
                     "slug_url": slug_url,
                     "site_name": site_name, "logo_url": logo_url,
                     "written_at": written_at.strftime("%m/%d/%Y, %H:%M:%S")})

    return {"message": f"Get all {category} news successfully",
            "data": get_pagination(news),
            "pagination": {
                "totalPages": (len(news) - 1) // offset + 1,
                "currentPage": 1,
                "total": len(news)
            }}

@app.get("/api/news/{slug_url}")
async def get_one(slug_url: str):
    articles = sql_session["session"].query(Article.id, Article.title, Article.link_source, Article.content, Article.slug_url, Article.written_at) \
                                    .filter(Article.slug_url == slug_url).order_by(Article.id.desc()).all()

    news = []
    for id, title, link_source, content, slug, written_at in articles:
        site_name, logo_url = get_site_logo(link_source)
        news.append({"id": id, "title": title, "link_source": link_source, "content": content, 
                     "slug_url": slug, "site_name": site_name, "logo_url": logo_url,
                     "audio_male-north": f"/api/news/audio/{id}/male-north",
                     "audio_female-north": f"/api/news/audio/{id}/female-north",
                     "audio_male-south": f"/api/news/audio/{id}/male-south",
                     "audio_female-south": f"/api/news/audio/{id}/female-south",
                     "audio_female-central": f"/api/news/audio/{id}/female-central",
                     "written_at": written_at.strftime("%m/%d/%Y, %H:%M:%S")})

    return {"message": news}

@app.get("/api/news/audio/{id}/{voice}")
async def get_audio(id: int, voice: Literal["male-north", "female-north", "male-south", "female-south", "female-central"]):
    folder_path = sql_session["session"].query(Article.path_audio).filter(Article.id == id).first()
    file_name = voice + ".wav"
    audio_path = os.path.join("audio", folder_path[0], file_name)

    def iterfile():
        with open(audio_path, mode="rb") as file:
            yield from file

    return StreamingResponse(iterfile(), media_type="audio/mpeg")
