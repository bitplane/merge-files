from merge_files.mergers import get


def test_get_env_file():
    merger = get("foo.env", ".env")
    assert merger.__name__ == "env"
