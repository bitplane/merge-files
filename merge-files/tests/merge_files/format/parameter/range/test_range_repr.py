from merge_files.format.parameter.range import Range


def test_repr_empty():
    assert repr(Range("")) == ":"
    assert repr(Range(":")) == ":"


def test_repr_stop_only():
    assert repr(Range("  102")) == "102"
    assert repr(Range(":123")) == "123"


def test_repr_start_only():
    assert repr(Range("  102:")) == "102:"


def test_repr_start_and_stop():
    assert repr(Range("  102 : 123  ")) == "102:123"
