import inspect
from enum import Enum
from typing import Any, Callable

from merge_files.formats.format import Format


class SupportLevel(Enum):
    """
    How well a file type or a conversion from one to the other is supported
    """

    DISABLED = -10
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


class MergeMethod:
    def __init__(self, func: Callable, source_format: Format, support: SupportLevel):
        self.source_format = source_format
        self.support = support
        self._func = func

    def __lt__(self, other: "MergeMethod") -> bool:
        return self.support.value > other.support.value

    def __getattr__(self, name) -> Any:
        return self._func.__getattr__(self, name)


def _merge_method_decorator(support: SupportLevel = SupportLevel.GENERIC):
    """
    Merge method factory function.

    This is used to create the merge_methods because decorators with arguments are weird, ugly time
    vampires that don't let us get arguments back out of the decorated function without performing
    the most disgusting sins. Fuck you, Python.
    """

    def decorator(func):
        """
        The actual decorator
        """
        if not callable(func):
            raise ValueError("merge_method can only be used on functions")

        argspec = inspect.getfullargspec(func)
        source_format = argspec.annotations.get("other")

        if not source_format:
            raise ValueError("merge_method must have an 'other' argument")

        return MergeMethod(func=func, source_format=source_format, support=support)

    return decorator


class MergeMethods:
    """
    Container for all the merge methods with the Enum values
    as members. Decorate with an instance.
    """

    def __init__(self):
        for level in SupportLevel:
            name: str = level.name
            setattr(self, name, _merge_method_decorator(level))

    def __call__(self, *args, **kwargs):
        return _merge_method_decorator()(*args, **kwargs)


merge_method = MergeMethods()
