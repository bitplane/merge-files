from merge_files.formats.format import Format
from merge_files.merge.merge_method import SupportLevel, merge_method
from pydantic import ValidationError
from pytest import raises


def test_raise_exception_when_no_other_argument():
    """
    Test that merge_method raises an exception when it's not used on a function
    """
    with raises(ValidationError):

        @merge_method
        def no_other():
            pass


def test_adds_attributes():
    """
    Test that merge_method adds a source_format and support attribute to the
    wrapped function.
    """

    @merge_method.MANGLING
    def test_func(other: Format):
        pass

    assert test_func.source_format == "Format"
    assert test_func.support == SupportLevel.MANGLING


def test_support_level_sortable():
    """
    These things should be sortable by support level, so we can pick the best one
    and move on to the next one if it fails.
    """

    @merge_method.LOSSLESS
    def first_choice(other: Format):
        pass

    @merge_method.MANGLING
    def last_choice(other: Format):
        pass

    # "comes before" rather than "is better than"
    assert first_choice < last_choice
