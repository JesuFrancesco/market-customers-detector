import logging
from datetime import datetime
import pytz

def setup_logger(logger_name: str) -> logging.Logger:
    TIMEZONE = pytz.timezone("America/Lima")
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    c_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M"
    )
    formatter.converter = lambda *args: datetime.now(TIMEZONE).timetuple()
    c_handler.setFormatter(formatter)
    logger.addHandler(c_handler)
    return logger

__all__ = [
    "setup_logger"
]