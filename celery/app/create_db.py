import os
import sqlalchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine, MetaData, Table, String, Integer, Text, Column, DateTime, Index, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import database_exists, create_database
from config import config
from models import news_category

engine = create_engine((f'postgresql+psycopg2://{config["POSTGRES_USER"]}:'
            f'{config["POSTGRES_PASSWORD"]}@{config["POSTGRES_HOST"]}:'
            f'{config["POSTGRES_PORT"]}/{config["POSTGRES_DB"]}'))

if not database_exists(engine.url):
    print("Init database")
    create_database(engine.url)
else:
    print("Database exists")

meta = MetaData()

conn = engine.connect()

articles = Table(
    "news", meta,
    Column("id", Integer, primary_key=True),
    Column("link_source", String),
    Column("title", String),
    Column("category", sqlalchemy.Enum(news_category)),
    Column("content", Text),
    Column("image_url", Text),
    Column("description", Text),
    Column("slug_url", Text),
    Column("path_audio", String),
    Column("written_at", DateTime),
    Column("created_at", DateTime),
    Index('idx_slug_url', 'slug_url')
)

admin = Table(
    "admin", meta,
    Column("id", Integer, primary_key=True),
    Column("username", String, unique=True),
    Column("password", String)
)

meta.create_all(engine)

# Init admin account
username = os.environ.get("ADMIN_USERNAME", "admin")
password = os.environ.get("ADMIN_PASSWORD", "1111")
# with engine.connect() as connection:
#     try:
#         result = connection.execute(text("INSERT INTO admin (username, password) VALUES (:username, :password)"), {"username": username, "password": password})
#         print("Init admin account")
#     except Exception as e:
#         print(e)
#         print("Account existed")
with conn.begin():
    try:
        conn.execute(admin.insert(), {"username": username, "password": password})
        conn.commit()
        print("Init admin account")
    except Exception as e:
        print(e)
        print("Account existed")