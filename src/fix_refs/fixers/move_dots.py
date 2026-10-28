"""
Move punctuation after reference tags
"""

from __future__ import annotations

import logging
import re
import wikitextparser as wtp

logger = logging.getLogger(__name__)


class DotsMover:
    """Fixer for moving punctuation marks after reference tags."""

    @staticmethod
    def get_dots(lang: str) -> str:
        dots: set[str] = {".", ",", "。", "।"}

        if lang == "hy":
            # dots_str = r".,。։।:"
            dots = {".", ",", "。", "։", "।", ":"}

        return "".join(dots)

    @classmethod
    def move_dots_after_refs(cls, text: str, lang: str) -> str:
        """Move punctuation marks after reference tags

        Args:
            text: Text containing references and punctuation
            lang: Language code

        Returns:
            Text with punctuation moved after references
        """
        dots_str = cls.get_dots(lang)
        regline = r"((?:\s*<ref[\s\S]+?(?:<\/ref|\/)>)+)"

        escaped = re.escape(dots_str)
        pattern = rf"([{escaped}]+)\s*{regline}"
        replacement = r"\2\1"

        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)

        return text

    @classmethod
    def move_dots_after_refs_new(cls, text: str, lang: str) -> str:
        """Move punctuation marks after reference tags

        Args:
            text: Text containing references and punctuation
            lang: Language code

        Returns:
            Text with punctuation moved after references
        """
        dots_str = cls.get_dots(lang)

        parsed = wtp.parse(text)
        # Go from last to first so earlier spans stay valid after each edit
        for tag in sorted(parsed.get_tags("ref"), key=lambda t: t.span[0], reverse=True):
            start, end = tag.span

            # Punctuation (and spaces) right before the ref
            before = text[:start].rstrip()
            stripped = before.rstrip(dots_str)
            moved = before[len(stripped) :]

            if not moved:
                continue

            # Put the punctuation after the ref, drop the spaces in between
            text = stripped + text[start:end] + moved + text[end:]

        return text


__all__ = [
    "DotsMover",
]
