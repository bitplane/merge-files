import inspect
import logging
from enum import Enum

from merge_files.utils.enum import validate_by_name


@validate_by_name
class LogLevel(Enum):
    """
    Supported log levels
    """

    CRITICAL = logging.CRITICAL
    """Log only critical errors that crash the program"""

    ERROR = logging.ERROR
    """Log all errors encountered while processing"""

    WARNING = logging.WARNING
    """Log warnings and errors. This is the default."""

    INFO = logging.INFO
    """Also log progress information"""

    DEBUG = logging.DEBUG
    """Log everything. Might be noisy"""


_loggiing_initialized = False


def setup(log_level: LogLevel = LogLevel.WARNING, logger=None) -> None:
    """
    Sets up the logging for the application
    """
    if not logger:
        logger = logging.getLogger()

    logger.setLevel(log_level.value)

    # output to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level.value)
    logger.addHandler(console_handler)


def get_logger() -> logging.Logger:
    """
    Get the logger for the calling module
    """

    frame = inspect.currentframe().f_back
    module_name = inspect.getmodule(frame).__name__

    logger = logging.getLogger(module_name)
    setup(logger=logger)

    return logger
