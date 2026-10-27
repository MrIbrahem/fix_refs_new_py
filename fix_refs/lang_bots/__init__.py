"""Language-specific bots"""

from __future__ import annotations

from .bg_bot import BulgarianBot, bg_fixes
from .es import SpanishBot, fix_es_all
from .hy_bot import ArmenianBot, hy_fixes
from .pl_bot import PolishBot, pl_fixes
from .pt_bot import PortugueseBot, pt_fixes
from .sw_bot import SwahiliBot, sw_fixes


class LanguageFixerPipeline:
    """Pipeline orchestrator for applying language-specific bot transformations."""

    def __init__(
        self,
        pl_bot: PolishBot | None = None,
        pt_bot: PortugueseBot | None = None,
        bg_bot: BulgarianBot | None = None,
        es_bot: SpanishBot | None = None,
        sw_bot: SwahiliBot | None = None,
        hy_bot: ArmenianBot | None = None,
    ) -> None:
        self.pl_bot = pl_bot or PolishBot()
        self.pt_bot = pt_bot or PortugueseBot()
        self.bg_bot = bg_bot or BulgarianBot()
        self.es_bot = es_bot or SpanishBot()
        self.sw_bot = sw_bot or SwahiliBot()
        self.hy_bot = hy_bot or ArmenianBot()

    def apply_language_fixes(self, text: str, title: str, lang: str, source_title: str, mdwiki_revid: int) -> str:
        """Apply language-specific transformations to text.

        Args:
            text: WikiText content
            title: Page title
            lang: Language code
            source_title: Source page title
            mdwiki_revid: MDWiki revision ID

        Returns:
            Transformed text
        """
        if lang == "pl":
            text = self.pl_bot.pl_fixes(text)

        elif lang == "pt":
            text = self.pt_bot.pt_fixes(text)

        elif lang == "bg":
            text = self.bg_bot.bg_fixes(text, source_title, mdwiki_revid)

        elif lang == "es":
            text = self.es_bot.fix_es_all(text, title, source_title, mdwiki_revid)

        elif lang == "sw":
            text = self.sw_bot.sw_fixes(text)

        elif lang == "hy":
            text = self.hy_bot.hy_fixes(text)

        return text


def apply_language_fixes(text, title, lang, source_title, mdwiki_revid) -> str:
    """Legacy wrapper for LanguageFixerPipeline.apply_language_fixes."""
    return LanguageFixerPipeline().apply_language_fixes(text, title, lang, source_title, mdwiki_revid)


__all__ = [
    "LanguageFixerPipeline",
    "apply_language_fixes",
]
