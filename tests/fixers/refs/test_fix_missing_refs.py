"""Tests for ReferenceExpander implementation in fix_refs/fixers/refs/fix_missing_refs.py."""

import json
from pathlib import Path
import pytest

from fix_refs.config import ConfigManager
from fix_refs.fixers.refs.fix_missing_refs import ReferenceExpander, fix_missing_refs


def test_reference_expander_end_to_end(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test the complete real flow of expanding a missing named reference from an MDWiki revision file.

    Flow: REVISIONS_PATH -> ConfigManager -> ReferenceExpander -> get_revision_file_path(1501810)
          -> 1501810/wikitext.txt -> get_full_text() -> refs_expand() -> expanded reference.
    """
    monkeypatch.setenv("REVISIONS_PATH", str(tmp_path))

    rev_dir = tmp_path / "1501810"
    rev_dir.mkdir(parents=True, exist_ok=True)
    rev_file = rev_dir / "wikitext.txt"
    rev_file.write_text("something <ref name=\"AHFS2016\">full ref</ref>", encoding="utf-8")

    config_manager = ConfigManager()
    expander = ReferenceExpander(config_manager)

    input_text = "This Ref tag should be full ref after fix missing references from 1501810/wikitext.txt <ref name=\"AHFS2016\" />"
    result = expander.fix_missing_refs(input_text, "Entecavir", 1501810)

    assert "<ref name=\"AHFS2016\">full ref</ref>" in result
    assert "<ref name=\"AHFS2016\" />" not in result


def test_legacy_fix_missing_refs_wrapper(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test legacy fix_missing_refs wrapper function using REVISIONS_PATH environment variable."""
    monkeypatch.setenv("REVISIONS_PATH", str(tmp_path))

    rev_dir = tmp_path / "1501810"
    rev_dir.mkdir(parents=True, exist_ok=True)
    rev_file = rev_dir / "wikitext.txt"
    rev_file.write_text("something <ref name=\"AHFS2016\">full ref</ref>", encoding="utf-8")

    input_text = "This Ref tag should be full ref after fix missing references from 1501810/wikitext.txt <ref name=\"AHFS2016\" />"
    result = fix_missing_refs(input_text, "Entecavir", 1501810)

    assert "<ref name=\"AHFS2016\">full ref</ref>" in result
    assert "<ref name=\"AHFS2016\" />" not in result


def test_get_full_text_existing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test get_full_text() returns the contents of 1501810/wikitext.txt."""
    monkeypatch.setenv("REVISIONS_PATH", str(tmp_path))

    rev_dir = tmp_path / "1501810"
    rev_dir.mkdir(parents=True, exist_ok=True)
    rev_file = rev_dir / "wikitext.txt"
    expected_content = "something <ref name=\"AHFS2016\">full ref</ref>"
    rev_file.write_text(expected_content, encoding="utf-8")

    config_manager = ConfigManager()
    expander = ReferenceExpander(config_manager)

    full_text = expander.get_full_text("Entecavir", 1501810)
    assert full_text == expected_content


def test_get_full_text_nonexistent(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test get_full_text() returns empty string when revision file does not exist."""
    monkeypatch.setenv("REVISIONS_PATH", str(tmp_path))

    config_manager = ConfigManager()
    expander = ReferenceExpander(config_manager)

    full_text = expander.get_full_text("Entecavir", 9999999)
    assert full_text == ""


def test_get_full_text_revid_zero_json_lookup(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Test get_full_text() with mdwiki_revid=0 uses find_mdwiki_revid() and json_data.json to discover revision."""
    monkeypatch.setenv("REVISIONS_PATH", str(tmp_path))

    json_file = tmp_path / "json_data.json"
    json_file.write_text(json.dumps({"Entecavir": "1501810"}), encoding="utf-8")

    rev_dir = tmp_path / "1501810"
    rev_dir.mkdir(parents=True, exist_ok=True)
    rev_file = rev_dir / "wikitext.txt"
    expected_content = "something <ref name=\"AHFS2016\">full ref</ref>"
    rev_file.write_text(expected_content, encoding="utf-8")

    config_manager = ConfigManager()
    expander = ReferenceExpander(config_manager)

    full_text = expander.get_full_text("Entecavir", 0)
    assert full_text == expected_content
