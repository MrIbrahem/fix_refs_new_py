"""Core functionality"""

from __future__ import annotations

from .fix_page import fix_one_page
from .settings import load_settings


def DoChangesToText1(
    source_title: str,
    title: str,
    text: str,
    lang: str,
    mdwiki_revid: int | str,
) -> str:
    """
    Apply configured text modifications to a specific page based on language settings.

    This function loads global settings, retrieves the configuration for the
    specified language, and parses boolean flags for various text transformation
    rules. It then delegates the actual text processing to the `fix_one_page`
    function with these parsed parameters.

    Args:
        source_title (str): The original title of the source page.
        title (str): The title of the target page to be processed.
        text (str): The raw text content of the page to be modified.
        lang (str): The language code, used to fetch language-specific settings.
        mdwiki_revid (int | str): The revision ID of the page from the MDWiki.

    Returns:
        str: The modified text content after applying all specified changes.
    """
    setting = load_settings()
    lang_default = setting.get(lang, {})

    move_dots = bool(int(lang_default.get("move_dots", 0)))
    expand = bool(int(lang_default.get("expend", 1))) or True
    add_en_lang = bool(int(lang_default.get("add_en_lang", 0)))

    return fix_one_page(
        text=text,
        title=title,
        lang=lang,
        move_dots=move_dots,
        expend_infobox=expand,
        add_en_lang=add_en_lang,
        source_title=source_title,
        mdwiki_revid=mdwiki_revid,
    )
