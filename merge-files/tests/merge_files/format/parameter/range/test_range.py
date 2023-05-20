import re

from merge_files.format.parameter.range import range_regex


def test_range_all():
    assert re.fullmatch(range_regex, ":")
    assert re.fullmatch(range_regex, "0:")
    assert re.fullmatch(range_regex, "::1")
    assert re.fullmatch(range_regex, "::")
    assert re.fullmatch(range_regex, "0x00::")


def test_invalid_range():
    assert not re.fullmatch(range_regex, "1:2:3:4")
    assert not re.fullmatch(range_regex, "")


def test_zero_step_invalid():
    assert not re.fullmatch(range_regex, ":0:0")
    assert not re.fullmatch(range_regex, ":0:  - 0x0000")
