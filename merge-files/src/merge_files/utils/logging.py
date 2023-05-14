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


def setup(log_level: LogLevel = LogLevel.WARNING) -> None:
    """
    Sets up the logging for the application
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level.value)

    # output to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level.value)
    root_logger.addHandler(console_handler)
