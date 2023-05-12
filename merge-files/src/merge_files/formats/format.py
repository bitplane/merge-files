from typing import List

from merge_files.merge.merger import Merger
from merge_files.merge.option import Option
from pydantic import BaseModel


class Format(BaseModel):
    """
    Defines a data format
    """

    def __init__(self, location: str):
        """
        Create a reference to, but don't load the data
        """
        self.location = location

    def dump(self) -> bytes:
        """
        Save the data
        """
        raise NotImplementedError()

    def merge(self, other: "Format", options: List[Option]) -> "Format":
        """
        Merge other's data into this one
        """
        raise NotImplementedError()

    @classmethod
    def is_supported(cls, location: str):
        """
        Returns True if this format can be used to read the given location
        """
        return False

    @classmethod
    def register(cls, merger: Merger):
        pass
