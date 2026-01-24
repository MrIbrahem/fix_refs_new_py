"""
Tests for Polish bot
"""

import pytest
from src.lang_bots.pl_bot import pl_fixes


class TestPolishBot:
    """Test Polish bot fixes"""

    def test_add_missing_param_to_choroba_infobox(self):
        """Test adding missing parameters to Choroba infobox"""
        text = "{{Choroba infobox|name=Test}}"
        result = pl_fixes(text)
        assert len(result) > len(text)
        assert "|" in result

    def test_dont_add_existing_params(self):
        """Test that existing parameters are not duplicated"""
        text = "{{Choroba infobox|ICD10=A|name=Test}}"
        result = pl_fixes(text)
        assert result.count("ICD10=") == 1

    def test_case_insensitive(self):
        """Test case-insensitive template matching"""
        text = "{{CHOROBA INFOBOX|name=Test}}"
        result = pl_fixes(text)
        assert len(result) > len(text)

    def test_no_change_on_other_text(self):
        """Test that other text remains unchanged"""
        text = "This is some regular text"
        result = pl_fixes(text)
        assert result == text
