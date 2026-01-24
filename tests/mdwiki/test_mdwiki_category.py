"""Tests for MDWiki category (md_catTest.php)

Converted from tests/md_catTest.php
"""
import pytest
from src.mdwiki.category import add_translated_from_mdwiki


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


@pytest.mark.skip(reason="Requires network access at get_cats, should be mocked")
class TestMdCategoryNetwork:
    """Test cases for MDWiki category addition"""

    def test_appends_category_when_conditions_met(self):
        """Test that category is appended for French language"""
        text = "This is a sample text"
        result = add_translated_from_mdwiki(text, "fr")
        expected = "This is a sample text\n[[Catégorie:Traduit de MDWiki]]\n"
        assert result == expected

    def test_does_not_append_when_category_exists(self):
        """Test that category is not appended if it already exists"""
        category = "[[Category:Translated from MDWiki (de)]]"
        text = "This is a sample text\n" + category
        result = add_translated_from_mdwiki(text, "de")
        assert result == text

    def test_handles_multiple_newlines(self):
        """Test handling of multiple newlines"""
        text = "This is a sample text\n\n"
        result = add_translated_from_mdwiki(text, "ru")
        expected = "This is a sample text\n\n\n[[Категория:Статьи, переведённые с MDWiki]]\n"
        assert result == expected

    def test_langs_ur(self):
        """Test Urdu language category"""
        lang = "ur"
        cat = "زمرہ:ایم ڈی وکی سے ترجمہ شدہ"
        text_no_cat = "This is a sample text\n\n"
        expected = f"{text_no_cat}\n[[{cat}]]\n"

        result = add_translated_from_mdwiki(text_no_cat, lang)
        assert result == expected

        # Test with existing category
        text_with_cat = f"This is a sample text\n\n[[{cat}]]\n"
        result = add_translated_from_mdwiki(text_with_cat, lang)
        assert result == text_with_cat

        # Test with fallback category
        text_with_cat2 = "This is a sample text\n\n[[category:Translated_from_MDWiki]]\n"
        result = add_translated_from_mdwiki(text_with_cat2, lang)
        assert result == text_with_cat2
