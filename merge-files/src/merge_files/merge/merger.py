from pathlib import Path
from typing import List, Type

from merge_files import formats
from merge_files.formats.format import Format
from merge_files.utils.discovery import search_subclasses


class Merger:
    """
    The merge manager.
    """

    def __init__(self):
        self.formats = self.find_supported_formats()
        self.sources = {format: [] for format in self.formats}
        self.dests = {format: [] for format in self.formats}

    @staticmethod
    def find_supported_formats() -> List[Type[Format]]:
        """
        Find all the file formats we support
        """
        path = Path(formats.__file__).parent

        return search_subclasses(path, Format)
