import time
from .celery import app

from .log import logging, fileHandler

logger = logging.getLogger(__name__)
logger.addHandler(fileHandler)


@app.task
def longtime_add(first, second):
    logger.info("Inicio de tarea, esperando 5 segundos")
    time.sleep(5)
    logger.info('Finalizacion de tarea')
    return f"{first} + {second} = {first + second}"
