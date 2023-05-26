import math

import pytest
from merge_files.format.parameter.range import Range


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
