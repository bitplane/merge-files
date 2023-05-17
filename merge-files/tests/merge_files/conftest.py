from pytest import fixture


@fixture(scope="session", autouse=True)
def setup_logging():
    """
    Sets up the logging for the application
    """
    from merge_files.utils.logging import setup

    setup()
