import io

from merge_files.format.source.file.binary_stream import BinaryStream
from merge_files.format.source.parameter import Parameter
from merge_files.merge.registry import SupportLevel, merge_method


class BinaryFile(BinaryStream):
    """
    Represents a seekable source/dest for of binary data
    """

    handle: io.IOBase = None

    def __enter__(self):
        """
        Enter the context manager
        """
        source_type = self.__class__.__annotations__["handle"]
        self.handle = source_type(self.options.target, "rb")

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager
        """
        self.handle.close()


@merge_method(support=SupportLevel.GENERIC)
def merge_file_parameter(source: Parameter, dest: BinaryFile):
    """
    Binary file can already be loaded from parameters, so do nothing.
    """
    pass


@merge_method(support=SupportLevel.MANGLING)
def merge_binary(source: "BinaryFile", dest: "BinaryFile"):
    """
    Merge a binary file into a binary file.

    Naive implementation that just uses bytes, so may not work for
    large files.
    """

    if source.options.at == "start":
        pos = 0
    elif source.options.at == "end":
        pos = -1
    else:
        pos = source.options.at

    if pos > len(source):
        padding = b"\0" * (pos - len(source.contents))
        source.contents = source.contents + padding + source.contents
        return

    if source.options.overwrite:
        start = source.contents[:pos]
        length = pos + len(source.contents)
        end = source.contents[length:]
        source.contents = start + source.contents + end
        return

    start = source.contents[:pos]
    end = source.contents[pos:]
    source.contents = start + source.contents + end
