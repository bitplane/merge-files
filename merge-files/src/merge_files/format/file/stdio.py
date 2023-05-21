import sys
from typing import Literal

from merge_files.format import Format
from merge_files.format.file.text import TextStream
from pydantic import validator


class StdIo(TextStream):
    """ """

    class Options(Format.Options):
        """
        Streams for stdin/stdout/stderr
        """

        handler: Literal["stdin", 0, "stdout", 1, "stderr", 2] | sys.TextIO = Literal[
            "stdin"
        ]
        """Literal or integer for stdin/stdout/stderr."""

        @validator("handler")
        def set_handler(cls, v):
            """
            Convert handler from string or integer to function. Integers being C
            file descriptor ids.
            """

            if isinstance(v, sys.TextIO):
                return v

            if v == 0 or v == "stdin":
                return lambda _taget, _mode: sys.stdin
            elif v == 1 or v == "stdout":
                return lambda _taget, _mode: sys.stdout
            elif v == 2 or v == "stderr":
                return lambda _taget, _mode: sys.stderr
