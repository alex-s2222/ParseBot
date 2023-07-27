from app.run import run
from log import initialization_log
from loguru import logger

if __name__ == '__main__':
    logger.debug('Run MainBot')
    initialization_log()
    run()


