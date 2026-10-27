"""Language-specific bots"""

from __future__ import annotations

from ...fixers.months import MonthTranslator, fix_months_in_refs
from .es_bot import SpanishTemplateFixer, fix_es
from .es_refs import SpanishRefMover, mv_es_refs
from .es_section_bot import SpanishSectionFixer, es_section


class SpanishBot:
    """Orchestrator bot for Spanish Wikipedia language-specific fixes."""

    def __init__(
        self,
        template_fixer: SpanishTemplateFixer | None = None,
        month_translator: MonthTranslator | None = None,
        ref_mover: SpanishRefMover | None = None,
        section_fixer: SpanishSectionFixer | None = None,
    ) -> None:
        self.template_fixer = template_fixer or SpanishTemplateFixer()
        self.month_translator = month_translator or MonthTranslator()
        self.ref_mover = ref_mover or SpanishRefMover()
        self.section_fixer = section_fixer or SpanishSectionFixer()

    def fix_es_all(self, text: str, title: str, source_title: str, mdwiki_revid: int) -> str:
        """Apply all Spanish-specific fixes to text

        Args:
            text: WikiText content
            title: Page title
            source_title: Source page title
            mdwiki_revid: MDWiki revision ID

        Returns:
            Fixed text
        """
        text = self.template_fixer.fix_es(text, title)
        text = self.month_translator.fix_months_in_refs(text, "es")
        text = self.ref_mover.mv_es_refs(text)
        text = self.section_fixer.es_section(source_title, text, str(mdwiki_revid))
        return text


def fix_es_all(text: str, title: str, source_title: str, mdwiki_revid: int) -> str:
    """Legacy wrapper for SpanishBot.fix_es_all."""
    return SpanishBot().fix_es_all(text, title, source_title, mdwiki_revid)


__all__ = [
    "SpanishBot",
    "fix_es_all",
]
