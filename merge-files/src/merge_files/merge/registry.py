import inspect
from enum import Enum
from typing import Callable, Dict, List, Type

from merge_files.format import Format
from pydantic import BaseModel


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


class MergeParams(BaseModel):
    """
    Tags a function as a way to convert / merge from one format to another.
    """

    func: Callable
    """The function wrapped by the method"""

    source_format: Type[Format]
    """The format that this method can merge from"""

    dest_format: Type[Format]
    """The format that this method merges into"""

    support: SupportLevel = SupportLevel.GENERIC
    """How well this method supports the source format"""

    def __lt__(self, other: "MergeParams") -> bool:
        """
        Ensure that MergeMethods are sortable by support level, a proxy to priority.
        """
        return self.support.value > other.support.value


class MergeRegistry(BaseModel):
    """
    Where merge methods are registered
    """

    by_source: Dict[Format, List[MergeParams]] = {}
    by_dest: Dict[Format, List[MergeParams]] = {}

    def register_merge(self, params: MergeParams) -> None:
        """
        Register a merge method
        """

        if params.source_format not in self.by_source:
            self.by_source[params.source_format] = []

        self.by_source[params.source_format].insert(params)
        self.by_source[params.source_format].sort()

        if params.dest_format not in self.by_dest:
            self.by_source[params.dest_format] = []

        self.by_dest[params.dest_format].insert(params)
        self.by_dest[params.dest_format].sort()

    def clear(self) -> None:
        """
        Clear all registered merge methods
        """

        self.by_source.clear()
        self.by_dest.clear()


registry = MergeRegistry()


def merge_method(support: SupportLevel = SupportLevel.GENERIC, streaming: bool = False):
    """
    Decorator for a function that can merge two data types together.
    """

    def decorate(func: Callable):
        func_args = inspect.getfullargspec(func)

        params = {"support": support, "func": func}

        for param in ["func", "source_format", "dest_format", "streaming"]:
            params[param] = func_args.annotations.get(param, None)

        obj = MergeParams.parse_obj(params)

        registry.register_merge(obj)

        return func

    return decorate
