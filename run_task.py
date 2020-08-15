from src.log import setup_custom_logger
from src.tasks import longtime_add

logger = setup_custom_logger(__name__)

if __name__ == '__main__':
    logger.info('Inicio de ejecucion de test')
    result = longtime_add.delay(4, 4)
    logger.info('Task result: ' + result.get(timeout=6))
