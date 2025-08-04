import sys

from loguru import logger


def setup_logging(log_file_path: str = "logs/kratio.log", level: str = "INFO", silent: bool = False) -> None:
    """
    Configures Loguru for logging to a file and console.

    Args:
        log_file_path (str): The path to the log file.
        level (str): The minimum logging level.
    """
    logger.remove()  # Remove default handler

    if not silent:
        logger.add(sys.stderr, level=level)

    logger.add(log_file_path, rotation="5 MB", level=level)
