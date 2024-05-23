import sqlalchemy
from sqlalchemy import Column, String, Integer, Time, DateTime, Date, Identity, ForeignKey, text, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

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



