"""
Some quacky type helpers so we don't have to use isinstance everywhere
"""

import math
from typing import Any


def to_int(value: str, default: int) -> int:
    """
    Convert a string to an integer. If the string is empty, return the default
    """
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        if "0x" in value:
            return int(value, 16)
        elif "0o" in value:
            return int(value, 8)
        elif "0b" in value:
            return int(value, 2)
        elif value == "inf" or value == "math.inf":
            return math.inf
        else:
            raise ValueError(f"Invalid integer value {value}")


def is_range(value: Any) -> bool:
    """
    Check if a value is a range-like object
    """
    return hasattr(value, "start") and hasattr(value, "stop")


def is_int(value: Any) -> bool:
    """
    Can this object be converted to an integer?
    """
    return hasattr(value, "__int__")
