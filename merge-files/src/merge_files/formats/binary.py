from typing import Literal

from merge_files.formats.file import File, FormatOptions
from merge_files.merge.merge_method import merge_method


class BinaryFileOptions(FormatOptions):
    """
    Options for binary files
    """

    at: int | Literal["start"] | Literal["start"] = Literal["end"]
    """
    Where to insert the data
    """

    overwrite: bool = True
    """
    Overwrite existing data? If False, then the data will be inserted
    """

    # bits: int = 8
    # truncate: bool = False


class BinaryFile(File):
    """
    Base class for binary files.
    """

    options: BinaryFileOptions

    @merge_method.MANGLING
    def merge_binary(self, other: "BinaryFile"):
        """
        Merge a binary file into a binary file.

        Naive implementation that just uses bytes, so may not work for
        large files.
        """

        if self.options.at == "start":
            pos = 0
        elif self.options.at == "end":
            pos = len(self.contents)
        else:
            pos = self.options.at

        if pos > len(self.contents):
            padding = b"\0" * (pos - len(self.contents))
            self.contents = self.contents + padding + other.contents
            return

        if self.options.overwrite:
            start = self.contents[:pos]
            length = pos + len(other.contents)
            end = self.contents[length:]
            self.contents = start + other.contents + end
            return

        start = self.contents[:pos]
        end = self.contents[pos:]
        self.contents = start + other.contents + end
