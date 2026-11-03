from src.fix_refs.core.mapping import LangSetting
from src.fix_refs.core.page_updater import PageUpdater

WIKI_TEXT_SOURCE = """
{{صندوق معلومات حالة طبية
|مرادفات=Juxta-epiphyseal fracture of the distal phalanx<ref name=Rad2024/>
|مسبب=Forced forward bending of the fingertip, [[crush injury]]<ref name="Rad2024"/>
|عوامل الخطر=
|التشخيص=Based on symptoms, [[X-rays]]<ref name='Rad2024' />
}}
Page lead.<ref name=Rad2024>full ref shouldn't be replaced</ref>
"""

FULL_TEXT = "<ref name=Rad2024>original ref from mdwiki.org</ref>"

OVERWRITE_EXPECTED = """{{صندوق معلومات حالة طبية
|مرادفات=Juxta-epiphyseal fracture of the distal phalanx<ref name=Rad2024/>
|مسبب=Forced forward bending of the fingertip, [[crush injury]]<ref name="Rad2024"/>
|عوامل الخطر=
|التشخيص=Based on symptoms, [[X-rays]]<ref name='Rad2024' />
}}
Page lead<ref name=Rad2024>original ref from mdwiki.org</ref>."""


def test_page_updater_keeps_custom_ref_body():
    result = PageUpdater().run(
        text=WIKI_TEXT_SOURCE,
        title="كسر عظمي",
        lang_setting=LangSetting(lang="ar", expend_infobox=True, overwrite_refs=False),
        source_title="Juxta-epiphyseal fracture",
        mdwiki_revid=123456,
        source_original_text=FULL_TEXT,
    )

    assert "full ref shouldn't be replaced" in result
    assert "original ref from mdwiki.org" not in result


def test_page_updater_overwrite_custom_ref_body():
    result = PageUpdater().run(
        text=WIKI_TEXT_SOURCE,
        title="كسر عظمي",
        lang_setting=LangSetting(lang="ar", expend_infobox=True, overwrite_refs=True),
        source_title="Juxta-epiphyseal fracture",
        mdwiki_revid=123456,
        source_original_text=FULL_TEXT,
    )
    assert result.strip() == OVERWRITE_EXPECTED.strip()
