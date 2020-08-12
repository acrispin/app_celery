from src.log import logging, fileHandler
from src.tasks import longtime_add

logger = logging.getLogger(__name__)
logger.addHandler(fileHandler)

if __name__ == '__main__':
    logger.info('Inicio de ejecucion de test')
    result = longtime_add.delay(4, 4)
    logger.info('Task result: ' + result.get(timeout=6))
