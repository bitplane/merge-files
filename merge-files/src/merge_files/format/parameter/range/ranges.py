from typing import Any, Union

from merge_files.format.parameter.range.range import Range
from merge_files.utils.types import is_int, is_range


class Ranges:
    """
    A list of ranges that are combined and sorted
    """

    ranges: list[Range]

    def __init__(self, value: str = ""):
        self.ranges = []
        ranges = [Range.parse_str(v) for v in str(value).split(",")]
        ranges = sorted(ranges)

        for r in ranges:
            self.append(r)

        super().__init__()

    def append(self, value: Range) -> None:
        """
        Add this range to the list of ranges.

        This mutates the object.
        """
        self.ranges.append(value)
        self.ranges.sort()

        i = 1

        while i < len(self.ranges):
            current = self.ranges[i]
            last = self.ranges[i - 1]
            if last.attached(current):
                self.ranges[i - 1] = current.join(last)
                del self.ranges[i]
                i -= 1
            i += 1

    def __eq__(self, other: "Ranges"):
        """
        Compare the two lists based on their string representations
        """
        return str(self) == str(other)

    def __repr__(self):
        """
        Return a code representation of this bunch of ranges
        """
        return f'{self.__class__.__name__}("{str(self)}")'

    def __str__(self):
        """
        Return a string representation of this bunch of ranges
        """
        return ",".join(str(r) for r in self.ranges)

    def __add__(self, other: Any) -> "Ranges":
        """
        Combine this range with another range
        """
        new = Ranges(self)
        if isinstance(other, Range):
            new.append(other)
            return new
        elif isinstance(other, str):
            other = Ranges(other)

        for o in other.ranges:
            new.append(o)

        return new

    def __contains__(self, other: Any) -> bool:
        """
        See if a value is in our ranges
        """
        # this is a disgusting copy/paste of Range.__contains__
        # and should be made a lot thinner
        if is_int(other):
            for r in self.ranges:
                if other in r:
                    return True
            return False

        if is_range(other):
            for r in self.ranges:
                if other in r:
                    return True
            return False

        if isinstance(other, Ranges):
            return other.ranges in self

        if isinstance(other, str):
            return Ranges(other) in self

        if hasattr(other, "__iter__"):
            # generic support for iterables
            for o in other:
                if o not in self:
                    return False
            return True

        # Do whatever Range can do
        for r in self.ranges:
            if other in r:
                return True
        return False

    def __iter__(self):
        """
        Iterate over the values in our ranges.

        Note that this could be boundless.
        """
        for r in self.ranges:
            for i in r:
                yield i

    def overlaps(self, other: Union["Ranges", str]) -> bool:
        """
        True if this range overlaps with the other range
        """
        other = Ranges(other)
        for r in self.ranges:
            for o in other.ranges:
                if r.overlaps(o):
                    return True

        return False

    @classmethod
    def validate(cls, value: Any) -> "Range":
        """
        Validate a value and convert it to a Range
        """
        if isinstance(value, cls):
            return value

        return cls(value)

    @classmethod
    def __get_validators__(cls):
        """
        For automatic validation in pydantic
        """
        yield cls.validate
