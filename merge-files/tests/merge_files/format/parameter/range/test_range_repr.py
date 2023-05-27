from merge_files.format.parameter.range.range import Range


def test_repr_empty():
    assert repr(Range("")) == "Range()"
    assert repr(Range(":")) == "Range()"


def test_repr_stop_only():
    assert repr(Range("  102")) == "Range(102)"
    assert repr(Range(":123")) == "Range(123)"


def test_repr_start_only():
    assert repr(Range("  102:")) == "Range(102, inf)"


def test_repr_start_and_stop():
    assert repr(Range("  102 : 123  ")) == "Range(102, 123)"
