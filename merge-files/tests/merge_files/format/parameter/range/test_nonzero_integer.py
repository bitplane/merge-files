import re

from merge_files.format.parameter.range import nonzero_integer_regex


def test_decimal_int_ordinary():
    assert not re.fullmatch(nonzero_integer_regex, "1234567890")


def test_zero_decimal():
    assert not re.fullmatch(nonzero_integer_regex, "0")
    assert not re.fullmatch(nonzero_integer_regex, "   0   ")


def test_zero_long():
    assert not re.fullmatch(nonzero_integer_regex, "0l")
    assert not re.fullmatch(nonzero_integer_regex, "000000L")


def test_zero_hex():
    assert not re.fullmatch(nonzero_integer_regex, "0x0")
    assert not re.fullmatch(nonzero_integer_regex, "    0x000000")
    assert not re.fullmatch(nonzero_integer_regex, "    0x000  ")


def test_zero_octal():
    assert not re.fullmatch(nonzero_integer_regex, "0o0")
    assert not re.fullmatch(nonzero_integer_regex, "  0o00  ")


def test_zero_binary():
    assert not re.fullmatch(nonzero_integer_regex, "0b0")
    assert not re.fullmatch(nonzero_integer_regex, "  0b00  ")
