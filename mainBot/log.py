from loguru import logger 
import sys

def initialization_log():
    logger.level("USER", no=38, color="<yellow>", icon="🐍")
    logger.level("DB", no=38, color="<blue>", icon='???')