import os
from decouple import config

import logging
from logging.handlers import RotatingFileHandler

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_LOG = 'app.log'
DIR_LOGS = 'logs'
DIR_LOGS = os.path.join(BASE_DIR, DIR_LOGS)
MAX_BYTES = 10*1024*1024  # 10MB
BACKUP_COUNT = 10
DEBUG = config('DEBUG', default=False, cast=bool)
LOGGER_LEVEL = logging.DEBUG if DEBUG else logging.INFO
FORMAT_LOGGER_TEXT = '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] - %(message)s'


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
