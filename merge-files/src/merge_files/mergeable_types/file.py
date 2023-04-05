import re
from typing import List
from pathlib import Path

from .mergeable import Mergeable, FileSupport, SupportLevel


class MergeableFile(Mergeable):
    """
    Base class for files, which gets loaded from a path.
    """

    def __init__(self, path: Path):
        super().__init__(path)

        self.contents: bytes = self.path.read_bytes()

    @classmethod
    def get_supported_types(cls) -> List[FileSupport]:
        return super().get_supported_types() + [
            FileSupport(SupportLevel, re.Pattern(".*"), "Binary data")
        ]