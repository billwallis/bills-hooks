import importlib.metadata
import pathlib

import pytest

from bills_hooks.check_dbt_project_version import hook


def test__hook_warning_can_be_printed(
    capsys: pytest.CaptureFixture,
):
    ret = hook.warn()
    out, err = capsys.readouterr()

    assert ret == 1
    assert err == ""
    assert "This hook must be used in a `local` repo." in out


def test__hook_succeeds_when_versions_match(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
):
    version = "1.2.3"
    with open(tmp_path / "dbt_project.yml", "w+") as f:
        f.write(f"version: {version}")
    monkeypatch.setattr(importlib.metadata, "version", lambda _: version)

    ret = hook.main(
        [
            *("--dbt-project-dir", str(tmp_path)),
            *("--python-project-name", "foo"),
        ]
    )

    assert ret == 0


def test__hook_fails_when_versions_do_not_match(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
):
    with open(tmp_path / "dbt_project.yml", "w+", encoding="utf-8") as f:
        f.write("version: 1.2.3  # 🤓")
    monkeypatch.setattr(importlib.metadata, "version", lambda _: "0.0.0")

    ret = hook.main(
        [
            *("--dbt-project-dir", str(tmp_path)),
            *("--python-project-name", "foo"),
        ]
    )

    assert ret == 1


def test__hook_fails_when_package_name_is_not_found(
    tmp_path: pathlib.Path,
    monkeypatch: pytest.MonkeyPatch,
):
    with open(tmp_path / "dbt_project.yml", "w+") as f:
        f.write("version: 1.2.3")

    ret = hook.main(
        [
            *("--dbt-project-dir", str(tmp_path)),
            *("--python-project-name", "foo"),
        ]
    )

    assert ret == 1
