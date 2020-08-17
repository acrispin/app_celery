
from celery import Celery
from decouple import config

from .log import setup_custom_logger

logger = setup_custom_logger(__name__)

logger.info("Celery, inicio de configuracion")

CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='amqp://', cast=str)
CELERY_BACKEND_URL = config('CELERY_BACKEND_URL', default='rpc://', cast=str)
CELERY_TIMEZONE = config('CELERY_TIMEZONE', default='UTC', cast=str)

app = Celery('src',
             broker=CELERY_BROKER_URL,
             backend=CELERY_BACKEND_URL,
             include=['src.tasks'])

app.conf.timezone = CELERY_TIMEZONE
# https://github.com/celery/celery/issues/4296
# https://github.com/celery/celery/issues/4627#issuecomment-396907957
# BROKER_TRANSPORT_OPTIONS = {"max_retries": 3, "interval_start": 0, "interval_step": 0.2, "interval_max": 0.5}
# Try 5 times. Initially try again immediately, then add 0.5 seconds for each subsequent try (with a maximum of 3 seconds). This comes out to roughly 3 seconds of total delay (0, 0.5, 1, 1.5).
# app.conf.broker_transport_options = {'max_retries': 4, 'interval_start': 0, 'interval_step': 0.5, 'interval_max': 3}
# The broker will retry 3 times, starting immediately, waiting 0.2 seconds more each time and never waiting more than 0.5 seconds so it will retry at
#app.conf.broker_transport_options = {'max_retries': 3, 'interval_start': 0, 'interval_step': 0.2, 'interval_max': 0.5}
# Con esta configuracion si el broker esta caido (rabbitmq) entonces demora en responder en promedio 6.15 segundos
app.conf.broker_transport_options = {'max_retries': 4, 'interval_start': 0, 'interval_step': 0.2, 'interval_max': 0.5}

# https://medium.com/better-programming/python-celery-best-practices-ae182730bb81
# app.conf.update()
app.conf.update(
    result_expires=60*60,
    task_acks_late=False,  # set 'True' when task if idempotent, Late acknowledgment - https://blog.daftcode.pl/working-with-asynchronous-celery-tasks-lessons-learned-32bb7495586b
    broker_url=CELERY_BROKER_URL,
    result_backend=CELERY_BROKER_URL
)

if __name__ == '__main__':
    app.start()
