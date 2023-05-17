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
        self.args = args
        self.stages = []
        self.formats = self.find_supported_formats()
        self.formats_by_name = {str(format): format for format in self.formats}

    def merge(self):
        """
        Where the magic happens
        """
        # create a parameter for each merge stage

        pipeline = [stage for stage in self.args.stages]

        index = 0
        while index < len(pipeline):
            stage = pipeline[index]

        raise NotImplementedError()

    @staticmethod
    def find_supported_formats(
        path: Path = Path(format.__file__),
    ) -> List[Type[Format]]:
        """
        Find all the file formats we support
        """
        return search_subclasses(path, Format)
