"""
Tests for citation parser
"""

import pytest
from src.parsers.citations import (
    get_citations,
    get_full_refs,
    get_short_citations,
    get_name,
    Citation
)


class TestGetCitations:
    """Test citation extraction"""

    def test_simple_citation(self):
        """Test extracting simple citation"""
        text = '<ref name="test">Content</ref>'
        citations = get_citations(text)
        assert len(citations) == 1
        assert citations[0].get_name() == "test"
        assert citations[0].get_content() == "Content"

    def test_no_citation(self):
        """Test with no citations"""
        text = "No citations here"
        citations = get_citations(text)
        assert len(citations) == 0

    def test_multiple_citations(self):
        """Test extracting multiple citations"""
        text = '<ref name="A">A</ref><ref name="B">B</ref>'
        citations = get_citations(text)
        assert len(citations) == 2
        assert citations[0].get_name() == "A"
        assert citations[1].get_name() == "B"


class TestGetShortCitations:
    """Test short citation extraction"""

    def test_short_citation(self):
        """Test extracting self-closing citation"""
        text = '<ref name="test"/>'
        citations = get_short_citations(text)
        assert len(citations) == 1
        assert citations[0].get_name() == "test"
        assert citations[0].get_content() == ""


class TestGetFullRefs:
    """Test full references mapping"""

    def test_full_refs_mapping(self):
        """Test creating full refs mapping"""
        text = '<ref name="test">Content</ref>'
        refs = get_full_refs(text)
        assert "test" in refs
        assert "Content" in refs["test"]


class TestGetName:
    """Test name extraction from attributes"""

    def test_extract_name_with_quotes(self):
        """Test extracting name with double quotes"""
        options = 'name="test"'
        assert get_name(options) == "test"

    def test_extract_name_single_quotes(self):
        """Test extracting name with single quotes"""
        options = "name='test'"
        assert get_name(options) == "test"

    def test_extract_name_no_quotes(self):
        """Test extracting name without quotes"""
        options = "name=test"
        assert get_name(options) == "test"

    def test_extract_name_empty_options(self):
        """Test with empty options"""
        assert get_name("") == ""

    def test_extract_name_no_name_attr(self):
        """Test when name attribute is missing"""
        options = "lang=en"
        assert get_name(options) == ""


class TestCitation:
    """Test Citation class"""

    def test_citation_to_string(self):
        """Test converting citation to string"""
        citation = Citation(
            content="Test content",
            tag='<ref name="test">Test content</ref>',
            name="test",
            options='name="test"'
        )
        result = citation.to_string()
        assert result == '<ref name="test">Test content</ref>'

    def test_citation_getters(self):
        """Test citation getter methods"""
        citation = Citation(
            content="Content",
            tag="<ref>Content</ref>",
            name="",
            options=""
        )
        assert citation.get_content() == "Content"
        assert citation.get_name() == ""
        assert citation.get_attributes() == ""
        assert citation.get_original_text() == "<ref>Content</ref>"
