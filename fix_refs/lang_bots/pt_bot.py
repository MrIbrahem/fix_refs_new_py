"""
Portuguese-specific bot fixes
"""

from __future__ import annotations

import logging
import re

from ..fixers.months import MonthTranslator

logger = logging.getLogger(__name__)


class PortugueseBot:
    """Bot for Portuguese Wikipedia language-specific fixes."""

    def __init__(self, month_translator: MonthTranslator | None = None) -> None:
        self.month_translator = month_translator or MonthTranslator()

    def rm_ref_spaces(self, newtext: str) -> str:
        """Remove spaces between punctuation and ref tags

        Args:
            newtext: Text to process

        Returns:
            Text with spaces removed
        """
        dot = r"(\.|,|。|।)"
        regline = r"((?:\s*<ref[\s\S]+?(?:<\/ref|\/)>)+)"
        pattern = r"\s*" + dot + r"\s*" + regline
        replacement = r"\1\2"

        newtext = re.sub(pattern, replacement, newtext)

        return newtext

    def pt_fixes(self, text: str) -> str:
        """Apply Portuguese-specific fixes to text

        Args:
            text: WikiText content

        Returns:
            Fixed text
        """
        text = self.month_translator.fix_months_in_refs(text, "pt")
        text = self.rm_ref_spaces(text)
        return text


def rm_ref_spaces(newtext: str) -> str:
    """Legacy wrapper for PortugueseBot.rm_ref_spaces."""
    return PortugueseBot().rm_ref_spaces(newtext)


def pt_fixes(text: str) -> str:
    """Legacy wrapper for PortugueseBot.pt_fixes."""
    return PortugueseBot().pt_fixes(text)


__all__ = [
    "PortugueseBot",
    "rm_ref_spaces",
    "pt_fixes",
]
