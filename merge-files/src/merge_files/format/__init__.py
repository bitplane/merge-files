from typing import Optional, TypeVar

from merge_files.merge.options import StageOptions
from pydantic import BaseModel, Field

FormatType = TypeVar("FormatType", bound="Format")
OptionsType = TypeVar("OptionsType", bound="Format.Options")


class Format(BaseModel):
    """
    Defines a data format
    """

    options: OptionsType | None = None
    """The options for the instance of thie object"""

    class Options(StageOptions):
        """
        General options for all formats
        """

        as_: Optional[FormatType.__name__] = Field(default=None, alias="as")
        """Force using a specific format"""

    def __init__(self, options: OptionsType):
        """
        Create a reference to the data we want to merge,
        but don't actually load it yet.
        """
        self.options = type(self.options).parse_raw(**options)
