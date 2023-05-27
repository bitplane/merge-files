from merge_files.format.parameter.range.range import Range
from merge_files.format.parameter.range.ranges import Ranges


def test_parse_single_range():
    r = Ranges("1:10")
    assert len(r.ranges) == 1
    assert r.ranges[0].start == 1
    assert r.ranges[0].stop == 10


def test_parse_multiple_ranges():
    r = Ranges("1:10, 20:30")

    assert len(r.ranges) == 2
    assert r.ranges[0].start == 1
    assert r.ranges[0].stop == 10
    assert r.ranges[1].start == 20
    assert r.ranges[1].stop == 30


def test_collapse_ranges():
    assert Ranges("0:10, 20:") == Ranges(":0x0a, 0x14:")
    assert Ranges(":,:") == Ranges("")
    assert Ranges("1:10, 5:15") == Ranges("1:15")


def test_combine_two_ranges():
    first = Ranges("1:10, 20:30")
    second = Ranges("0:5, 100:200")
    combined = first + second
    expected = Ranges("0:10,20:30,100:200")

    assert first in combined
    assert second in combined
    assert expected == combined


def test_combine_ranges_with_single_range():
    first = Ranges("1:10, 20:30")
    second = Range("0:5")
    combined = first + second
    expected = Ranges("0:10,20:30")

    assert first in combined
    assert second in combined
    assert combined == expected


def test_combine_ranges_with_string():
    first = Ranges("1:10, 20:30")
    second = "0:5"
    combined = first + second
    expected = Ranges("0:10,20:30")

    assert first in combined
    assert second in combined
    assert combined == expected


def test_combine_ranges_with_overlap():
    first = Ranges("11:15,20:25")
    second = Ranges("0:12, 100:")
    combined = first + second
    expected = Ranges("0:15,20:25,100:")

    assert first in combined
    assert second in combined
    assert combined == expected


def test_iterator():
    assert list(Ranges("1:5, 10:15")) == [1, 2, 3, 4, 10, 11, 12, 13, 14]


def test_range_ranges_equal():
    assert Ranges("10") == Range("0:10")
    assert Range("0:10") == Ranges("10")


def test_repr():
    ranges = Ranges(" 0x01:0b10, 15:20 , 30:")
    assert repr(ranges) == 'Ranges("1:2,15:20,30:")'


def test_membership_int():
    ranges = Ranges("1:10,20:30,100:150")

    assert 0 not in ranges
    assert 1 in ranges
    assert 5 in ranges
    assert 10 not in ranges
    assert 19 not in ranges
    assert 20 in ranges
    assert 30 not in ranges
    assert 100 in ranges
    assert 149 in ranges
    assert 150 not in ranges


def test_membership_sequence():
    ranges = Ranges("1:10,20:30,100:150")

    assert range(10, 15) not in ranges
    assert range(100, 110) in ranges


def test_membership_range():
    ranges = Ranges("1:10,20:30,100:150")

    assert Range(20, 30) in ranges
    assert Range() not in ranges
