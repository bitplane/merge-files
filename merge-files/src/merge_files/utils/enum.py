# Daniil Fajnberg
# https://stackoverflow.com/a/75601761/146642
# CC-BY-SA 4.0

from collections.abc import Callable, Iterator
from enum import EnumMeta
from typing import Any, Optional, TypeVar, cast

from pydantic.fields import ModelField

E = TypeVar("E", bound=EnumMeta)


def __modify_enum_schema__(
    field_schema: dict[str, Any],
    field: Optional[ModelField],
) -> None:
    if field is None:
        return
    field_schema["enum"] = list(cast(EnumMeta, field.type_).__members__.keys())


def __enum_name_validator__(v: Any, field: ModelField) -> Any:
    assert isinstance(field.type_, EnumMeta)
    if isinstance(v, field.type_):
        return v  # value is already an enum member
    try:
        return field.type_[v]  # get enum member by name
    except KeyError:
        raise ValueError(f"Invalid {field.type_.__name__} `{v}`")


def __get_enum_validators__() -> Iterator[Callable[..., Any]]:
    yield __enum_name_validator__


def validate_by_name(cls: E) -> E:
    setattr(cls, "__modify_schema__", __modify_enum_schema__)
    setattr(cls, "__get_validators__", __get_enum_validators__)
    return cls
