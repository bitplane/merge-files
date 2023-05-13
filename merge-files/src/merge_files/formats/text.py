import os
from encodings.aliases import aliases
from typing import List, Literal, Optional

import chardet
from merge_files.formats.file import File, FormatOptions
from merge_files.merge.merge_method import SupportLevel, merge_method
from merge_files.utils.text import LineEndings, detect_line_endings


class TextFileOptions(FormatOptions):
    """
    Options for loading and merging into text data
    """

    at: int | Literal["start", "end"] = Literal["end"]
    """
    Where to insert/append the data; "start", "end" or a line number
    """

    newlines: Optional[LineEndings | str] = None
    """
    The type of newlines to use. Defaults to whatever is in the
    destination file, or the platform's default if the file is empty.

    Feel free to abuse this to remove line endings
    """

    encoding: str = "auto"
    """
    The character encoding to use. This will default to UTF-8 for an
    empty file, but otherwise will be detected using chardet.

    For a greppable list of encodings, use `--help text_file.encodings`
    """

    upgrade: bool = False
    """
    If set, then the file will be upgraded to UTF-8 if the characters
    in the source file can't be represented in the destinaton encoding.
    """


class TextFile(File):
    """
    Represents lines of text.
    """

    options: TextFileOptions
    """The options passed to the file"""

    encodings: List[str] = list(set(aliases.keys()))
    f"""All supported encodings:

    {os.linesep.join(encodings)}
    """

    lines: List[str] = []
    """The lines of text"""

    _encoding: str = None
    _line_endings: str = None

    @merge_method(SupportLevel.FULL)
    def merge_text(self, other: "TextFile"):
        """
        Merge other's data into this one
        """

        raise NotImplementedError()

    def read(self):
        """
        Load the data into this object
        """
        super().read()

        if self.options.encoding == "auto":
            if self.contents == b"":
                self._encoding = "utf8"
            else:
                # todo: use the confidenece level and try multiple encodings
                # if below some threshold ()
                self._encoding = chardet.detect(self.contents)["encoding"] or "utf8"
        else:
            self._encoding = self.options.encoding

        # todo: if there's only one line with no ending, we should probably
        # use the other file's line endings rather than coerce it to the
        # os's default.
        self._line_endings = detect_line_endings(self.contents) or os.linesep

        self.lines = self.contents.decode(self._encoding).split(self._line_endings)

    def dump(self) -> bytes:
        """
        Output the data in its native format
        """
        # todo: make this a generator
        return self._line_endings.join(self.lines).encode(self._encoding)
        # for line in self.lines:
        #     yield line
        #     yield self._line_endings
