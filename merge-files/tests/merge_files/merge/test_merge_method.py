from merge_files.merge.registry import merge_method
from pydantic import ValidationError
from pytest import raises


def test_validation_error_no_args():
    """
    Test that merge_method raises an exception when it's used on a
    function with no arguments
    """
    with raises(ValidationError):

        @merge_method()
        def no_other():
            pass
