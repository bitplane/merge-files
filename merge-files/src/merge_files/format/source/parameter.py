from merge_files.format import Format


class Parameter(Format):
    """
    Represents a parameter passed in on the command line
    """

    class Options(Format.Options):
        """
        Options for a parameter
        """

    target: str
    """The target file, folder, URL or whatever"""
