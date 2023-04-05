from enum import Enum
from pathlib import Path
from typing import Optional, List
from pydantic import BaseModel

from merge_files.merge.stage import Option


class SupportLevel(Enum):
    """
    How well a file type is supported
    """

    DISABLED = -10
    """Not intended for use, or doesn't work"""

    LAST_DITCH = 0
    """Last resort. Usually not what you want and won't be chosen automatically"""

    GENERIC = 10
    """Generic type. If something better isn't found, this will be used."""

    LIMITED_SUPPORT = 20
    """Limited support. Will emit a warning."""

    IDEAL = 50
    """Ideal type. """


class FileSupport(BaseModel):
    """
    Information about how well a file type is supported
    """

    level: SupportLevel
    """Priority of this type. Higher priority types are tried first"""

    pattern: str
    """List of extensions that this type can load"""

    options: List[Option]
    """Merge stage options supported by this type"""

    description: str = ""
    """Description of this type"""



class Mergeable:
    """
    Base class for mergeable things
    """

    def __init__(self, path: Path):
        if not self.can_load(path):
            raise ValueError(f"{type(self).__name__} can't load {path}")

        self.path: Path = path

    @classmethod
    def get_supported_types(cls) -> List[FileSupport]:
        """
        Get a list of supported file types
        """
        return []

    @classmethod
    def get_formats(self) -> List[Formats]:
        """

        """
        return None