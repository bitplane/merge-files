import pytest
from merge_files.format.parameter.range import Range, Ranges


def test_equality():
    assert Range(":") == Range("0:")
    assert Range(":10") == Range("0:10")


def test_equality_str():
    assert Range("") == ":"
    assert Range(":10") == "0:10"


def test_equality_int():
    assert Range("0:1") == 0
    assert Range("10:11") == 10
    assert Range("11") != 10


def test_sort_order():
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


def test_doesnt_contain_none():
    assert None not in Range(":")


def test_contains_text():
    with pytest.raises(TypeError):
        "hello" in Range(":")


def test_contains_unsupported_type():
    class Crash:
        pass

    with pytest.raises(TypeError):
        Crash() in Range(":")


def test_equality_other_type():
    class Crash:
        pass

    with pytest.raises(TypeError):
        Range(":") == Crash()


def test_plus_operator():
    assert Range("1:10") + Range("5:15") == Range("1:15")
    assert Range(":10") + Range("9:") == Range(":")


def test_plus_operator_non_overlapping():
    assert Range("1:10") + Range("11:15") == Ranges("1:10,11:15")


def test_add_adjacent_ranges():
    assert Range("0:5") + Range("5:10") == Range("0:10")


def test_iterator():
    assert list(Range("1:10")) == [1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert list(Range("5")) == [0, 1, 2, 3, 4]


def test_add_ranges_to_range():
    first = Range("1:10")
    second = Ranges("11:15, 20:25")
    combined = first + second

    assert first in combined
    assert second in combined
    assert combined == Ranges("1:10,11:15,20:25")
