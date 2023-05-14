import pytest
from merge_files.merge.stage import parse_args
from merge_files.utils.logging import LogLevel


def test_parse_args():
    """
    Tests the parse_args function
    """
    args = parse_args(["--option1", "--option2=value", "file1", "--option3", "file2"])
    stages = args.stages

    assert len(stages) == 2
    assert stages[0].target == "file1"
    assert stages[0].options == {"option1": True, "option2": "value"}
    assert stages[1].target == "file2"
    assert stages[1].options == {"option3": True}


def test_no_options():
    """
    Tests the parse_args function when no options are passed
    """
    args = parse_args(["file1", "file2"])
    stages = args.stages

    assert len(stages) == 2
    assert stages[0].options == {}
    assert stages[0].target == "file1"
    assert stages[1].options == {}
    assert stages[1].target == "file2"


def test_no_files():
    """
    Tests the parse_args function when no files are passed
    """
    args = parse_args(["--option1", "--option2=value"])
    stages = args.stages

    assert len(stages) == 1
    assert stages[0].options == {"option1": True, "option2": "value"}
    assert not stages[0].target


def test_no_options_or_files():
    """
    Tests the parse_args function when no options or files are passed
    """
    args = parse_args([])

    assert not args.stages


def test_file_starts_with_hyphen():
    args = parse_args(["--", "--file1"])

    stage = args.stages[0]
    assert stage.target == "--file1"


def test_unexpected_end_of_arguments():
    """
    Tests the parse_args function when the arguments end unexpectedly
    """
    with pytest.raises(ValueError):
        parse_args(["--option1", "--option2=value", "file1", "--option3", "--"])


def test_manually_set_target():
    """
    You can set the target manually since it's a field
    """
    args = parse_args(["--target=file1.txt", "--target=file2.txt"])
    stages = args.stages

    assert len(stages) == 2
    assert stages[0].target == "file1.txt"
    assert stages[1].target == "file2.txt"


def test_help():
    """
    Tests the parse_args function when the help flag is passed
    """

    args = parse_args(["--help"])

    assert args.options.help
    assert not args.stages


def test_set_log_level():
    """
    Set the log level to debug
    """

    args = parse_args(["--log-level=DEBUG", "file1.txt", "file2.txt"])

    assert args.options.log_level == LogLevel.DEBUG
