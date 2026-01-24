"""Tests for category parser (category.py)

Converted from tests/Parse/CategoryTest.php
"""
import pytest
from src.parsers.category import get_categories


class TestCategory:
    """Test cases for category parsing"""

    def test_get_categories_with_simple_categories(self):
        """Test extracting simple categories from text"""
        text = "This is some text [[Category:Example]] and more text [[Category:Test]]"
        expected = {
            "Example": "[[Category:Example]]",
            "Test": "[[Category:Test]]"
        }
        result = get_categories(text)
        assert result == expected

    def test_get_categories_with_no_categories(self):
        """Test text with no categories"""
        text = "This is some text without any categories"
        expected = {}
        result = get_categories(text)
        assert result == expected

    def test_get_categories_with_pipe_separator(self):
        """Test categories with pipe separator (sort key)"""
        text = "Text with [[Category:Example|sort key]] and [[Category:Test|another key]]"
        expected = {
            "Example": "[[Category:Example|sort key]]",
            "Test": "[[Category:Test|another key]]"
        }
        result = get_categories(text)
        assert result == expected

    def test_get_categories_with_spaces(self):
        """Test categories with extra spaces"""
        text = "Text with [[ Category : Example with spaces ]] and [[  Category:Test  ]]"
        expected = {
            "Example with spaces": "[[ Category : Example with spaces ]]",
            "Test": "[[  Category:Test  ]]"
        }
        result = get_categories(text)
        assert result == expected

    def test_get_categories_with_special_characters(self):
        """Test categories with special characters"""
        text = "Text with [[Category:Example & Test]] and [[Category:Something (else)]]"
        expected = {
            "Example & Test": "[[Category:Example & Test]]",
            "Something (else)": "[[Category:Something (else)]]"
        }
        result = get_categories(text)
        assert result == expected

    def test_get_categories_with_duplicate_categories(self):
        """Test handling duplicate categories"""
        text = "Text with [[Category:Example]] and more [[Category:Example]]"
        expected = {
            "Example": "[[Category:Example]]"
        }
        result = get_categories(text)
        assert result == expected

    def test_get_categories_with_multiline_text(self):
        """Test categories in multiline text"""
        text = """Start of text
[[Category:First category]]
Middle of text
[[Category:Second category]]
End of text"""
        expected = {
            "First category": "[[Category:First category]]",
            "Second category": "[[Category:Second category]]"
        }
        result = get_categories(text)
        assert result == expected

    def test_get_categories_with_empty_input(self):
        """Test with empty input"""
        text = ""
        expected = {}
        result = get_categories(text)
        assert result == expected

    def test_get_categories_with_multiple_pipes(self):
        """Test categories with multiple pipes"""
        text = "Text with [[Category:Example|sort|key]] and [[Category:Test]]"
        expected = {
            "Example": "[[Category:Example|sort|key]]",
            "Test": "[[Category:Test]]"
        }
        result = get_categories(text)
        assert result == expected

    def test_get_categories_with_unicode_characters(self):
        """Test categories with unicode characters"""
        text = "Text with [[Category:مثال]] and [[Category:測試]]"
        expected = {
            "مثال": "[[Category:مثال]]",
            "測試": "[[Category:測試]]"
        }
        result = get_categories(text)
        assert result == expected

    def test_get_categories_with_mixed_case(self):
        """Test categories with mixed case"""
        text = "Text with [[category:example]] and [[CATEGORY:TEST]]"
        expected = {
            "example": "[[category:example]]",
            "TEST": "[[CATEGORY:TEST]]"
        }
        result = get_categories(text)
        assert result == expected

    def test_get_categories_with_templates_inside(self):
        """Test categories with templates inside"""
        text = "Text with [[Category:Example{{template}}]] and [[Category:Test]]"
        expected = {
            "Example{{template}}": "[[Category:Example{{template}}]]",
            "Test": "[[Category:Test]]"
        }
        result = get_categories(text)
        assert result == expected

    def test_get_single_category(self):
        """يختبر استخراج تصنيف واحد من النص"""
        text = "Some text here [[Category:PHP]] more text."
        expected = {
            "PHP": "[[Category:PHP]]"
        }
        assert get_categories(text) == expected

    def test_get_multiple_categories(self):
        """يختبر استخراج عدة تصنيفات من النص"""
        text = "[[Category:Programming]] and [[Category:Web development]]."
        expected = {
            "Programming": "[[Category:Programming]]",
            "Web development": "[[Category:Web development]]"
        }
        assert get_categories(text) == expected

    def test_no_categories_found(self):
        """يختبر نصًا لا يحتوي على أي تصنيفات"""
        text = "This is a text with no categories."
        assert get_categories(text) == {}

    def test_category_with_extra_whitespace(self):
        """يختبر وجود مسافات إضافية حول اسم التصنيف"""
        text = "[[Category:  Test Category  ]]"
        expected = {
            "Test Category": "[[Category:  Test Category  ]]"
        }
        assert get_categories(text) == expected

    def test_case_insensitive_category_tag(self):
        """يختبر اختلاف حالة الأحرف في كلمة Category"""
        text = "[[category:Case Insensitive]]"
        expected = {
            "Case Insensitive": "[[category:Case Insensitive]]"
        }
        assert get_categories(text) == expected

    def test_category_with_sort_key(self):
        """يختبر التصنيفات التي تحتوي على مفتاح فرز (sort key)"""
        text = "[[Category:Musicians|Beatles]]"
        expected = {
            "Musicians": "[[Category:Musicians|Beatles]]"
        }
        assert get_categories(text) == expected

    def test_mixed_and_complex_categories(self):
        """يختبر وجود عدة تصنيفات مع مفاتيح فرز ومسافات"""
        text = "A complex text [[Category:Software|S]] and another one [[  category :  Databases  ]]."
        expected = {
            "Software": "[[Category:Software|S]]",
            "Databases": "[[  category :  Databases  ]]"
        }
        assert get_categories(text) == expected

    def test_get_categories_with_nested_brackets(self):
        """Test categories with nested brackets/templates"""
        text = "Text with [[category:Example {{nested}} | {{!}} ]] and [[CategorY:Test]]"
        expected = {
            "Example {{nested}}": "[[category:Example {{nested}} | {{!}} ]]",
            "Test": "[[CategorY:Test]]"
        }
        result = get_categories(text)
        assert result == expected
