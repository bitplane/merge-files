import math
from typing import Iterable, Union

from pydantic import ConstrainedStr


def str_to_int(value: str, default: int) -> int:
    """
    Convert a string to an integer. If the string is empty, return the default
    """
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        if value == "inf" or value == "end":
            return math.inf
        elif "0x" in value:
            return int(value, 16)
        elif "0o" in value:
            return int(value, 8)
        elif "0b" in value:
            return int(value, 2)
        else:
            raise ValueError(f"Invalid integer value {value}")


class Range(ConstrainedStr):
    def __init__(self, value: str = ""):
        vals = [v.strip() for v in value.split(":")]

        if len(vals) > 2:
            raise ValueError("Too many values, only start and stop are allowed")

        if len(vals) == 1:
            self.start = 0
            self.stop = str_to_int(vals[0], math.inf)
        else:
            self.start = str_to_int(vals[0], 0)
            self.stop = str_to_int(vals[1], math.inf)

        if self.start < 0:
            raise ValueError(f"start must be positive (not {self.start})")

        if self.stop < 0:
            raise ValueError(f"stop must be positive (not {self.stop})")

        if self.start >= self.stop:
            raise ValueError(
                f"start must be less than stop (not {self.start} >= {self.stop}))"
            )

        super().__init__()

    def __repr__(self):
        if not self.start and self.stop is math.inf:
            return ":"
        elif self.start == 0:
            return f"{self.stop}"
        elif self.stop is math.inf:
            return f"{self.start}:"
        else:
            return f"{self.start}:{self.stop}"

    def __eq__(self, other):
        return self.start == other.start and self.stop == other.stop

    def __lt__(self, other: "Range"):
        """
        Just for sorting. Makes no claims about the ranges being comparable
        """
        start = self.start or 0
        other_start = other.start or 0

        return start < other_start

    def __contains__(self, other: Union["Range", int, float, Iterable]) -> bool:
        """
        See if a value is in this range
        """
        if other is None:
            return False

        if isinstance(other, (int, float)):
            return self.start <= other <= self.last

        if isinstance(other, Range):
            start_inside = other.start in self
            last_inside = self.stop is None or other.last in self

            return start_inside and last_inside

        if hasattr(other, "__iter__"):
            for o in other:
                if o is other:
                    raise TypeError(f"Can't recurse on {type(other)}")
                if o not in self:
                    return False
            return True

        raise TypeError(f"Unsupported type {type(other)}")

    def __add__(self, other: "Range") -> "Range":
        """
        Combine this range with another range
        """
        return self.combine(other)

    @property
    def is_full(self) -> bool:
        """
        True if this range starts at zero and has no end
        """
        return self.start == 0 and self.stop is math.inf

    @property
    def last(self) -> Union[int, float]:
        """
        Gets the last value in this range. Will return infinity if the range
        has no end
        """
        return self.stop - 1

    def overlaps(self, other: "Range") -> bool:
        """
        True if this range overlaps with the other range
        """
        if self in other or other in self:
            return True

        if self.start in other or other.start in self:
            return True

        return False

    def combine(self, other: "Range") -> "Range":
        """
        Combine this range with another range
        """
        if not self.overlaps(other):
            raise ValueError("Ranges do not overlap")

        r = Range()
        r.start = min(self.start, other.start)
        r.stop = max(self.stop, other.stop)

        return r


class Ranges(ConstrainedStr):
    ranges: list[Range]

    def __init__(self, value: str = ""):
        self.ranges = []
        ranges = [Range(v.strip()) for v in value.split(",")]
        ranges = sorted(ranges)

        for r in ranges:
            self.append(r)

        super().__init__()

    @classmethod
    def validate(cls, value: Union[str, "Ranges"]):
        if isinstance(value, str):
            return cls(value)
        elif isinstance(value, cls):
            return value

    def append(self, value: Range):
        """
        Combine overlapping ranges
        """
        self.ranges.append(value)
        self.ranges.sort()
        i = 0
        while i < len(self.ranges):
            try:
                self.ranges[i] = self.ranges[i].combine(self.ranges[i + 1])
                del self.ranges[i + 1]
            except IndexError:
                break
            except ValueError:
                i += 1

    def __eq__(self, other: "Ranges"):
        return repr(self) == repr(other)

    def __repr__(self):
        return ",".join(repr(r) for r in self.ranges)

    def __contains__(self, other: Union["Ranges", Range, int, float, Iterable]) -> bool:
        """
        See if a value is in this range
        """
        if other is None:
            return False

        if isinstance(other, (int, float)):
            for r in self.ranges:
                if other in r:
                    return True
            return False

        if isinstance(other, Range):
            for r in self.ranges:
                if other in r:
                    return True
            return False

        if isinstance(other, Ranges):
            return other.ranges in self

        if hasattr(other, "__iter__"):
            for o in other:
                if o is other:
                    raise TypeError(f"Can't recurse on {type(other)}")
                if o not in self:
                    return False
            return True

        raise TypeError(f"Unsupported type {type(other)}")
