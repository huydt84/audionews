import os
import sqlalchemy
from sqlalchemy import Column, String, Integer, Time, DateTime, Date, Identity, ForeignKey, text, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import jwt

from datetime import datetime, timedelta, timezone
from typing import Union
from typing_extensions import Annotated

NEWS_CATEGORY = [
    "news",
    "world",
    "life",
    "health",
    "economy",
    "vehicle",
    "education",
    "sport",
    "law",
    "youth"
]

news_category = enum.Enum('News_Category', {field: field for field in NEWS_CATEGORY}, type=str)

Base = declarative_base()

class Article(Base):
    __tablename__ = 'news'

    id = Column(Integer, Identity(start=1), primary_key=True, autoincrement=True)
    link_source = Column(String(255))
    title = Column(String(255))
    category = Column(sqlalchemy.Enum(news_category))
    content = Column(Text)
    image_url = Column(Text)
    description = Column(Text)
    slug_url = Column(Text)
    path_audio = Column(String(255))
    written_at = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())


class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, Identity(start=1), primary_key=True, autoincrement=True)
    username = Column(String(225), nullable=False, unique=True)
    password = Column(String(255), nullable=False)

    def __repr__(self):
        """Returns string representation of model instance"""
        return "<User {username!r}>".format(username=self.username)
    
    def validate_password(self, password) -> bool:
        """Confirms password validity"""
        return password == self.password

    def create_access_token(self, expires_delta: Union[timedelta, None] = None):
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=1)
        to_encode = {"username": self.username, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, os.environ.get("JWT_SECRET_KEY"))
        return encoded_jwt
    
    def change_password(self, session, old_password, new_password):
        if self.password != old_password:
            return False
        
        self.password = new_password
        session.commit()
        return True
