from merge_files.merge.stage import parse_args


def test_parse_args():
    """
    Tests the parse_args function
    """
    args = parse_args(['--option1', '--option2=value', 'file1', '--option3', 'file2'])

    assert len(args) == 2
    assert args[0].file == 'file1'
    assert args[0].options[0].name == 'option1'
    assert args[0].options[1].name == 'option2'
    assert args[0].options[1].value == 'value'
    assert args[1].file == 'file2'
    assert args[1].options[0].name == 'option3'


def test_parse_args_no_options():
    """
    Tests the parse_args function when no options are passed
    """
    args = parse_args(['file1', 'file2'])
    
    assert len(args) == 2
    assert not args[0].options
    assert args[0].file == 'file1'
    assert not args[1].options
    assert args[1].file == 'file2'


def test_parse_args_no_files():
    """
    Tests the parse_args function when no files are passed
    """
    args = parse_args(['--option1', '--option2=value'])
    
    assert len(args) == 1
    assert args[0].options[0].name == 'option1'
    assert args[0].options[1].name == 'option2'
    assert args[0].options[1].value == 'value'
    assert not args[0].file


def test_parse_args_no_options_or_files():
    """
    Tests the parse_args function when no options or files are passed
    """
    args = parse_args([])
    
    assert not args


def test_parse_args_file_starts_with_hyphen():

    args = parse_args(['--', '--file1'])
    
    assert len(args) == 1
    assert args[0].file == '--file1'

