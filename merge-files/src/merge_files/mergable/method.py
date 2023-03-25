from enum import Enum


class Method(str, Enum):
    """
    How to combine the data.

    """

    default = "default"
    """
    Do the most sensible thing for the data format.
    In a text or binary file file, this might be concat+append.
    In a CSV file, this might be combine+append.
    """

    concat = "concat"
    """Add rows of data to the end of the existing data"""

    combine = "combine"
    """Add columns on the end of the existing data"""

    prepend = "prepend"
    """Insert before the existing data rather than append"""

    overwrite = "overwrite"
    """Replace the existing data"""
