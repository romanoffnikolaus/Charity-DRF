from db import Session, News
from bs4 import BeautifulSoup
import requests


def parse_data_and_save():
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
