"""
Tests for attribute utilities
"""

import pytest
from src.bots.attrs_utils import (
    parse_attributes,
    get_attrs
)


class TestParseAttributes:
    """Test attribute parsing"""

    def test_parse_simple_attribute(self):
        """Test parsing simple attribute"""
        attrs = parse_attributes('name="test"')
        assert "name" in attrs
        assert attrs["name"] == '"test"'

    def test_parse_multiple_attributes(self):
        """Test parsing multiple attributes"""
        attrs = parse_attributes('name="test" lang="en"')
        assert "name" in attrs
        assert "lang" in attrs
        assert attrs["lang"] == '"en"'

    def test_parse_empty_string(self):
        """Test parsing empty string"""
        attrs = parse_attributes("")
        assert len(attrs) == 0


class TestGetAttrs:
    """Test getting attributes"""

    def test_get_name_attribute(self):
        """Test getting name attribute"""
        attrs = get_attrs('name="test"')
        assert "name" in attrs

    def test_get_multiple_attrs(self):
        """Test getting multiple attributes"""
        attrs = get_attrs('name="test" lang="en" group="A"')
        assert len(attrs) >= 3

    def test_case_insensitive(self):
        """Test case insensitivity of attribute names"""
        attrs = get_attrs('NAME="test"')
        assert "name" in attrs

    def test_empty_attrs(self):
        """Test with empty attributes"""
        attrs = get_attrs("")
        assert len(attrs) == 0
