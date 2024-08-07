from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm

import os
from typing import Literal, Union
from datetime import datetime, timedelta, timezone
from typing_extensions import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
import requests

import sqlalchemy
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from config import config
from models import Article, Admin

requests.adapters.DEFAULT_RETRIES = 5

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str

class PasswordChanger(BaseModel):
    old_password: str
    new_password: str

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


def get_existed_api_audio(folder_path: str, id: int, voice: Literal["male-north", "female-north", "male-south", "female-south", "female-central"]):
    file_name = voice + ".wav"
    audio_path = os.path.join("audio", folder_path, file_name)

    # Check if audio file was created
    if os.path.exists(audio_path):
        return f"/api/news/audio/{id}/{voice}"
    return None
    

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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    timeout_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credentials expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.environ.get("JWT_SECRET_KEY"), algorithms=["HS256"])

        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        
        exp = payload.get("exp")
        if exp is None: 
            raise credentials_exception
        if datetime.fromtimestamp(exp) < datetime.now():
            raise timeout_exception

    except InvalidTokenError:
        raise credentials_exception
    except Exception as e:
        print(e)
    user: Admin = sql_session["session"].query(Admin).filter(Admin.username == username).one()
    if user is None:
        raise credentials_exception
    return User(username=user.username)


@app.post('/login')
async def login(payload: OAuth2PasswordRequestForm = Depends()):
    try:
        user: Admin = sql_session["session"].query(Admin).filter(Admin.username == payload.username).one()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user credentials"
        )

    is_validated: bool = user.validate_password(payload.password)
    if not is_validated:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid password"
        )

    return Token(access_token=user.create_access_token(), token_type="bearer")


@app.get("/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@app.post("/change-password")
async def change_password(pc: PasswordChanger, current_user: User = Depends(get_current_user)):
    user: Admin = sql_session["session"].query(Admin).filter(Admin.username == current_user.username).one()
    success = user.change_password(
        session=sql_session["session"],
        old_password=pc.old_password,
        new_password=pc.new_password
    )

    if success:
        return {"success": True, "message": "Change password successfully!"}
    else:
        return {"success": False, "message": "Failed! Old password is incorrect!"}


@app.get("/api/statistic")
async def statistic(current_user: User = Depends(get_current_user)):
    articles = sql_session["session"].query(Article.id, Article.link_source, Article.category).all()

    sites = {}
    categories = {}
    for id, link_source, category in articles:
        site_name, _ = get_site_logo(link_source)
        if site_name in sites:
            sites[site_name] += 1
        else:
            sites[site_name] = 1

        if category in categories:
            categories[category] += 1
        else:
            categories[category] = 1

    return {"message": "Get all-time statistics successfully",
            "data": {
                "all": len(articles),
                "categories": categories,
                "sites": sites
            }}

@app.get("/api/statistic/last")
async def statistic(hour: int = 1, current_user: User = Depends(get_current_user)):
    articles = sql_session["session"].query(Article.id, Article.link_source, Article.category) \
                                    .filter(Article.created_at + timedelta(hours=hour) > datetime.now()).all()

    sites = {}
    categories = {}
    for id, link_source, category in articles:
        site_name, _ = get_site_logo(link_source)
        if site_name in sites:
            sites[site_name] += 1
        else:
            sites[site_name] = 1

        if category in categories:
            categories[category] += 1
        else:
            categories[category] = 1

    return {"message": f"Get statistics within {hour} hour(s) successfully",
            "data": {
                "all": len(articles),
                "categories": categories,
                "sites": sites
            }}

@app.delete("/api/news/{id}")
async def delete_news(id: int, current_user: User = Depends(get_current_user)):
    article = sql_session["session"].query(Article).filter(Article.id == id).first()
    if article:
        sql_session["session"].delete(article)
        sql_session["session"].commit()
        return {"message": "Article deleted successfully"}
    else:
        return {"message": "Article not found"}


@app.get("/api/news")
async def get_all(page: int = 1, offset: int = 40):
    total = sql_session["session"].query(func.count(Article.id)).scalar()
    start_idx = (page - 1) * offset
    articles = sql_session["session"].query(Article.id, Article.title, Article.link_source, Article.image_url, Article.description, Article.slug_url, Article.written_at) \
                                    .order_by(Article.written_at.desc()).limit(offset).offset(start_idx).all()

    news = []
    for id, title, link_source, image_url, description, slug_url, written_at in articles:
        site_name, logo_url = get_site_logo(link_source)
        news.append({"id": id, "title": title, "link_source": link_source,
                     "image_url": image_url, "description": description,
                     "slug_url": slug_url,
                     "site_name": site_name, "logo_url": logo_url,
                     "written_at": written_at.strftime("%m/%d/%Y, %H:%M:%S")})

    return {"message": "Get all news successfully",
            "data": news,
            "pagination": {
                "totalPages": (total - 1) // offset + 1,
                "currentPage": page,
                "total": total
            }}


@app.get("/api/news/category/{category}")
async def get_all_category(category: str, page: int = 1, offset: int = 40):
    total = sql_session["session"].query(func.count(Article.id)).filter(Article.category == category).scalar()
    start_idx = (page - 1) * offset
    articles = sql_session["session"].query(Article.id, Article.title, Article.link_source, Article.image_url, Article.description, Article.slug_url, Article.written_at) \
                                    .filter(Article.category == category).order_by(Article.written_at.desc()).limit(offset).offset(start_idx).all()

    news = []
    for id, title, link_source, image_url, description, slug_url, written_at in articles:
        site_name, logo_url = get_site_logo(link_source)
        news.append({"id": id, "title": title, "link_source": link_source,
                     "image_url": image_url, "description": description,
                     "slug_url": slug_url,
                     "site_name": site_name, "logo_url": logo_url,
                     "written_at": written_at.strftime("%m/%d/%Y, %H:%M:%S")})

    return {"message": f"Get all {category} news successfully",
            "data": news,
            "pagination": {
                "totalPages": (total - 1) // offset + 1,
                "currentPage": page,
                "total": total
            }}

@app.get("/api/news/{slug_url}")
async def get_one(slug_url: str):
    articles = sql_session["session"].query(Article.id, Article.title, Article.link_source, Article.image_url, Article.description, Article.content, Article.slug_url, Article.written_at, Article.path_audio) \
                                    .filter(Article.slug_url == slug_url).order_by(Article.id.desc()).all()

    news = []
    for id, title, link_source, image_url, description, content, slug, written_at, path_audio in articles:
        site_name, logo_url = get_site_logo(link_source)


        news.append({"id": id, "title": title, "link_source": link_source, 
                     "image_url": image_url, "description": description, "content": content, 
                     "slug_url": slug, "site_name": site_name, "logo_url": logo_url,
                     "audio_male-north": get_existed_api_audio(path_audio, id, "male-north"),
                     "audio_female-north": get_existed_api_audio(path_audio, id, "female-north"),
                     "audio_male-south": get_existed_api_audio(path_audio, id, "male-south"),
                     "audio_female-south": get_existed_api_audio(path_audio, id, "female-south"),
                     "audio_female-central": get_existed_api_audio(path_audio, id, "female-central"),
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

@app.get("/api/news/generate-audio/{id}")
async def delete_news(id: int, current_user: User = Depends(get_current_user)):
    item = sql_session["session"].query(Article.content, Article.path_audio).filter(Article.id == id).first()
    if item:
        (content, path_audio) = item

        tts_api = "http://tts_service:3000/tts"
        response = requests.post(url=tts_api, json={"content": content, "folder_name": path_audio}, timeout=120)

        if response.status_code == 200:
            return {"message": "Generate audio successfully"}
        else:
            return {"message": "Something went wrong. Please try again later"}
        
    else:
        return {"message": f"Article not found"}