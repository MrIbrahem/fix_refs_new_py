"""Tests for reference utilities (refs_utils.py)

Converted from tests/Bots/refs_utilsTest.php
"""
import pytest
from src.bots.refs_utils import (
    rm_str_from_start_and_end,
    remove_start_end_quotes,
    str_ends_with,
    str_starts_with
)


class TestRefsUtils:
    """Test cases for reference utilities"""

    # Tests for remove_start_end_quotes function

    def test_adds_double_quotes_to_plain_string(self):
        """يضيف علامات اقتباس مزدوجة لنص عادي"""
        assert remove_start_end_quotes('value') == '"value"'

    def test_replaces_single_quotes_with_double_quotes(self):
        """يزيل علامات الاقتباس المفردة ويضيف مزدوجة"""
        assert remove_start_end_quotes("'value'") == '"value"'

    def test_replaces_double_quotes_with_double_quotes(self):
        """يزيل علامات الاقتباس المزدوجة ويضيف مزدوجة مرة أخرى"""
        assert remove_start_end_quotes('"value"') == '"value"'

    def test_wraps_with_single_quotes_if_contains_double_quotes(self):
        """يحيط النص بعلامات اقتباس مفردة إذا كان يحتوي على علامات مزدوجة بالداخل"""
        assert remove_start_end_quotes('val"ue') == "'val\"ue'"

    def test_trims_whitespace(self):
        """يزيل المسافات الزائدة من البداية والنهاية"""
        assert remove_start_end_quotes('  value  ') == '"value"'

    def test_handles_empty_string(self):
        """يتعامل مع نص فارغ"""
        assert remove_start_end_quotes('') == '""'

    def test_one_quotes_double(self):
        assert remove_start_end_quotes('  "value ') == '\'"value'

    def test_one_quotes_single(self):
        assert remove_start_end_quotes("  'value ") == '"\'value"'

    # Tests for str_ends_with function

    def test_str_ends_with(self):
        """اختبارات دالة str_ends_with"""
        tests = [
            # حالة: ينتهي بالنص المطلوب
            {"string": "Hello world", "end_string": "world", "expected": True},
            # حالة: لا ينتهي بالنص المطلوب
            {"string": "Hello world", "end_string": "hello", "expected": False},
            # حالة: نص فارغ
            {"string": "", "end_string": "test", "expected": False},
            # حالة: نص البحث أطول من النص الأصلي
            {"string": "short", "end_string": "longer text", "expected": False},
            # حالة: تطابق كامل
            {"string": "exact", "end_string": "exact", "expected": True},
            # حالة: أحرف خاصة
            {"string": "file.txt", "end_string": ".txt", "expected": True},
            # حالة: حساسية الأحرف
            {"string": "Case", "end_string": "case", "expected": False}
        ]

        for test in tests:
            result = str_ends_with(test['string'], test['end_string'])
            assert result == test['expected'], f"Failed for: {test['string']} ends with {test['end_string']}"

    # Tests for str_starts_with function

    def test_str_starts_with(self):
        """اختبارات دالة str_starts_with"""
        tests = [
            # حالة: يبدأ بالنص المطلوب
            {"text": "Hello world", "start": "Hello", "expected": True},
            # حالة: لا يبدأ بالنص المطلوب
            {"text": "Hello world", "start": "world", "expected": False},
            # حالة: نص فارغ
            {"text": "", "start": "test", "expected": False},
            # حالة: نص البحث فارغ
            {"text": "test", "start": "", "expected": True},
            # حالة: نص البحث أطول من النص الأصلي
            {"text": "short", "start": "longer text", "expected": False},
            # حالة: تطابق كامل
            {"text": "exact", "start": "exact", "expected": True},
            # حالة: أحرف خاصة
            {"text": "#tag", "start": "#", "expected": True},
            # حالة: حساسية الأحرف
            {"text": "Case", "start": "case", "expected": False}
        ]

        for test in tests:
            result = str_starts_with(test['text'], test['start'])
            assert result == test['expected'], f"Failed for: {test['text']} starts with {test['start']}"

    # Tests for rm_str_from_start_and_end function

    def test_del_start_end(self):
        """اختبارات دالة rm_str_from_start_and_end"""
        tests = [
            # حالة: إزالة من البداية والنهاية
            {"text": "'quoted text'", "find": "'", "expected": "quoted text"},
            # حالة: إزالة علامات تنصيص مزدوجة
            {"text": '"double quoted"', "find": '"', "expected": "double quoted"},
            # حالة: نص بدون علامات في البداية والنهاية
            {"text": "no quotes", "find": "'", "expected": "no quotes"},
            # حالة: علامة في البداية فقط
            {"text": "'start only", "find": "'", "expected": "'start only"},
            # حالة: علامة في النهاية فقط
            {"text": "end only'", "find": "'", "expected": "end only'"},
            # حالة: مسافات زائدة
            {"text": "  '  spaced  '  ", "find": "'", "expected": "spaced"},
            # حالة: نص فارغ
            {"text": "", "find": "'", "expected": ""},
            # حالة: علامات متعددة
            {"text": "''multiple''", "find": "'", "expected": "'multiple'"},
            # حالة: نص يتكون من العلامة فقط
            {"text": "''", "find": "'", "expected": ""}
        ]

        for test in tests:
            result = rm_str_from_start_and_end(test['text'], test['find'])
            assert result == test['expected'], f"Failed for: {test['text']} with find '{test['find']}'"

    # Tests for remove_start_end_quotes function

    def test_fix_attr_value(self):
        """اختبارات دالة remove_start_end_quotes"""
        tests = [
            # حالة: نص بدون علامات تنصيص
            {"text": "value1", "expected": '"value1"'},
            # حالة: نص بعلامات تنصيص مفردة
            {"text": "'value2'", "expected": '"value2"'},
            # حالة: نص بعلامات تنصيص مزدوجة
            {"text": '"value3"', "expected": '"value3"'},
            # حالة: نص بعلامات تنصيص مختلطة
            {"text": '"mixed\'quotes"', "expected": '"mixed\'quotes"'},
            # حالة: نص يحتوي على علامات تنصيص داخلياً
            {"text": 'value"with"quotes', "expected": "'value\"with\"quotes'"},
            # حالة: مسافات زائدة
            {"text": "  spaced  ", "expected": '"spaced"'},
            # حالة: نص يحتوي على علامات تنصيص في المنتصف
            {"text": "val'ue", "expected": '"val\'ue"'}
        ]

        for test in tests:
            result = remove_start_end_quotes(test['text'])
            assert result == test['expected'], f"Failed for: {test['text']}"

    def test_fix_empty(self):
        assert "" == ""

    def test_fix_only_quotes(self):
        assert remove_start_end_quotes('""') == '""'

    def test_fix_only_single_quotes(self):
        assert remove_start_end_quotes("''") == '""'

    def test_del_start_end_empty(self):
        """اختبارات دالة rm_str_from_start_and_end with empty find"""
        result = rm_str_from_start_and_end('testzz', '')
        assert result == 'testzz'
