import time
import datetime
from dateutil.parser import parse
import schedule
import requests
import feedparser
from bs4 import BeautifulSoup

from worker import celery
from config import config


class Article:
    def __init__(self, title, url, published, category, image_url, description):
        self.title = title
        self.url = url
        self.category = category
        self.published = published
        self.content = ""
        self.image_url = image_url
        self.description = description


def process_rss(rss_site: str, category: str):
    NewsFeed = feedparser.parse(rss_site)
    
    now = datetime.datetime.now()
    list_article = []
    for entry in NewsFeed.entries:
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

        article = Article(entry.title, entry.link, time_published, category, img_url, description)
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
        page = requests.get(article.url)
        soup = BeautifulSoup(page.text, "html.parser")

        for paragraph in soup.find_all('p'):
            article.content += paragraph.get_text()
            article.content += "\n"

        celery.send_task(config["CELERY_TASK"], 
                        args=[article.title, article.url, article.category, article.published, article.content, article.image_url, article.description],
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
        page = requests.get(article.url)
        soup = BeautifulSoup(page.text, "html.parser")

        for paragraph in soup.find_all('p'):
            article.content += paragraph.get_text()
            article.content += "\n"

        celery.send_task(config["CELERY_TASK"], 
                        args=[article.title, article.url, article.category, article.published, article.content, article.image_url, article.description],
                        queue="tasks")

    return list_article

def etl_vtcnews():
    news = process_rss("https://vtcnews.vn/rss/thoi-su.rss", "news")
    world = process_rss("https://vtcnews.vn/rss/the-gioi.rss", "world")
    # health = process_rss("https://vtcnews.vn/rss/suc-khoe.rss", "health")
    # economy = process_rss("https://vtcnews.vn/rss/kinh-te.rss", "economy")
    # vehicle = process_rss("https://vtcnews.vn/rss/oto-xe-may.rss", "vehicle")
    education = process_rss("https://vtcnews.vn/rss/giao-duc.rss", "education")
    sport = process_rss("https://vtcnews.vn/rss/the-thao.rss", "sport")
    # law = process_rss("https://vtcnews.vn/rss/phap-luat.rss", "law")
    # youth = process_rss("https://vtcnews.vn/rss/gioi-tre.rss", "youth")

    # list_article = news + world + health + economy + vehicle + education + sport + law + youth
    list_article = news + world + education + sport
    print(len(list_article))

    for article in list_article:
        page = requests.get(article.url)
        soup = BeautifulSoup(page.text, "html.parser")

        for paragraph in soup.find_all('p'):
            article.content += paragraph.get_text()
            article.content += "\n"

        celery.send_task(config["CELERY_TASK"], 
                        args=[article.title, article.url, article.category, article.published, article.content, article.image_url, article.description],
                        queue="tasks")

    return list_article

def etl_thanhnien():
    news = process_rss("https://thanhnien.vn/rss/thoi-su.rss", "news")
    world = process_rss("https://thanhnien.vn/rss/the-gioi.rss", "world")
    # life = process_rss("https://thanhnien.vn/rss/doi-song.rss", "life")
    # health = process_rss("https://thanhnien.vn/rss/suc-khoe.rss", "health")
    # economy = process_rss("https://thanhnien.vn/rss/kinh-te.rss", "economy")
    # vehicle = process_rss("https://thanhnien.vn/rss/xe.rss", "vehicle")
    education = process_rss("https://thanhnien.vn/rss/giao-duc.rss", "education")
    sport = process_rss("https://thanhnien.vn/rss/the-thao.rss", "sport")
    # youth = process_rss("https://thanhnien.vn/rss/gioi-tre.rss", "youth")

    # list_article = news + world + life + health + economy + vehicle + education + sport + youth
    list_article = news + world + education + sport
    print(len(list_article))

    for article in list_article:
        page = requests.get(article.url)
        soup = BeautifulSoup(page.text, "html.parser")

        for paragraph in soup.find_all('p'):
            # TODO: find a way to exclude footer text

            article.content += paragraph.get_text()
            article.content += "\n"

        celery.send_task(config["CELERY_TASK"], 
                        args=[article.title, article.url, article.category, article.published, article.content, article.image_url, article.description],
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
        page = requests.get(article.url)
        soup = BeautifulSoup(page.text, "html.parser")

        for paragraph in soup.find_all('p'):
            # TODO: find a way to exclude footer text and class story__cate

            article.content += paragraph.get_text()
            article.content += "\n"

        celery.send_task(config["CELERY_TASK"], 
                        args=[article.title, article.url, article.category, article.published, article.content, article.image_url, article.description],
                        queue="tasks")

    return list_article

def crawl():
    print("Start Crawling!!!")
    etl_vnexpress()
    # etl_thanhnien()
    # etl_dantri()
    # etl_tienphong()
    # etl_vtcnews()

# For testing
crawl()

# schedule.every(1).minutes.do(crawl)

# while True:
#     schedule.run_pending()
#     time.sleep(1)
        