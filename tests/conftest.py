import pytest
from utils import vcr_kwargs, DEFAULT_OUTPUT_FOLDER


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
