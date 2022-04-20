# Test directory -- file structure

Directories:

1. `cassettes/`: Location of vcrpy and pytest-vcr cassettes.

Files:

1. `conftest.py`: Location of pytest global and configuration fixtures.
2. `utils.py`: Location of global Python helper objects (i.e. constants and `Ozone` instance) to use in tests.
3. `test_*.py`: Test files, each file is testing one public method.
