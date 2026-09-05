"""
Tests for citation parser
"""

from fix_refs.parsers.citations_parser import (
    get_all_citations,
    get_full_refs,
    get_short_refs,
)


class TestGetAllRefs:
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

    def test_get_regex_citations_with_multiple_refs(self):
        """Test extracting multiple citations from text"""
        text = '<ref name="ref1">Content 1</ref> Text <ref name="ref2">Content 2</ref>'
        citations = get_all_citations(text)

        assert len(citations) == 2
        assert citations[0].name == "ref1"
        assert citations[0].contents == "Content 1"
        assert citations[0].tag == '<ref name="ref1">Content 1</ref>'

    def test_get_regex_citations_with_no_refs(self):
        """Test extracting citations from text with no references"""
        text = "No references here"
        citations = get_all_citations(text)
        assert len(citations) == 0

    def test_get_citations_with_no_name(self):
        """Test citations without name attribute"""
        text = "<ref>Content without name</ref>"
        citations = get_all_citations(text)

        assert len(citations) == 1
        assert citations[0].name == ""
        assert citations[0].contents == "Content without name"

    def test_get_citations_with_multiple_attributes(self):
        """Test citations with multiple attributes"""
        text = '<ref name="test" group="notes">Content</ref>'
        citations = get_all_citations(text)

        assert len(citations) == 1
        assert citations[0].name == "test"
        assert "group" in citations[0].attrs


class TestGetShortRefs:
    """Test short citation extraction"""

    def test_short_citation(self):
        """Test extracting self-closing citation"""
        text = '<ref name="test"/>'
        citations = get_short_refs(text)
        assert len(citations) == 1
        assert citations[0].name == "test"
        assert citations[0].contents == ""

    def test_get_short_citations(self):
        """Test getting short/self-closing citations"""
        text = '<ref name="ref1"/> Text <ref name="ref2"/>'
        short_refs = get_short_refs(text)

        assert len(short_refs) == 2
        assert short_refs[0].name == "ref1"
        assert short_refs[0].tag == '<ref name="ref1"/>'

    def test_get_short_citations_with_spaces(self):
        """Test short citations with extra spaces"""
        text = '<ref name="test" /> <ref name="test2"/>'
        short_refs = get_short_refs(text)

        assert len(short_refs) == 2
        assert short_refs[0].name == "test"
        assert short_refs[1].name == "test2"

    def test_get_short_citations_empty(self):
        """Test short citations with empty text"""
        short_refs = get_short_refs("")
        assert len(short_refs) == 0

    def test_get_short_citations_mixed_with_full(self):
        """Test extracting short citations mixed with full citations"""
        text = '<ref name="full">Full content</ref> <ref name="short"/>'
        short_refs = get_short_refs(text)

        assert len(short_refs) == 1
        assert short_refs[0].name == "short"


class TestGetFullRefs:
    """Test full references mapping"""

    def test_full_refs_mapping(self):
        """Test creating full refs mapping"""
        text = '<ref name="test">Content</ref>'
        refs = get_full_refs(text)
        assert "test" in refs
        assert "Content" in refs["test"]

    def test_get_full_refs(self):
        """Test getting full reference mapping"""
        text = '<ref name="ref2"/><ref name="ref1">Content 1</ref> <ref name="ref2">Content 2</ref>'
        full_refs = get_full_refs(text)

        assert len(full_refs) == 2
        assert full_refs["ref1"] == '<ref name="ref1">Content 1</ref>'
        assert full_refs["ref2"] == '<ref name="ref2">Content 2</ref>'

    def test_get_full_refs_with_unnamed_refs(self):
        """Test full refs with unnamed citations (should be excluded)"""
        text = '<ref name="ref2"/><ref>Unnamed</ref> <ref name="test">Named</ref>'
        full_refs = get_full_refs(text)

        assert len(full_refs) == 1
        assert "test" in full_refs
        assert full_refs["test"] == '<ref name="test">Named</ref>'

    def test_get_full_refs_empty_text(self):
        """Test full refs with empty text"""
        full_refs = get_full_refs('<ref name="ref2"/>')
        assert len(full_refs) == 0
