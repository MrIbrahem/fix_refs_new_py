"""
Tests for mini fixes
"""

import pytest
from src.bots.mini_fixes import (
    mini_fixes,
    mini_fixes_after_fixing,
    refs_tags_spaces,
    fix_sections_titles,
    remove_space_before_ref_tags,
    fix_prefix
)


class TestMiniFixes:
    """Test main mini fixes function"""

    def test_minimal_text(self):
        """Test with minimal text"""
        result = mini_fixes("Test", "en")
        assert "Test" in result


class TestRefsTagsSpaces:
    """Test reference tag spacing fixes"""

    def test_remove_space_between_refs(self):
        """Test removing space between closing and opening refs"""
        text = "</ref> <ref name=\"test\">Content</ref>"
        result = refs_tags_spaces(text)
        assert "</ref> <ref" not in result
        assert "</ref><ref" in result

    def test_remove_space_self_closing(self):
        """Test removing space with self-closing ref"""
        text = "<ref name=\"A\"/><ref name=\"B\">Content</ref>"
        result = refs_tags_spaces(text)
        assert "/><ref" in result

    def test_remove_space_after_ref(self):
        """Test removing space after ref"""
        text = "> <ref name=\"test\">Content</ref>"
        result = refs_tags_spaces(text)
        assert "> <ref" not in result
        assert "><ref" in result


class TestFixSectionsTitles:
    """Test section title fixes"""

    def test_croatian_references(self):
        """Test Croatian translation"""
        text = "==References=="
        result = fix_sections_titles(text, "hr")
        assert "== Izvori ==" in result

    def test_swahili_references(self):
        """Test Swahili translation"""
        text = "==References=="
        result = fix_sections_titles(text, "sw")
        assert "== Marejeo ==" in result

    def test_no_translation_for_english(self):
        """Test no translation for English"""
        text = "==References=="
        result = fix_sections_titles(text, "en")
        assert "==References==" in result


class TestRemoveSpaceBeforeRefTags:
    """Test space removal before ref tags"""

    def test_remove_space_before_dot(self):
        """Test removing space before dot"""
        text = "Text .<ref name=\"test\">Content</ref>"
        result = remove_space_before_ref_tags(text, "en")
        assert "Text.<ref" in result

    def test_remove_space_before_comma(self):
        """Test removing space before comma"""
        text = "Text ,<ref name=\"test\">Content</ref>"
        result = remove_space_before_ref_tags(text, "en")
        assert "Text,<ref" in result


class TestFixPrefix:
    """Test interwiki link prefix fixes"""

    def test_remove_en_prefix(self):
        """Test removing English interwiki prefix"""
        text = "[[:en:Test|Display]]"
        result = fix_prefix(text, "en")
        assert "[[Test|Display]]" in result
        assert "[[:en:" not in result

    def test_remove_lang_prefix(self):
        """Test removing language interwiki prefix"""
        text = "[[:es:Prueba|Display]]"
        result = fix_prefix(text, "es")
        assert "[[Prueba|Display]]" in result
        assert "[[:es:" not in result


class TestMiniFixesAfterFixing:
    """Test fixes applied after main fixing"""

    def test_remove_empty_lines(self):
        """Test removing empty lines"""
        text = "Line 1\n\n\nLine 2"
        result = mini_fixes_after_fixing(text, "en")
        assert "\n\n\n" not in result
