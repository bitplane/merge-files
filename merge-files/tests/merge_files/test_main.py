import pytest
from merge_files.main import parse_args


def test_parse_args():
    args = parse_args(["--source=hello", "--dest=world", "--update"])
    assert args.source == "hello"
    assert args.dest == "world"
    assert args.update


def test_parse_args_default_no_update():
    args = parse_args(["--source=hello", "--dest=world"])
    assert not args.update


def test_parse_args_source_required():
    with pytest.raises(SystemExit):
        parse_args(["--dest=world"])


def test_parse_args_dest_required():
    with pytest.raises(SystemExit):
        parse_args(["--source=megatron"])
