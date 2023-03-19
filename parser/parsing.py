from db import Session, News, Disaster
from bs4 import BeautifulSoup
import requests


def parse_news_and_save():
    base_url = 'https://www.foxnews.com'
    url = 'https://www.foxnews.com/category/world/disasters'
    session = Session()

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    news = soup.find_all('article', class_='article')
    for n in news:
        n: BeautifulSoup
        title = n.find('h4', class_='title').text
        link = base_url + n.find('h4', class_='title').find('a').get('href')
        location = n.find('span', class_='eyebrow').text
        time = n.find('span', class_='time').text
        news = News(
            title=title,
            link=link,
            location=location,
            time=time,
        )
        session.add(news)
        session.commit()
    session.close()

def get_news():
    parse_news_and_save()
    session = Session()
    news = session.query(News).all()

    return news


def parse_disasters_and_save():
    url = 'https://reliefweb.int'
    session = Session()

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    disasters = soup.find_all(
        'article', class_='rw-river-article--headline rw-river-article rw-river-article--report rw-river-article--with-image rw-river-article--with-summary')

    for d in disasters:
        d: BeautifulSoup
        title = d.find('h3', class_='rw-river-article__title').text.strip()
        location = d.find('a', 'rw-entity-country-slug__link').text
        link = url + d.find('a', 'rw-entity-meta__tag-link').get('href')
        disaster = Disaster(
            title=title,
            location=location,
            link=link,
        )
        session.add(disaster)
        session.commit()
    session.close()


def get_disasters():
    parse_disasters_and_save()
    session = Session()
    disasters = session.query(Disaster).all()
    return disasters
