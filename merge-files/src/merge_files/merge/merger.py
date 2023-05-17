from pathlib import Path
from typing import List, Type

from merge_files import format
from merge_files.format import Format
from merge_files.merge.args import Arguments
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
        self.formats_by_name = {str(format): format for format in self.formats}

    def merge(self):
        """
        Where the magic happens
        """

        # ok we need a graph format
        # 1. get candidates for stage (matching args)

        # Find formats compatible with the stage options
        # for each stage, find the highest priority format that supports it
        # if no format supports it, find intermediate conversions.
        #  - Emit a warning

        raise NotImplementedError()

    @staticmethod
    def find_supported_formats(
        path: Path = Path(format.__file__),
    ) -> List[Type[Format]]:
        """
        Find all the file formats we support
        """
        return search_subclasses(path, Format)
