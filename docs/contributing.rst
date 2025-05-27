Contributing
============

Thank you for your interest in contributing to **andebox**!

andebox is a CLI tool to assist Ansible developers by encapsulating common tasks such as running `ansible-test`, managing tox environments, and more. We welcome contributions of all kinds: bug reports, feature requests, code, tests, and documentation.

Project Philosophy
------------------
- Focus on developer experience and automation for Ansible module and collection development.
- Prioritize code quality, maintainability, and clear documentation.
- Follow best practices for Python and Ansible development.

How to Contribute
-----------------
1. **Check open issues and discussions**: Your idea or bug may already be tracked.
2. **Open a new issue**: If your contribution is new, please open an issue to discuss it before submitting a pull request (PR).
3. **Fork the repository** and create a feature branch for your work.
4. **Write clear, maintainable code**: Follow the code style and conventions described below.
5. **Add or update tests**: All new features and bug fixes should include tests.
6. **Document your changes**: Update or add documentation as needed.
7. **Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for your commit messages**. This project uses [semantic-release](https://semantic-release.gitbook.io/) to automate versioning and changelogs based on commit messages.
8. **Submit a pull request**: Reference the relevant issue(s) and describe your changes clearly.

Development Setup
-----------------
- **Python 3.11+** is required.
- This project uses [tox](https://tox.readthedocs.io/) for all development tasks (testing, linting, docs, etc).
- **VS Code Dev Container**: This repository includes a [Dev Container](https://code.visualstudio.com/docs/devcontainers/containers) configuration. It is highly recommended to use it for development, as it provides a pre-configured environment with all necessary tools and dependencies.
- Install tox if you don't have it:

  .. code-block:: shell

     pip install tox

- To run all checks (lint, tests):

  .. code-block:: shell

     tox

- To run tests for a specific Python version (e.g., 3.13):

  .. code-block:: shell

     tox -e py313
     tox -e py   # for the current Python version

- To build the documentation:

  .. code-block:: shell

     tox -e docs

- To update dependencies (requires git access):

  .. code-block:: shell

     tox -e deps

- Pre-commit hooks are recommended. Assuming you already have ``pre-commit`` installed, install the hooks with:

  .. code-block:: shell

     pre-commit install --install-hooks

Code Style
----------
- Code must be formatted with **black** and pass **flake8** and **pylint** checks (run as part of the default tox run).
- Use type annotations where possible.
- Keep code readable and avoid unnecessary comments.
- Follow the conventions already present in the codebase.

Testing
-------
- Tests are written with **pytest**.
- Run tests with:

  .. code-block:: shell

     tox
     # or for a specific Python version:
     tox -e py311

- Coverage is measured with **pytest-cov**. Aim for high coverage.
- If your nwly written test is very slow (minutes to run), mark it with ``@pytest.mark.slow``. These "slow" tests will not be part of
  the regular test run, but there is a weekly GHA workflow that will run all tests including the slow ones.

Documentation
-------------
- Documentation is in reStructuredText and built with **Sphinx**.
- To build the docs locally:

  .. code-block:: shell

     tox -e docs

- Add or update docstrings and user documentation as needed.

Pull Requests
-------------
- Reference related issues in your PR description.
- Ensure your branch is up to date with `main` before submitting.
- All checks (lint, tests, docs) must pass in CI before merge.
- **Use conventional commit messages** (see above). PRs that do not follow this may be asked to reword commits.
- Versioning and changelogs are managed automatically by semantic-release based on your commit messages.

Reporting Issues
----------------
- Use the [GitHub issue tracker](https://github.com/russoz-ansible/andebox/issues) for bugs, feature requests, and questions.
- Provide as much detail as possible, including steps to reproduce, environment, and version info.

License and Copyright
---------------------
- All contributions are licensed under the MIT License (see LICENSES/MIT.txt).
- Please include the appropriate SPDX headers in new files.

Thank you for helping make andebox better!
