from src.log import setup_custom_logger

logger = setup_custom_logger(__name__)

if __name__ == '__main__':
    logger.info('Inicio')
    try:
        from src import job2
        job2.run()
    except Exception as ex:
        logger.exception(ex)
        input("Press Enter to close...")
    except KeyboardInterrupt as key:
        logger.warning("Se finaliza ejecucion de proceso.")
        input("Press Enter to close...")
