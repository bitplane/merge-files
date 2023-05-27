import math

import pytest
from merge_files.format.parameter.range.range import Range


def test_range():
    val = Range("1:2")

    assert val.start == 1
    assert val.stop == 2


def test_too_many_values():
    with pytest.raises(ValueError):
        Range("1:2:3")


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


def test_hex_range():
    assert Range("0x1:0x10") == Range("1:16")


def test_binary_range():
    assert Range("0b0:0b100") == Range(":4")


def test_octal_range():
    assert Range("0o0:0o10") == Range(":8")


def test_invalid_ints():
    with pytest.raises(ValueError):
        Range("bleep:bloop")


def test_inf():
    assert Range("0:inf") == Range(":")


def test_start_after_stop():
    with pytest.raises(ValueError):
        Range("10:1")


def test_two_start_positions():
    with pytest.raises(ValueError):
        Range(value=1, start=0, stop=2)


def test_start_and_stop():
    r = Range(10, 20)

    assert r.start == 10
    assert r.stop == 20


def test_value_with_integer():
    r = Range(2)

    assert r.start == 0
    assert r.stop == 2
