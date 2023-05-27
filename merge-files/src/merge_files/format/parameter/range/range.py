import math
from typing import Any, Iterable, Union

from merge_files.utils.types import is_int, is_range, to_int


class Range:
    """
    A single range of values
    """

    start: int = 0
    stop: Union[int, float] = math.inf

    def __init__(
        self, value: Any = None, stop: Union[int, float] = None, start: int = None
    ):
        """
        Construct a range from a value, start and stop, or a value and stop, similar to Python slice
        and range notation, but with no step and no negative ranges.

        If just a value is passed, and it has a start and stop attribute, those will be used as the
        start and stop values. If it's a string, it will be parsed as a range string (e.g. "0:10",
        "1:" and so on). If it's an integer or math.inf, it will be used as the stop value.

        If a value and stop are passed, the value will be used as the start value and the stop will be
        used as the stop value. If a start and stop are passed, they will be used as the start and stop
        values.

        If no values are passed then it'll default to the full range from 0 to infinity.
        """
        has_no_params = value is stop is start is None
        value_only = value is not None and (stop is start is None)
        start_value_and_stop = value is not None and stop is not None
        inconsistent = value is not None and start is not None

        if inconsistent:
            raise ValueError("Got two values for start position")

        if start_value_and_stop:
            self.start = value
            self.stop = stop

        elif value_only:
            if is_range(value):
                self.start = value.start
                self.stop = value.stop
            elif isinstance(value, str):
                # do this rather than change all the tests
                other = self.parse_str(value)
                self.start = other.start
                self.stop = other.stop
            else:
                self.start = 0
                self.stop = value

        elif has_no_params:
            self.start = 0
            self.stop = math.inf
        else:
            self.start = start or 0
            self.stop = stop or math.inf

        # Convert to integers
        self.start = int(self.start)
        if self.stop != math.inf:
            self.stop = int(self.stop)

        if self.start < 0 or self.stop < 0:
            raise ValueError("Start and stop must be positive")

        if self.start > self.stop:
            raise ValueError("Stop can't be before start")

        super().__init__()

    @classmethod
    def parse_str(cls, value: str) -> "Range":
        """
        Construct Range from a string, Python slice notation
        """
        vals = [v.strip() for v in str(value).split(":")]

        if len(vals) > 2:
            raise ValueError("Too many values, Only start and stop are allowed")

        if len(vals) == 1:
            start = 0
            stop = to_int(vals[0], math.inf)
        else:
            start = to_int(vals[0], 0)
            stop = to_int(vals[1], math.inf)

        return cls(start=start, stop=stop)

    def __repr__(self):
        name = self.__class__.__name__
        if not self.start and self.stop is math.inf:
            return f"{name}()"
        elif self.start == 0:
            return f"{name}({self.stop})"
        else:
            return f"{name}({self.start}, {self.stop})"

    def __str__(self):
        """
        Convert to a string
        """
        if not self.start and self.stop is math.inf:
            return ":"
        elif self.start == 0:
            return f"{self.stop}"
        elif self.stop is math.inf:
            return f"{self.start}:"
        else:
            return f"{self.start}:{self.stop}"

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other: Any) -> bool:
        if is_int(other):
            return self.start == other and self.stop == other + 1
        if isinstance(other, str):
            return self == self.parse_str(other)
        elif not is_range(other):
            return str(self) == str(other)

        return self.start == other.start and self.stop == other.stop

    def __lt__(self, other: Any) -> bool:
        """
        Just for sorting. Makes no claims about the ranges being comparable
        """
        if is_range(other):
            start = self.start or 0
            other_start = other.start or 0
        else:
            return self.start < other

        return start < other_start

    def __contains__(self, other: Union["Range", int, float, Iterable]) -> bool:
        """
        See if a value is in this range
        """
        if is_int(other):
            return self.start <= other <= self.last

        if is_range(other):
            start_inside = other.start in self
            last_inside = self.stop is None or (other.stop - 1) in self

            return start_inside and last_inside

        if isinstance(other, str):
            return self.parse_str(other) in self

        if hasattr(other, "__iter__"):
            for o in other:
                if o not in self:
                    return False
            return True

        raise TypeError(f"Unsupported type {type(other)}")

    def __add__(self, other: Any) -> "Range":
        """
        Join two ranges together, if possible, and return a new one
        """
        return self.join(other)

    def __iter__(self):
        """
        Iterate over the values in this range
        """
        i = self.start
        while i < self.stop:
            yield i
            i += 1

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

    def adjacent(self, other: "Range") -> bool:
        """
        True if this range is adjacent to the other range
        """
        if self.stop == other.start or other.stop == self.start:
            return True

        return False

    def attached(self, other: "Range") -> bool:
        """
        True if this range is adjacent or overlaps the other range
        """
        return self.adjacent(other) or self.overlaps(other)

    def join(self, other: "Range") -> "Range":
        """
        Return a new range that is the combination of this range and the other
        """
        if not self.attached(other):
            raise ValueError(f"{self} and {other} aren't touching")

        r = Range()
        r.start = min(self.start, other.start)
        r.stop = max(self.stop, other.stop)

        return r

    @classmethod
    def validate(cls, value: Any) -> "Range":
        """
        Validate a value and convert it to a Range
        """
        if isinstance(value, cls):
            return value

        if isinstance(value, str):
            return cls.parse_str(value)

        return cls(value)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate
