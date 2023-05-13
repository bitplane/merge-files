from typing import Any, Dict, List

from pydantic import BaseModel


class StageOptions(BaseModel):
    """
    Command line options for a stage.
    """

    target: str
    """The target file. This is the default"""


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

    help: str | bool = False
    """
    Display the help text.
    """

    debug: str | bool = False
    """
    Display debug information.

    If a log level is given, we can
    """


class Arguments(BaseModel):
    """
    Command line arguments
    """

    main: MainOptions
    """Global options"""

    stages: List[UnparsedStage]
    """The merge stages"""
