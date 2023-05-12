from pathlib import Path

from merge_files.formats.format import Format
from merge_files.merge.merger import Merger


class BinaryFile(Format):
    """
    Base class for files, which gets loaded from a path.
    """

    def __init__(self, path: Path):
        super().__init__(path)

        self.contents: bytes = self.path.read_bytes()

    @classmethod
    def register(cls, merger: Merger):
        super().register()
