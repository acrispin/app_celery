from datetime import datetime, timedelta
import random
import uuid

import requests
import schedule
import time

from decouple import config
from .log import logging, setup_custom_logger

logger = setup_custom_logger(__name__)

JOB_FORMATO_HORA = config('JOB_2_FORMATO_HORA', default='%H:%M:%S', cast=str)
JOB_HORA_INICIO = config('JOB_2_HORA_INICIO', default='08:01:05', cast=str)
JOB_HORA_FIN = config('JOB_2_HORA_FIN', default='08:02:15', cast=str)
JOB_INTERVAL_SECONDS = config('JOB_2_INTERVAL_SECONDS', default=3, cast=int)
JOB_RUN_IMMEDIATELY = config('JOB_2_RUN_IMMEDIATELY', default=True, cast=bool)

TIME_INI = datetime.strptime(JOB_HORA_INICIO, JOB_FORMATO_HORA).time()
TIME_FIN = datetime.strptime(JOB_HORA_FIN, JOB_FORMATO_HORA).time()
HORA_INI = None
HORA_FIN = None


def get_hora_ini():
    kwargs = {'microsecond': 0, 'second': TIME_INI.second, 'minute': TIME_INI.minute, 'hour': TIME_INI.hour}
    return datetime.now().replace(**kwargs)


def get_hora_fin():
    kwargs = {'microsecond': 0, 'second': TIME_FIN.second, 'minute': TIME_FIN.minute, 'hour': TIME_FIN.hour}
    _fin = datetime.now().replace(**kwargs)
    if HORA_INI >= _fin:
        _fin += timedelta(days=1)
    return _fin


def calculate_dates():
    global HORA_INI, HORA_FIN
    HORA_INI = get_hora_ini()
    HORA_FIN = get_hora_fin()
    logger.debug(f"Hora inicio: {HORA_INI}, Hora fin: {HORA_FIN}")


"""
https://github.com/dbader/schedule
https://schedule.readthedocs.io/en/stable/
"""


def job(_ejecucion_inmediata=False):
    _id = uuid.uuid1()
    # datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")  # parse date format 'yyyy-mm-dd HH:MM:SS.fff'
    logger.info(f"JOB_2, Inicio con job_id: {_id}")
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("JOB_2, modo DEBUG de job.")
    try:
        _delay = int(random.uniform(1, 5))
        logger.info(f"JOB_2, Procesando request para job_id: {_id} con _delay: {_delay} segundos")
        response = requests.post(f'https://httpbin.org/delay/{_delay}', timeout=5)
        logger.info(f"JOB_2, Request finalizado, response: {response.text.encode('utf8')}")
    except Exception as ex:
        logger.info(f"JOB_2, Ejecucion con error de job_id: {_id}")
        logger.exception(ex)
    else:
        logger.info(f"JOB_2, Ejecucion correcta de job_id: {_id}")
    finally:
        if datetime.now() >= HORA_FIN or _ejecucion_inmediata:
            if _ejecucion_inmediata:
                _diff_date = HORA_INI - datetime.now() \
                    if HORA_INI > datetime.now() \
                    else HORA_INI + timedelta(days=1) - datetime.now()
                _total_seg = _diff_date.total_seconds()
                logger.info(f"JOB_2, Se finaliza job inmediato job_id: {_id}, siguiente ejecucion en {_total_seg} seg.")
            else:
                _jobs = [_job for _job in schedule.jobs if wrap_job.__name__ in _job.tags]
                _total_seg = (_jobs[0].next_run - datetime.now()).total_seconds() if len(_jobs) > 0 else -1
                logger.info(f"JOB_2, Se finaliza rango horario job_id: {_id}, siguiente ejecucion en {_total_seg} seg.")
            return schedule.CancelJob
        logger.info(f"JOB_2, Finalizacion de job_id: {_id}, siguiente ejecucion en {JOB_INTERVAL_SECONDS} segundos")
        return None


def wrap_job():
    calculate_dates()
    logger.info(f"Inicio de ejecucion JOB_2 wrapper con intervalo de '{JOB_INTERVAL_SECONDS}' segundos y "
                f"entre las [{HORA_INI} - {HORA_FIN}] horas.")
    job()
    schedule.every(JOB_INTERVAL_SECONDS).seconds.do(job)


if __name__ == '__main__':
    calculate_dates()
    logger.info(f"Inicio de configuracion de JOB_2 con intervalo de '{JOB_INTERVAL_SECONDS}' segundos y "
                f"entre las [{HORA_INI.time()} - {HORA_FIN.time()}] horas diariamente.")
    if JOB_RUN_IMMEDIATELY:
        logger.info("Ejecucion inmediata de JOB_2.")
        # schedule.every().seconds.do(job, True)
        job(True)
    schedule.every().day.at(JOB_HORA_INICIO).do(wrap_job).tag(wrap_job.__name__)
    logger.info(f"Se configura correctamente job wrapper, siguiente ejecucion en {schedule.idle_seconds()} seg.")
    while True:
        schedule.run_pending()
        time.sleep(1)

"""
python -m src.job2
"""
