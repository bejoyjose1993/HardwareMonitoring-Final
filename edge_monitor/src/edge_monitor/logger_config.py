import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "edge_monitor.log")


def set_logging(_name_:str, level=logging.INFO):
    logger = logging.getLogger(_name_)
    logger.setLevel(level)

    # Console handler
    handler = logging.StreamHandler()
    formater = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s", 
        datefmt= "%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formater)

    # File handler
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=3)
    file_handler.setFormatter(formater)

    logger.addHandler(handler)
    logger.addHandler(file_handler)

    return logger
     