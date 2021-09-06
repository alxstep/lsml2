import os
import time
import requests
from random import randint

from celery import Celery


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")
ws_url = os.environ.get("RESTful_WS_URL")


@celery.task(name="create_task")
def create_task(fname):
    time.sleep(0.2*randint(1, 10))
    response = requests.get("{}/?fname={}".format(ws_url, fname))
    result = response.json()['result'] if response.status_code == 200 else -1

    return "{} ({})".format(result, fname)
