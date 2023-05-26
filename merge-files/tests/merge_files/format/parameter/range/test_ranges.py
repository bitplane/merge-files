from merge_files.format.parameter.range import Range, Ranges


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


def test_combine_ranges():
    assert Ranges("0:10, 20:") == Ranges(":0x0a, 0x14:")
    assert Ranges(":,:") == Ranges("")
    assert Ranges("1:10, 5:15") == Ranges("1:15")


def test_combine_ranges_with_overlap():
    first = Ranges("11:15,20:25")
    second = Ranges("0:12, 100:")
    combined = first + second
    expected = Ranges("0:15,20:25,100:")

    assert first in combined
    assert second in combined
    assert combined == expected


def test_combine_range_and_ranges():
    first = Range("5:10") + Range("30:35")
    second = Ranges("0:12, 100:")
    combined = first + second
    expected = Ranges("12,30:35,100:")

    assert combined == expected


def test_iterator():
    assert list(Ranges("1:5, 10:15")) == [1, 2, 3, 4, 10, 11, 12, 13, 14]
