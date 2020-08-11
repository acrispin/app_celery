
from log import logging, fileHandler

logger = logging.getLogger(__name__)
logger.addHandler(fileHandler)

if __name__ == '__main__':
    logger.info('Inicio')
