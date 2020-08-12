import time
from .celery import app

from .log import logging, fileHandler

logger = logging.getLogger(__name__)
logger.addHandler(fileHandler)


# https://docs.celeryproject.org/en/latest/userguide/tasks.html#bound-tasks
@app.task(bind=True)
def longtime_add(self, first, second):
    logger.info("Inicio de tarea, esperando 5 segundos, id: " + self.request.id)
    time.sleep(5)
    logger.info('Finalizacion de tarea')
    return f"{first} + {second} = {first + second}"
