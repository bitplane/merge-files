from merge_files.merge.merger import Merger


def test_find_mergeable_types():
    formats = Merger.find_supported_formats()

    assert len(formats) > 0
