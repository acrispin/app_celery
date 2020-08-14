import os
from decouple import config

import logging
from logging.handlers import RotatingFileHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_LOG = os.path.basename(BASE_DIR) + ".log"
DIR_NAME_LOGS = 'logs'
DIR_LOGS = os.path.join(BASE_DIR, DIR_NAME_LOGS)
MAX_BYTES = 50*1024*1024  # 50MB
BACKUP_COUNT = 10
DEBUG = config('DEBUG', default=False, cast=bool)
LOGGER_LEVEL = logging.DEBUG if DEBUG else logging.INFO
FORMAT_LOGGER_TEXT = '%(levelname)s [%(asctime)s] [%(name)s.%(funcName)s:%(lineno)d] -> %(message)s'

if not os.path.isdir(DIR_LOGS):
    os.mkdir(DIR_LOGS)

logging.basicConfig(
    level=LOGGER_LEVEL,
    format=FORMAT_LOGGER_TEXT
    )

formatter = logging.Formatter(FORMAT_LOGGER_TEXT)
fileHandler = RotatingFileHandler(
    filename=f'{DIR_LOGS}/{FILE_LOG}',
    maxBytes=MAX_BYTES,
    backupCount=BACKUP_COUNT)
fileHandler.setLevel(LOGGER_LEVEL)
fileHandler.setFormatter(formatter)

logging = logging

SENTRY_DSN = config('SENTRY_DSN', default='', cast=str)
if SENTRY_DSN:
    # https://sentry.io/siunicon-dev/360_python_dev/getting-started/python/
    import sentry_sdk
    if not sentry_sdk.Hub.current.client:
        sentry_sdk.init(SENTRY_DSN)
        logger = logging.getLogger(__name__)
        logger.addHandler(fileHandler)
        logger.info("Se configura sentry")
