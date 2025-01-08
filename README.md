<div align="center">

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![tests](https://github.com/Bilbottom/bills-hooks/actions/workflows/tests.yaml/badge.svg)](https://github.com/Bilbottom/bills-hooks/actions/workflows/tests.yaml)
[![coverage](coverage.svg)](https://github.com/dbrgn/coverage-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/Bilbottom/bills-hooks)

[![code style: prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg?style=flat-square)](https://github.com/prettier/prettier)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Bilbottom/bills-hooks/main.svg)](https://results.pre-commit.ci/latest/github/Bilbottom/bills-hooks/main)

</div>

---

# Bill's Hooks

Pre-commit hooks for my own projects.

## Usage

Add the following hook to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/Bilbottom/bills-hooks
  rev: v0.0.1
  hooks:
    - id: gitmoji-conventional-commit
```

## Available Hooks

### `gitmoji-conventional-commit` ([source](bills_hooks/gitmoji_conventional_commit/hook.py))

> [!WARNING]
>
> This is still in development and does not validate the commit message against the conventional commit framework yet.

This hook checks that your commit messages are (optionally) prefixed with a [gitmoji](https://gitmoji.dev/) and follow the [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) format.

Inspired by:

- https://github.com/compilerla/conventional-pre-commit
