<div align="center">

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![tests](https://github.com/billwallis/bills-hooks/actions/workflows/tests.yaml/badge.svg)](https://github.com/billwallis/bills-hooks/actions/workflows/tests.yaml)
[![coverage](coverage.svg)](https://github.com/dbrgn/coverage-badge)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/billwallis/bills-hooks/main.svg)](https://results.pre-commit.ci/latest/github/billwallis/bills-hooks/main)
[![GitHub last commit](https://img.shields.io/github/last-commit/billwallis/bills-hooks)](https://shields.io/badges/git-hub-last-commit)

</div>

---

# Bill's Hooks

Pre-commit hooks for my own projects.

## Usage

Add the following hooks to your `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/billwallis/bills-hooks
  rev: v0.0.8
  hooks:
    - id: check-filename-pattern
      args: ["--regex", "<some-regex-pattern>"]
    - id: gitmoji-conventional-commit # warning: still in development
    - id: tidy-gitkeep
```

## Available Hooks

### `check-filename-pattern` ([source](bills_hooks/check_filename_pattern/hook.py))

This hook checks filenames against a given pattern.

Specify the regular expression pattern with the `--regex` argument. Optionally use the `--name-only` flag to just match against file name (including extension).

This is useful for, say, checking that all files in a directory follow a given pattern. For example, all Python test files in the `tests/` directory start with `test_`:

```yaml
hooks:
  - id: check-filename-pattern
    files: '^tests/.*\.py$'
    exclude: '^.*/(conftest\.py|__init__\.py)$'
    args: ["--name-only", "--regex", '^test_.*\.py$']
```

### `gitmoji-conventional-commit` ([source](bills_hooks/gitmoji_conventional_commit/hook.py))

> [!WARNING]
>
> This is still in development and does not validate the commit message against the conventional commit framework yet.

This hook checks that your commit messages are (optionally) prefixed with a [gitmoji](https://gitmoji.dev/) and follow the [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) format.

Inspired by:

- https://github.com/compilerla/conventional-pre-commit

### `tidy-gitkeep` ([source](bills_hooks/tidy_gitkeep/hook.py))

This hook removes redundant `.gitkeep` files from your repository.

A `.gitkeep` file is redundant if the directory it is in has any other files that are not ignored by git. The non-ignored files can be in the same directory or in subdirectories.

This can also be run as a CLI:

```shell
uvx --from 'git+https://github.com/billwallis/bills-hooks' tidy-gitkeep .
```

## Contributing

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and then install the dependencies:

```bash
uvx --from poethepoet poe install
```
