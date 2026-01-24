"""Tests for expend_refs (expend_refsTest.php)

Converted from tests/Bots/expend_refsTest.php
"""
import pytest
from src.bots.expend_refs import refs_expand_work


class TestExpendRefs:
    """Test cases for expanding references"""

    def test_refs_expand_work_with_simple_case(self):
        """Test expanding a simple self-closing reference"""
        input_text = '<ref name="ref1">Full content</ref> Text <ref name="ref1"/>'
        expected = '<ref name="ref1">Full content</ref> Text <ref name="ref1">Full content</ref>'
        assert refs_expand_work(input_text) == expected

    def test_refs_expand_work_with_no_matching_ref(self):
        """Test when self-closing ref has no matching full ref"""
        input_text = '<ref name="ref1">Full content</ref> Text <ref name="ref2"/>'
        expected = '<ref name="ref1">Full content</ref> Text <ref name="ref2"/>'
        assert refs_expand_work(input_text) == expected

    def test_refs_expand_work_with_multiple_refs(self):
        """Test expanding multiple different references"""
        input_text = '<ref name="ref1">Content 1</ref> <ref name="ref2">Content 2</ref> Text <ref name="ref1"/> <ref name="ref2"/>'
        expected = '<ref name="ref1">Content 1</ref> <ref name="ref2">Content 2</ref> Text <ref name="ref1">Content 1</ref> <ref name="ref2">Content 2</ref>'
        assert refs_expand_work(input_text) == expected

    def test_refs_expand_work_with_alltext_parameter(self):
        """Test using separate alltext parameter for source of full refs"""
        first = 'Text <ref name="ref1"/>'
        alltext = '<ref name="ref1">Full content</ref>'
        expected = 'Text <ref name="ref1">Full content</ref>'
        assert refs_expand_work(first, alltext) == expected

    def test_refs_expand_work_with_empty_input(self):
        """Test with empty input string"""
        assert refs_expand_work("") == ""

    def test_refs_expand_work_with_no_refs(self):
        """Test with text that has no references"""
        input_text = 'No references here'
        assert refs_expand_work(input_text) == input_text

    def test_refs_expand_work_preserves_original_formatting(self):
        """Test that original spacing in content is preserved"""
        input_text = '<ref name="ref1">  Full content  </ref> Text <ref name="ref1"/>'
        expected = '<ref name="ref1">  Full content  </ref> Text <ref name="ref1">  Full content  </ref>'
        assert refs_expand_work(input_text) == expected

    def test_refs_expand_work_with_special_characters(self):
        """Test with special characters in reference content"""
        input_text = '<ref name="ref1">Content with "quotes" & \'apostrophes\'</ref> Text <ref name="ref1"/>'
        expected = '<ref name="ref1">Content with "quotes" & \'apostrophes\'</ref> Text <ref name="ref1">Content with "quotes" & \'apostrophes\'</ref>'
        assert refs_expand_work(input_text) == expected

    def test_refs_expand_work_with_single_quotes_in_name(self):
        """Test with single quotes in ref name attribute"""
        input_text = '<ref name=\'ref1\'>Full content</ref> Text <ref name=\'ref1\'/>'
        expected = '<ref name=\'ref1\'>Full content</ref> Text <ref name=\'ref1\'>Full content</ref>'
        assert refs_expand_work(input_text) == expected

    def test_refs_expand_work_with_mixed_quotes(self):
        """Test with mixed quote styles in name attribute"""
        input_text = '<ref name="ref1">Full content</ref> Text <ref name=\'ref1\'/>'
        expected = '<ref name="ref1">Full content</ref> Text <ref name="ref1">Full content</ref>'
        assert refs_expand_work(input_text) == expected

    def test_refs_expand_work_multiple_same_refs(self):
        """Test multiple self-closing refs with same name"""
        input_text = '<ref name="ref1">Content</ref> A <ref name="ref1"/> B <ref name="ref1"/>'
        expected = '<ref name="ref1">Content</ref> A <ref name="ref1">Content</ref> B <ref name="ref1">Content</ref>'
        assert refs_expand_work(input_text) == expected
