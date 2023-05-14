from enum import Enum


class LineEndings(Enum):
    """
    Line ending types for text files in various platforms
    """

    lf = b"\n"
    """
    Line feed, the standard on UNIX systems
    """

    crlf = b"\r\n"
    """
    Carriage return + line feed, for Windows systems
    """

    cr = b"\r"
    """
    Carriage return, the standard on Mac OS 9 and earlier, and on
    older 8-bit systems.
    """

    z = b"\0"
    """
    Null byte. Used by some command line tools. Useful, but not
    recommended.
    """


def detect_line_endings(data: bytes, max_size=1_024_000) -> bytes:
    """
    Detect the line endings used in some text data.

    Processes the first 1MB of data, and returns the first line ending
    it finds. If no line endings are found, returns an empty byte array.
    """
    pos = chunk_size = 1_024

    max_size = min(len(data), max_size)

    while pos < max_size:
        start = pos - chunk_size
        chunk = data[start:pos]
        for line_ending in LineEndings:
            if line_ending.value in chunk:
                return line_ending.value
        pos += chunk_size

    return b""
