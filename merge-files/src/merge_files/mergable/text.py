from pathlib import Path

import chardet

from .mergable import MergableFile, MergeMethod

NULL = 0


class TextFile(MergableFile):
    """
    A text file.
    Merges by concatenating onto the end of a given file
    """

    usable_methods = [
        MergeMethod.default,
        MergeMethod.preserve,
        MergeMethod.overwrite,
        MergeMethod.combine,
        MergeMethod.append,
        MergeMethod.prepend,
    ]

    def merge(self, other: bytes, method: MergeMethod) -> bytes:
        """
        Merge the contents into the other file and return it.
        """
        if method == MergeMethod.preserve:
            return other
        elif method == MergeMethod.overwrite:
            return self.contents
        elif method in (MergeMethod.combine, MergeMethod.append, MergeMethod.default):
            return concatenate(self.contents, other.contents)
        elif method == MergeMethod.prepend:
            return concatenate(other.contents, self.contents)
        else:
            raise ValueError("Invalid merge method")

    @classmethod
    def can_load(cls, source: Path) -> bool:
        """
        We don't like files with null bytes in them, and they
        must have a detectable character encoding.
        """
        if not source.is_file():
            return False

        data = source.read_bytes()

        encoding = chardet.detect(data)["encoding"]

        return encoding and NULL not in data


def concatenate(source: bytes, dest: bytes, update=False) -> bytes:
    """
    If the files are text, then a newline will be inserted between them,
    otherwise they will be concatenated together
    """

    if update:
        raise NotImplementedError("Can't update in concatenation")

    if source in dest:
        return dest
    else:
        binary = NULL in dest

        dst_encoding = chardet.detect(dest)["encoding"]
        src_encoding = chardet.detect(source)["encoding"]

        if not binary and dst_encoding and src_encoding:
            source_text = source.decode(src_encoding)

            if dest[-1] != b"\n"[0]:
                return dest + b"\n" + source_text.encode(dst_encoding)
            else:
                return dest + source_text.encode(dst_encoding)

    return dest + source
