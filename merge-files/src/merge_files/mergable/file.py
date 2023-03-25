from pathlib import Path

from .mergable import Mergable


class MergableFile(Mergable):
    """
    Base class for files, which gets loaded from a path.
    """

    def __init__(self, path: Path):
        super().__init__(path)

        self.contents: bytes = self.path.read_bytes()
