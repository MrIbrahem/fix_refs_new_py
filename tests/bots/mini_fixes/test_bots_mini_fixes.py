"""Tests for mini fixes (mini_fixes.py)

Converted from tests/Bots/mini_fixes_botTest.php
"""
import pytest
from src.bots.mini_fixes import (
    fix_sections_titles,
    remove_space_before_ref_tags,
    refs_tags_spaces,
    fix_prefix
)


class TestMiniFixes:
    """Test cases for mini fixes functionality"""

    # Tests for fix_sections_titles

    def test_sections_titles_ru(self):
        """Test section title fixes for Russian language"""
        texts = [
            {
                "old": "== Ссылки  ==\n====Ссылки====\n\n== Примечания 3 ==",
                "new": "== Примечания ==\n==== Примечания ====\n\n== Примечания 3 =="
            },
            {
                "old": "== Ссылки  ==\n====Ссылки====\n\n== Примечания 3 ==",
                "new": "== Примечания ==\n==== Примечания ====\n\n== Примечания 3 =="
            }
        ]

        for tab in texts:
            text = tab['old']
            new = tab['new']
            new_text = fix_sections_titles(text, "ru")
            assert new == new_text, f"Failed for: {text}"

    def test_sections_titles_hr(self):
        """Test section title fixes for Croatian language"""
        texts = [
            {
                "old": "== Reference  ==",
                "new": "== Izvori =="
            },
            {
                "old": "== Reference  ==\n\n====References====\n\n== References 3 ==",
                "new": "== Izvori ==\n\n==== Izvori ====\n\n== References 3 =="
            }
        ]

        for tab in texts:
            text = tab['old']
            new = tab['new']
            new_text = fix_sections_titles(text, "hr")
            assert new == new_text, f"Failed for: {text}"

    def test_sections_titles_sw(self):
        """Test section title fixes for Swahili language"""
        text = "== Marejeleo 1 ==\n\n====Marejeleo====\n\n=== Marejeleo ==="
        new = "== Marejeleo 1 ==\n\n==== Marejeo ====\n\n=== Marejeo ==="
        new_text = fix_sections_titles(text, "sw")
        assert new == new_text

    # Tests for remove_space_before_ref_tags

    def test_remove_space_before_ref_tags(self):
        """اختبارات دالة remove_space_before_ref_tags"""
        tests = [
            # حالة: مسافة قبل <ref> بعد نقطة
            {
                "text": "جملة. <ref>مرجع</ref>",
                "lang": "ar",
                "expected": "جملة.<ref>مرجع</ref>"
            },
            # حالة: مسافة قبل <ref> بعد فاصلة
            {
                "text": "جملة, <ref>مرجع</ref>",
                "lang": "ar",
                "expected": "جملة,<ref>مرجع</ref>"
            },
            # حالة: مسافات متعددة
            {
                "text": "جملة.   <ref>مرجع</ref>",
                "lang": "sw",
                "expected": "جملة.<ref>مرجع</ref>"
            },
            # حالة: بدون مسافات (لا يجب أن يتغير النص)
            {
                "text": "جملة.<ref>مرجع</ref>",
                "lang": "bn",
                "expected": "جملة.<ref>مرجع</ref>"
            },
            # حالة: علامات ترقيم مختلفة
            {
                "text": "جملة। <ref>مرجع</ref>",
                "lang": "ar",
                "expected": "جملة।<ref>مرجع</ref>"
            },
            # حالة: نص بدون مراجع
            {
                "text": "نص عادي بدون مراجع",
                "lang": "ar",
                "expected": "نص عادي بدون مراجع"
            }
        ]

        for test in tests:
            result = remove_space_before_ref_tags(test['text'], test['lang'])
            assert result == test['expected'], f"Failed for: {test['text']}"

    # Tests for refs_tags_spaces

    def test_refs_tags_spaces(self):
        """اختبارات دالة refs_tags_spaces"""
        tests = [
            # حالة: مسافة بين </ref> و <ref>
            {
                "text": "نص</ref> <ref>مرجع</ref>",
                "expected": "نص</ref><ref>مرجع</ref>"
            },
            # حالة: مسافات متعددة
            {
                "text": "نص</ref>   <ref>مرجع</ref>",
                "expected": "نص</ref><ref>مرجع</ref>"
            },
            # حالة: وسم مغلق ذاتيًا
            {
                "text": 'نص<ref name="test"/> <ref>مرجع</ref>',
                "expected": 'نص<ref name="test"/><ref>مرجع</ref>'
            },
            # حالة: مسافة بعد وسم الإغلاق
            {
                "text": "نص> <ref>مرجع</ref>",
                "expected": "نص><ref>مرجع</ref>"
            },
            # حالة: نص بدون مراجع متجاورة
            {
                "text": "نص عادي <ref>مرجع</ref> ونص آخر",
                "expected": "نص عادي <ref>مرجع</ref> ونص آخر"
            },
            # حالة: مراجع متعددة متجاورة
            {
                "text": "</ref> <ref name=A/> <ref name=B>",
                "expected": "</ref><ref name=A/><ref name=B>"
            }
        ]

        for test in tests:
            result = refs_tags_spaces(test['text'])
            assert result == test['expected'], f"Failed for: {test['text']}"

    # Tests for fix_prefix

    def test_fix_prefix(self):
        """اختبارات دالة fix_prefix"""
        tests = [
            # حالة: رابط باللغة الإنجليزية
            {
                "text": "[[:en:Example|مثال]]",
                "lang": "ar",
                "expected": "[[Example|مثال]]"
            },
            # حالة: رابط بنفس لغة النص
            {
                "text": "[[:ar:مثال|نص]]",
                "lang": "ar",
                "expected": "[[مثال|نص]]"
            },
            # حالة: رابط بلغة أخرى (لا يجب أن يتغير)
            {
                "text": "[[:fr:Exemple|نص]]",
                "lang": "ar",
                "expected": "[[:fr:Exemple|نص]]"
            },
            # حالة: روابط متعددة
            {
                "text": "[[:en:Page1|نص1]] و [[:ar:صفحة|نص2]]",
                "lang": "ar",
                "expected": "[[Page1|نص1]] و [[صفحة|نص2]]"
            },
            # حالة: رابط بدون نص بديل
            {
                "text": "[[:en:Example]]",
                "lang": "ar",
                "expected": "[[Example]]"
            },
            # حالة: نص بدون روابط
            {
                "text": "نص عادي بدون روابط",
                "lang": "ar",
                "expected": "نص عادي بدون روابط"
            }
        ]

        for test in tests:
            result = fix_prefix(test['text'], test['lang'])
            assert result == test['expected'], f"Failed for: {test['text']}"
