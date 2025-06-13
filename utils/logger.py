import logging
import os
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("sonosphere")

LOG_FILENAME = "sonosphere.log"
LOG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(LOG_DIR, LOG_FILENAME)


def setup_logger(level: int = logging.INFO) -> None:
    """
    Configura il logger con un formattatore personalizzato e gestori multipli.

    Parameters:
        level: Livello di logging (default: logging.INFO)
    """

    logger.setLevel(level)

    if logger.handlers:
        return

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        LOG_PATH, maxBytes=5 * 1024 * 1024, backupCount=3  # 5 MB
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    logger.addHandler(console_handler)

    logger.info("Logger configurato con successo")


def get_logger() -> logging.Logger:
    """
    Ottiene l'istanza del logger già configurato.

    Returns:
        logging.Logger: L'istanza del logger.
    """

    return logger
