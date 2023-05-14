import inspect
from enum import Enum
from typing import Callable

from pydantic import BaseModel, ValidationError, validator


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


class MergeMethod(BaseModel):
    """
    Tags a function as a way to convert / merge from one format to another.
    """

    func: Callable
    """The function wrapped by the method"""

    source_format: str = None
    """The format that this method can merge from"""

    support: SupportLevel = SupportLevel.GENERIC
    """How well this method supports the source format"""

    @validator("source_format", pre=True, always=True)
    def validate_source_format(cls, source_format, values):
        func = values["func"]
        argspec = inspect.getfullargspec(func)
        source_format = argspec.annotations.get("other", None)

        if source_format is None:
            raise ValidationError("Missing 'other' argument on wrapped function")

        # coerce to a string because we might be loading the module it lives in
        # and end up with infinite recursion if we try to load it again.
        if not isinstance(source_format, str):
            source_format = str(source_format.__name__)

        return source_format

    def __lt__(self, other: "MergeMethod") -> bool:
        """
        Ensure that MergeMethods are sortable by support level, a proxy to priority.
        This could be made more complex for specific.
        """
        return self.support.value > other.support.value


def _merge_method_decorator(support: SupportLevel = SupportLevel.GENERIC):
    """
    Merge method factory function.

    This is used to create the merge_methods because decorators with arguments are weird, ugly time
    vampires that don't let us get arguments back out of the decorated function without performing
    the most disgusting sins. Fuck you, Python.
    """

    def create(func):
        return MergeMethod(support=support, func=func)

    return create


class MergeMethods:
    """
    Container for all the merge methods with the Enum values
    as members. Decorate with an instance.
    """

    def __init__(self):
        for level in SupportLevel:
            name: str = level.name
            setattr(self, name, _merge_method_decorator(support=level))

    def __call__(self, *args, **kwargs):
        return _merge_method_decorator()(*args, **kwargs)


merge_method = MergeMethods()
