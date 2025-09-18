import logging
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(override=True)

def setup_logger(name="report"):
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    today = datetime.today().strftime("%m-%d-%Y")

    # Get base name of the DATA_PATH from .env
    data_path = os.getenv("DATA_PATH", "")
    if data_path:
        base = os.path.basename(os.path.normpath(data_path))
        base_name, _ = os.path.splitext(base)  # strips extension if it exists
    else:
        base_name = "unknown"

    log_filename = f"{today}_{base_name}.log"
    log_path = os.path.join("logs", log_filename)
    os.makedirs("logs", exist_ok=True)

    file_handler = logging.FileHandler(log_path)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)

    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
