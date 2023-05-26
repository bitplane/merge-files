from merge_files.merge.merger import Merger


def test_find_mergeable_types():
    formats = Merger.find_supported_formats()

    # from merge_files.merge.registry import registry

    assert len(formats) > 0


# def test_construct_merger():
#     args = Arguments()
#     merger = Merger(args)
#     merger  # breakpoint
