import time
import datetime
from dateutil.parser import parse
import schedule
import requests
import feedparser
from bs4 import BeautifulSoup
import ftfy
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from worker import celery
from config import config
from models import Article
from utils import slug

engine = create_engine((f'postgresql+psycopg2://{config["POSTGRES_USER"]}:'
            f'{config["POSTGRES_PASSWORD"]}@{config["POSTGRES_HOST"]}:'
            f'{config["POSTGRES_PORT"]}/{config["POSTGRES_DB"]}'))

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


def process_rss(rss_site: str, category: str, fix_text: bool = False):
    NewsFeed = feedparser.parse(rss_site)
    
    now = datetime.datetime.now()
    list_article = []
    for entry in NewsFeed.entries:
        # Get title and url
        title = entry.title
        url = entry.link

        # Get time
        time_published = parse(entry.published)
        time_published = time_published.replace(tzinfo=None)
        if now - time_published >= datetime.timedelta(hours=1):
            break

        # Get description
        description_html = entry.get('description', '')
        soup = BeautifulSoup(description_html, 'html.parser')
        description = soup.get_text()

        # Get image url
        img_tag = soup.find('img')
        img_url = img_tag['src'] if img_tag else ""

        # Fix text (for thanhnien)
        if fix_text:
            title = ftfy.fix_text(title)
            description = ftfy.fix_text(description)

        article = Article(title=title, 
                          link_source=url, 
                          written_at=time_published,
                          content="", 
                          category=category, 
                          image_url=img_url, 
                          description=description,
                          slug_url=slug(title),
                          path_audio=str(uuid.uuid4()))
        list_article.append(article)

    return list_article


def etl_vnexpress():
    news = process_rss("https://vnexpress.net/rss/thoi-su.rss", "news")
    world = process_rss("https://vnexpress.net/rss/the-gioi.rss", "world")
    # life = process_rss("https://vnexpress.net/rss/gia-dinh.rss", "life")
    # health = process_rss("https://vnexpress.net/rss/suc-khoe.rss", "health")
    # economy = process_rss("https://vnexpress.net/rss/kinh-doanh.rss", "economy")
    # vehicle = process_rss("https://vnexpress.net/rss/oto-xe-may.rss", "vehicle")
    education = process_rss("https://vnexpress.net/rss/giao-duc.rss", "education")
    sport = process_rss("https://vnexpress.net/rss/the-thao.rss", "sport")
    # law = process_rss("https://vnexpress.net/rss/phap-luat.rss", "law")

    # list_article = news + world + life + health + economy + vehicle + education + sport + law
    list_article = news + world + education + sport
    print(len(list_article))

    for article in list_article:
        page = requests.get(article.link_source)
        soup = BeautifulSoup(page.content, "html.parser")

        content_div = soup.find('div', {"class":"fck_detail"})
        if content_div:
            paragraphs = content_div.find_all('p')
            article.content = '\n'.join([p.get_text() for p in paragraphs if not (p.has_attr('class') and 'Image' in p['class'])])

        session.add(article)
        session.commit()

        celery.send_task(config["CELERY_TASK"], 
                        args=[article.path_audio, article.content],
                        queue="tasks")

    return list_article

def etl_dantri():
    news = process_rss("https://dantri.com.vn/rss/su-kien.rss", "news")
    world = process_rss("https://dantri.com.vn/rss/the-gioi.rss", "world")
    # life = process_rss("https://dantri.com.vn/rss/doi-song.rss", "life")
    # health = process_rss("https://dantri.com.vn/rss/suc-khoe.rss", "health")
    # economy = process_rss("https://dantri.com.vn/rss/kinh-doanh.rss", "economy")
    # vehicle = process_rss("https://dantri.com.vn/rss/o-to-xe-may.rss", "vehicle")
    education = process_rss("https://dantri.com.vn/rss/giao-duc.rss", "education")
    sport = process_rss("https://dantri.com.vn/rss/the-thao.rss", "sport")
    # law = process_rss("https://dantri.com.vn/rss/phap-luat.rss", "law")

    # list_article = news + world + life + health + economy + vehicle + education + sport + law
    list_article = news + world + education + sport
    print(len(list_article))

    for article in list_article:
        page = requests.get(article.link_source)
        soup = BeautifulSoup(page.content, "html.parser")

        content_div = soup.find('div', {"class":"singular-content"})
        if content_div:
            paragraphs = content_div.find_all('p')
            article.content = '\n'.join([p.get_text() for p in paragraphs if not p.find_parent('figcaption')])

        session.add(article)
        session.commit()

        celery.send_task(config["CELERY_TASK"], 
                        args=[article.path_audio, article.content],
                        queue="tasks")

    return list_article

def etl_thanhnien():
    news = process_rss("https://thanhnien.vn/rss/thoi-su.rss", "news", fix_text=True)
    world = process_rss("https://thanhnien.vn/rss/the-gioi.rss", "world", fix_text=True)
    # life = process_rss("https://thanhnien.vn/rss/doi-song.rss", "life", fix_text=True)
    # health = process_rss("https://thanhnien.vn/rss/suc-khoe.rss", "health", fix_text=True)
    # economy = process_rss("https://thanhnien.vn/rss/kinh-te.rss", "economy", fix_text=True)
    # vehicle = process_rss("https://thanhnien.vn/rss/xe.rss", "vehicle", fix_text=True)
    education = process_rss("https://thanhnien.vn/rss/giao-duc.rss", "education", fix_text=True)
    sport = process_rss("https://thanhnien.vn/rss/the-thao.rss", "sport", fix_text=True)
    # youth = process_rss("https://thanhnien.vn/rss/gioi-tre.rss", "youth", fix_text=True)

    # list_article = news + world + life + health + economy + vehicle + education + sport + youth
    list_article = news + world + education + sport
    print(len(list_article))

    for article in list_article:
        page = requests.get(article.link_source)
        soup = BeautifulSoup(page.content, "html.parser")

        content_div = soup.find('div', {"class":"detail-content afcbc-body"})
        if content_div:
            paragraphs = content_div.find_all('p')
            article.content = '\n'.join([p.get_text() for p in paragraphs if not p.has_attr('data-placeholder')])

        session.add(article)
        session.commit()

        celery.send_task(config["CELERY_TASK"], 
                        args=[article.path_audio, article.content],
                        queue="tasks")

    return list_article

def etl_tienphong():
    news = process_rss("https://tienphong.vn/rss/thoi-su-421.rss", "news")
    world = process_rss("https://tienphong.vn/rss/the-gioi-5.rss", "world")
    # health = process_rss("https://tienphong.vn/rss/suc-khoe-210.rss", "health")
    # economy = process_rss("https://tienphong.vn/rss/kinh-te-3.rss", "economy")
    # vehicle = process_rss("https://tienphong.vn/rss/xe-113.rss", "vehicle")
    education = process_rss("https://tienphong.vn/rss/giao-duc-71.rss", "education")
    sport = process_rss("https://tienphong.vn/rss/the-thao-11.rss", "sport")
    # law = process_rss("https://tienphong.vn/rss/phap-luat-12.rss", "law")
    # youth = process_rss("https://tienphong.vn/rss/gioi-tre-4.rss", "youth")

    # list_article = news + world + health + economy + vehicle + education + sport + law + youth
    list_article = news + world + education + sport
    print(len(list_article))

    for article in list_article:
        page = requests.get(article.link_source)
        soup = BeautifulSoup(page.content, "html.parser")

        content_div = soup.find('div', {"class":"article__body cms-body"})
        if content_div:
            paragraphs = content_div.find_all('p')
            article.content = '\n'.join([p.get_text() for p in paragraphs])

        session.add(article)
        session.commit()

        celery.send_task(config["CELERY_TASK"], 
                        args=[article.path_audio, article.content],
                        queue="tasks")

    return list_article

def crawl():
    print("Start Crawling!!!")
    etl_vnexpress()
    etl_thanhnien()
    etl_dantri()
    etl_tienphong()

# For testing
crawl()

# schedule.every(1).minutes.do(crawl)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
        