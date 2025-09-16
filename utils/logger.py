# import logging
# import os
# from datetime import datetime

# def setup_logger(name="report"):
#     logger = logging.getLogger(name)
#     if logger.hasHandlers():
#         return logger

#     logger.setLevel(logging.INFO)

#     today = datetime.today().strftime("%m-%d-%Y")
#     cwd = os.path.basename(os.getcwd())
#     log_filename = f"{today}_{cwd}.log"
#     log_path = os.path.join("logs", log_filename)
#     os.makedirs("logs", exist_ok=True)

#     file_handler = logging.FileHandler(log_path)
#     console_handler = logging.StreamHandler()

#     formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
#     file_handler.setFormatter(formatter)
#     console_handler.setFormatter(formatter)

#     logger.addHandler(file_handler)
#     logger.addHandler(console_handler)

#     return logger


import logging
import os
from datetime import datetime

def setup_logger(name="report"):
    logger = logging.getLogger(name)

    if logger.hasHandlers():
        return logger 

    logger.setLevel(logging.INFO)
    logger.propagate = False 

    try:
        today = datetime.today().strftime("%m-%d-%Y")
        cwd = os.path.basename(os.getcwd()) or "log"
        log_filename = f"{today}_{cwd}.log"
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, log_filename)

        # File handler
        file_handler = logging.FileHandler(log_path, mode='a')
        file_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s"))

        # Add handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        logger.info(f"Logger initialized. Writing to: {log_path}")
        return logger

    except Exception as e:
        print(f"[LOGGER ERROR] Failed to initialize logger: {e}")
        raise
