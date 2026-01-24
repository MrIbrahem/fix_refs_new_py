"""Tests for Bulgarian language bot (bg_bot.py)

Converted from tests/bg_bots/fix_bgTest.php
"""
import pytest
from src.lang_bots.bg_bot import bg_section, bg_fixes


class TestBgSection:
    """Test cases for bg_section function"""

    def test_bg_section_with_existing_translation_template(self):
        """Text already has translation template - should return text as is"""
        text = "Some text here\n{{Превод от|mdwiki|Example|123456}}\n[[Категория:Test]]"
        result = bg_section(text, "Example", "123456")
        assert result == text

    def test_bg_section_add_template_before_first_bulgarian_category(self):
        """Text has Bulgarian category - should add template before first category"""
        text = "Regular text\n[[Категория:Test]]\n[[Category:Another]]"
        expected = "Regular text\n{{Превод от|mdwiki|TestTitle|789}}\n[[Категория:Test]]\n[[Category:Another]]"
        result = bg_section(text, "TestTitle", "789")
        assert result == expected

    def test_bg_section_add_template_before_first_english_category(self):
        """Text has English category - should add template before first category"""
        text = "Some text\n[[Category:English]]\n[[Категория:Bulgarian]]"
        expected = "Some text\n{{Превод от|mdwiki|EnglishTitle|111}}\n[[Category:English]]\n[[Категория:Bulgarian]]"
        result = bg_section(text, "EnglishTitle", "111")
        assert result == expected

    def test_bg_section_without_categories(self):
        """Text has no categories - should add template at the end"""
        text = "Text without categories"
        expected = "Text without categories\n\n{{Превод от|mdwiki|Test|222}}\n"
        result = bg_section(text, "Test", "222")
        assert result == expected

    def test_bg_section_case_insensitive_template_detection(self):
        """Text has translation template with different cases - should be detected"""
        text1 = "{{Превод от|mdwiki|Test|123}}"
        text2 = "{{ превод от |mdwiki|Test|123}}"
        text3 = "{{ПРЕВОД ОТ|mdwiki|Test|123}}"

        result1 = bg_section(text1, "NewTitle", "456")
        result2 = bg_section(text2, "NewTitle", "456")
        result3 = bg_section(text3, "NewTitle", "456")

        assert result1 == text1
        assert result2 == text2
        assert result3 == text3

    def test_bg_section_with_multiple_categories(self):
        """Text with multiple categories - should add template before first category"""
        text = "Text\n[[Category:First]]\n[[Категория:Second]]\n[[Category:Third]]"
        expected = "Text\n{{Превод от|mdwiki|MultiCat|333}}\n[[Category:First]]\n[[Категория:Second]]\n[[Category:Third]]"
        result = bg_section(text, "MultiCat", "333")
        assert result == expected

    def test_bg_section_template_added_at_correct_position(self):
        """Template should be inserted exactly before the first category match"""
        text = "Line 1\nLine 2\n[[Category:Test]]\nLine 4"
        expected = "Line 1\nLine 2\n{{Превод от|mdwiki|Position|444}}\n[[Category:Test]]\nLine 4"
        result = bg_section(text, "Position", "444")
        assert result == expected

    def test_already_has_template(self):
        """Already has template - no change"""
        text = "Some intro\n{{Превод от|mdwiki|TestTitle|12345}}\n[[Категория:Drugs]]"
        result = bg_section(text, "Naproxen", "1468415")
        assert result == text

    def test_add_before_bg_category(self):
        """Add template before Bulgarian category"""
        text = "Intro text\n[[Категория:Medicine]]"
        expected = "Intro text\n{{Превод от|mdwiki|Naproxen|1468415}}\n[[Категория:Medicine]]"
        result = bg_section(text, "Naproxen", "1468415")
        assert result == expected

    def test_add_before_en_category(self):
        """Add template before English category"""
        text = "Intro text\n[[Category:Medicine]]"
        expected = "Intro text\n{{Превод от|mdwiki|Naproxen|1468415}}\n[[Category:Medicine]]"
        result = bg_section(text, "Naproxen", "1468415")
        assert result == expected

    def test_add_at_end_if_no_category(self):
        """Add template at end if no category"""
        text = "Some intro\nSome content"
        expected = "Some intro\nSome content\n\n{{Превод от|mdwiki|Naproxen|1468415}}\n"
        result = bg_section(text, "Naproxen", "1468415")
        assert result == expected

    def test_add_before_first_of_multiple_categories(self):
        """Add template before first of multiple categories"""
        text = "Intro text\n[[Категория:First]]\n[[Category:Second]]"
        expected = "Intro text\n{{Превод от|mdwiki|Naproxen|1468415}}\n[[Категория:First]]\n[[Category:Second]]"
        result = bg_section(text, "Naproxen", "1468415")
        assert result == expected

    def test_empty_text(self):
        """Empty text"""
        text = ""
        expected = "\n{{Превод от|mdwiki|Naproxen|1468415}}\n"
        result = bg_section(text, "Naproxen", "1468415")
        assert result == expected


class TestBgFixes:
    """Test cases for bg_fixes function"""

    def test_bg_fixes_remove_translated_category_and_add_template(self):
        """Should remove translated category and add translation template"""
        text = "Test text\n[[Category:Translated from MDWiki]]\n[[Категория:Test]]"
        expected = "Test text\n{{Превод от|mdwiki|TestTitle|444}}\n\n[[Категория:Test]]"
        result = bg_fixes(text, "TestTitle", "444")
        assert result == expected

    def test_bg_fixes_with_existing_translation_template(self):
        """Text has existing template - should keep it and remove translated category"""
        text = "Text\n{{Превод от|mdwiki|Existing|555}}\n[[Category:Translated from MDWiki]]\n[[Категория:Test]]"
        expected = "Text\n{{Превод от|mdwiki|Existing|555}}\n\n[[Категория:Test]]"
        result = bg_fixes(text, "NewTitle", "666")
        assert result == expected

    def test_bg_fixes_case_insensitive_translated_category_removal(self):
        """Should remove translated category with different cases"""
        text1 = "[[Category:Translated from MDWiki]]\n[[Категория:Test]]"
        text2 = "[[категория:translated from mdwiki]]\n[[Категория:Test]]"
        text3 = "[[CATEGORY:TRANSLATED FROM MDWIKI]]\n[[Категория:Test]]"

        expected = "{{Превод от|mdwiki|Test|777}}\n\n[[Категория:Test]]"

        result1 = bg_fixes(text1, "Test", "777")
        result2 = bg_fixes(text2, "Test", "777")
        result3 = bg_fixes(text3, "Test", "777")

        assert result1 == expected
        assert result2 == expected
        assert result3 == expected

    def test_bg_fixes_without_translated_category(self):
        """Text without translated category - only add translation template if needed"""
        text = "Regular text\n[[Категория:Test]]"
        expected = "Regular text\n{{Превод от|mdwiki|Simple|888}}\n[[Категория:Test]]"
        result = bg_fixes(text, "Simple", "888")
        assert result == expected

    def test_bg_fixes_empty_text(self):
        """Empty text"""
        text = ""
        expected = "\n{{Превод от|mdwiki|Empty|999}}\n"
        result = bg_fixes(text, "Empty", "999")
        assert result == expected

    def test_bg_fixes_only_translated_category(self):
        """Text contains only translated category"""
        text = "[[Category:Translated from MDWiki]]"
        expected = "{{Превод от|mdwiki|OnlyTranslated|1010}}\n"
        result = bg_fixes(text, "OnlyTranslated", "1010")
        assert result == expected

    def test_bg_fixes_translated_category_without_other_categories(self):
        """Text with translated category but no other categories"""
        text = "Regular text\n[[Category:Translated from MDWiki]]"
        expected = "Regular text\n{{Превод от|mdwiki|NoOtherCats|1111}}\n"
        result = bg_fixes(text, "NoOtherCats", "1111")
        assert result == expected

    def test_bg_fixes_with_whitespace_in_category(self):
        """Category with extra whitespace should still be removed"""
        text = "Text\n[[Category:  Translated from MDWiki  ]]\n[[Категория:Test]]"
        expected = "Text\n{{Превод от|mdwiki|Whitespace|1212}}\n\n[[Категория:Test]]"
        result = bg_fixes(text, "Whitespace", "1212")
        assert result == expected

    def test_bg_fixes_multiple_translated_categories(self):
        """Text with multiple translated categories"""
        text = "Text\n[[Category:Translated from MDWiki]]\n[[категория:translated from mdwiki]]\n[[Category:Test]]"
        expected = "Text\n{{Превод от|mdwiki|Multiple|1414}}\n\n\n[[Category:Test]]"
        result = bg_fixes(text, "Multiple", "1414")
        assert result == expected

    def test_bg_fixes_mixed_content(self):
        """Complex text with mixed content"""
        text = "Introduction\n{{Some other template}}\n[[Category:Translated from MDWiki]]\n\nContent here\n[[Категория:Main]]\n[[Category:Secondary]]"
        expected = "Introduction\n{{Some other template}}\n{{Превод от|mdwiki|Mixed|1515}}\n\n\nContent here\n[[Категория:Main]]\n[[Category:Secondary]]"
        result = bg_fixes(text, "Mixed", "1515")
        assert result == expected
