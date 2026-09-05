"""Language-specific bots"""

from .bg_bot import bg_fixes
from .es import fix_es_all
from .hy_bot import hy_fixes
from .pl_bot import pl_fixes
from .pt_bot import pt_fixes
from .sw_bot import sw_fixes


def apply_language_fixes(text, title, lang, source_title, mdwiki_revid) -> str:

    if lang == "pl":
        text = pl_fixes(text)

    elif lang == "pt":
        text = pt_fixes(text)

    elif lang == "bg":
        text = bg_fixes(text, source_title, mdwiki_revid)

    elif lang == "es":
        text = fix_es_all(text, title, source_title, mdwiki_revid)

    elif lang == "sw":
        text = sw_fixes(text)

    elif lang == "hy":
        text = hy_fixes(text)

    return text


__all__ = [
    "apply_language_fixes",
]
