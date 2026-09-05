"""
Tests for citation parser
"""

from fix_refs.parsers.citations import (
    get_all_citations,
    get_full_refs,
    get_short_refs,
)


class TestGetCitations:
    """Test citation extraction"""

    def test_simple_citation(self):
        """Test extracting simple citation"""
        text = '<ref name="test">Content</ref>'
        citations = get_all_citations(text)
        assert len(citations) == 1
        assert citations[0].name == "test"
        assert citations[0].contents == "Content"

    def test_no_citation(self):
        """Test with no citations"""
        text = "No citations here"
        citations = get_all_citations(text)
        assert len(citations) == 0

    def test_multiple_citations(self):
        """Test extracting multiple citations"""
        text = '<ref name="A">A</ref><ref name="B">B</ref>'
        citations = get_all_citations(text)
        assert len(citations) == 2
        assert citations[0].name == "A"
        assert citations[1].name == "B"


class TestGetShortCitations:
    """Test short citation extraction"""

    def test_short_citation(self):
        """Test extracting self-closing citation"""
        text = '<ref name="test"/>'
        citations = get_short_refs(text)
        assert len(citations) == 1
        assert citations[0].name == "test"
        assert citations[0].contents == ""


class TestGetFullRefs:
    """Test full references mapping"""

    def test_full_refs_mapping(self):
        """Test creating full refs mapping"""
        text = '<ref name="test">Content</ref>'
        refs = get_full_refs(text)
        assert "test" in refs
        assert "Content" in refs["test"]
