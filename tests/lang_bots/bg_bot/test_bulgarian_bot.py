"""
Tests for Bulgarian bot
"""

import pytest
from src.lang_bots.bg_bot import bg_fixes


class TestBulgarianBot:
    """Test Bulgarian bot fixes"""

    def test_add_translation_template(self):
        """Test adding Bulgarian translation template"""
        text = "Some content here"
        result = bg_fixes(text, "TestPage", 12345)
        assert len(result) > len(text)
        assert "mdwiki" in result

    def test_skip_if_template_exists(self):
        """Test skipping if translation template already exists"""
        text = "Some {{Pravod ot|mdwiki|Old|123}} content"
        result = bg_fixes(text, "TestPage", 12345)
        assert result.count("{{Pravod ot|mdwiki") == 1

    def test_remove_translated_from_mdwiki_category(self):
        """Test removing Translated from MDWiki category"""
        text = "[[Category:Translated from MDWiki]]"
        result = bg_fixes(text, "", 0)
        assert "[[Category:Translated from MDWiki]]" not in result

    def test_insert_before_category(self):
        """Test inserting template before category"""
        text = "Content\n[[Category:Test]]"
        result = bg_fixes(text, "TestPage", 12345)
        lines = result.split('\n')
        assert len(lines) > 2

    def test_no_change_on_regular_text(self):
        """Test that regular text gets template added"""
        text = "This is some regular text"
        result = bg_fixes(text, "", 0)
        assert len(result) > len(text)
