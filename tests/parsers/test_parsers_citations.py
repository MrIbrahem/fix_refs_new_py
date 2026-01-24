"""Tests for citation parser (citations.py)

Converted from tests/Parse/Citations_regTest.php
"""
import pytest
from src.parsers.citations import (
    get_name,
    get_citations,
    get_full_refs,
    get_short_citations,
    Citation
)


class TestCitations:
    """Test cases for citation parsing"""

    # Tests for get_name function

    def test_get_name_with_double_quotes(self):
        """Test getting name with double quotes"""
        assert get_name('name="test_name"') == "test_name"

    def test_get_name_with_single_quotes(self):
        """Test getting name with single quotes"""
        assert get_name("name='test_name'") == "test_name"

    def test_get_name_without_quotes(self):
        """Test getting name without quotes"""
        assert get_name("name=test_name") == "test_name"

    def test_get_name_with_spaces(self):
        """Test getting name with spaces"""
        assert get_name("name = 'test name'") == "test name"

    def test_get_name_empty(self):
        """Test getting name from empty or non-name input"""
        assert get_name("") == ""
        assert get_name("other_attr=value") == ""

    # Tests for get_citations function

    def test_get_reg_citations_with_multiple_refs(self):
        """Test extracting multiple citations from text"""
        text = '<ref name="ref1">Content 1</ref> Text <ref name="ref2">Content 2</ref>'
        citations = get_citations(text)

        assert len(citations) == 2
        assert citations[0].name == "ref1"
        assert citations[0].content == "Content 1"
        assert citations[0].tag == '<ref name="ref1">Content 1</ref>'

    def test_get_reg_citations_with_no_refs(self):
        """Test extracting citations from text with no references"""
        text = 'No references here'
        citations = get_citations(text)
        assert len(citations) == 0

    def test_get_citations_with_no_name(self):
        """Test citations without name attribute"""
        text = '<ref>Content without name</ref>'
        citations = get_citations(text)

        assert len(citations) == 1
        assert citations[0].name == ""
        assert citations[0].content == "Content without name"

    def test_get_citations_with_multiple_attributes(self):
        """Test citations with multiple attributes"""
        text = '<ref name="test" group="notes">Content</ref>'
        citations = get_citations(text)

        assert len(citations) == 1
        assert citations[0].name == "test"
        assert "group" in citations[0].options

    # Tests for get_full_refs function

    def test_get_full_refs(self):
        """Test getting full reference mapping"""
        text = '<ref name="ref1">Content 1</ref> <ref name="ref2">Content 2</ref>'
        full_refs = get_full_refs(text)

        assert len(full_refs) == 2
        assert full_refs["ref1"] == '<ref name="ref1">Content 1</ref>'
        assert full_refs["ref2"] == '<ref name="ref2">Content 2</ref>'

    def test_get_full_refs_with_unnamed_refs(self):
        """Test full refs with unnamed citations (should be excluded)"""
        text = '<ref>Unnamed</ref> <ref name="test">Named</ref>'
        full_refs = get_full_refs(text)

        assert len(full_refs) == 1
        assert "test" in full_refs
        assert full_refs["test"] == '<ref name="test">Named</ref>'

    def test_get_full_refs_empty_text(self):
        """Test full refs with empty text"""
        full_refs = get_full_refs("")
        assert len(full_refs) == 0

    # Tests for get_short_citations function

    def test_get_short_citations(self):
        """Test getting short/self-closing citations"""
        text = '<ref name="ref1"/> Text <ref name="ref2"/>'
        short_refs = get_short_citations(text)

        assert len(short_refs) == 2
        assert short_refs[0].name == "ref1"
        assert short_refs[0].tag == '<ref name="ref1"/>'

    def test_get_short_citations_with_spaces(self):
        """Test short citations with extra spaces"""
        text = '<ref name="test" /> <ref name="test2"/>'
        short_refs = get_short_citations(text)

        assert len(short_refs) == 2
        assert short_refs[0].name == "test"
        assert short_refs[1].name == "test2"

    def test_get_short_citations_empty(self):
        """Test short citations with empty text"""
        short_refs = get_short_citations("")
        assert len(short_refs) == 0

    def test_get_short_citations_mixed_with_full(self):
        """Test extracting short citations mixed with full citations"""
        text = '<ref name="full">Full content</ref> <ref name="short"/>'
        short_refs = get_short_citations(text)

        assert len(short_refs) == 1
        assert short_refs[0].name == "short"
