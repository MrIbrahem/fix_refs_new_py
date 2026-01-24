"""Tests for attribute utilities (attrs_utils.py)

Converted from tests/Bots/attrs_utilsTest.php
"""
import pytest
from src.bots.attrs_utils import parse_attributes, get_attrs


class TestAttrsUtils:
    """Test cases for attribute parsing utilities"""

    @pytest.fixture(autouse=True)
    def setup_data(self):
        """Set up test data - equivalent to setUp() in PHP"""
        self.data = {
            'علامات اقتباس مزدوجة': (
                'name="reuters" group="G1"',
                {'name': '"reuters"', 'group': '"G1"'}
            ),
            'علامات اقتباس مفردة': (
                "name='reuters' group='G1'",
                {'name': "'reuters'", 'group': "'G1'"}
            ),
            'بدون علامات اقتباس': (
                'name=reuters group=G1',
                {'name': 'reuters', 'group': 'G1'}
            ),
            'سمات بدون قيمة': (
                'disabled name="test"',
                {'disabled': '', 'name': '"test"'}
            ),
            'مزيج من السمات': (
                'name="reuters" group=\'G1\' access=public disabled',
                {'name': '"reuters"', 'group': "'G1'", 'access': 'public', 'disabled': ''}
            ),
            'مسافات إضافية': (
                '  name = "reuters"   group = G1 ',
                {'name': '"reuters"', 'group': 'G1'}
            ),
            'حالة أحرف مختلفة لأسماء السمات': (
                'Name="reuters" GROUP="G1"',
                {'name': '"reuters"', 'group': '"G1"'}
            ),
            'نص فارغ': (
                '',
                {}
            ),
            'سمة مع شرطة سفلية': (
                'access_date="2023-01-01"',
                {'access_date': '"2023-01-01"'}
            )
        }

    def test_parse_attributes(self):
        """Test parse_attributes function"""
        for name, tab in self.data.items():
            result = parse_attributes(tab[0])
            assert result == tab[1], f"Failed for test case: {name}"

    def test_get_attrs(self):
        """Test get_attrs function"""
        for name, tab in self.data.items():
            result = get_attrs(tab[0])
            assert result == tab[1], f"Failed for test case: {name}"

    def test_get_attrs_alt(self):
        """Test get_attrs with additional test cases"""
        tests = [
            # حالة: سمة واحدة مع قيمة
            {"text": 'name="test"', "expected": {"name": '"test"'}},
            # حالة: سمة واحدة بدون قيمة
            {"text": 'name', "expected": {"name": ""}},
            # حالة: سمات متعددة
            {"text": 'name="test" group="notes"', "expected": {"name": '"test"', "group": '"notes"'}},
            # حالة: سمات مع مسافات زائدة
            {"text": '  name  =  "test"  group  =  "notes"  ', "expected": {"name": '"test"', "group": '"notes"'}},
            # حالة: سمة بعلامات تنصيص مفردة
            {"text": "name='test'", "expected": {"name": "'test'"}},
            # حالة: سمة بدون علامات تنصيص
            {"text": "name=test", "expected": {"name": "test"}},
            # حالة: نص فارغ
            {"text": "", "expected": {}},
            # حالة: سمة تحتوي على مسافات في القيمة
            {"text": 'name="test value"', "expected": {"name": '"test value"'}}
        ]

        for test in tests:
            result = get_attrs(test['text'])
            assert result == test['expected'], f"Failed for text: {test['text']}"
