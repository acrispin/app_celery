
from celery import Celery
from decouple import config

from .log import logging, fileHandler

logger = logging.getLogger(__name__)
logger.addHandler(fileHandler)

logger.info("Celery, inicio de configuracion")

CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='amqp://', cast=str)
CELERY_BACKEND_URL = config('CELERY_BACKEND_URL', default='rpc://', cast=str)
CELERY_TIMEZONE = config('CELERY_TIMEZONE', default='UTC', cast=str)

app = Celery('src',
             broker=CELERY_BROKER_URL,
             backend=CELERY_BACKEND_URL,
             include=['src.tasks'])

app.conf.timezone = CELERY_TIMEZONE

if __name__ == '__main__':
    app.start()
