"""Language-specific bots"""

from __future__ import annotations

import logging

from .es_bot import fix_es
from .es_section_bot import es_section


def fix_es_all(text: str, title: str, source_title: str, mdwiki_revid: int) -> str:
    """Apply all Spanish-specific fixes to text

    Args:
        text: WikiText content
        title: Page title
        source_title: Source page title
        mdwiki_revid: MDWiki revision ID

    Returns:
        Fixed text
    """
    text = fix_es(text, title)
    text = es_section(source_title, text, str(mdwiki_revid))
    return text


__all__ = [
    "fix_es_all",
]
