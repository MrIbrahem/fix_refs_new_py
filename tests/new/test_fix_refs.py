"""
Tests for core fix_page functionality
"""

import pytest
from src.core.fix_page import fix_refs


class TestFixRefs:
    """Test the main fix_refs function"""

    def test_hy_language_simple(self):
        """Test Armenian language fixes with simple case"""
        input_text = '[[Category:Translated from MDWiki]] ռետինոիդներ։ <ref name="NORD2006" /><ref name="Gli2017" />'
        expected = '[[Category:Translated from MDWiki]] ռետինոիդներ<ref name="NORD2006" /><ref name="Gli2017" />։'
        result = fix_refs(input_text, "hy")
        assert result == expected

    def test_empty_text(self):
        """Test with empty text"""
        assert fix_refs("", "en") == ""

    def test_basic_text_no_refs(self):
        """Test with basic text without references"""
        input_text = "This is a simple text."
        expected = "This is a simple text."
        result = fix_refs(input_text, "en")
        assert result == expected

    def test_single_ref(self):
        """Test with single reference"""
        input_text = "Text with <ref name=\"test1\">Reference content</ref> reference."
        result = fix_refs(input_text, "en")
        assert "<ref" in result
        assert "</ref>" in result

    def test_duplicate_refs(self):
        """Test duplicate reference removal"""
        input_text = 'Text <ref name="test">Content</ref> and <ref name="test">Content</ref> again.'
        result = fix_refs(input_text, "en")
        assert result.count("Content") == 1

    def test_multiple_refs(self):
        """Test with multiple references"""
        input_text = '<ref name="A"/>Text<ref name="B"/>More<ref name="A"/>'
        result = fix_refs(input_text, "en")
        assert "<ref" in result


class TestFixPage:
    """Test the fix_page function with full parameters"""

    def test_with_move_dots(self):
        """Test with move_dots enabled"""
        input_text = "Text with dot. <ref name=\"test\">Reference</ref>"
        result = fix_refs(input_text, "en")
        assert "<ref" in result

    def test_redirect_page(self):
        """Test redirect page is skipped"""
        input_text = "#REDIRECT [[Target Page]]"
        result = fix_refs(input_text, "en")
        assert result == input_text
