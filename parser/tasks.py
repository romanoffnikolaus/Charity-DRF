from parsing import get_news, get_alter_news, get_disasters
from core.celery import app
import time

@app.task
def parse_news_and_save_celery():
    while True:
        news = get_news()
        alter_news = get_alter_news()
        time.sleep(600)

@app.task
def parse_disasters_and_save_celery():
    while True:
        disasters = get_disasters()
        time.sleep(600)
