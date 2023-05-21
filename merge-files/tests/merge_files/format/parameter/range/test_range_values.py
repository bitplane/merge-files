import math

import pytest
from merge_files.format.parameter.range import Range


def test_range():
    val = Range("1:2")

    assert val.start == 1
    assert val.stop == 2


def test_range_negative_start():
    with pytest.raises(ValueError):
        Range("-1:2")


def test_range_negative_stop():
    with pytest.raises(ValueError):
        Range("1:-2")


def test_range_no_start():
    val = Range(":2")

    assert val.start == 0
    assert val.stop == 2


def test_range_no_stop():
    val = Range("1:")

    assert val.start == 1
    assert val.stop == math.inf


def test_range_no_start_no_stop():
    val = Range(":")

    assert val.start == 0
    assert val.stop == math.inf


def test_repr_empty():
    assert repr(Range("")) == ":"
    assert repr(Range(":")) == ":"


def test_repr_stop_only():
    assert repr(Range("  102")) == "102"
    assert repr(Range(":123")) == "123"


def test_repr_start_only():
    assert repr(Range("  102:")) == "102:"


def test_repr_start_and_stop():
    assert repr(Range("  102 : 123  ")) == "102:123"


def test_too_many_values():
    with pytest.raises(ValueError):
        Range("1:2:3")


def test_equality():
    assert Range(":") == Range("0:")
    assert Range(":10") == Range("0:10")


def test_ordering():
    """
    Sorted by start value only
    """
    assert not Range(":") < Range(":10")
    assert not Range(":10") < Range(":11")

    assert Range(":") < Range("1:")
    assert Range("5:") > Range("1:10")


def test_contains_int():
    """
    Range should be like python ranges - end value is not included
    """
    assert 1 in Range("1:10")
    assert 9 in Range("1:10")
    assert 5 in Range("1:10")
    assert 0 not in Range("1:10")
    assert 10 not in Range("1:10")


def test_contains_sequence():
    assert (1, 2, 3, 4, 5) in Range("1:6")
    assert (1, 2, 3, 4, 5) not in Range("1:5")


def test_contains_range():
    assert Range("1:5") in Range("1:10")
    assert Range("1:10") not in Range("1:5")
    assert Range(":") not in Range("2:10")
    assert Range("2:10") in Range("2:")
    assert Range("2:") not in Range("2:10")


def test_contains_none():
    assert None not in Range(":")


def test_contains_string():
    with pytest.raises(TypeError):
        "hello" in Range(":")


def test_contains_unsupported_type():
    class Crash:
        pass

    with pytest.raises(TypeError):
        Crash() in Range(":")


def test_is_full():
    assert Range(":").is_full
    assert Range("0:").is_full
    assert not Range("1:").is_full
    assert not Range("1:10").is_full


def test_overlaps():
    assert Range("1:10").overlaps(Range("5:15"))
    assert Range(":10").overlaps(Range("9:"))

    assert Range("5:10").overlaps(Range(":"))
    assert Range(":").overlaps(Range(":"))
    assert Range("1:100").overlaps(Range("0:1000"))

    assert not Range("1:10").overlaps(Range("11:15"))
    assert not Range("1:10").overlaps(Range("11:"))


def test_combine():
    assert Range("1:10").combine(Range("5:15")) == Range("1:15")
    assert Range(":10").combine(Range("9:")) == Range(":")
