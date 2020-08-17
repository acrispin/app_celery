import random
import uuid

import requests
import schedule
import time

from decouple import config
from .log import logging, setup_custom_logger

logger = setup_custom_logger(__name__)


JOB_INTERVAL_SECONDS = config('JOB_INTERVAL_SECONDS', default=60, cast=int)
JOB_RUN_IMMEDIATELY = config('JOB_RUN_IMMEDIATELY', default=False, cast=bool)

"""
https://github.com/dbader/schedule
https://schedule.readthedocs.io/en/stable/
"""


def job():
    _id = uuid.uuid1()
    logger.info(f"JOB, Inicio con job_id: {_id}")
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("JOB, modo debug de job.")
    try:
        _delay = int(random.uniform(1, 10))
        logger.info(f"JOB, Procesando request para job id: {_id} con _delay: {_delay} segundos")
        response = requests.post(f'https://httpbin.org/delay/{_delay}', timeout=8.2)
        logger.info(f"JOB, Request finalizado, response: {response.text.encode('utf8')}")
    except Exception as ex:
        logger.exception(ex)
    else:
        logger.info(f"JOB, Ejecucion sin excepcion de job, id: {_id}")
    finally:
        logger.info(f"JOB, Finalizacion de job, id: {_id}, siguiente ejecucion en {JOB_INTERVAL_SECONDS} segundos")


# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)
# schedule.every(3).to(7).seconds.do(job)  # run job random interval
# schedule.every(JOB_INTERVAL_SECONDS).seconds.do(job)

if __name__ == '__main__':
    logger.info(f"Inicio de configuracion de job con intervalo de {JOB_INTERVAL_SECONDS}")
    if JOB_RUN_IMMEDIATELY:
        logger.info("Ejecucion inmediata de job.")
        job()
    schedule.every(JOB_INTERVAL_SECONDS).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

"""
python -m src.job
"""
