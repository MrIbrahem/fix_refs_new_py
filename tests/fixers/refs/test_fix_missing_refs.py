"""Tests for ReferenceExpander implementation in fix_refs/fixers/refs/fix_missing_refs.py."""

import json
from pathlib import Path

import pytest

from src.fix_refs.config import ConfigManager
from src.fix_refs.fixers.refs.fix_missing_refs import ReferenceExpander

REVID = 1501810
TITLE = "Entecavir"
REVISION_CONTENT = 'something <ref name="AHFS2016">full ref</ref>'
INPUT_TEXT = (
    'This Ref tag should be full ref after fix missing references from 1501810/wikitext.txt <ref name="AHFS2016" />'
)
EXPANDED_REF = '<ref name="AHFS2016">full ref</ref>'
SHORT_REF = '<ref name="AHFS2016" />'


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
def expander(revisions_path: Path) -> ReferenceExpander:
    """ReferenceExpander built from ConfigManager (reads REVISIONS_PATH)."""
    return ReferenceExpander(ConfigManager())


class TestReferenceExpander:
    """ReferenceExpander.fix_missing_refs() full flow.

    Flow: REVISIONS_PATH -> ConfigManager -> ReferenceExpander -> get_revision_file_path(1501810)
          -> 1501810/wikitext.txt -> get_full_text() -> refs_expand() -> expanded reference.
    """

    @pytest.mark.usefixtures("revision_file")
    def test_expands_missing_named_ref(self, expander: ReferenceExpander) -> None:
        result = expander.fix_missing_refs(INPUT_TEXT, TITLE, REVID)

        assert EXPANDED_REF in result
        assert SHORT_REF not in result


class TestGetFullText:
    """ReferenceExpander.get_full_text()."""

    @pytest.mark.usefixtures("revision_file")
    def test_existing_revision_file(self, expander: ReferenceExpander) -> None:
        full_text = expander.get_full_text(TITLE, REVID)

        assert full_text == REVISION_CONTENT

    def test_nonexistent_revision_file(self, expander: ReferenceExpander) -> None:
        full_text = expander.get_full_text(TITLE, 9999999)

        assert full_text == ""

    @pytest.mark.usefixtures("revision_file")
    def test_revid_zero_uses_json_lookup(self, revisions_path: Path, expander: ReferenceExpander) -> None:
        """mdwiki_revid=0 -> find_mdwiki_revid() reads json_data.json to discover the revision."""
        json_file = revisions_path / "json_data.json"
        json_file.write_text(json.dumps({TITLE: str(REVID)}), encoding="utf-8")

        full_text = expander.get_full_text(TITLE, 0)

        assert full_text == REVISION_CONTENT


# Common ways editors write the same named reference
SHORT_REF_VARIANTS = [
    pytest.param('<ref name="AHFS2016" />', id="short-double-space"),
    pytest.param('<ref name="AHFS2016"/>', id="short-double-nospace"),
    pytest.param("<ref name='AHFS2016' />", id="short-single-space"),
    pytest.param("<ref name='AHFS2016'/>", id="short-single-nospace"),
    pytest.param("<ref name=AHFS2016 />", id="short-noquote-space"),
    pytest.param("<ref name=AHFS2016/>", id="short-noquote-nospace"),
]

FULL_REF_VARIANTS = [
    pytest.param('<ref name="AHFS2016">full ref</ref>', id="full-double"),
    pytest.param("<ref name='AHFS2016'>full ref</ref>", id="full-single"),
    pytest.param("<ref name=AHFS2016>full ref</ref>", id="full-noquote"),
]


class TestQuoteVariants:
    """Quote styles (" / ' / none) and self-closing spacing, in both the short and the full ref."""

    @pytest.mark.parametrize("full_ref", FULL_REF_VARIANTS)
    @pytest.mark.parametrize("short_ref", SHORT_REF_VARIANTS)
    def test_short_ref_is_expanded(
        self,
        expander: ReferenceExpander,
        write_revision,
        short_ref: str,
        full_ref: str,
    ) -> None:
        write_revision(f"something {full_ref}")
        text = f"This ref should be expanded {short_ref}"

        result = expander.fix_missing_refs(text, TITLE, REVID)

        assert "full ref</ref>" in result
        assert short_ref not in result

    @pytest.mark.parametrize("short_ref", SHORT_REF_VARIANTS)
    def test_short_ref_not_found_stays_unchanged(
        self,
        expander: ReferenceExpander,
        write_revision,
        short_ref: str,
    ) -> None:
        """If the revision has no such named ref, the short ref must be left as-is."""
        write_revision("something without refs")
        text = f"text {short_ref}"

        result = expander.fix_missing_refs(text, TITLE, REVID)

        assert result == text
