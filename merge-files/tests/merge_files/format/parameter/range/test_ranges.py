from merge_files.format.parameter.range import Ranges


def test_parse_single_range():
    r = Ranges("1:10")
    assert r.ranges[0].start == 1
    assert r.ranges[0].stop == 10


def test_parse_multiple_ranges():
    r = Ranges("1:10, 20:30")
    assert r.ranges[0].start == 1
    assert r.ranges[0].stop == 10
    assert r.ranges[1].start == 20
    assert r.ranges[1].stop == 30
