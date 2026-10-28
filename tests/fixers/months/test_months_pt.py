"""
Tests for month handling
"""

from src.fix_refs.fixers.months import MonthTranslator


class TestNewDate:
    """Test date conversion"""

    def test_portuguese_month(self):
        """Test Portuguese month conversion in full date"""
        result = MonthTranslator().new_date("January 2020", "pt")
        assert result == "janeiro 2020"

    def test_portuguese_full_date(self):
        """Test Portuguese full date with day"""
        result = MonthTranslator().new_date("15 January 2020", "pt")
        assert "15 de janeiro 2020" == result

    def test_alternative_date_format(self):
        """Test alternative date format"""
        result = MonthTranslator().new_date("January 15, 2020", "pt")
        assert "15 de janeiro 2020" == result

    def test_all_months_portuguese(self):
        """Test all months in Portuguese with year"""
        months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        for month in months:
            result = MonthTranslator().new_date(f"{month} 2020", "pt")
            assert "2020" in result


class TestMakeDateNewValPt:
    """Test new_date with Portuguese date"""

    def test_portuguese_wrapper(self):
        result = MonthTranslator().new_date("January 2020", "pt")
        assert "janeiro" in result
