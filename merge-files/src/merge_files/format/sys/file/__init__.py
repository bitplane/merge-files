import io
from abc import ABCMeta
from enum import Enum
from typing import Literal

from merge_files.format import Format


class SeekMode(Enum):
    """
    Says which point to seek from
    """

    SEEK_SET = 0
    """Seek from the start of the file"""

    SEEK_CUR = 1
    """Seek from the current position in the file"""

    SEEK_END = 2
    """Seek from the end of the file"""


class BaseFile(Format):
    """
    Represents a stream of binary data, like a file, TTY or socket
    """

    handle: io.IOBase = None

    @ABCMeta
    class Options(Format.Options):
        """
        Base options for file-like sources
        """

        handler: Literal["None"] = Literal["None"]
        """
        Name of the handler to use.
        SAFETY: Use a Literal["Choice1", "Choice2"] or it can run arbitrary code.
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

    def tell(self) -> int:
        """
        Get the current position in the file.
        """
        return self.handle.tell()


def RandomAccessFile(BaseFile):
    """
    A file where you can change the cursor position
    """

    def seek(self, offset: int, whence: SeekMode = SeekMode.SEEK_SET):
        """
        Seek to a position in the file.
        """
        return self.handle.seek(offset)


def ReadableFile(BaseFile):
    """
    A file that can be accessed in read mode
    """
    
    def read(self, size=-1) -> bytes:
        """
        Read data from the file.
        """
        return self.handle.read(size)


def WritableFile(BaseFile):
    """
    A file that can be written to
    """

    def write(self, bytes) -> int:
        """
        Write data to the file.
        """
        return self.handle.write(bytes)
