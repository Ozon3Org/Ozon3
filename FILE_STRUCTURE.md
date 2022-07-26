# File Structure
This document is a reference primer on Ozon3's files: what, where, and for what.

- [src/](#src)
  - [media/](#media)
  - [ozon3/](#ozon3)
    - [ozon3.py](#ozon3py)
    - [urls.py](#urlspy)
    - [historical/](#historical)
      - [relevant_funcs.py](#relevant_funcspy)
      - [_reverse_engineered.py](#_reverse_engineeredpy)
- [tests/](#tests)
  - [cassettes/](#cassettes)
  - [conftest.py](#conftestpy)
  - [test_*.py](#test_py)
  - [utils.py](#utilspy)
- [.pre-commit-config.yaml](#pre-commit-configyaml)
- [pyproject.toml, setup.py, and setup.cfg](#pyprojecttoml-setuppy-and-setupcfg)
- [requirements.txt](#requirementstxt)
- [.github/](#github)
  - [ISSUE_TEMPLATE/](#issue_template)
  - [workflows/](#workflows)
    - [lint.yml](#lintyml)
    - [package-publish.yml](#package-publishyml)
    - [take.yml](#takeyml)

## src/

This is the directory where main Ozon3 source code lives.

### media/

This subdirectory contains media related to Ozon3's documentation (README). Included here are demo GIFs and Ozon3 logo.

### ozon3/

This module is where core Ozon3 code lives.

#### ozon3.py

Main module that contains Ozon3's class definition.

#### urls.py

Helper module that contains definitions for WAQI API's URL endpoints.

#### historical/

This subfolder contains Python code relevant for historical data collection feature. It's mostly hack-ish and reverse-engineered from AQI's frontend website.

##### relevant_funcs.py

This file contains relevant JavaScript functions wrapped as one long triple-quoted Python string. These JavaScript functions are excerpted from AQI's frontend and are treated as black box that can convert server-sent data into readable format.

##### _reverse_engineered.py

This file contains most of code required to run the JavaScript functions and convert the result back into Python format that can be used by the rest of Ozon3.

## tests/

This is where the test suite lives.

### cassettes/

This folder is where VCR.py cassettes are stored. Each folder here corresponds to one test file. Each file in each folder corresponds to one test function.

### conftest.py

Pytest global and configuration fixtures are defined here.

### test_*.py

These are test files. One test file is responsible for testing one of Ozon3's public method.

### utils.py

Constants and objects that are used repeatedly throughout the entire test suite are defined here instead of in each file, to reduce repetitions and make it easier to change things if necessary.

## .pre-commit-config.yaml

Configuration file for pre-commit hooks. Specifies what pre-commit hooks to use, from which repository, and what version.

## pyproject.toml, setup.py, and setup.cfg

Files used for purposes of packaging and installation. Also contains package information for use in PyPI like version information, author name, PyPI category tags, etc.

## requirements.txt

Dependency requirement file for development. Non-developing users won't need to install packages in this file, as the installation process will install the user requirements automatically.

## .github/

This folder is related to GitHub repository and not necessarily part of Ozon3 package.

### ISSUE_TEMPLATE/

Files in this folder are templates meant for newly opened issues.

### workflows/

This folder contains configuration files for running GitHub actions and workflows, including CI/CD tools.

#### lint.yml

CI/CD tool: linter and style checker.

#### package-publish.yml

CI/CD tool: package and publish a release for each tags.

#### take.yml

GitHub workflow: allow users to claim an issue and get it assigned to themselves without maintainers having to explicitly perform the assigning.
