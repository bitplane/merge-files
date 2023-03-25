from pathlib import Path

from .file import File
from .method import Method

NULL = 0


class BinaryFile(File):
    """
    A bunch of bytes.
    """

    usable_methods = [
        Method.default,
        Method.preserve,
        Method.overwrite,
        Method.append,
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
