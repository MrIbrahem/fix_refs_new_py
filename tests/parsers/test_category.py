"""
Tests for category parser
"""

import pytest
from src.parsers.category import (
    get_categories,
    get_category_list,
    has_category
)


class TestGetCategories:
    """Test category extraction"""

    def test_simple_category(self):
        """Test extracting simple category"""
        text = "[[Category:Test]]"
        categories = get_categories(text)
        assert "Test" in categories
        assert categories["Test"] == "[[Category:Test]]"

    def test_category_with_pipe(self):
        """Test extracting category with display name"""
        text = "[[Category:Test|Display Name]]"
        categories = get_categories(text)
        assert "Test" in categories

    def test_multiple_categories(self):
        """Test extracting multiple categories"""
        text = "[[Category:A]][[Category:B]]"
        categories = get_categories(text)
        assert len(categories) == 2
        assert "A" in categories
        assert "B" in categories

    def test_no_categories(self):
        """Test with no categories"""
        text = "No categories here"
        categories = get_categories(text)
        assert len(categories) == 0

    def test_category_with_spaces(self):
        """Test extracting category with spaces"""
        text = "[[Category:Test Category]]"
        categories = get_categories(text)
        assert "Test Category" in categories


class TestGetCategoryList:
    """Test category list extraction"""

    def test_get_list(self):
        """Test getting category names as list"""
        text = "[[Category:A]][[Category:B]]"
        categories = get_category_list(text)
        assert isinstance(categories, list)
        assert "A" in categories
        assert "B" in categories


class TestHasCategory:
    """Test category presence check"""

    def test_has_existing_category(self):
        """Test checking for existing category"""
        text = "[[Category:Test]]"
        assert has_category(text, "Test") is True

    def test_has_missing_category(self):
        """Test checking for missing category"""
        text = "[[Category:Other]]"
        assert has_category(text, "Test") is False

    def test_case_insensitive(self):
        """Test case sensitivity"""
        text = "[[Category:Test]]"
        assert has_category(text, "test") is False
