"""
Tests for Armenian bot
"""

import pytest
from src.lang_bots.hy_bot import hy_fixes


class TestArmenianBot:
    """Test Armenian bot fixes"""

    def test_remove_space_before_punctuation(self):
        """Test removing space between ref and punctuation"""
        text = "տեքստ <ref name=\"test\">content</ref>։"
        result = hy_fixes(text)
        assert "</ref>։" in result

    def test_keep_punctuation_attached(self):
        """Test keeping punctuation attached to self-closing ref"""
        text = "Տեքստ <ref name=\"test\"/>."
        result = hy_fixes(text)
        assert "/>." in result

    def test_multiple_punctuation(self):
        """Test with multiple punctuation marks"""
        text = "տեքստ <ref>content</ref>։:"
        result = hy_fixes(text)
        assert "</ref>։:" in result

    def test_no_change_without_refs(self):
        """Test that text without refs remains unchanged"""
        text = "Սահման տեքստ առանց"
        result = hy_fixes(text)
        assert result == text
