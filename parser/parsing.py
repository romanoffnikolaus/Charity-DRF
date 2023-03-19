from db import Session, News, AlterNews, Disaster
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


def parse_alter_news_and_save():
    url = 'https://reliefweb.int'
    session = Session()

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    news = soup.find_all(
        'article', class_='rw-river-article--headline rw-river-article rw-river-article--report rw-river-article--with-image rw-river-article--with-summary')

    for n in news:
        n: BeautifulSoup
        title = n.find('h3', class_='rw-river-article__title').text.strip()
        location = n.find('a', 'rw-entity-country-slug__link').text
        link = url + n.find('a', 'rw-entity-meta__tag-link').get('href')
        news = AlterNews(
            title=title,
            location=location,
            link=link,
        )
        session.add(news)
        session.commit()
    session.close()


def get_alter_news():
    parse_alter_news_and_save()
    session = Session()
    alter_news = session.query(AlterNews).all()
    return alter_news


def parse_disasters_and_save():
    url = 'https://reliefweb.int/disasters'
    session = Session()

    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    disasters = soup.find_all(
        'article', 'rw-river-article--card rw-river-article rw-river-article--disaster')

    for d in disasters:
        d: BeautifulSoup
        title = d.find('h3', class_='rw-river-article__title').text.strip()
        disaster_type = d.find(
            'dd', class_='rw-entity-meta__tag-value rw-entity-meta__tag-value--disaster-type rw-entity-meta__tag-value--taglist').text.strip()
        affected_countries = d.find(
            'dd', class_='rw-entity-meta__tag-value rw-entity-meta__tag-value--country rw-entity-meta__tag-value--taglist rw-entity-meta__tag-value--last'
        ).find('a', class_='rw-entity-meta__tag-link').text
        disaster = Disaster(
            title=title,
            disaster_type=disaster_type,
            affected_countries=affected_countries,
        )
        session.add(disaster)
        session.commit()
    session.close()


def get_disasters():
    parse_disasters_and_save()
    session = Session()
    disasters = session.query(Disaster).all()
    return disasters
