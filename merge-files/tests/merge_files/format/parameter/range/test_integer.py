import re

from merge_files.format.parameter.range import integer_regex


def test_decimal_int_ordinary():
    assert re.fullmatch(integer_regex, "1234567890")
    assert re.fullmatch(integer_regex, "0")


def test_decimal_int_underscore():
    assert re.fullmatch(integer_regex, "1_2_3")
    assert not re.fullmatch(integer_regex, "1__2_3")
    assert not re.fullmatch(integer_regex, "_3")
    assert not re.fullmatch(integer_regex, "3_")


def test_decimal_int_long():
    """
    Basic tests for decimal integers.
    """

    assert re.fullmatch(integer_regex, "1234567890l")
    assert re.fullmatch(integer_regex, "0l")
    assert re.fullmatch(integer_regex, "1_2_3L")


def test_hexadecimal():
    assert re.fullmatch(integer_regex, "0x1234567890abcdefABCDEF")
    assert re.fullmatch(integer_regex, "0x0")
    assert re.fullmatch(integer_regex, "0x1_2_3")
    assert not re.fullmatch(integer_regex, "0x1_2_3L")


def test_octal():
    assert re.fullmatch(integer_regex, "0o1234567")
    assert re.fullmatch(integer_regex, "0o0")
    assert re.fullmatch(integer_regex, "0o1_2_3")


def test_binary():
    assert re.fullmatch(integer_regex, "0b101010101000011")
    assert re.fullmatch(integer_regex, "0b0")
    assert re.fullmatch(integer_regex, "0b1_0_1_0_1_0_1_0_1_0_1_0_1_0_1_0")


def test_decimal_whitespace():
    assert not re.fullmatch(integer_regex, "0 0 1")


def test_sign():
    assert re.fullmatch(integer_regex, "+1234567890")
    assert re.fullmatch(integer_regex, "-1234567890")
    assert not re.fullmatch(integer_regex, "++1234567890")
    assert not re.fullmatch(integer_regex, "--1234567890")
    assert not re.fullmatch(integer_regex, "-+1234567890")
