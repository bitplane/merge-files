from typing import Optional

from merge_files.merge.options import StageOptions
from pydantic import BaseModel, ValidationError


class FormatOptions(StageOptions):
    """
    General options for all formats
    """

    format: Optional[str] = None
    """
    Force using a specific format
    """


class Format(BaseModel):
    """
    Defines a data format
    """

    options: FormatOptions

    def __init__(self, options: FormatOptions):
        """
        Create a reference to the data we want to merge,
        but don't actually load it yet.
        """
        self.options: FormatOptions = options

    def read(self):
        """
        Load the data into this object
        """
        raise NotImplementedError()

    def dump(self) -> bytes:
        """
        Dump the data out to a bytes object
        """
        raise NotImplementedError()

    def write(self):
        """
        Commit the data to the target
        """
        raise NotImplementedError()

    @classmethod
    def validate(cls, options: dict) -> FormatOptions:
        """
        Returns stage options if this format can be used to read the given
        target given the options provided. Can raise an exception to force an
        early-out.

        You can use validation rules in the `options` class variable to
        force an exception, or override this method and add your own logic.
        """
        validated: FormatOptions = cls.__annotations__["options"](**options)

        if validated.format == "format":
            raise ValidationError("The 'format' base class can't be used directly")

        return validated

    @classmethod
    def get_merge_methods(cls):
        """
        Return a list of things that can be merged in to this format.

        This is a list of functions that have been decorated with
        `merge_method`.
        """
        return [value for value in cls.__dict__.values() if hasattr(value, "support")]
