"""
Tests for Swahili bot
"""

import pytest
from src.lang_bots.sw_bot import sw_fixes


class TestSwahiliBot:
    """Test Swahili bot fixes"""

    def test_fix_marejeleo_section_title(self):
        """Test fixing Marejeleo to Marejeo in section title"""
        text = "== Marejeleo == Section content"
        result = sw_fixes(text)
        assert "== Marejeo ==" in result

    def test_no_change_on_other_text(self):
        """Test that other text remains unchanged"""
        text = "This is some text here"
        result = sw_fixes(text)
        assert result == text

    def test_multiple_equals(self):
        """Test with multiple equals signs"""
        text = "=== Marejeleo ==="
        result = sw_fixes(text)
        assert "=== Marejeo ===" in result

    def test_case_insensitive(self):
        """Test case-insensitive replacement"""
        text = "== MAREJELEO =="
        result = sw_fixes(text)
        assert "== Marejeo ==" in result
