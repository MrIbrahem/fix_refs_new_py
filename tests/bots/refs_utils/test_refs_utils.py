"""
Tests for reference utilities
"""

import pytest
from src.bots.refs_utils import (
    str_ends_with,
    str_starts_with,
    rm_str_from_start_and_end,
    remove_start_end_quotes
)


class TestStrEndsWith:
    """Test str_ends_with function"""

    def test_ends_with_true(self):
        """Test when string ends with substring"""
        assert str_ends_with("Hello World", "World") is True

    def test_ends_with_false(self):
        """Test when string doesn't end with substring"""
        assert str_ends_with("Hello World", "Hello") is False

    def test_ends_with_empty(self):
        """Test with empty substring"""
        assert str_ends_with("Test", "") is True


class TestStrStartsWith:
    """Test str_starts_with function"""

    def test_starts_with_true(self):
        """Test when string starts with substring"""
        assert str_starts_with("Hello World", "Hello") is True

    def test_starts_with_false(self):
        """Test when string doesn't start with substring"""
        assert str_starts_with("Hello World", "World") is False

    def test_starts_with_empty(self):
        """Test with empty substring"""
        assert str_starts_with("Test", "") is True


class TestRmStrFromStartAndEnd:
    """Test removing string from start and end"""

    def test_remove_quotes(self):
        """Test removing quotes from both ends"""
        result = rm_str_from_start_and_end('"test"', '"')
        assert result == "test"

    def test_no_match(self):
        """Test when string not at both ends"""
        result = rm_str_from_start_and_end("testx", "test")
        assert result == "testx"

    def test_empty_find(self):
        """Test with empty find string"""
        result = rm_str_from_start_and_end("test", "")
        assert result == "test"


class TestRemoveStartEndQuotes:
    """Test normalizing quotes"""

    def test_double_quotes(self):
        """Test with double quotes"""
        result = remove_start_end_quotes('"test"')
        assert result == '"test"'

    def test_single_quotes(self):
        """Test with single quotes"""
        result = remove_start_end_quotes("'test'")
        assert result == '"test"'

    def test_no_quotes(self):
        """Test without quotes"""
        result = remove_start_end_quotes("test")
        assert result == '"test"'

    def test_mixed_quotes(self):
        """Test removing both types of quotes"""
        result = remove_start_end_quotes('"\'test\'"')
        assert result.startswith('"')
        assert result.endswith('"')
