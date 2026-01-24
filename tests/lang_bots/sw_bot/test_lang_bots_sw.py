"""Tests for Swahili bot (swTest.php)

Converted from tests/swTest.php
"""
import pytest
from src.lang_bots.sw_bot import sw_fixes


class TestSwFixes:
    """Test cases for Swahili bot fixes"""

    def test_fix_temps_and_months_1(self):
        assert sw_fixes("== Marejeleo ==") == "== Marejeo =="

    def test_fix_temps_and_months_2(self):
        assert sw_fixes("==Marejeleo==") == "== Marejeo =="

    def test_extra_spaces_around_the_word(self):
        assert sw_fixes("====   Marejeleo   ====") == "==== Marejeo ===="

    def test_case_insensitivity_mixed(self):
        assert sw_fixes("====== MaReJeLeO ======") == "====== Marejeo ======"

    def test_additional_text(self):
        assert sw_fixes("== Marejeleo na Maoni ==") == "== Marejeleo na Maoni =="

    def test_sw_fixes_comprehensive(self):
        tests = [
            # Case: Case insensitivity (lowercase)
            {
                "input": "=== marejeleo ===",
                "expected": "=== Marejeo ==="
            },
            # Case: Multiple occurrences
            {
                "input": "== Marejeleo ==\nSome text\n== marejeleo ==",
                "expected": "== Marejeo ==\nSome text\n== Marejeo =="
            },
            # Case: In the middle of content
            {
                "input": "This is a section: == Marejeleo ==",
                "expected": "This is a section: == Marejeo =="
            },
            # Case: Similar word that should NOT be replaced
            {
                "input": "== MarejeleoMengine ==",
                "expected": "== MarejeleoMengine =="
            },
            # Case: Different word that should NOT be replaced
            {
                "input": "=== Viungo ===",
                "expected": "=== Viungo ==="
            },
            # Case: Empty string
            {
                "input": "",
                "expected": ""
            },
            # Case: No matching pattern
            {
                "input": "This is just regular text",
                "expected": "This is just regular text"
            },
            # Case: Multiple spaces between equals and word
            {
                "input": "==     Marejeleo     ==",
                "expected": "== Marejeo =="
            },
            # Case: Tabs instead of spaces
            {
                "input": "==\tMarejeleo\t==",
                "expected": "== Marejeo =="
            },
            # Case: Mixed whitespace
            {
                "input": "== \t \n Marejeleo \n \t ==",
                "expected": "== Marejeo =="
            },
            # Case: Multiple occurrences in one line
            {
                "input": "== Marejeleo == and == marejeleo ==",
                "expected": "== Marejeleo == and == Marejeo =="
            }
        ]

        for test in tests:
            result = sw_fixes(test['input'])
            assert result == test['expected'], f"Failed for: {test['input']}"
