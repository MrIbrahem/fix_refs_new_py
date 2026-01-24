"""
Main fix_page function and interface
"""

from ..bots.remove_duplicate_refs import remove_duplicate_refs_with_attrs
from ..bots.mini_fixes import mini_fixes, mini_fixes_after_fixing
from ..bots.add_lang_en_bot import add_lang_en_to_refs
from ..bots.move_dots import move_dots_after_refs
from ..bots.fix_missing_refs import fix_missing_refs
from ..bots.redirect import is_redirect
from ..mdwiki.category import add_translated_from_mdwiki
from ..infobox.expend_infobox import expand_infobox_in_text
from ..lang_bots import apply_language_fixes
from ..utils.debug import echo_test

def fix_page(
    text: str,
    title: str,
    move_dots: bool,
    infobox: bool,
    add_en_lang: bool,
    lang: str,
    source_title: str = "",
    mdwiki_revid: int = 0
) -> str:
    """Main function to fix Wikipedia page references and formatting

    Args:
        text: Page content
        title: Page title
        move_dots: Whether to move dots after references
        infobox: Whether to expand infobox
        add_en_lang: Whether to add English language parameter
        lang: Language code
        source_title: Source page title
        mdwiki_revid: MDWiki revision ID

    Returns:
        Fixed page content
    """
    text_org = text

    if is_redirect(title, text):
        return text

    if infobox or lang == "es":
        text = expand_infobox_in_text(text, title, "")

    text = mini_fixes(text, lang)
    text = fix_missing_refs(text, source_title, mdwiki_revid)
    text = remove_duplicate_refs_with_attrs(text)

    if move_dots:
        echo_test("move_dots\n")
        text = move_dots_after_refs(text, lang)

    if add_en_lang:
        echo_test("add_en_lang\n")
        text = add_lang_en_to_refs(text)

    text = apply_language_fixes(text, title, lang, source_title, mdwiki_revid)

    text = add_translated_from_mdwiki(text, lang)

    text = mini_fixes_after_fixing(text, lang)

    return text if text else text_org


def fix_refs(text: str, lang: str = "en") -> str:
    """Simple interface to fix references in wikitext

    Args:
        text: WikiText content to fix
        lang: Language code (default: 'en')

    Returns:
        Fixed WikiText content
    """
    return fix_page(
        text=text,
        title="",
        move_dots=True,
        infobox=True,
        add_en_lang=False,
        lang=lang,
        source_title="",
        mdwiki_revid=0
    )
