"""Tests for MDWiki category (md_catTest.php)

Converted from tests/md_catTest.php
"""

from unittest.mock import patch

from fix_refs.mdwiki.category import add_translated_from_mdwiki

# Mock data for get_mdwiki_category responses
MOCK_CATS = {
    "fr": "Catégorie:Traduit de MDWiki",
    "de": "Category:Translated from MDWiki (de)",
    "ru": "Категория:Статьи, переведённые с MDWiki",
    "ur": "زمرہ:ایم ڈی وکی سے ترجمہ شدہ",
}


def mock_get_mdwiki_category(lang):
    """Mock implementation of get_mdwiki_category"""
    return MOCK_CATS.get(lang, f"Category:Translated from MDWiki ({lang})")


class TestMdCategory:
    """Test cases for MDWiki category addition"""

    @patch("fix_refs.mdwiki.category.get_mdwiki_category", side_effect=mock_get_mdwiki_category)
    def test_appends_category_when_conditions_met(self, mock_cats):
        """Test that category is appended for French language"""
        text = "This is a sample text"
        result = add_translated_from_mdwiki(text, "fr")
        expected = "This is a sample text\n[[Catégorie:Traduit de MDWiki]]\n"
        assert result == expected

    @patch("fix_refs.mdwiki.category.get_mdwiki_category", side_effect=mock_get_mdwiki_category)
    def test_does_not_append_when_category_exists(self, mock_cats):
        """Test that category is not appended if it already exists"""
        category = "[[Category:Translated from MDWiki (de)]]"
        text = "This is a sample text\n" + category
        result = add_translated_from_mdwiki(text, "de")
        assert result == text

    @patch("fix_refs.mdwiki.category.get_mdwiki_category", side_effect=mock_get_mdwiki_category)
    def test_handles_multiple_newlines(self, mock_cats):
        """Test handling of multiple newlines"""
        text = "This is a sample text\n\n"
        result = add_translated_from_mdwiki(text, "ru")
        expected = "This is a sample text\n\n\n[[Категория:Статьи, переведённые с MDWiki]]\n"
        assert result == expected

    @patch("fix_refs.mdwiki.category.get_mdwiki_category", side_effect=mock_get_mdwiki_category)
    def test_langs_ur(self, mock_cats):
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
