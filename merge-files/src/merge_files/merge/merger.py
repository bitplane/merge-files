from pathlib import Path
from typing import List, Type

from merge_files import formats
from merge_files.formats.format import Format
from merge_files.merge.stage import Arguments
from merge_files.utils.code import search_subclasses


class Merger:
    """
    The merge manager.
    """

    def __init__(self, args: Arguments):
        self.options = args.options
        self.stage_dicts = args.stages
        self.stages = []
        self.formats = self.find_supported_formats()
        self.sources = {format: [] for format in self.formats}
        self.dests = {format: [] for format in self.formats}

    def merge(self):
        """
        Where the magic happens
        """
        # Find formats compatible with the stage options
        # for each stage, find the highest priority format that supports it
        # if no format supports it, find intermediate conversions.
        #  - Emit a warning

        raise NotImplementedError()

    @staticmethod
    def find_supported_formats() -> List[Type[Format]]:
        """
        Find all the file formats we support
        """
        path = Path(formats.__file__).parent

        return search_subclasses(path, Format)
