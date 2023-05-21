from pathlib import Path
from typing import List, Type

from merge_files import format
from merge_files.format import Format
from merge_files.merge.args import Arguments
from merge_files.utils.code import search_subclasses

FORMAT_PATH = Path(format.__file__).parent


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

        # index = 0
        # stages = self.args.stages
        # pipeline: List[Format] = []

        # for i in range(len(stages) - 1):
        #    pipeline += find_merge(stages[index], stages[index + 1])

        # add stdout step
        # if not pipeline[-1].config.get('write', False):
        #     pipeline.append()

        # for c in pipeline:
        #    next = tranform.source_format(transform.args, next)

        # finished!

    @staticmethod
    def find_supported_formats(path: Path = FORMAT_PATH) -> List[Type[Format]]:
        """
        Find all the file formats we support
        """
        return search_subclasses(path, Format)
