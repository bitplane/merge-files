from typing import Any, Dict, List

from merge_files.utils import logging
from pydantic import BaseModel


class StageOptions(BaseModel):
    """
    Command line options for a stage.
    """

    target: str
    """The source or destination data for this stage"""


class UnparsedStage(StageOptions):
    """
    Command line options for a stage before they are resolved and converted into
    the appropriate StageOptions for the format conversion pipeline.
    """

    options: Dict[str, Any]
    """The options for this stage."""

    target: str
    """The target file. When we hit this, we know we're done with the options for this stage"""


class MainOptions(BaseModel):
    """
    Global options for the pipeline.
    """

    help: bool = False
    """
    Display the help text.
    """

    log_level: logging.LogLevel = logging.LogLevel.WARNING
    """
    Show debug messages.
    """


class Arguments(BaseModel):
    """
    Command line arguments
    """

    options: MainOptions
    """Global options"""

    stages: List[UnparsedStage]
    """The merge stages"""
