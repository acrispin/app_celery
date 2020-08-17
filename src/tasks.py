import random
import time
from types import SimpleNamespace

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


# Retrying tasks can be tricky
# Make task idempotent to be sure that if the job is done only once
# Use “late acknowledgment” for idempotent tasks to protect them against incomplete execution.
# https://blog.daftcode.pl/working-with-asynchronous-celery-tasks-lessons-learned-32bb7495586b
# the task will be retried every 60 seconds until it has finally succeeded or failed (maximum 120 times)
@app.task(bind=True, default_retry_delay=60, max_retries=120, acks_late=True)
def send_welcome_email_task(self, user_id):
    logger.info(f"Inicio de tarea, id: {self.request.id}")
    logger.info(f"Try task id {self.request.id} : {self.request.retries}/{self.max_retries}")
    # obtener ultima version del usuario desde la bd
    # user = User.objects.select_for_update().get(id=user_id)

    # https://stackoverflow.com/questions/29290359/existence-of-mutable-named-tuple-in-python/40330531#40330531
    user = SimpleNamespace(is_welcome_email_sent=False)  # solo para pruebas
    # user.save = lambda: True  # solo para pruebas
    # https://realpython.com/python-lambda/
    # https://stackoverflow.com/questions/1233448/no-multiline-lambda-in-python-why-not/13672943#13672943
    user.save = lambda: (logger.info("Saved ...."), None, )  # imprime y retorna None, solo para pruebas
    if user.is_welcome_email_sent:
        return "OK"
    try:
        # enviar email al usuario
        # send_email(email=user.email, subject='Welcome', content='...')

        # https://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python
        if random.choice([True, False]):
            num = 1 / 0
        pass
    except Exception as ex:  # use SMTPException
        logger.exception(ex)
        logger.info(f"Retry de tarea, id: {self.request.id}")
        self.retry(exc=ex)
    else:  # no exception
        logger.info(f"Ejecucion sin excepcion de tarea, id: {self.request.id}")
        # guardar el estado de procesado en la bd
        user.is_welcome_email_sent = True
        user.save()
    finally:
        logger.info(f"Finalizacion de tarea, id: {self.request.id}")
        # the finally clause is executed in any event
        # the finally clause is useful for releasing external resources (such as files or network connections),
        # regardless of whether the use of the resource was successful.
        pass
