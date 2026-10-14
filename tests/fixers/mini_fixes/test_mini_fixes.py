"""
Tests for mini fixes
"""

from fix_refs.fixers.mini_fixes import (
    MiniFixes,
)


class TestMiniFixes:
    """Test cases for mini fixes functionality"""

    # Tests for fix_sections_titles

    def test_sections_titles_ru(self):
        """Test section title fixes for Russian language"""
        texts = [
            {
                "old": "== Ссылки  ==\n====Ссылки====\n\n== Примечания 3 ==",
                "new": "== Примечания ==\n==== Примечания ====\n\n== Примечания 3 ==",
            },
            {
                "old": "== Ссылки  ==\n====Ссылки====\n\n== Примечания 3 ==",
                "new": "== Примечания ==\n==== Примечания ====\n\n== Примечания 3 ==",
            },
        ]

        fixer = MiniFixes()
        for tab in texts:
            text = tab["old"]
            new = tab["new"]
            new_text = fixer.fix_sections_titles(text, "ru")
            assert new == new_text, f"Failed for: {text}"

    def test_sections_titles_hr(self):
        """Test section title fixes for Croatian language"""
        texts = [
            {"old": "== Reference  ==", "new": "== Izvori =="},
            {
                "old": "== Reference  ==\n\n====References====\n\n== References 3 ==",
                "new": "== Izvori ==\n\n==== Izvori ====\n\n== References 3 ==",
            },
        ]

        fixer = MiniFixes()
        for tab in texts:
            text = tab["old"]
            new = tab["new"]
            new_text = fixer.fix_sections_titles(text, "hr")
            assert new == new_text, f"Failed for: {text}"

    def test_sections_titles_sw(self):
        """Test section title fixes for Swahili language"""
        text = "== Marejeleo 1 ==\n\n====Marejeleo====\n\n=== Marejeleo ==="
        new = "== Marejeleo 1 ==\n\n==== Marejeo ====\n\n=== Marejeo ==="
        fixer = MiniFixes()
        new_text = fixer.fix_sections_titles(text, "sw")
        assert new == new_text

    # Tests for remove_space_before_ref_tags

    def test_remove_space_before_ref_tags(self):
        """اختبارات دالة remove_space_before_ref_tags"""
        tests = [
            # حالة: مسافة قبل <ref> بعد نقطة
            {"text": "جملة. <ref>مرجع</ref>", "lang": "ar", "expected": "جملة.<ref>مرجع</ref>"},
            # حالة: مسافة قبل <ref> بعد فاصلة
            {"text": "جملة, <ref>مرجع</ref>", "lang": "ar", "expected": "جملة,<ref>مرجع</ref>"},
            # حالة: مسافات متعددة
            {"text": "جملة.   <ref>مرجع</ref>", "lang": "sw", "expected": "جملة.<ref>مرجع</ref>"},
            # حالة: بدون مسافات (لا يجب أن يتغير النص)
            {"text": "جملة.<ref>مرجع</ref>", "lang": "bn", "expected": "جملة.<ref>مرجع</ref>"},
            # حالة: علامات ترقيم مختلفة
            {"text": "جملة। <ref>مرجع</ref>", "lang": "ar", "expected": "جملة।<ref>مرجع</ref>"},
            # حالة: نص بدون مراجع
            {"text": "نص عادي بدون مراجع", "lang": "ar", "expected": "نص عادي بدون مراجع"},
        ]

        fixer = MiniFixes()
        for test in tests:
            result = fixer.remove_space_before_ref_tags(test["text"], test["lang"])
            assert result == test["expected"], f"Failed for: {test['text']}"

    # Tests for refs_tags_spaces

    def test_refs_tags_spaces(self):
        """اختبارات دالة refs_tags_spaces"""
        tests = [
            # حالة: مسافة بين </ref> و <ref>
            {"text": "نص</ref> <ref>مرجع</ref>", "expected": "نص</ref><ref>مرجع</ref>"},
            # حالة: مسافات متعددة
            {"text": "نص</ref>   <ref>مرجع</ref>", "expected": "نص</ref><ref>مرجع</ref>"},
            # حالة: وسم مغلق ذاتيًا
            {"text": 'نص<ref name="test"/> <ref>مرجع</ref>', "expected": 'نص<ref name="test"/><ref>مرجع</ref>'},
            # حالة: مسافة بعد وسم الإغلاق
            {"text": "نص> <ref>مرجع</ref>", "expected": "نص><ref>مرجع</ref>"},
            # حالة: نص بدون مراجع متجاورة
            {"text": "نص عادي <ref>مرجع</ref> ونص آخر", "expected": "نص عادي <ref>مرجع</ref> ونص آخر"},
            # حالة: مراجع متعددة متجاورة
            {"text": "</ref> <ref name=A/> <ref name=B>", "expected": "</ref><ref name=A/><ref name=B>"},
        ]

        fixer = MiniFixes()
        for test in tests:
            result = fixer.refs_tags_spaces(test["text"])
            assert result == test["expected"], f"Failed for: {test['text']}"

    # Tests for fix_prefix

    def test_fix_prefix(self):
        """اختبارات دالة fix_prefix"""
        tests = [
            # حالة: رابط باللغة الإنجليزية
            {"text": "[[:en:Example|مثال]]", "lang": "ar", "expected": "[[Example|مثال]]"},
            # حالة: رابط بنفس لغة النص
            {"text": "[[:ar:مثال|نص]]", "lang": "ar", "expected": "[[مثال|نص]]"},
            # حالة: رابط بلغة أخرى (لا يجب أن يتغير)
            {"text": "[[:fr:Exemple|نص]]", "lang": "ar", "expected": "[[:fr:Exemple|نص]]"},
            # حالة: روابط متعددة
            {"text": "[[:en:Page1|نص1]] و [[:ar:صفحة|نص2]]", "lang": "ar", "expected": "[[Page1|نص1]] و [[صفحة|نص2]]"},
            # حالة: رابط بدون نص بديل
            {"text": "[[:en:Example]]", "lang": "ar", "expected": "[[Example]]"},
            # حالة: نص بدون روابط
            {"text": "نص عادي بدون روابط", "lang": "ar", "expected": "نص عادي بدون روابط"},
        ]
        fixer = MiniFixes()

        for test in tests:
            result = fixer.fix_prefix(test["text"], test["lang"])
            assert result == test["expected"], f"Failed for: {test['text']}"

    def test_minimal_text(self):
        """Test with minimal text"""
        result = MiniFixes().mini_fixes("Test", "en")
        assert "Test" in result


class TestRefsTagsSpaces:
    """Test reference tag spacing fixes"""

    def test_remove_space_between_refs(self):
        """Test removing space between closing and opening refs"""
        text = '</ref> <ref name="test">Content</ref>'
        fixer = MiniFixes()
        result = fixer.refs_tags_spaces(text)
        assert "</ref> <ref" not in result
        assert "</ref><ref" in result

    def test_remove_space_self_closing(self):
        """Test removing space with self-closing ref"""
        text = '<ref name="A"/><ref name="B">Content</ref>'
        fixer = MiniFixes()
        result = fixer.refs_tags_spaces(text)
        assert "/><ref" in result

    def test_remove_space_after_ref(self):
        """Test removing space after ref"""
        text = '> <ref name="test">Content</ref>'
        fixer = MiniFixes()
        result = fixer.refs_tags_spaces(text)
        assert "> <ref" not in result
        assert "><ref" in result


class TestFixSectionsTitles:
    """Test section title fixes"""

    def test_croatian_references(self):
        """Test Croatian translation"""
        text = "==References=="
        fixer = MiniFixes()
        result = fixer.fix_sections_titles(text, "hr")
        assert "== Izvori ==" in result

    def test_swahili_references(self):
        """Test Swahili translation"""
        text = "==References=="
        fixer = MiniFixes()
        result = fixer.fix_sections_titles(text, "sw")
        assert "== Marejeo ==" in result

    def test_no_translation_for_english(self):
        """Test no translation for English"""
        text = "==References=="
        fixer = MiniFixes()
        result = fixer.fix_sections_titles(text, "en")
        assert "==References==" in result


class TestRemoveSpaceBeforeRefTags:
    """Test space removal before ref tags"""

    def test_remove_space_before_dot(self):
        """Test removing space before dot"""
        text = 'Text .<ref name="test">Content</ref>'
        fixer = MiniFixes()
        result = fixer.remove_space_before_ref_tags(text, "en")
        assert "Text.<ref" in result

    def test_remove_space_before_comma(self):
        """Test removing space before comma"""
        text = 'Text ,<ref name="test">Content</ref>'
        fixer = MiniFixes()
        result = fixer.remove_space_before_ref_tags(text, "en")
        assert "Text,<ref" in result


class TestFixPrefix:
    """Test interwiki link prefix fixes"""

    def test_remove_en_prefix(self):
        """Test removing English interwiki prefix"""
        text = "[[:en:Test|Display]]"
        fixer = MiniFixes()
        result = fixer.fix_prefix(text, "en")
        assert "[[Test|Display]]" in result
        assert "[[:en:" not in result

    def test_remove_lang_prefix(self):
        """Test removing language interwiki prefix"""
        text = "[[:es:Prueba|Display]]"
        fixer = MiniFixes()
        result = fixer.fix_prefix(text, "es")
        assert "[[Prueba|Display]]" in result
        assert "[[:es:" not in result


class TestMiniFixesAfterFixing:
    """Test fixes applied after main fixing"""

    def test_remove_empty_lines(self):
        """Test removing empty lines"""
        text = "Line 1\n\n\nLine 2"
        result = MiniFixes().mini_fixes_after_fixing(text, "en")
        assert "\n\n\n" not in result
