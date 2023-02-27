import pytest
from merge_files.main import parse_args


def test_parse_args():
    args = parse_args(["hello", "world", "--update"])
    assert args.source == "hello"
    assert args.dest == "world"
    assert args.update


def test_default_no_update():
    args = parse_args(["hello", "world"])
    assert not args.update


def test_two_args_required():
    with pytest.raises(SystemExit):
        parse_args(["meh"])


def test_args_required():
    with pytest.raises(SystemExit):
        parse_args([])
