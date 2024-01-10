import logging
from datetime import datetime as dt
import os


def __setup_logger(logger, logging_dir=""):
    # Define a blank logger
    logger.setLevel(logging.INFO)

    # Make sure the logger doesn't have pre-existing handlers
    logger.handlers.clear()

    # Get current time
    now = dt.now().strftime("%y%m%d_%H%M%S")

    # Define formatter
    formatter = logging.Formatter("%(levelname)s,%(asctime)s,%(funcName)s,%(message)s")

    # Define a stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Define file handler
    file_handler = logging.FileHandler(os.path.join(logging_dir, f"log_{now}.csv"))
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return 
