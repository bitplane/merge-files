from merge_files.mergable.binary import concatenate


def test_concatenate_text_files():
    dest = b"hello\nworld"
    source = b"goodbye\nworld"

    assert concatenate(source, dest) == b"hello\nworld\ngoodbye\nworld"


def test_concatenate_text_files_with_newline():
    dest = b"hello\nworld\n"
    source = b"goodbye\nworld"

    assert concatenate(source, dest) == b"hello\nworld\ngoodbye\nworld"


def test_concatenate_binary_files():
    dest = b"\x00\x01"
    source = b"\x02\03"

    assert concatenate(source, dest) == b"\x00\x01\x02\03"


def test_no_dupes():
    dest = b"hello world"
    source = b"hello"

    assert concatenate(source, dest) == b"hello world"
