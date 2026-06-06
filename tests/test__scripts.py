"""
Test that the scripts are registered.
"""

import shlex
import subprocess
import textwrap


def run(cmd: str) -> tuple[int, str, str]:
    proc = subprocess.run(
        args=shlex.split(cmd),
        check=False,
        capture_output=True,
    )

    assert isinstance(proc.stdout, bytes)
    assert isinstance(proc.stderr, bytes)

    return (
        proc.returncode,
        proc.stdout.decode(encoding="utf-8"),
        proc.stderr.decode(encoding="utf-8"),
    )


def test__banned_python_code():
    rc, _, _ = run("banned-python-code --help")
    assert rc == 0


def test__check_dbt_project_version_warning():
    rc, out, err = run("_check-dbt-project-version-warning --help")
    assert rc == 1
    # TODO: Shouldn't this be in stderr?
    assert out == textwrap.dedent(
        """\
        \x1b[1;31mThis hook must be used in a `local` repo.\x1b[0m

        Install the repo and add the following hook configuration for
        this hook instead:

          - repo: local
            hooks:
              - id: check-dbt-project-version
                name: Check dbt project version
                entry: >
                  check-dbt-project-version
                  --dbt-project-dir '<dbt_project.yml directory>'
                  --python-project-name '<target repo name>'
                language: unsupported
                always_run: true
                pass_filenames: false

        """
    )
    assert err == ""


def test__check_dbt_project_version():
    rc, _, _ = run("check-dbt-project-version --help")
    assert rc == 0


def test__check_filename_pattern():
    rc, _, _ = run("check-filename-pattern --help")
    assert rc == 0


def test__check_no_commit_comment():
    rc, _, _ = run("check-no-commit-comment --help")
    assert rc == 0


def test__gitmoji_conventional_commit():
    rc, _, _ = run("gitmoji-conventional-commit --help")
    assert rc == 0


def test__tidy_gitkeep():
    rc, _, _ = run("tidy-gitkeep --help")
    assert rc == 0
