import math

from merge_files.format.parameter.range import Range


def test_is_full():
    assert Range(":").is_full
    assert Range("0:").is_full
    assert not Range("1:").is_full
    assert not Range("1:10").is_full


def test_last():
    assert Range("").last == math.inf
    assert Range("10").last == 9
