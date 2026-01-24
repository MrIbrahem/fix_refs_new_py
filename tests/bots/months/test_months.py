"""
Tests for month handling
"""

import pytest
from src.bots.months import (
    new_date,
    make_date_new_val_pt,
    make_date_new_val_es
)


class TestNewDate:
    """Test date conversion"""

    def test_portuguese_month(self):
        """Test Portuguese month conversion in full date"""
        result = new_date("January 2020", "pt")
        assert result == "janeiro 2020"

    def test_portuguese_full_date(self):
        """Test Portuguese full date with day"""
        result = new_date("15 January 2020", "pt")
        assert "15 de janeiro 2020" == result

    def test_spanish_month(self):
        """Test Spanish month conversion in full date"""
        result = new_date("January 2020", "es")
        assert result == "enero de 2020"

    def test_spanish_full_date_with_de(self):
        """Test Spanish full date uses 'de'"""
        result = new_date("January 2020", "es")
        assert "enero de 2020" == result

    def test_spanish_full_date_with_day(self):
        """Test Spanish full date with day"""
        result = new_date("15 January 2020", "es")
        assert "15 de enero de 2020" == result

    def test_unsupported_language(self):
        """Test with unsupported language"""
        result = new_date("January", "de")
        assert result == "January"

    def test_alternative_date_format(self):
        """Test alternative date format"""
        result = new_date("January 15, 2020", "pt")
        assert "15 de janeiro 2020" == result

    def test_all_months_portuguese(self):
        """Test all months in Portuguese with year"""
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        for month in months:
            result = new_date(f"{month} 2020", "pt")
            assert "2020" in result

    def test_all_months_spanish(self):
        """Test all months in Spanish with year"""
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        for month in months:
            result = new_date(f"{month} 2020", "es")
            assert "de 2020" in result


class TestMakeDateNewValPt:
    """Test Portuguese date wrapper"""

    def test_portuguese_wrapper(self):
        """Test Portuguese date wrapper function"""
        result = make_date_new_val_pt("January 2020")
        assert "janeiro" in result


class TestMakeDateNewValEs:
    """Test Spanish date wrapper"""

    def test_spanish_wrapper(self):
        """Test Spanish date wrapper function"""
        result = make_date_new_val_es("January 2020")
        assert "enero" in result
