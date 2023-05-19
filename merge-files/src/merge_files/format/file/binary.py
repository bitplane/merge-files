from merge_files.format import Format
from merge_files.format.file import BaseFile, ReadableFile, WritableFile
from merge_files.format.parameter import Parameter
from merge_files.format.parameter.eval import Eval
from merge_files.merge.registry import SupportLevel, merge_method


class BinaryStream(BaseFile, ReadableFile, WritableFile):
    """
    Represents a stream of binary data that's read like a file.
    """

    class Options(Format.Options):
        """
        Options for binary data stream.
        """

        selection: Eval = Eval("source")
        """
        Filters the data stream. Use range.
        """

        overwrite: bool = True
        """
        Overwrite existing data? If False, then the data will be inserted,
        which isn't usually what you want in binary data as it destroys offsets.
        """

        truncate: bool = False
        """
        Truncate the output data to the length of the input data?
        """


class BinaryFile(BinaryStream):
    """
    Represents a seekable source/dest for of binary data.
    """

    def __enter__(self):
        """
        Enter the context manager.
        """
        source_type = self.__class__.__annotations__["handle"]
        self.handle = source_type(self.options.target, "rb")

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager.
        """
        self.handle.close()


@merge_method(support=SupportLevel.GENERIC, stream=True)
def parameter_to_stream(source: Parameter, dest: BinaryStream):
    pass


@merge_method(support=SupportLevel.GENERIC)
def parameter_to_file(source: Parameter, dest: BinaryFile):
    pass


@merge_method(support=SupportLevel.MANGLING)
def merge_binary(source: "BinaryStream", dest: "BinaryStream"):
    """
    Merge a binary stream into a binary stream.
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
