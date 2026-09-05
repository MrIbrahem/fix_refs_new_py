"""Core functionality"""

from __future__ import annotations

from .fix_page import fix_one_page
from .settings import load_settings


def DoChangesToText1(source_title: str, title: str, text: str, lang: str, mdwiki_revid: int | str) -> str:

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
