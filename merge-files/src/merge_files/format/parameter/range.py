import math
from typing import Iterable, Union

from pydantic import ConstrainedStr


class Range(ConstrainedStr):
    def __init__(self, value: str = ""):
        vals = [v.strip() for v in value.split(":")]

        if len(vals) > 2:
            raise ValueError("Too many values, only start and stop are allowed")

        if len(vals) == 1:
            self.stop = int(vals[0]) if vals[0] != "" else math.inf
            self.start = 0
        else:
            self.start = int(vals[0]) if vals[0] else 0
            self.stop = int(vals[1]) if vals[1] != "" else math.inf

        if self.start < 0:
            raise ValueError("start must be positive")

        if self.stop < 0:
            raise ValueError("stop must be positive")

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

    @property
    def is_full(self) -> bool:
        """
        True if this range starts at zero and has no end
        """
        return self.start == 0 and self.stop is math.inf

    @property
    def last(self) -> Union[int, float]:
        """
        Gets the last value in this range. Will return infinity if the range has no end
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

    def __repr__(self):
        return ",".join([str(r) for r in self.ranges])

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
