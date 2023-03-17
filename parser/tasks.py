from parsing import parse_data_and_save
from core.celery import app
import time

@app.task
def parse_data_and_save_celery():
    while True:
        parse_data_and_save()
        time.sleep(600)
