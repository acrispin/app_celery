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

PATH_LOGS = config('PATH_LOGS', default='', cast=str)
_message_path = ''
if PATH_LOGS:
    # https://medium.com/@ageitgey/python-3-quick-tip-the-easy-way-to-deal-with-file-paths-on-windows-mac-and-linux-11a072b58d5f
    _message_path += f"Se encuentra path personalizado '{PATH_LOGS}', "
    _message_path += f"Se reemplaza path base '{DIR_LOGS}', "
    from pathlib import Path
    DIR_LOGS = Path(PATH_LOGS)
    _message_path += f"Nuevo path de logs '{DIR_LOGS}'"

if not os.path.isdir(DIR_LOGS):
    os.mkdir(DIR_LOGS)

logging.basicConfig(
    level=LOGGER_LEVEL,
    format=FORMAT_LOGGER_TEXT
    )

formatter = logging.Formatter(FORMAT_LOGGER_TEXT)
fileHandler = RotatingFileHandler(
    # filename=f'{DIR_LOGS}/{FILE_LOG}',
    filename=os.path.join(DIR_LOGS, FILE_LOG),
    maxBytes=MAX_BYTES,
    backupCount=BACKUP_COUNT)
fileHandler.setLevel(LOGGER_LEVEL)
fileHandler.setFormatter(formatter)

logging = logging


def setup_custom_logger(_name):
    _logger = logging.getLogger(_name)
    _logger.addHandler(fileHandler)
    return _logger


logger = setup_custom_logger(__name__)
logger.info(f"Se configura modulo log en modo: {logging.getLevelName(LOGGER_LEVEL)}")
logger.info(f"Ruta de archivo logs: {os.path.join(DIR_LOGS, FILE_LOG)}")
if logger.isEnabledFor(logging.DEBUG):
    logger.debug(f"Path logs personalizado: {_message_path}")


SENTRY_DSN = config('SENTRY_DSN', default='', cast=str)
if SENTRY_DSN:
    logger.info(f"SENTRY, Se encuentra cadena dsn: {SENTRY_DSN}")
    # https://sentry.io/siunicon-dev/360_python_dev/getting-started/python/
    import sentry_sdk
    if not sentry_sdk.Hub.current.client:
        try:
            sentry_sdk.init(SENTRY_DSN)
            logger.info("SENTRY, Se inicializa correctamente.")
        except Exception as ex:
            logger.warning("SENTRY, Excepcion en configuracion")
            logger.exception(ex)
