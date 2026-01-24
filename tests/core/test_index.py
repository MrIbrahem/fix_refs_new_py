"""Tests for index (indexTest.php)

Converted from tests/indexTest.php
"""
from src.core.fix_page import fix_page


class TestIndex:
    """Test cases for index processing"""

    def fix_page_wrap(self, text: str, lang: str, move_dots: bool, infobox: bool, add_en_lang: bool) -> str:
        """Wrapper function matching PHP test signature"""
        return fix_page(text, "title", move_dots, infobox, add_en_lang, lang, 'SomeTitle', 0)

    def test_part_3(self):
        """Test simple Armenian text with references"""
        input_text = '[[Category:Translated from MDWiki]] ռետինոիդներ։ <ref name="NORD2006" /><ref name="Gli2017" />'
        expected = '[[Category:Translated from MDWiki]] ռետինոիդներ<ref name="NORD2006" /><ref name="Gli2017" />։'
        result = self.fix_page_wrap(input_text, 'hy', True, True, True)
        assert result == expected

    def test_part_4(self):
        """Test Armenian text with complex reference"""
        input_text = '[[Category:Translated from MDWiki]] Այն առաջին անգամ արձանագրվել է 1750 թվականին Ամերիկայում գտնվող քահանա Օլիվեր Հարթի օրագրային գրառման մեջ <ref name="Sc2011">{{Cite book|last=Schachner|first=Lawrence A.|last2=Hansen|first2=Ronald C.|title=Pediatric Dermatology E-Book|date=2011|publisher=Elsevier Health Sciences|isbn=978-0723436652|page=598|url=https://books.google.com/books?id=tAlGLYplkacC&pg=PA598|language=en|url-status=live|archive-url=https://web.archive.org/web/20171105195802/https://books.google.com/books?id=tAlGLYplkacC&pg=PA598|archive-date=November 5, 2017}}</ref>։'
        expected = '[[Category:Translated from MDWiki]] Այն առաջին անգամ արձանագրվել է 1750 թվականին Ամերիկայում գտնվող քահանա Օլիվեր Հարթի օրագրային գրառման մեջ<ref name="Sc2011">{{Cite book|last=Schachner|first=Lawrence A.|last2=Hansen|first2=Ronald C.|title=Pediatric Dermatology E-Book|date=2011|publisher=Elsevier Health Sciences|isbn=978-0723436652|page=598|url=https://books.google.com/books?id=tAlGLYplkacC&pg=PA598|language=en|url-status=live|archive-url=https://web.archive.org/web/20171105195802/https://books.google.com/books?id=tAlGLYplkacC&pg=PA598|archive-date=November 5, 2017}}</ref>։'
        result = self.fix_page_wrap(input_text, 'hy', True, True, True)
        assert result == expected
