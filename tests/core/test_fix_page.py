"""Tests for fix_page (FixpageTest.php)

Converted from tests/FixpageTest.php
"""

from src.fix_refs.core.fix_page import PageUpdater
from src.fix_refs.core.mapping import LangSetting, PageContext


class TestFixPage:
    """Test cases for PageUpdater.run function"""

    def fix_page_wrap(self, text: str, lang: str) -> str:
        """Wrapper function matching PHP test signature"""
        lang_setting = LangSetting(
            lang=lang,
            move_dots=True,
            expend_infobox=True,
            add_en_lang=False,
            add_category=False,
        )

        fixer = PageUpdater()
        return fixer.run(
            text=text,
            title="title",
            source_title="",
            mdwiki_revid=0,
            lang_setting=lang_setting,
        )

    def test_part_1(self):
        """Test Armenian text with references and punctuation"""
        input_text = '[[Category:Translated from MDWiki]] ռետինոիդներ։ <ref name="NORD2006" /><ref name="Gli2017" />'
        expected = '[[Category:Translated from MDWiki]] ռետինոիդներ<ref name="NORD2006" /><ref name="Gli2017" />։'
        result = self.fix_page_wrap(input_text, "hy")
        assert result == expected

    def test_move_dots(self, monkeypatch):
        updater = PageUpdater()
        monkeypatch.setattr(updater.dots_mover, "move_dots_after_refs", lambda t, lang: t + "!")
        ctx = PageContext(text="abc", title="t", lang_setting=LangSetting(lang="de"))
        updater._move_dots(ctx)
        assert ctx.text == "abc!"
