from celery import Celery
import time
import datetime
import schedule
import requests
import feedparser
from bs4 import BeautifulSoup


app = Celery('crawler',
            broker='amqp://admin:mypass@rabbit:5672',
            backend='rpc://')

class Article:
    def __init__(self, title, url, published, category):
        self.title = title
        self.url = url
        self.category = category
        self.published = published
        self.content = ""


def process_rss(rss_site: str, category: str):
    NewsFeed = feedparser.parse(rss_site)
    
    now = datetime.datetime.now()
    list_article = []
    for entry in NewsFeed.entries:
        time_published = datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %z')
        time_published = time_published.replace(tzinfo=None)
        if now - time_published >= datetime.timedelta(hours=1):
            break

        article = Article(entry.title, entry.link, time_published, category)
        list_article.append(article)

    return list_article


def etl_vnexpress():
    news = process_rss("https://vnexpress.net/rss/thoi-su.rss", "news")
    world = process_rss("https://vnexpress.net/rss/the-gioi.rss", "world")
    life = process_rss("https://vnexpress.net/rss/gia-dinh.rss", "life")
    health = process_rss("https://vnexpress.net/rss/suc-khoe.rss", "health")
    economy = process_rss("https://vnexpress.net/rss/kinh-doanh.rss", "economy")
    vehicle = process_rss("https://vnexpress.net/rss/oto-xe-may.rss", "vehicle")
    education = process_rss("https://vnexpress.net/rss/giao-duc.rss", "education")
    sport = process_rss("https://vnexpress.net/rss/the-thao.rss", "sport")
    law = process_rss("https://vnexpress.net/rss/phap-luat.rss", "law")

    list_article = news + world + life + health + economy + vehicle + education + sport + law

    for article in list_article:
        page = requests.get(article.url)
        soup = BeautifulSoup(page.text, "html.parser")

        for paragraph in soup.find_all('p'):
            article.content += paragraph.get_text()
            article.content += "\n"

def etl_dantri():
    news = process_rss("https://dantri.com.vn/rss/su-kien.rss", "news")
    world = process_rss("https://dantri.com.vn/rss/the-gioi.rss", "world")
    life = process_rss("https://dantri.com.vn/rss/doi-song.rss", "life")
    health = process_rss("https://dantri.com.vn/rss/suc-khoe.rss", "health")
    economy = process_rss("https://dantri.com.vn/rss/kinh-doanh.rss", "economy")
    vehicle = process_rss("https://dantri.com.vn/rss/o-to-xe-may.rss", "vehicle")
    education = process_rss("https://dantri.com.vn/rss/giao-duc.rss", "education")
    sport = process_rss("https://dantri.com.vn/rss/the-thao.rss", "sport")
    law = process_rss("https://dantri.com.vn/rss/phap-luat.rss", "law")

    list_article = news + world + life + health + economy + vehicle + education + sport + law

    for article in list_article:
        page = requests.get(article.url)
        soup = BeautifulSoup(page.text, "html.parser")

        for paragraph in soup.find_all('p'):
            article.content += paragraph.get_text()
            article.content += "\n"

def etl_vtcnews():
    news = process_rss("https://vtcnews.vn/rss/thoi-su.rss", "news")
    world = process_rss("https://vtcnews.vn/rss/the-gioi.rss", "world")
    health = process_rss("https://vtcnews.vn/rss/suc-khoe.rss", "health")
    economy = process_rss("https://vtcnews.vn/rss/kinh-te.rss", "economy")
    vehicle = process_rss("https://vtcnews.vn/rss/oto-xe-may.rss", "vehicle")
    education = process_rss("https://vtcnews.vn/rss/giao-duc.rss", "education")
    sport = process_rss("https://vtcnews.vn/rss/the-thao.rss", "sport")
    law = process_rss("https://vtcnews.vn/rss/phap-luat.rss", "law")
    youth = process_rss("https://vtcnews.vn/rss/gioi-tre.rss", "youth")

    list_article = news + world + health + economy + vehicle + education + sport + law + youth

    for article in list_article:
        page = requests.get(article.url)
        soup = BeautifulSoup(page.text, "html.parser")

        for paragraph in soup.find_all('p'):
            article.content += paragraph.get_text()
            article.content += "\n"

def etl_thanhnien():
    news = process_rss("https://thanhnien.vn/rss/thoi-su.rss", "news")
    world = process_rss("https://thanhnien.vn/rss/the-gioi.rss", "world")
    life = process_rss("https://thanhnien.vn/rss/doi-song.rss", "life")
    health = process_rss("https://thanhnien.vn/rss/suc-khoe.rss", "health")
    economy = process_rss("https://thanhnien.vn/rss/kinh-te.rss", "economy")
    vehicle = process_rss("https://thanhnien.vn/rss/xe.rss", "vehicle")
    education = process_rss("https://thanhnien.vn/rss/giao-duc.rss", "education")
    sport = process_rss("https://thanhnien.vn/rss/the-thao.rss", "sport")
    youth = process_rss("https://thanhnien.vn/rss/gioi-tre.rss", "youth")

    list_article = news + world + life + health + economy + vehicle + education + sport + youth

    for article in list_article:
        page = requests.get(article.url)
        soup = BeautifulSoup(page.text, "html.parser")

        for paragraph in soup.find_all('p'):
            # TODO: find a way to exclude footer text

            article.content += paragraph.get_text()
            article.content += "\n"

def etl_tienphong():
    news = process_rss("https://tienphong.vn/rss/thoi-su-421.rss", "news")
    world = process_rss("https://tienphong.vn/rss/the-gioi-5.rss", "world")
    health = process_rss("https://tienphong.vn/rss/suc-khoe-210.rss", "health")
    economy = process_rss("https://tienphong.vn/rss/kinh-te-3.rss", "economy")
    vehicle = process_rss("https://tienphong.vn/rss/xe-113.rss", "vehicle")
    education = process_rss("https://tienphong.vn/rss/giao-duc-71.rss", "education")
    sport = process_rss("https://tienphong.vn/rss/the-thao-11.rss", "sport")
    law = process_rss("https://tienphong.vn/rss/phap-luat-12.rss", "law")
    youth = process_rss("https://tienphong.vn/rss/gioi-tre-4.rss", "youth")

    list_article = news + world + health + economy + vehicle + education + sport + law + youth

    for article in list_article:
        page = requests.get(article.url)
        soup = BeautifulSoup(page.text, "html.parser")

        for paragraph in soup.find_all('p'):
            # TODO: find a way to exclude footer text and class story__cate

            article.content += paragraph.get_text()
            article.content += "\n"