import inspect
from enum import IntEnum
from functools import wraps


class SupportLevel(IntEnum):
    """
    How well a file type or a conversion from one to the other is supported
    """

    NONE = -10
    """I can't do anything with this. Sorry."""

    MANGLING = 0
    """I'll do it if you force me to, but you might not like the results"""

    GENERIC = 10
    """I've got a trick for doing this, and it'll probably work. Will emit a warning"""

    GOOD = 20
    """Supports this format but not all of its features. Good enough."""

    FULL = 50
    """Fully supports this data format and all of its features."""

    LOSSLESS = 100
    """Supports this data format and all of its features, and doesn't lose any data in the process."""


def merge_method(func, support: SupportLevel = SupportLevel.GENERIC):
    """
    Use this to decorate a merge method, so that it can be found by the merger,
    sorted by priority, etc.
    """

    argspec = inspect.getfullargspec(func)
    specified_class = argspec.annotations.get(argspec.args[1])

    @wraps(func)
    def wrapper(self, actual_class: specified_class):
        setattr(func, "source_format", specified_class)
        setattr(func, "support", support)

        setattr(func, "__lt__", lambda self, other: self.support < other.support)

        result = func(self, actual_class)
        return result

    return wrapper
