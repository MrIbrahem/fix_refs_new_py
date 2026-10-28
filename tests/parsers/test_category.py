"""
Tests for category parser
"""

from src.fix_refs.parsers.category import CategoryParser


class TestGetCategories:
    """Test category extraction"""

    def test_simple_category(self):
        """Test extracting simple category"""
        text = "[[Category:Test]]"
        categories = CategoryParser().get_categories(text)
        assert "Test" in categories
        assert categories["Test"] == "[[Category:Test]]"

    def test_category_with_pipe(self):
        """Test extracting category with display name"""
        text = "[[Category:Test|Display Name]]"
        categories = CategoryParser().get_categories(text)
        assert "Test" in categories

    def test_multiple_categories(self):
        """Test extracting multiple categories"""
        text = "[[Category:A]][[Category:B]]"
        categories = CategoryParser().get_categories(text)
        assert len(categories) == 2
        assert "A" in categories
        assert "B" in categories

    def test_no_categories(self):
        """Test with no categories"""
        text = "No categories here"
        categories = CategoryParser().get_categories(text)
        assert len(categories) == 0

    def test_category_with_spaces(self):
        """Test extracting category with spaces"""
        text = "[[Category:Test Category]]"
        categories = CategoryParser().get_categories(text)
        assert "Test Category" in categories

    def test_get_categories_with_simple_categories(self):
        """Test extracting simple categories from text"""
        text = "This is some text [[Category:Example]] and more text [[Category:Test]]"
        expected = {"Example": "[[Category:Example]]", "Test": "[[Category:Test]]"}
        result = CategoryParser().get_categories(text)
        assert result == expected

    def test_get_categories_with_no_categories(self):
        """Test text with no categories"""
        text = "This is some text without any categories"
        expected = {}
        result = CategoryParser().get_categories(text)
        assert result == expected

    def test_get_categories_with_pipe_separator(self):
        """Test categories with pipe separator (sort key)"""
        text = "Text with [[Category:Example|sort key]] and [[Category:Test|another key]]"
        expected = {"Example": "[[Category:Example|sort key]]", "Test": "[[Category:Test|another key]]"}
        result = CategoryParser().get_categories(text)
        assert result == expected

    def test_get_categories_with_spaces(self):
        """Test categories with extra spaces"""
        text = "Text with [[ Category : Example with spaces ]] and [[  Category:Test  ]]"
        expected = {"Example with spaces": "[[ Category : Example with spaces ]]", "Test": "[[  Category:Test  ]]"}
        result = CategoryParser().get_categories(text)
        assert result == expected

    def test_get_categories_with_special_characters(self):
        """Test categories with special characters"""
        text = "Text with [[Category:Example & Test]] and [[Category:Something (else)]]"
        expected = {
            "Example & Test": "[[Category:Example & Test]]",
            "Something (else)": "[[Category:Something (else)]]",
        }
        result = CategoryParser().get_categories(text)
        assert result == expected

    def test_get_categories_with_duplicate_categories(self):
        """Test handling duplicate categories"""
        text = "Text with [[Category:Example]] and more [[Category:Example]]"
        expected = {"Example": "[[Category:Example]]"}
        result = CategoryParser().get_categories(text)
        assert result == expected

    def test_get_categories_with_multiline_text(self):
        """Test categories in multiline text"""
        text = (
            """Start of text\n[[Category:First category]]\nMiddle of text\n[[Category:Second category]]\nEnd of text"""
        )
        expected = {"First category": "[[Category:First category]]", "Second category": "[[Category:Second category]]"}
        result = CategoryParser().get_categories(text)
        assert result == expected

    def test_get_categories_with_empty_input(self):
        """Test with empty input"""
        text = ""
        expected = {}
        result = CategoryParser().get_categories(text)
        assert result == expected

    def test_get_categories_with_multiple_pipes(self):
        """Test categories with multiple pipes"""
        text = "Text with [[Category:Example|sort|key]] and [[Category:Test]]"
        expected = {"Example": "[[Category:Example|sort|key]]", "Test": "[[Category:Test]]"}
        result = CategoryParser().get_categories(text)
        assert result == expected

    def test_get_categories_with_unicode_characters(self):
        """Test categories with unicode characters"""
        text = "Text with [[Category:مثال]] and [[Category:測試]]"
        expected = {"مثال": "[[Category:مثال]]", "測試": "[[Category:測試]]"}
        result = CategoryParser().get_categories(text)
        assert result == expected

    def test_get_categories_with_mixed_case(self):
        """Test categories with mixed case"""
        text = "Text with [[category:example]] and [[CATEGORY:TEST]]"
        expected = {"example": "[[category:example]]", "TEST": "[[CATEGORY:TEST]]"}
        result = CategoryParser().get_categories(text)
        assert result == expected

    def test_get_categories_with_templates_inside(self):
        """Test categories with templates inside"""
        text = "Text with [[Category:Example{{template}}]] and [[Category:Test]]"
        expected = {"Example{{template}}": "[[Category:Example{{template}}]]", "Test": "[[Category:Test]]"}
        result = CategoryParser().get_categories(text)
        assert result == expected

    def test_get_single_category(self):
        """يختبر استخراج تصنيف واحد من النص"""
        text = "Some text here [[Category:PHP]] more text."
        expected = {"PHP": "[[Category:PHP]]"}
        assert CategoryParser().get_categories(text) == expected

    def test_get_multiple_categories(self):
        """يختبر استخراج عدة تصنيفات من النص"""
        text = "[[Category:Programming]] and [[Category:Web development]]."
        expected = {"Programming": "[[Category:Programming]]", "Web development": "[[Category:Web development]]"}
        assert CategoryParser().get_categories(text) == expected

    def test_no_categories_found(self):
        """يختبر نصًا لا يحتوي على أي تصنيفات"""
        text = "This is a text with no categories."
        assert CategoryParser().get_categories(text) == {}

    def test_category_with_extra_whitespace(self):
        """يختبر وجود مسافات إضافية حول اسم التصنيف"""
        text = "[[Category:  Test Category  ]]"
        expected = {"Test Category": "[[Category:  Test Category  ]]"}
        assert CategoryParser().get_categories(text) == expected

    def test_case_insensitive_category_tag(self):
        """يختبر اختلاف حالة الأحرف في كلمة Category"""
        text = "[[category:Case Insensitive]]"
        expected = {"Case Insensitive": "[[category:Case Insensitive]]"}
        assert CategoryParser().get_categories(text) == expected

    def test_category_with_sort_key(self):
        """يختبر التصنيفات التي تحتوي على مفتاح فرز (sort key)"""
        text = "[[Category:Musicians|Beatles]]"
        expected = {"Musicians": "[[Category:Musicians|Beatles]]"}
        assert CategoryParser().get_categories(text) == expected

    def test_mixed_and_complex_categories(self):
        """يختبر وجود عدة تصنيفات مع مفاتيح فرز ومسافات"""
        text = "A complex text [[Category:Software|S]] and another one [[  category :  Databases  ]]."
        expected = {"Software": "[[Category:Software|S]]", "Databases": "[[  category :  Databases  ]]"}
        assert CategoryParser().get_categories(text) == expected

    def test_get_categories_with_nested_brackets(self):
        """Test categories with nested brackets/templates"""
        text = "Text with [[category:Example {{nested}} | {{!}} ]] and [[CategorY:Test]]"
        expected = {"Example {{nested}}": "[[category:Example {{nested}} | {{!}} ]]", "Test": "[[CategorY:Test]]"}
        result = CategoryParser().get_categories(text)
        assert result == expected


class TestGetCategoryList:
    """Test category list extraction"""

    def test_get_list(self):
        """Test getting category names as list"""
        text = "[[Category:A]][[Category:B]]"
        categories = CategoryParser().get_categories(text)
        categories_list = list(categories)
        assert isinstance(categories, dict)

        assert "A" in categories_list
        assert "B" in categories_list


class TestHasCategory:
    """Test category presence check"""

    def test_has_existing_category(self):
        """Test checking for existing category"""
        text = "[[Category:Test]]"
        assert CategoryParser().has_category(text, "Test") is True

    def test_has_missing_category(self):
        """Test checking for missing category"""
        text = "[[Category:Other]]"
        assert CategoryParser().has_category(text, "Test") is False

    def test_case_insensitive(self):
        """Test case sensitivity"""
        text = "[[Category:Test]]"
        assert CategoryParser().has_category(text, "test") is False
