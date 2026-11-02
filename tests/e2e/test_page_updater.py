
from src.fix_refs.core.fix_page import PageUpdater  # adjust path
from src.fix_refs.core.mapping import LangSetting  # adjust path


def test_page_updater_keeps_custom_ref_body():
    wiki_text = """
{{صندوق معلومات حالة طبية
|مرادفات=Juxta-epiphyseal fracture of the distal phalanx<ref name=Rad2024/>
|مسبب=Forced forward bending of the fingertip, [[crush injury]]<ref name="Rad2024"/>
|عوامل الخطر=
|التشخيص=Based on symptoms, [[X-rays]]<ref name='Rad2024' />
}}
Page lead.<ref name=Rad2024>full ref shouldn't be replaced</ref>
"""
    full_text = "<ref name=Rad2024>original ref from mdwiki.org</ref>"

    result = PageUpdater().run(
        text=wiki_text,
        title="كسر عظمي",
        lang_setting=LangSetting(lang="ar", expend_infobox=True),
        source_title="Juxta-epiphyseal fracture",
        mdwiki_revid=123456,
        source_original_text=full_text,
    )

    assert "full ref shouldn't be replaced" in result
    assert "original ref from mdwiki.org" not in result
