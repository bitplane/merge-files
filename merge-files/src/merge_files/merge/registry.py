"""
Contains the registry of merge methods.
"""

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

    source: Type[Format]
    """The format that this method can merge from"""

    dest: Type[Format]
    """The format that this method merges into"""

    support: SupportLevel = SupportLevel.GENERIC
    """How well this method supports the source format"""

    streaming: bool = False
    """Does this method support streaming? If so, we prefer this method"""

    def __lt__(self, other: "MergeParams") -> bool:
        """
        Compare two merge methods to see which one comes first.
        """

        equal_support = self.support.value == other.support.value
        better_support = self.support.value > other.support.value

        lower_ram_usage = self.streaming and not other.streaming

        return better_support or (equal_support and lower_ram_usage)


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

        if params.source not in self.by_source:
            self.by_source[params.source] = []

        self.by_source[params.source].append(params)
        self.by_source[params.source].sort()

        if params.dest not in self.by_dest:
            self.by_dest[params.dest] = []

        self.by_dest[params.dest].append(params)
        self.by_dest[params.dest].sort()

    def get_merge(self, source: Format, dest: Format) -> List[MergeParams]:
        """
        Get a list of merge methods that can convert from the source to the dest
        format.
        """

        return self.by_source.get(source, [])

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

        params = {"support": support, "func": func, "streaming": streaming}

        for param in ["source", "dest"]:
            params[param] = func_args.annotations.get(param, None)

        obj = MergeParams.parse_obj(params)

        registry.register_merge(obj)

        return func

    return decorate
