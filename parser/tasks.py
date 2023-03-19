from parsing import get_news, get_disasters
from core.celery import app
import time

@app.task
def parse_NewsDisasters_and_save_celery():
    while True:
        news = get_news()
        disasters = get_disasters()
        time.sleep(600)
