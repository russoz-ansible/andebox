# andebox

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Project Does

**Andebox** (Ansible Developer Toolbox) is a CLI utility that helps Ansible developers run tests (sanity, unit, integration) from collection root directories without complex setup. It wraps `ansible-test`, `tox`, and `vagrant` with automatic environment and directory management.
It also provides other tools supporting develoment of Ansible collections.

## Commands

All commands use Poetry or poe (poethepoet):

```bash
# Install dependencies
poetry install --with dev

# Lint
poetry run ruff check .

# Format
poetry run ruff format .

# Run all QA checks (lint + format check + tests)
poe qa

# Run all tests with coverage
poetry run pytest -v --cov --cov-branch

# Run a single test file
poetry run pytest tests/test_action_ignorefile.py -v

# Run a single test by name
poetry run pytest tests/test_action_ignorefile.py::TestClassName::test_method -v

# Build docs
poe docs
```

Poe tasks: `test`, `lint`, `fmt`, `check` (lint+format check), `qa` (check+test), `docs`, `deps`.

## Architecture

### Plugin System

`cli.py` dynamically discovers action modules from `actions/` and registers any module that exposes `app = typer.Typer(...)`. Each action is a standalone module that:

- Creates a `typer.Typer` app with `name` and `help`
- Defines command functions decorated with `@app.callback(invoke_without_command=True)`
- Receives context via `typer.Context` (global options like `--collection` and `--venv` in `ctx.obj`)

### Context Abstraction

[andebox/context.py](andebox/context.py) auto-detects whether you're in an Ansible collection or Ansible core repo by searching for `meta/runtime.yml` (collection) or `bin/ansible-playbook` (core). The context handles:

- Locating the project root
- Creating temp directories with the right structure for `ansible-test`
- Setting environment variables
- Copying files into the temp tree

All actions receive a context object — they never manage directory structure themselves.

### Key Actions

| File | Purpose |
| ---- | ------- |
| `actions/ansibletest.py` | Wraps `ansible-test sanity/units/integration` |
| `actions/toxtest.py` | Runs tests via tox |
| `actions/vagrant.py` | Runs tests in Vagrant VMs (uses fabric for SSH) |
| `actions/ignorefile.py` | Parses and analyzes `ansible-test` ignore files |
| `actions/runtime.py` | Queries `meta/runtime.yml` status |
| `actions/yaml_doc.py` | YAML documentation handling |
| `actions/docsite.py` | Builds documentation via `antsibull-docs` |

### Entry Point

`python -m andebox` → `__main__.py` → `cli.py:run()` → typer `app()` → dispatches to registered action sub-app.

## Testing

Tests live in `tests/`. Each action has a corresponding test file. `tests/conftest.py` has shared fixtures; `tests/utils.py` has helpers.

Coverage artifacts go to `htmlcov/` (HTML) and `junit.xml`.

## Code Style

- Formatter + Linter + Import sorter: **ruff**
- Pre-commit hooks are configured — run `pre-commit install` after cloning.
