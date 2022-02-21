# Contributing to Ozon3

:tada::+1: First off, thanks for taking the time to contribute! :tada::+1:

The following is a set of guidelines for contributing to [Ozon3](https://github.com/Milind220/Ozone). These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

#### Table Of Contents

[I don't want to read this whole thing, I just have a question!!!](#i-dont-want-to-read-this-whole-thing-i-just-have-a-question)

[What should I know before I get started?](#what-should-i-know-before-i-get-started)
  * [File Structure](#file-structure)

[How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Suggesting Enhancements or Feature](#suggesting-enhancements-or-features)
  * [Your First Code Contribution](#your-first-code-contribution)
  * [Pull Requests](#pull-requests)

[Styleguides](#styleguides)
  * [Git Commit Messages](#git-commit-messages)
  * [Python Styleguide](#python-styleguide)

## I don't want to read this whole thing I just have a question!!!

> **Note:** Please don't file an issue to ask a question. Search for your question in issues and see if it's already been answered. 

## What should I know before I get started?

### File Structure
Ozon3 is currently an extremely simple package.
* The package itself is in the ```src/ozone``` directory.
* [ozone.py](https://github.com/Milind220/Ozone/tree/main/src/ozone/ozone.py) contains the Ozone class that does most of the fetching of the data.
* [urls.py](https://github.com/Milind220/Ozone/tree/main/src/ozone/urls.py) contains a URLs class with the API endpoints and base urls.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check [this list](#before-submitting-a-bug-report) as you might find out that you don't need to create one. When you are creating a bug report, please [include as many details as possible](#how-do-i-submit-a-good-bug-report).

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

#### Before Submitting A Bug Report

* **Perform a [cursory search](https://github.com/Milind220/Ozone/issues)** to see if the problem has already been reported. If it has **and the issue is still open**, add a comment to the existing issue instead of opening a new one.

#### How Do I Submit A (Good) Bug Report?
Bugs are tracked as [GitHub issues](https://guides.github.com/features/issues/).

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the steps which reproduce the problem** in as many details as possible.
* **Provide specific examples to demonstrate the steps**. Include links to files or GitHub projects, or copy/pasteable snippets. If you're providing snippets in the issue, use [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the behavior you observed after following the steps** and point out the problem with that behavior. **Explain which behavior you expected to see instead and why.**
* Feel free to **include screenshots / animated GIFs** to clearly demonstrate the problem. 
* **If the problem wasn't triggered by a specific action**, describe what you were doing before the problem happened and share more information using the guidelines below.

Consider providing additional context by answering these questions:

* **Did the problem start happening recently** (e.g. after updating to a new version of Ozon3) or was this always a problem?
* **Can you reliably reproduce the issue?** If not, provide details about how often the problem happens and under which conditions it normally happens.
* **Which version of Ozon3 are you using?**

### Suggesting Enhancements or Features

This section guides you through submitting an enhancement/feature suggestion for Ozon3.



#### Before Submitting An Enhancement Suggestion

Please check the [issues](https://github.com/Milind220/Ozone/issues) list, as you may find that it's already been suggested. When you are creating an enhancement suggestion.

#### How Do I Submit A (Good) Enhancement/Feature Suggestion?

Enhancement/feature suggestions are tracked as [GitHub issues](https://guides.github.com/features/issues/).

* **Use a clear and descriptive title** for the issue to identify the suggestion/feature. Explain the idea well in the description.
* **Describe the current behavior** and **which behavior you expected to see instead**.
* **Explain why this enhancement would be useful** to most Ozon3 users.

### Your First Code Contribution

Unsure where to begin contributing to Atom? You can start by looking through these  `first-contribution`, `beginner`, `help-wanted` issues:

* `first-contribution`  should only require a few lines of code. Or are improvements are documentation.
* `beginner` issues are a step up, and may involve a couple of methods/tests.
* `help-wanted` issues are slightly trickier and require more code and logic.

### Pull Requests (PR's)

Here's how you can get started:

_SETUP_
1. **Switch to the dev branch** of the Github repository. This is where all pre-release changes and additions are made. 
2. **Fork the dev branch**. This creates your own personal copy of the project, which you access through your Github profile.
3. **Clone your forked project**. This creates a copy on your computer where you can make all your changes.
4. **Set your fork as the 'origin' remote** with `git remote add origin URL_OF_YOUR_FORK`.
5. **Set the original project url as the 'upstream' remote** with `git remote add upstream https://github.com/Milind220/Ozone.git`. 
6. **Pull from the original project's dev branch to make sure you're synced up** before you make your own changes. `git pull upstream dev`. Then switch to the dev branch on your computer with `git checkout dev`.
7. Whoohoo! You can now make changes to the code!
8. **Make sure to commit logical changes only**. Don't commit things that you're trying out and haven't tested.
9. When you're done, **test out the changes that you've made to the package.** Proceed if all's good.
10. **Push the changes to your forked repository**. 
11. Return to your forked repo on Github and click on `compare and pull request` to begin the PR.
12. Describe your PR, Submit it and wait for it to be merged! 


#### Also
* Follow the [styleguides](#styleguides)
* Write a detailed pull request (PR)

You may have to complete additional work, tests, or other changes before your pull request is accepted.

#### :tada::+1: _CONGRATULATIONS YOU MADE A PULL REQUEST_ :tada::+1: 

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Limit the first line to 72 characters or less
* When only changing documentation, include `[Doc]` in the commit title
* When making a bugfix, include [BugFix] in commit title.
* Try and add descriptions where needed.

### Python Styleguide
* Follow the [pep8](https://www.python.org/dev/peps/pep-0008/) styleguide
* Format with flake8 and black
* Add docstrings as shown in existing code
