import math
import random
import time
from types import SimpleNamespace

import celery
import requests
from celery import shared_task
from decouple import config

from .celery import app

from .log import logging, setup_custom_logger

logger = setup_custom_logger(__name__)

FORCE_EXCEPTION_TASK = False
_retry_delay = config('TASK_DEFAULT_RETRY_DELAY', default=60, cast=int)
_max_retries = config('TASK_MAX_RETRIES', default=120, cast=int)
logger.info(f"Inicializando task, _retry_delay: {_retry_delay}, _max_retries: {_max_retries}")


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
# if default_retry_delay=60 and max_retries=120
@app.task(bind=True, default_retry_delay=_retry_delay, max_retries=_max_retries, acks_late=True)
def send_welcome_email_task(self, user_id):
    logger.info(f"Inicio de tarea, id: {self.request.id}, user_id: {user_id}")
    logger.info(f"Try task id {self.request.id} : {self.request.retries}/{self.max_retries}")
    # obtener ultima version del usuario desde la bd
    # user = User.objects.select_for_update().get(id=user_id)

    # https://stackoverflow.com/questions/29290359/existence-of-mutable-named-tuple-in-python/40330531#40330531
    user = SimpleNamespace(is_welcome_email_sent=False)  # solo para pruebas
    # user.save = lambda: True  # solo para pruebas
    # https://realpython.com/python-lambda/
    # https://stackoverflow.com/questions/1233448/no-multiline-lambda-in-python-why-not/13672943#13672943
    user.save = lambda: (logger.info("Saved ...."), None,)  # imprime y retorna None, solo para pruebas
    if user.is_welcome_email_sent:
        return "OK"
    try:
        # enviar email al usuario
        # send_email(email=user.email, subject='Welcome', content='...')

        # https://stackoverflow.com/questions/6824681/get-a-random-boolean-in-python
        if random.choice([True, False]) or FORCE_EXCEPTION_TASK:
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


# https://www.vinta.com.br/blog/2018/celery-wild-tips-and-tricks-run-async-tasks-real-world/
def exponential_backoff(task_self):
    minutes = task_self.default_retry_delay / 60
    rand = random.uniform(minutes, minutes * 1.3)
    return int(rand ** task_self.request.retries) * 60


def exponential_backoff2(task_self):
    _delay = task_self.default_retry_delay
    _rand = random.uniform(_delay, _delay * 1.5)
    _retries = task_self.request.retries if task_self.request.retries > 0 else 1
    _countdown = int(_rand * math.log(_retries)) + 1
    logger.info(f"_delay: {_delay}, _rand: {_rand}, _retries: {_retries} => _countdown: {_countdown}")
    return _countdown


@app.task(bind=True, default_retry_delay=_retry_delay, max_retries=_max_retries, acks_late=True)
def send_welcome_email_task2(self, user_id):
    logger.info(f"Inicio de tarea 2, id: {self.request.id}, user_id: {user_id}")
    logger.info(f"Try task id {self.request.id} : {self.request.retries}/{self.max_retries}")

    user = SimpleNamespace(is_welcome_email_sent=False)  # solo para pruebas
    user.save = lambda: (logger.info("Saved ...."), None,)  # imprime y retorna None, solo para pruebas
    if user.is_welcome_email_sent:
        return "OK"
    try:
        if random.choice([True, False]) or FORCE_EXCEPTION_TASK:
            num = 1 / 0
        pass
    except Exception as ex:
        logger.exception(ex)
        logger.info(f"Retry de tarea, id: {self.request.id}")
        self.retry(exc=ex, countdown=exponential_backoff2(self))
    else:
        logger.info(f"Ejecucion sin excepcion de tarea, id: {self.request.id}")
        user.is_welcome_email_sent = True
        user.save()
    finally:
        logger.info(f"Finalizacion de tarea, id: {self.request.id}")
        pass


# https://docs.celeryproject.org/en/stable/userguide/tasks.html#automatic-retry-for-known-exceptions
@app.task(bind=True,
          acks_late=True,
          autoretry_for=(Exception,),
          retry_kwargs={'max_retries': _max_retries, 'default_retry_delay': _retry_delay},
          retry_backoff=True)  # omite default_retry_delay, usa countdown
def send_welcome_email_task3(self, user_id):
    """
    La desventaja es que no se puede imprimir la excepcion ni enviar por sentry, se tendria que integrar con celery
    """
    logger.info(f"Inicio de tarea 2, id: {self.request.id}, user_id: {user_id}")
    logger.info(f"Try task 2 id {self.request.id}: {self.request.retries}/{self.retry_kwargs['max_retries']}, "
                f"countdown={self.retry_kwargs.get('countdown', 0)}")
    user = SimpleNamespace(is_welcome_email_sent=False)  # solo para pruebas
    user.save = lambda: (logger.info("Saved ...."), None,)  # imprime y retorna None, solo para pruebas
    if user.is_welcome_email_sent:
        return "OK"

    if random.choice([True, False]) or FORCE_EXCEPTION_TASK:
        num = 1 / 0
    logger.info(f"Ejecucion sin excepcion de tarea, id: {self.request.id}")
    user.is_welcome_email_sent = True
    user.save()
    logger.info(f"Finalizacion de tarea, id: {self.request.id}")


# https://testdriven.io/blog/retrying-failed-celery-tasks/
# https://www.vinta.com.br/blog/2018/celery-wild-tips-and-tricks-run-async-tasks-real-world/ (Time limiting)
# https://stackoverflow.com/questions/25442482/softtimeout-and-timeout-in-celery-tasks-dont-work
# https://docs.celeryproject.org/en/stable/reference/celery.app.task.html#celery.app.task.Task.time_limit
# task_time_limit no funciona en windows
@shared_task(bind=True, task_time_limit=3)
def task_process_notification(self, _delay=1):
    logger.info(f"task resques with delay: {_delay}")
    # self.max_retries por defecto es 3
    logger.info(f"Try task id {self.request.id} : {self.request.retries}/{self.max_retries}")
    try:
        if not random.choice([0, 1]) or FORCE_EXCEPTION_TASK:
            raise Exception()

        logger.info(f"Procesando request para task id: {self.request.id}")
        response = requests.post(f'https://httpbin.org/delay/{_delay}')
        logger.info(f"response: {response.text.encode('utf8')}")
    except Exception as e:
        logger.exception('exception raised, it would be retry after 5 seconds')
        raise self.retry(exc=e, countdown=5)


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 7, 'countdown': 5})
def task_process_notification2(self, _delay=1):
    logger.info(f"task resques with delay: {_delay}")
    logger.info(f"Try task id {self.request.id}: {self.request.retries}/{self.retry_kwargs['max_retries']}, "
                f"countdown={self.retry_kwargs.get('countdown', 0)}")
    if not random.choice([0, 1]) or FORCE_EXCEPTION_TASK:
        raise Exception()

    response = requests.post(f'https://httpbin.org/delay/{_delay}')
    logger.info(f"response: {response.text.encode('utf8')}")


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_retries': 5})
def task_process_notification3(self, _delay=1):
    logger.info(f"task resques with delay: {_delay}")
    logger.info(f"Try task id {self.request.id}: {self.request.retries}/{self.retry_kwargs['max_retries']}, "
                f"countdown={self.retry_kwargs.get('countdown', 0)}")
    if not random.choice([0, 1]) or FORCE_EXCEPTION_TASK:
        raise Exception()

    response = requests.post(f'https://httpbin.org/delay/{_delay}')
    logger.info(f"response: {response.text.encode('utf8')}")


class BaseTaskWithRetry(celery.Task):
    autoretry_for = (Exception, KeyError)
    retry_backoff = True
    retry_jitter = False
    retry_kwargs = {'max_retries': 5}


@shared_task(bind=True, base=BaseTaskWithRetry)
def task_process_notification4(self, _delay=1):
    logger.info(f"task resques with delay: {_delay}")
    logger.info(f"Try task id {self.request.id}: {self.request.retries}/{self.retry_kwargs['max_retries']}, "
                f"countdown={self.retry_kwargs.get('countdown', 0)}")
    if not random.choice([0, 1]) or FORCE_EXCEPTION_TASK:
        raise Exception()

    response = requests.post(f'https://httpbin.org/delay/{_delay}')
    logger.info(f"response: {response.text.encode('utf8')}")
