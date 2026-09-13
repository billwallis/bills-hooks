# Developing hooks interactively

It is often desirable to test a hook by running it on a separate target repository. The pre-commit documentation has a small section dedicated to this:

- https://pre-commit.com/#developing-hooks-interactively

For example, the local version of this repo could be tested with:

```shell
pre-commit try-repo /path/to/bills-hooks tidy-gitkeep --verbose --all-files
pre-commit try-repo /path/to/bills-hooks gitmoji-conventional-commit --verbose --all-files --hook-stage commit-msg --commit-msg-filename ""
```

...or, using the remote version:

```shell
pre-commit try-repo https://github.com/billwallis/bills-hooks gitmoji-conventional-commit --verbose --all-files --hook-stage commit-msg --commit-msg-filename ""
```

## Temporary pre-commit configuration file

It can be convenient to temporarily write a pre-commit configuration file to run several hooks via pre-commit. The sample below works on POSIX platforms:

```shell
TEST_CONFIG='test.pre-commit-config.yaml'
HEAD_REF=$(git -C '/Users/bill/repos/billwallis/bills-hooks' rev-parse HEAD)

cat >> $TEST_CONFIG << EOF
repos:
  - repo: meta
    hooks:
      - id: identity

  - repo: ../bills-hooks
    rev: $HEAD_REF
    hooks:
      - id: banned-python-code
      - id: check-dbt-project-version
      - id: check-filename-pattern
      - id: check-no-commit-comment
      - id: gitmoji-conventional-commit
      - id: tidy-gitkeep
EOF

pre-commit run --all-files --config "$PWD/$TEST_CONFIG"
```
