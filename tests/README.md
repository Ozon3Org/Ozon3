# Test directory -- file structure

Directories:

1. `cassettes/`: Location of vcrpy and pytest-recording cassettes.

Files:

1. `conftest.py`: Location of pytest global and configuration fixtures.
2. `utils.py`: Location of global Python helper objects (i.e. constants and `Ozone` instance) to use in tests.
3. `test_*.py`: Test files, each file is testing one public method.

# Setting up and running tests

After setting development environment as pointed out in CONTRIBUTING.md, you should already have all necessary testing packages installed. To run all tests, invoke this command from the root directory.

```sh
pytest
```

# Updating tests

Generally, tests should correspond to the necessary specification/expectation of Ozone users. Tests will help us identify if our code is still in line with such expectations.

Tests should be updated when e.g.:
- There is a new functionality. In this case, add necessary tests accordingly.
- There is a change in existing functionality that is in line with the expectation of Ozone users. In this case, the tests become outdated and need to be updated.
- There is a new bug or previously unencountered or undocumented behavior. Add them to the existing tests to make sure the same bug will never slip past again in the future.

# About the cassettes and pytest-recording

This test suite is testing Ozone's functionality, so interaction with outside sources need to be mocked. Ozone uses pytest-recording plugin that uses vcrpy under the hood to record request-response pairs. These request-response pairs are stored as `.yaml` files in `tests/cassettes` directory.

The `test/cassettes` directory is organized as follows:

- Each folder per one test file.
- Each `.yaml` file per one test function.

For the purposes of this test suite, these request-response pairs are **assumed** to be all correct. In the event that WAQI API changes their specifications (unlikely), these request-response pairs need to be re-recorded. See the next section.

# Adding or updating cassettes

By default, pytest-recording will only use existing cassettes for testing, and will raise error if there's a new interaction that is not contained in existing cassettes. This prevents "accidentally" making a request that is not already been mocked.

This default behavior can be overridden by giving a `record-mode` argument when invoking `pytest`:

- `pytest --record-mode=once` to write new cassettes but not new request-response pairs within existing cassettes.
- `pytest --record-mode=new_episodes` to write new interactions, even when there's an existing cassette.
- `pytest --record-mode=rewrite` to rewrite all existing cassettes.
- `pytest --record-mode=all` to record all interactions again.
- `pytest --record-mode=none`(default) to only use existing cassettes and raise error if there's a new request that is not recorded in the existing cassettes.

> To have more confidence that the tests will not go over the wire, the `--block-network` flag can also be passed to block all network access.

For more information about pytest-recording:
- [pytest-recording homepage](https://github.com/kiwicom/pytest-recording)
- [VCRpy documentation about record modes](https://vcrpy.readthedocs.io/en/latest/usage.html#record-modes)
