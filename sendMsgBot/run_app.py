from app.run import run
from loguru import logger


if __name__ == '__main__':
    logger.debug('Bot starting')
    run()