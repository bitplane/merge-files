from merge_files.utils.discovery import subclasses


class Base:
    pass


class Depth1(Base):
    pass


class Depth2(Depth1):
    pass


class Depth3(Depth2):
    pass


class Mixin:
    pass


class MultipleInheritance(Depth1, Base, Mixin):
    pass


class NoInheritance:
    pass


def test_subclasses_full():
    """
    Test that subclasses returns the correct subclasses

    Like we don't expect to get the Mixin class, because it's not a subclass
    of Base.
    """

    expected = {Depth1, Depth2, Depth3, MultipleInheritance}
    actual = subclasses(Base)

    assert actual == expected


def test_no_children():
    """
    Should get an empty set
    """

    expected = set()
    actual = subclasses(NoInheritance)

    assert actual == expected
