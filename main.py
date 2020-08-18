from src import job2
from src.log import setup_custom_logger

logger = setup_custom_logger(__name__)

if __name__ == '__main__':
    logger.info('Inicio')
    job2.run()
