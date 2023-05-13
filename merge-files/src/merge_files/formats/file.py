from pathlib import Path

from merge_files.formats.format import Format, FormatOptions
from merge_files.merge.options import StageOptions


class File(Format):
    """
    Base class for files, which get loaded from a path.
    """

    options: FormatOptions

    def __init__(self, options: StageOptions):
        """
        Create a reference to the data we want to merge,
        but don't actually load it yet.
        """
        super().__init__(options)

        self.path: Path = Path(self.options.target)
        self.contents = None

    def read(self):
        """
        Load the data into this object
        """
        if self.path.exists():
            self.contents = self.path.read_bytes()
        else:
            self.contents = b""

    def dump(self) -> bytes:
        """
        Output the data in its native format
        """
        return self.contents

    def write(self):
        """
        Save the changes to the target
        """
        self.path.write_bytes(self.dump())

    @classmethod
    def validate(cls, options: dict) -> FormatOptions:
        """
        Returns True if this format can be used to read/write the given location
        """
        validated: FormatOptions = super().validate(options)
        path = Path(validated.target)

        if path.is_dir():
            raise ValueError(f"Target {path} is a directory")

        return validated
