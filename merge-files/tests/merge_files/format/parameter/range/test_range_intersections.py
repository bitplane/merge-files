from merge_files.format.parameter.range import Range


def test_combine():
    assert Range("1:10").combine(Range("5:15")) == Range("1:15")
    assert Range(":10").combine(Range("9:")) == Range(":")


def test_combine_adjacent():
    assert Range("1:10").combine(Range("10:15")) == Range("1:15")
    assert Range("1:10").combine(Range("0:1")) == Range("0:10")


def test_overlaps():
    assert Range("1:10").overlaps(Range("5:15"))
    assert Range(":10").overlaps(Range("9:"))

    assert Range("5:10").overlaps(Range(":"))
    assert Range(":").overlaps(Range(":"))
    assert Range("1:100").overlaps(Range("0:1000"))

    assert not Range("1:10").overlaps(Range("11:15"))
    assert not Range("1:10").overlaps(Range("11:"))


def test_adjacent():
    assert Range("1:10").adjacent(Range("10:15"))
    assert Range("1:10").adjacent(Range("0:1"))


def test_not_adjacent():
    assert not Range("1:10").adjacent(Range("0:10"))
    assert not Range("1:10").adjacent(Range("11:15"))
    assert not Range("1:10").adjacent(Range("11:"))
