"""Tests for ConfigManager"""

import json
from pathlib import Path

import pytest
from src.fix_refs.config import ConfigManager

REVID = 1501810
TITLE = "Entecavir"
REVISION_CONTENT = 'something <ref name="AHFS2016">full ref</ref>'


@pytest.fixture
def revisions_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Point REVISIONS_PATH to an empty temp directory."""
    monkeypatch.setenv("REVISIONS_PATH", str(tmp_path))
    return tmp_path


@pytest.fixture
def revision_file(revisions_path: Path) -> Path:
    """Create <REVISIONS_PATH>/1501810/wikitext.txt with the full reference."""
    rev_dir = revisions_path / str(REVID)
    rev_dir.mkdir(parents=True, exist_ok=True)
    rev_file = rev_dir / "wikitext.txt"
    rev_file.write_text(REVISION_CONTENT, encoding="utf-8")
    return rev_file


@pytest.fixture
def write_revision(revisions_path: Path):
    """Factory: write custom wikitext into <REVISIONS_PATH>/1501810/wikitext.txt."""

    def _factory(content: str) -> Path:
        rev_dir = revisions_path / str(REVID)
        rev_dir.mkdir(parents=True, exist_ok=True)
        rev_file = rev_dir / "wikitext.txt"
        rev_file.write_text(content, encoding="utf-8")
        return rev_file

    return _factory


@pytest.fixture
def config() -> ConfigManager:
    """ReferenceExpander built from ConfigManager (reads REVISIONS_PATH)."""
    return ConfigManager.load()


class TestGetFullText:
    """ReferenceExpander.get_full_text()."""

    @pytest.mark.usefixtures("revision_file")
    def test_existing_revision_file(self, config: ConfigManager) -> None:
        full_text = config.get_full_text(TITLE, REVID)

        assert full_text == REVISION_CONTENT

    def test_nonexistent_revision_file(self, config: ConfigManager) -> None:
        full_text = config.get_full_text(TITLE, 9999999)

        assert full_text == ""

    @pytest.mark.usefixtures("revision_file")
    def test_revid_zero_uses_json_lookup(self, revisions_path: Path, config: ConfigManager) -> None:
        """mdwiki_revid=0 -> find_mdwiki_revid() reads json_data.json to discover the revision."""
        json_file = revisions_path / "json_data.json"
        json_file.write_text(json.dumps({TITLE: str(REVID)}), encoding="utf-8")

        full_text = config.get_full_text(TITLE, 0)

        assert full_text == REVISION_CONTENT
