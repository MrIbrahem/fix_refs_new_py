"""Tests for fix_page (FixpageTest.php)

Converted from tests/FixpageTest.php
"""
import pytest
from fix_refs.core.fix_page import fix_one_page


class TestFixPage:
    """Test cases for fix_one_page function"""

    def fix_page_wrap(self, text: str, lang: str) -> str:
        """Wrapper function matching PHP test signature"""
        return fix_one_page(
            text=text,
            title="",
            lang=lang,
            move_dots=True,
            expend_infobox=True,
            add_en_lang=False,
            source_title='',
            mdwiki_revid=0,
        )

    def test_part_1(self):
        """Test Armenian text with references and punctuation"""
        input_text = '[[Category:Translated from MDWiki]] ռետինոիդներ։ <ref name="NORD2006" /><ref name="Gli2017" />'
        expected = '[[Category:Translated from MDWiki]] ռետինոիդներ<ref name="NORD2006" /><ref name="Gli2017" />։'
        result = self.fix_page_wrap(input_text, 'hy')
        assert result == expected
