import logging
import os
from datetime import datetime

def setup_logger(name="report"):
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    today = datetime.today().strftime("%m-%d-%Y")
    cwd = os.path.basename(os.getcwd())
    log_filename = f"{today}_{cwd}.log"
    log_path = os.path.join("logs", log_filename)
    os.makedirs("logs", exist_ok=True)

    file_handler = logging.FileHandler(log_path)
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
