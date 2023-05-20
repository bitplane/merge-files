from merge_files.format import OptionsType
from merge_files.format.file import BaseFile, ReadableFile, WritableFile
from merge_files.format.parameter import Parameter
from merge_files.merge.registry import SupportLevel, merge_method


class BinaryStream(BaseFile, ReadableFile, WritableFile):
    """
    Represents a stream of binary data that's read like a file.
    """

    class Options(OptionsType):
        """
        Options for binary data stream.
        """

        from_: str = "0:-1"
        """

        """

        to: str = "0:-1"

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

    # options: BinaryStream.Options = source.options

    # selection = options.selection()

    raise NotImplementedError("TODO: implement binary merging")
