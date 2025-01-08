"""
Unit tests for the ``bills_hooks.gitmoji_conventional_commit._dev`` module.
"""

import pathlib
import textwrap

import pytest

import bills_hooks.gitmoji_conventional_commit._dev as dev


@pytest.fixture
def gitmojis_json() -> str:
    """
    A JSON object corresponding to the gitmojis.
    """
    return textwrap.dedent(
        """
        {
          "$schema": "https://gitmoji.dev/api/gitmojis/schema",
          "gitmojis": [
            {
              "emoji": "🎨",
              "code": ":art:",
              "description": "Improving structure / format of the code."
            },
            {
              "emoji": "⚡️",
              "code": ":zap:",
              "description": "Improving performance."
            }
          ]
        }
        """
    )


@pytest.fixture
def gitmojis_yaml() -> str:
    """
    A YAML object corresponding to the gitmojis.
    """
    return textwrap.dedent(
        """
        $schema: https://gitmoji.dev/api/gitmojis/schema
        gitmojis:
        - code: ':art:'
          description: Improving structure / format of the code.
          emoji: 🎨
        - code: ':zap:'
          description: Improving performance.
          emoji: ⚡️
        """
    )


@pytest.fixture
def gitmojis_url(tmp_path: pathlib.Path, gitmojis_json: str) -> str:
    """
    The URL for the gitmojis.
    """
    url = tmp_path / "gitmojis.json"
    url.write_text(gitmojis_json, encoding="utf-8")

    return url.as_uri()


def test__collect_gitmoji(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: pathlib.Path,
    gitmojis_url: str,
    gitmojis_yaml: str,
) -> None:
    """
    Test the ``collect_gitmoji`` function.
    """
    monkeypatch.setattr(dev, "GITMOJIS_URL", gitmojis_url)
    monkeypatch.setattr(dev, "SOURCE_ROOT", tmp_path)

    expected = tmp_path / "gitmoji_conventional_commit/gitmojis.yaml"
    # Ensure the parent directory exists otherwise write will fail
    expected.parent.mkdir(parents=True, exist_ok=True)

    dev.collect_gitmoji()

    assert expected.exists()
    assert expected.read_text(encoding="utf-8").strip() == gitmojis_yaml.strip()
