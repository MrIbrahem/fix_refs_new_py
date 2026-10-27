"""
Tests for core fix_page functionality
"""

from src.fix_refs.core.fix_page import LangSetting, PageUpdater


def _fix_one(
    *,
    text: str,
    title: str,
    source_title: str = "",
    mdwiki_revid: int | str = 0,
    lang_setting: LangSetting | None = None,
    lang: str,
    move_dots: bool = True,
    expend_infobox: bool = True,
    add_en_lang: bool = False,
    add_category: bool = False,
) -> str:
    """
    Backward-compatible wrapper around PageUpdater.

    If ``lang_setting`` is given it takes precedence; otherwise one is built
    from the individual keyword arguments (kept for backward compatibility).
    """
    if lang_setting is None:
        lang_setting = LangSetting(
            lang=lang,
            move_dots=move_dots,
            expend_infobox=expend_infobox,
            add_en_lang=add_en_lang,
            add_category=add_category,
        )

    fixer = PageUpdater()

    return fixer.run(
        text=text,
        title=title,
        source_title=source_title,
        mdwiki_revid=mdwiki_revid,
        lang_setting=lang_setting,
    )


class TestFixRefs:
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


class TestFixPage:
    """Test the main function with full parameters"""

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
