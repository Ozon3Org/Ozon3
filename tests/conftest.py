import pytest
from utils import vcr_kwargs, DEFAULT_OUTPUT_FOLDER


# Pytest configurations. Modified from
# https://docs.pytest.org/en/7.1.x/example/simple.html#control-skipping-of-tests-according-to-command-line-option

# Add option for CLI invocation
def pytest_addoption(parser):
    parser.addoption(
        "--skip-slow", action="store_true", default=False, help="skip slow tests"
    )


# Register pytest.mark.slow
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: mark test as slow to run")


# Run slow tests unless --skip_slow is given
def pytest_collection_modifyitems(config, items):
    if config.getoption("--skip-slow"):
        skip_slow = pytest.mark.skip(reason="skipped due to --skip-slow")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)


# Configuration fixture for pytest-vcr
@pytest.fixture(scope="session")
def vcr_config():
    return vcr_kwargs


# Automatically use this fixture for each test
# to clean up the output directory
@pytest.fixture(autouse=True)
def cleanup_output():
    if DEFAULT_OUTPUT_FOLDER.exists():
        for file in DEFAULT_OUTPUT_FOLDER.iterdir():
            file.unlink()
        DEFAULT_OUTPUT_FOLDER.rmdir()
    yield
    if DEFAULT_OUTPUT_FOLDER.exists():
        for file in DEFAULT_OUTPUT_FOLDER.iterdir():
            file.unlink()
        DEFAULT_OUTPUT_FOLDER.rmdir()
