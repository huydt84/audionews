import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, MetaData, Table, String, Integer, Text, Column, DateTime
from sqlalchemy.orm import sessionmaker
from config import config
from models import news_category

engine = create_engine((f'postgresql+psycopg2://{config["POSTGRES_USER"]}:'
            f'{config["POSTGRES_PASSWORD"]}@{config["POSTGRES_HOST"]}:'
            f'{config["POSTGRES_PORT"]}/{config["POSTGRES_DB"]}'))

meta = MetaData()

conn = engine.connect()

articles = Table(
    "news", meta,
    Column("id", Integer, primary_key=True),
    Column("link_source", String),
    Column("title", String),
    Column("category", sqlalchemy.Enum(news_category)),
    Column("content", Text),
    Column("path_audio", String),
    Column("written_at", DateTime),
    Column("created_at", DateTime)
)

meta.create_all(engine)