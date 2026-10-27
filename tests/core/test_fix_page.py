"""Tests for fix_page (FixpageTest.php)

Converted from tests/FixpageTest.php
"""

from fix_refs.core.fix_page import LangSetting, PageFixer


class TestFixPage:
    """Test cases for PageFixer.run function"""

    def fix_page_wrap(self, text: str, lang: str) -> str:
        """Wrapper function matching PHP test signature"""
        lang_setting = LangSetting(
            lang=lang,
            move_dots=True,
            expend_infobox=True,
            add_en_lang=False,
            add_category=False,
        )

        fixer = PageFixer(
            text=text,
            title="title",
            source_title="",
            mdwiki_revid=0,
            lang_setting=lang_setting,
        )
        return fixer.run()

    def test_part_1(self):
        """Test Armenian text with references and punctuation"""
        input_text = '[[Category:Translated from MDWiki]] ռետինոիդներ։ <ref name="NORD2006" /><ref name="Gli2017" />'
        expected = '[[Category:Translated from MDWiki]] ռետինոիդներ<ref name="NORD2006" /><ref name="Gli2017" />։'
        result = self.fix_page_wrap(input_text, "hy")
        assert result == expected
