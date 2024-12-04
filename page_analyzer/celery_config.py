import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()
CELERY_BROKER_URL = os.getenv('REDIS_URL')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL')


def make_celery():
    celery = Celery(
        main='page_analyzer',
        broker=CELERY_BROKER_URL,
        backend=CELERY_RESULT_BACKEND
    )
    return celery


celery_app = make_celery()
