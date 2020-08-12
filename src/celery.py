
from celery import Celery

from .log import logging, fileHandler

logger = logging.getLogger(__name__)
logger.addHandler(fileHandler)

logger.info("Celery, inicio de configuracion")

app = Celery('src',
             broker='amqp://guest:guest@localhost:5672',
             backend='rpc://',
             include=['src.tasks'])

app.conf.timezone = 'America/Lima'

if __name__ == '__main__':
    app.start()
