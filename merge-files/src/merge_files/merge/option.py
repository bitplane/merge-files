from typing import Optional, Type

from pydantic import BaseModel


class Option(BaseModel):
    """
    Represents a command line option
    """

    name: str
    """The key for this option"""

    value: Optional[str] = None
    """The value for this option, if it has one"""

    value_type: Type = str
    """The type of the value"""

    description: str
    """What this option does"""


class Options(BaseModel):
    """
    The list of command line options
    """

    target: str
    """The target file/folder/url"""

    options: list[Option]
    """The options"""


GLOBAL_OPTIONS = [Option(name="help", description="Show this help message")]
