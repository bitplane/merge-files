from enum import IntEnum
from typing import Callable, List, Type

from merge_files.formats.format import Format
from merge_files.merge.option import Option
from pydantic import BaseModel


class SupportLevel(IntEnum):
    """
    How well a file type or a conversion from one to the other is supported
    """

    NONE = -10
    """I can't do anything with this. Sorry."""

    MANGLING = 0
    """I'll do it if you force me to, but you might not like the results"""

    GENERIC = 10
    """I've got a trick for doing this, and it'll probably work. Will emit a warning"""

    GOOD = 20
    """Supports this format but not all of its features. Good enough."""

    FULL = 50
    """Fully supports this data format and all of its features."""

    LOSSLESS = 100
    """Supports this data format and all of its features, and doesn't lose any data in the process."""


class Support(BaseModel):
    """
    Defines a supported format
    """

    level: SupportLevel
    """Priority of this type. Higher priority types are tried first"""

    source: Type[Format]
    """The type of thing we're merging from"""

    dest: Type[Format]
    """The thing we're merging into"""

    options: List[Option]
    """Command line options that can be used to control this merge"""

    merge: Callable
    """The function to call (on the target) to do the merge"""

    check: Callable
    """Function to call in order to check if this thing can be merged"""

    def __lt__(self, other):
        """
        Sort by priority
        """
        return self.level < other.level
