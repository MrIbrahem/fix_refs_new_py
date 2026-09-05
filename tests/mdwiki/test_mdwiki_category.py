"""Tests for MDWiki category (md_catTest.php)

Converted from tests/md_catTest.php
"""

from fix_refs.mdwiki.category import add_translated_from_mdwiki


class TestMdCategory:
    """Test cases for MDWiki category addition"""

    def test_equals(self):
        """Test that existing translated category is preserved"""
        text = "[[Kategorija:Translated from MDWiki]]"
        result = add_translated_from_mdwiki(text, "hr")
        assert result == text

    def test_skip_langs_it(self):
        """Test that Italian language is skipped"""
        text = "This is a sample text"
        result = add_translated_from_mdwiki(text, "it")
        assert result == text

    def test_does_not_append_when_fallback_category_exists(self):
        """Test that category is not appended if fallback exists"""
        text = "This is a sample text\n[[Category:Translated from MDWiki]]"
        result = add_translated_from_mdwiki(text, "es")
        assert result == text
