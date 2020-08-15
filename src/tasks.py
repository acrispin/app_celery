import time
from .celery import app

from .log import logging, setup_custom_logger

logger = setup_custom_logger(__name__)


# para obtener el id del task, se necesitar bind
# https://docs.celeryproject.org/en/latest/userguide/tasks.html#bound-tasks
@app.task(bind=True)
def longtime_add(self, first, second):
    logger.info("Inicio de tarea, esperando 5 segundos, id: " + self.request.id)
    time.sleep(5)
    logger.info('Finalizacion de tarea')
    return f"{first} + {second} = {first + second}"


#  serializer='json' es por defecto, no se necesitar indicar
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#task-serializer
# https://docs.celeryproject.org/en/latest/userguide/calling.html#calling-serializers
@app.task(bind=True, serializer='json')
def check_obj(self, obj):
    logger.info("Inicio de tarea, esperando 3 segundos, id: " + self.request.id)
    time.sleep(3)
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("obj: " + str(obj))
    logger.info('Finalizacion de tarea')
    return f"OK"
