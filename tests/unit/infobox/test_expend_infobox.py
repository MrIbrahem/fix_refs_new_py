"""Tests for infobox expansion (expend_infobox.py)

Converted from tests/infoboxes/infoboxTest.php and tests/infoboxes/infobox2Test.php
"""

from src.fix_refs.infobox.expend_infobox import InfoboxExpander


class TestInfobox:
    """Test cases for infobox expansion"""

    def test_expend_new_simple_template(self):
        """Test _expend_new with a simple template"""
        # Test with basic template
        result = InfoboxExpander()._expend_new("{{test}}")
        assert result == "{{test\n}}"

    def test_make_section_0(self):
        """Test extract_lead_section function"""
        text = "Some text before\n==Section==\nContent after"
        result = InfoboxExpander.extract_lead_section(text)
        assert result == "Some text before\n"

        # Test without sections
        text2 = "Just some text"
        result2 = InfoboxExpander.extract_lead_section(text2)
        assert result2 == text2

    def test_expend_infobox_basic(self):
        """Test expend_infobox with basic infobox"""
        text = """{{Infobox drug|name=Test}}\nSome content"""
        result = InfoboxExpander().expand_infobox_in_text(text, "TestPage")
        assert isinstance(result, str)
        assert len(result) > 0

    # Note: Full infoboxTest.php test requires file-based I/O
    # The test_expend_new_FileText would require reading from test data files
    # This is a simplified version - for full testing, create test data files


class TestDoComments:
    """Test cases for infobox expansion"""

    def test_do_comments(self):
        """Test do_comments function"""
        text = """Some text\n<!-- Legal data -->\nMore text\n<!-- Clinical data -->\nEnd"""
        result = InfoboxExpander().do_comments(text)
        # Comments should be reformatted with proper spacing
        assert "<!-- Legal data -->" in result
        assert "<!-- Clinical data -->" in result

    def test_do_comments_with_multiple_sections(self):
        """Test do_comments with various comment types"""
        text = """<!-- Names -->\n<!-- Clinical data -->\n<!-- Legal data -->\n<!-- Pharmacokinetic data -->\n<!-- Chemical and physical data -->"""
        result = InfoboxExpander().do_comments(text)
        # All comments should still be present
        assert "<!-- Names -->" in result
        assert "<!-- Clinical data -->" in result
        assert "<!-- Legal data -->" in result
