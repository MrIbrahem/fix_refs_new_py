"""
Main fix_one_page function and interface
"""

from ..bots.add_lang_en_bot import add_lang_en_to_refs
from ..bots.fix_missing_refs import fix_missing_refs
from ..bots.mini_fixes import mini_fixes, mini_fixes_after_fixing
from ..bots.move_dots import move_dots_after_refs
from ..bots.redirect import is_redirect
from ..bots.remove_duplicate_refs import remove_duplicate_refs_with_attrs
from ..infobox.expend_infobox import expand_infobox_in_text
from ..lang_bots import apply_language_fixes
from ..mdwiki.category import add_translated_from_mdwiki
from ..utils.debug import echo_test


def expand_infobox_if_needed(text, title, lang, expend_infobox):
    if expend_infobox or lang == "es":
        text = expand_infobox_in_text(text, title, "")
    return text


def fix_one_page(
    text: str,
    title: str,
    lang: str,
    move_dots: bool = True,
    expend_infobox: bool = True,
    add_en_lang: bool = False,
    add_category: bool = False,
    source_title: str = "",
    mdwiki_revid: int = 0,
) -> str:
    """Main function to fix Wikipedia page references and formatting

    Args:
        text: Page content
        title: Page title
        move_dots: Whether to move dots after references
        infobox: Whether to expand infobox
        add_en_lang: Whether to add English language parameter
        add_category: Whether to add category for MDWiki translations
        lang: Language code
        source_title: Source page title
        mdwiki_revid: MDWiki revision ID

    Returns:
        Fixed page content
    """
    text_org = text

    if is_redirect(title, text):
        return text

    text = expand_infobox_if_needed(text, title, lang, expend_infobox)

    text = mini_fixes(text, lang)
    text = fix_missing_refs(text, source_title, mdwiki_revid)
    text = remove_duplicate_refs_with_attrs(text)

    if move_dots:
        echo_test("move_dots\n")
        text = move_dots_after_refs(text, lang)

    if add_en_lang:
        echo_test("add_en_lang\n")
        text = add_lang_en_to_refs(text)

    text_with_lang_fixes = apply_language_fixes(text, title, lang, source_title, mdwiki_revid)

    if text_with_lang_fixes:
        text = text_with_lang_fixes
        # Re-expand infobox if language fixes made changes
        text = expand_infobox_if_needed(text, title, lang, expend_infobox)

    if add_category:
        text = add_translated_from_mdwiki(text, lang)

    text = mini_fixes_after_fixing(text, lang)

    if not text.strip():
        return text_org

    return text
