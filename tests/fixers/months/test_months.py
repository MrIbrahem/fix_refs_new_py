"""
Tests for month handling
"""

from src.fix_refs.fixers.months import MonthTranslator


class TestNewDate:
    """Test date conversion"""

    def test_unsupported_language(self):
        """Test with unsupported language"""
        result = MonthTranslator().new_date("January", "de")
        assert result == "January"
