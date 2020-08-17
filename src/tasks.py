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


# Retrying tasks can be tricky
# Make task idempotent to be sure that if the job is done only once
# Use “late acknowledgment” for idempotent tasks to protect them against incomplete execution.
# https://blog.daftcode.pl/working-with-asynchronous-celery-tasks-lessons-learned-32bb7495586b
# the task will be retried every 60 seconds until it has finally succeeded or failed (maximum 120 times)
@app.task(bind=True, default_retry_delay=60, max_retries=120, acks_late=True)
def send_welcome_email_task(self, user_id):
    # obtener ultima version del usuario desde la bd
    # user = User.objects.select_for_update().get(id=user_id)
    user = {}
    if user.is_welcome_email_sent:
        return "OK"
    try:
        # enviar email al usuario
        # send_email(email=user.email, subject='Welcome', content='...')
        pass
    except Exception as ex:  # use SMTPException
        self.retry(exc=ex)
    else:  # no exception
        # guardar el estado de procesado en la bd
        user.is_welcome_email_sent = True
        user.save()
    finally:
        # the finally clause is executed in any event
        # the finally clause is useful for releasing external resources (such as files or network connections),
        # regardless of whether the use of the resource was successful.
        pass
