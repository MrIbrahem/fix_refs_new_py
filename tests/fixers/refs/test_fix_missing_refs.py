"""Tests for RefExpander implementation in fix_refs/fixers/refs/expend_refs.py."""

import pytest
from src.fix_refs.fixers.refs.expend_refs import RefExpander


class TestReferenceExpander:
    """RefExpander.run() full flow."""

    def test_expands_missing_named_ref(self) -> None:
        input_text = 'This Ref tag should be full ref after fix missing references from 1501810/wikitext.txt <ref name="AHFS2016" />'
        result = RefExpander().run(
            input_text,
            source_text='something <ref name="AHFS2016">full ref</ref>',
        )

        assert '<ref name="AHFS2016">full ref</ref>' in result
        assert '<ref name="AHFS2016" />' not in result


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
        short_ref: str,
        full_ref: str,
    ) -> None:
        full_text = f"something {full_ref}"
        text = f"This ref should be expanded {short_ref}"

        result = RefExpander().run(
            text=text,
            source_text=full_text,
        )

        assert "full ref</ref>" in result
        assert short_ref not in result

    @pytest.mark.parametrize("short_ref", SHORT_REF_VARIANTS)
    def test_short_ref_not_found_stays_unchanged(
        self,
        short_ref: str,
    ) -> None:
        """If the revision has no such named ref, the short ref must be left as-is."""
        full_text = "something without refs"
        text = f"text {short_ref}"

        result = RefExpander().run(
            text=text,
            source_text=full_text,
        )

        assert result == text
