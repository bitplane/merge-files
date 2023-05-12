import re
from enum import Enum
from pathlib import Path
from typing import List, Optional, Union

from pydantic import BaseModel

from .file import MergeableFile
from .mergeable import FileSupport, SupportLevel
from .method import Method

NULL = 0


class PositionalConstant(Enum):
    """
    Where to put the list data in the file
    """

    START = "start"
    END = "end"


ListPosition = Union[PositionalConstant, int]


class NumericCombine(Enum):
    """
    How to combine binary data
    """

    INSERT = "insert"
    OVERWRITE = "overwrite"
    XOR = "xor"


class Options(BaseModel):
    """
    Options for merging binary files
    """

    at: ListPosition = PositionalConstant.END
    """
    Where to put the data. "start", "end" or an offset in bytes
    """

    overwrite: Optional[bool] = None
    """
    Overwrite the destination data?
    """

    method: Optional[Method] = None


# options = [
#    MergeOption(name="at", value="end", description="Put our data at the end of the file"),
#
# ]


class BinaryFile(MergeableFile):
    """
    A bunch of bytes.
    """

    usable_methods = [
        Method.default,
        Method.overwrite,
        Method.prepend,
    ]

    def merge(self, other: bytes, method: Method) -> bytes:
        """
        Merge the contents into the other file and return it.
        """
        if method == Method.preserve:
            return other
        elif method == Method.overwrite:
            return self.contents
        elif method == Method.append or method == Method.default:
            return other + self.contents
        elif method == Method.prepend:
            return self.contents + other
        else:
            raise ValueError("Invalid merge method")

    @classmethod
    def can_load(cls, source: Path) -> bool:
        """
        We can load any file, 'cause we're just a bunch of bytes
        """
        return source.is_file()

    @classmethod
    def get_supported_types(cls) -> List[FileSupport]:
        return super().get_supported_types() + [
            FileSupport(
                SupportLevel.MANGLING,
                re.Pattern(".*"),
                [
                    Options(
                        name="append",
                        value="true",
                        description="Put our data at the end of the file",
                    ),
                ],
                "Binary data",
            )
        ]
