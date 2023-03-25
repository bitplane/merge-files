from pathlib import Path

from .method import Method


class Mergable:
    """
    Base class for mergeable things
    """

    merge_methods = []
    """Merge methods that we can use"""

    def __init__(self, path: Path):
        if not self.can_load(path):
            raise ValueError(f"{type(self).__name__} can't load {path}")

        self.path: Path = path

    def merge(self, other: "Mergable", method: Method) -> bytes:
        """
        Merge the contents into the other and return it
        """
        if not self.can_merge(other, method):
            raise ValueError(f"Can't merge {method.name}")

    @classmethod
    def can_load(path: Path) -> bool:
        """
        Can we load this type?
        """
        return False

    @classmethod
    def can_merge(cls, other: Path, method: Method) -> bool:
        """
        Can we merge into this type?
        """
        return method in cls.merge_methods and cls.can_load(other)
