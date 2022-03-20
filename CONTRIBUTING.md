# Contributing to Ozone

:tada::+1: First off, thanks for taking the time to contribute! :tada::+1:

It might not be obvious but we appreciate all forms of contribution.

The following is a set of guidelines for contributing to [Ozone](https://github.com/Milind220/Ozone). These are mostly guidelines, not rules. Use your best judgment. Feel free to propose changes to this document in a pull request.

> **Important note:** Make sure you make PRs to `dev` branch, not `main`. See [below](#making-a-pull-request) for more information.

#### Table of Contents

- [How Can I Contribute?](#how-can-i-contribute)

  - [Reporting bugs](#reporting-bugs)
  - [Suggesting enhancements/features](#suggesting-enhancements/features)
  - [Making a pull request](#making-a-pull-request)
  - [Get an issue assigned to you](#get-an-issue-assigned-to-you)

- [Setting Up Local Development Environment](#setting-up-local-development-environment)

  - [Getting a local copy](#getting-a-local-copy)
  - [Setting up a development environment](#setting-up-a-development-environment)
  - [Pushing changes and opening a pull request](#pushing-changes-and-opening-a-pull-request)

- [Style Guides](#style-guides)

  - [Commit message style guide](#git-commit-messages)
  - [Python style guide](#python-style-guide)

- [Github Branching Model](#github-branching-model)



## How Can I Contribute?

### Reporting bugs

1. Before submitting a bug report, make sure to do a cursory search on [issues](https://github.com/Milind220/Ozone/issues) to see if it's already reported. If it's already reported, add a comment under the issue thread instead of opening a new one.

2. Use clear and descriptive title.

3. Include in the body of the issue:

   - **Expected behavior**: What do you expect should happen?
   - **Actual behavior**: What actually happened and why it's a problem?
   - **Steps to reproduce the problem**. Be very specific. Give example code block. Other contributors want to run it in their device to make sure they see what you saw. Having detailed steps and examples can make it easier to demonstrate and track down a problem.
   - **Version information**: What version of Python you're using? What version of Ozone? Do you install through `pip` or by cloning the Github repository? What is your OS and what version?

   You can include screenshots/GIFs, if relevant.

Additionally, you can also confirm other people's bug report by running their provided code and steps in your local machine and see if the same problem shows up. Every test helps, especially if your device setup is different (i.e. has different OS or Python version) from the original bug report.

### Suggesting enhancements/features

1. Before submitting a feature suggestion,  make sure to do a cursory search in [issues](https://github.com/Milind220/Ozone/issues) to see if it's already suggested.

2. Use clear and descriptive title.

3. Lay out the details of your suggestion in the body issue. Make sure to also:

   - Describe the current behavior and explain what would you like to see instead.
   - Explain why your suggestion would be useful for Ozone users.

### Making a pull request

You can also make a pull request to fix an existing bug or add a feature.

Unsure where to begin contributing to Ozone? You can start by looking through these  `first-contribution`, `beginner`, `help-wanted` issues:

* `first-contribution` issues should only require a few lines of code or are improvements on the documentation.
* `beginner` issues are a step up, and may involve a couple of methods/tests.
* `help-wanted` issues are slightly trickier.

One very important thing is to make sure you only make PR's to the `dev` branch and not the `main` branch. The main branch is stable, and `dev` branch changes will be merged into `main` periodically once it's confirmed that they don't have any breaking changes.

### Get an issue assigned to you

If you find an issue that you'd like to tackle - get it assigned to yourself by commenting on it with:

```
Hold my beer, I got this
```

## Setting Up Local Development Environment

### Getting a local copy

1. Fork this repository.

2. Clone your fork to your local device.

3. Set your fork as `origin` remote. This is usually done automatically if you're using `git clone` command. To do it manually:

   ```sh
   git remote add origin URL_OF_YOUR_FORK
   ```

4. Set original repository as `upstream` remote.

   ```sh
   git remote add upstream https://github.com/Milind220/Ozone.git
   ```

5. Pull from original repository to make sure you're synced up.

   ```sh
   git pull upstream dev:dev
   ```

   You may want to do it once in a long while to make sure your local dev branch is in sync with the `upstream` remote.

6. Checkout the `dev` branch, and make a new branch from there to make changes.

   ```sh
   git checkout dev
   git checkout -b my-feature-branch
   ```

### Setting up a development environment

1. Create and activate a virtual environment.

   e.g. using Python's built-in `venv` module:

   ```sh
   python -m venv venv
   venv/scripts/activate
   ```

2. Within the virtual environment, install the requirements. Afterwards, install the package in editable mode.

   ```sh
   pip install -r requirements.txt
   pip install -e .
   ```

3. Activate pre-commit hooks.

   ```sh
   pre-commit install
   ```

   From this point on, pre-commit hooks will run linters and formatters automatically before every commit. If there's a problem, the commit will abort. You'll need to fix the problem before committing again.

4. Your local development environment is ready to use. Feel free to code away. Make sure to only commit logical changes that are already tested. Don't commit things you just try out and haven't tested.

5. When you're done coding, again, **test out the changes that you've made to the package.** Proceed if all is good.

### Pushing changes and opening a pull request

1. Push the changes to your forked repository.

2. Return to your forked repository on Github and click on `compare and pull request` to begin the PR. **Make sure the base branch is `dev`, not `main`.**

3. Describe your PR, submit it and wait for it to be merged! You may be required to do additional work or changes before it is merged.



## Style Guides

### Git commit messages

Commmits should be made in this format:

```
<type>[optional scope]: <description>

<optional detailed description>
```

* fix: To show that a bug fix or patch has been made
* feat: To show that a new feature/enhancement has been added
* BREAKING CHANGE: For changes that introduce backwards-incompatible updates
* refactor: If you've rearranged/refactored existing code by splitting it into seperate files/methods/functions/classes
* test: Any modification of tests
* ci/cd: Any addition of continuous integration/deployement tasks, such as GitHub actions
* chore: Things like version bumps, change in dependencies etc. Behind the scenes stuff that doesn't affect the API
* docs: For entirely documentation related changes. README, CONTRIBUTING, CODE_OF_CONDUCT, and even docstrings in methods, all come under this
* style: If your commit is solely to do with things like spaces instead of tabs, or " instead of '. This can be used if you've formatted code with black/flake8 and wish to make a commit

> **Note:** The above guidelines were added on 8th Mar, 2022. All commits before this time do not have these prefixes.

Here are a few other tips:

* Use the present tense ("Add feature" not "Added feature").
* Limit the first line to 72 characters or less.
* Add descriptions where needed, to explain your commit in more detail.

### Python style guide

* Follow the [pep8](https://www.python.org/dev/peps/pep-0008/) styleguide.
* Format with flake8 and black.
* Add docstrings with formats as shown in existing code.



## Github Branching Model

Ozone branches are created using a Github branching model. In this branching model, each branch serves a purpose and offers team members a shared undestanding  of the branching system.

See more information on this branching model [here](https://github.com/Milind220/Ozone/discussions/24).
