import time
from .celery import app

from .log import logging, fileHandler

logger = logging.getLogger(__name__)
logger.addHandler(fileHandler)


@app.task
def longtime_add(x, y):
    logger.info("Inicio de tarea, esperando 4 segundos")
    time.sleep(4)
    logger.info('Finalizacion de tarea')
    return f"{x} + {y} = {x + y}"
