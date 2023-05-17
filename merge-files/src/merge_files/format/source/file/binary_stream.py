from typing import Literal

from merge_files.format import Format
from merge_files.format.source.parameter import Parameter
from merge_files.merge.registry import SupportLevel, merge_method


class BinaryStream(Format):
    """
    Represents a stream of binary data, like a file, TTY or socket.
    """

    class Options(Format.Options):
        """
        Options for binary files.
        """

        at: int | Literal["start", "end"] = Literal["end"]
        """
        Where to insert the data in the output data.
        """

        overwrite: bool = True
        """
        Overwrite existing data? If False, then the data will be inserted,
        which isn't usually what you want in binary data.
        """

        truncate: bool = False
        """
        Truncate the output data to the length of the input data?
        """


@merge_method(support=SupportLevel.GENERIC, stream=True)
def merge_file_parameter(source: Parameter, dest: BinaryStream):
    """
    Binary stream can already be loaded from parameters, so do nothing.
    """
    pass
