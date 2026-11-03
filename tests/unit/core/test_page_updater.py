"""Tests for page_updater (FixpageTest.php)

Converted from tests/FixpageTest.php
"""

from src.fix_refs.core.mapping import LangSetting
from src.fix_refs.core.page_updater import PageUpdater


class TestPageUpdaterHyLang:
    """Test cases for index processing"""

    def fix_page_wrap(self, text: str, lang: str) -> str:
        """Wrapper function matching PHP test signature"""
        lang_setting = {
            "lang": lang,
            "move_dots": True,
            "expend_infobox": True,
            "add_en_lang": True,
        }

        fixer = PageUpdater()
        return fixer.run(
            text=text,
            title="title",
            source_title="SomeTitle",
            mdwiki_revid=0,
            lang_setting=lang_setting,
        )

    def test_part_3(self):
        """Test simple Armenian text with references"""
        input_text = '[[Category:Translated from MDWiki]] ռետինոիդներ։ <ref name="NORD2006" /><ref name="Gli2017" />'
        expected = '[[Category:Translated from MDWiki]] ռետինոիդներ<ref name="NORD2006" /><ref name="Gli2017" />։'
        result = self.fix_page_wrap(input_text, "hy")
        assert result == expected

    def test_part_4(self):
        """Test Armenian text with complex reference"""
        input_text = '[[Category:Translated from MDWiki]] Այն առաջին անգամ արձանագրվել է 1750 թվականին Ամերիկայում գտնվող քահանա Օլիվեր Հարթի օրագրային գրառման մեջ <ref name="Sc2011">{{Cite book|last=Schachner|first=Lawrence A.|last2=Hansen|first2=Ronald C.|title=Pediatric Dermatology E-Book|date=2011|publisher=Elsevier Health Sciences|isbn=978-0723436652|page=598|url=https://books.google.com/books?id=tAlGLYplkacC&pg=PA598|language=en|url-status=live|archive-url=https://web.archive.org/web/20171105195802/https://books.google.com/books?id=tAlGLYplkacC&pg=PA598|archive-date=November 5, 2017}}</ref>։'
        expected = '[[Category:Translated from MDWiki]] Այն առաջին անգամ արձանագրվել է 1750 թվականին Ամերիկայում գտնվող քահանա Օլիվեր Հարթի օրագրային գրառման մեջ<ref name="Sc2011">{{Cite book|last=Schachner|first=Lawrence A.|last2=Hansen|first2=Ronald C.|title=Pediatric Dermatology E-Book|date=2011|publisher=Elsevier Health Sciences|isbn=978-0723436652|page=598|url=https://books.google.com/books?id=tAlGLYplkacC&pg=PA598|language=en|url-status=live|archive-url=https://web.archive.org/web/20171105195802/https://books.google.com/books?id=tAlGLYplkacC&pg=PA598|archive-date=November 5, 2017}}</ref>։'
        result = self.fix_page_wrap(input_text, "hy")
        assert result == expected


class TestPageUpdaterPages:
    """Test cases for PageUpdater.run function"""

    def fix_page_wrap(self, text: str, lang: str) -> str:
        """Wrapper function matching PHP test signature"""
        lang_setting = LangSetting(
            lang=lang,
            move_dots=True,
            expend_infobox=True,
            add_en_lang=False,
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

    def test_with_move_dots(self):
        """Test with move_dots enabled"""
        input_text = 'Text with dot. <ref name="test">Reference</ref>'
        result = _fix_one(text=input_text, title="", lang="en")
        assert "<ref" in result

    def test_redirect_page(self):
        """Test redirect page is skipped"""
        input_text = "#REDIRECT [[Target Page]]"
        result = _fix_one(text=input_text, title="", lang="en")
        assert result == input_text


def _fix_one(
    text: str,
    title: str,
    lang: str,
) -> str:
    """ """
    lang_setting = {
        "lang": lang,
        "move_dots": True,
        "expend_infobox": True,
        "add_en_lang": False,
    }

    fixer = PageUpdater()

    return fixer.run(
        text=text,
        title=title,
        lang_setting=lang_setting,
    )


class TestPageUpdaterForRefs:
    """Test the main function"""

    def test_hy_language_simple(self):
        """Test Armenian language fixes with simple case"""
        input_text = '[[Category:Translated from MDWiki]] ռետինոիդներ։ <ref name="NORD2006" /><ref name="Gli2017" />'
        expected = '[[Category:Translated from MDWiki]] ռետինոիդներ<ref name="NORD2006" /><ref name="Gli2017" />։'
        result = _fix_one(text=input_text, title="", lang="hy")
        assert result == expected

    def test_empty_text(self):
        """Test with empty text"""
        assert _fix_one(text="", title="", lang="en") == ""

    def test_basic_text_no_refs(self):
        """Test with basic text without references"""
        input_text = "This is a simple text."
        expected = "This is a simple text."
        result = _fix_one(text=input_text, title="", lang="en")
        assert result == expected

    def test_single_ref(self):
        """Test with single reference"""
        input_text = 'Text with <ref name="test1">Reference content</ref> reference.'
        result = _fix_one(text=input_text, title="", lang="en")
        assert "<ref" in result
        assert "</ref>" in result

    def test_duplicate_refs(self):
        """Test duplicate reference removal"""
        input_text = 'Text <ref name="test">Content</ref> and <ref name="test">Content</ref> again.'
        result = _fix_one(text=input_text, title="", lang="en")
        assert result.count("Content") == 1

    def test_multiple_refs(self):
        """Test with multiple references"""
        input_text = '<ref name="A"/>Text<ref name="B"/>More<ref name="A"/>'
        result = _fix_one(text=input_text, title="", lang="en")
        assert "<ref" in result
