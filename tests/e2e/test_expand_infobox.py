import pytest
from src.fix_refs.core.mapping import LangSetting
from src.fix_refs.core.page_updater import PageUpdater
from src.fix_refs.infobox.expend_infobox import InfoboxExpander

WIKI_TEXT_SOURCE = """{{Databox}}

'''Croup''' ({{IPAc-en|k|ɹ|uː|p|}} {{respell|KROOP}}; from [[Southern Scots|southeastern Scots]], {{tooltip|prob.|probably}} echoic)"""


def test_page_updater():
    result = PageUpdater().run(
        text=WIKI_TEXT_SOURCE,
        title="Croup",
        lang_setting=LangSetting(lang="gpe", expend_infobox=True, overwrite_refs=False),
        source_title="Croup",
        mdwiki_revid=1501413,
        source_original_text=WIKI_TEXT_SOURCE,
    )

    assert result.strip() == WIKI_TEXT_SOURCE.strip()


def test_infobox_expander():
    result = InfoboxExpander().expand_infobox_in_text(WIKI_TEXT_SOURCE, "Croup")

    assert result.strip() == WIKI_TEXT_SOURCE.strip()


@pytest.mark.skip(reason="This test is not implemented yet")
def test_infobox_expander_template_only():
    text = "{{IPAc-en|k|ɹ|uː|p|}}"
    result = InfoboxExpander().expand_infobox_in_text(text, "Croup")

    assert result.strip() == text.strip()


def test_extract_text_before_triple_single_quote():
    result = InfoboxExpander().extract_text_before_triple_single_quote(WIKI_TEXT_SOURCE)

    assert result.strip() == "{{Databox}}"
