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
from ..infobox.expend_infobox import Expend_Infobox
from ..lang_bots.pl_bot import pl_fixes
from ..lang_bots.pt_bot import pt_fixes
from ..lang_bots.bg_bot import bg_fixes
from ..lang_bots.es.es_bot import fix_es
from ..lang_bots.es.es_section_bot import es_section
from ..lang_bots.sw_bot import sw_fixes
from ..lang_bots.hy_bot import hy_fixes
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

    if lang == "pl":
        text = pl_fixes(text)

    if infobox or lang == "es":
        echo_test("Expend_Infobox\n")
        text = Expend_Infobox(text, title, "")

    text = mini_fixes(text, lang)
    text = fix_missing_refs(text, source_title, mdwiki_revid)
    text = remove_duplicate_refs_with_attrs(text)

    if move_dots:
        echo_test("move_dots\n")
        text = move_dots_after_refs(text, lang)

    if add_en_lang:
        echo_test("add_en_lang\n")
        text = add_lang_en_to_refs(text)

    if lang == "pt":
        text = pt_fixes(text)

    elif lang == "bg":
        text = bg_fixes(text, source_title, mdwiki_revid)

    elif lang == "es":
        text = fix_es(text, title)
        text = es_section(source_title, text, str(mdwiki_revid))

    elif lang == "sw":
        text = sw_fixes(text)

    elif lang == "hy":
        text = hy_fixes(text)

    if lang != "bg":
        text = add_translated_from_mdwiki(text, lang)

    text = mini_fixes_after_fixing(text, lang)

    return text if text else text_org


def expend_infobox(text: str, title: str, options: str = "") -> str:
    """Expand infobox templates using infobox/expend_infobox module

    Args:
        text: Page content
        title: Page title
        options: Additional options

    Returns:
        Text with expanded infobox
    """

    return Expend_Infobox(text, title, options)


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
