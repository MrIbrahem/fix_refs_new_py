"""
Tests for MDWiki category_service
"""

from src.fix_refs.mdwiki.category_service import MDWikiCategoryService


class TestMDWikiCategoryService:
    """Test cases for MDWikiCategoryService.add_translated_from_mdwiki function"""

    def test_equals(self):
        """Test that existing translated category is preserved"""
        text = "[[Kategorija:Translated from MDWiki]]"
        result = MDWikiCategoryService().add_translated_from_mdwiki(text, "hr")
        assert result == text

    def test_skip_langs_it(self):
        """Test that Italian language is skipped"""
        text = "This is a sample text"
        result = MDWikiCategoryService().add_translated_from_mdwiki(text, "it")
        assert result == text

    def test_does_not_append_when_fallback_category_exists(self):
        """Test that category is not appended if fallback exists"""
        text = "This is a sample text\n[[Category:translated_from mdwiki|z]]"
        result = MDWikiCategoryService().add_translated_from_mdwiki(text, "es")
        assert result == text


class TestAddMdwikiCategory:
    """Test cases for MDWikiCategoryService.add_mdwiki_category function"""

    def test_equals(self):
        """Test that existing translated category is preserved"""
        text = "[[Kategorija:Translated from MDWiki]]"
        result = MDWikiCategoryService().add_mdwiki_category(text, "hr")
        assert result == text

    def test_add_category(self):
        text = "This is a sample text"
        result = MDWikiCategoryService().add_mdwiki_category(text, "[[Category:test| ]]")
        assert "[[Category:test| ]]" in result

    def test_does_not_append_when_fallback_category_exists(self):
        """Test that category is not appended if fallback exists"""
        text = "This is a sample text\n[[Category:translated from mdwiki]]"
        result = MDWikiCategoryService().add_mdwiki_category(text, "es")
        assert result == text
