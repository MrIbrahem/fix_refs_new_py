"""Language-specific bots"""

from __future__ import annotations

from .bg_bot import BulgarianBot
from .es import SpanishBot
from .hy_bot import ArmenianBot
from .pl_bot import PolishBot
from .pt_bot import PortugueseBot
from .sw_bot import SwahiliBot


class LanguageFixerPipeline:
    """Pipeline orchestrator for applying language-specific bot transformations."""

    def __init__(self) -> None:
        self.pl_bot = PolishBot()
        self.pt_bot = PortugueseBot()
        self.bg_bot = BulgarianBot()
        self.es_bot = SpanishBot()
        self.sw_bot = SwahiliBot()
        self.hy_bot = ArmenianBot()

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


__all__ = [
    "LanguageFixerPipeline",
]
