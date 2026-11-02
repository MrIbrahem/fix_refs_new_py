"""Tests for fix_page (FixpageTest.php)

Converted from tests/FixpageTest.php
"""

from src.fix_refs.core.fix_page import PageUpdater
from src.fix_refs.core.mapping import LangSetting


class TestFixPage:
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

    def test_page_updater_preserves_custom_body_when_source_original_text_provided(self):
        """References with existing body in target text are not overwritten by source_original_text."""
        updater = PageUpdater()

        wiki_text = """{{صندوق معلومات حالة طبية
|مرادفات=Juxta-epiphyseal fracture of the distal phalanx<ref name=Rad2024/>
|مسبب=Forced forward bending of the fingertip, [[crush injury]]<ref name="Rad2024"/>
|عوامل الخطر=
|التشخيص=Based on symptoms, [[X-rays]]<ref name='Rad2024' />
}}
Page lead.<ref name=Rad2024>full ref shouldn't be replaced</ref>"""

        full_text = """<ref name=Rad2024>original ref from mdwiki.org</ref>"""

        lang_setting = LangSetting(lang="ar", expend_infobox=True)

        updated_text = updater.run(
            text=wiki_text,
            title="كسر عظمي",
            lang_setting=lang_setting,
            source_title="Juxta-epiphyseal fracture",
            mdwiki_revid=123456,
            source_original_text=full_text,
        )

        assert "full ref shouldn't be replaced" in updated_text
        assert "original ref from mdwiki.org" not in updated_text
        # Ensure template short refs retained their attributes without normalization
        assert "<ref name=Rad2024/>" in updated_text
        assert '<ref name="Rad2024"/>' in updated_text
        assert "<ref name='Rad2024' />" in updated_text
