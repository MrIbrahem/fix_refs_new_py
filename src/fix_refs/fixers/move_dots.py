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
    def move_dots_after_refs_old(cls, text: str, lang: str) -> str:
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
    def move_dots_after_refs(cls, text: str, lang: str) -> str:
        """Move punctuation marks after reference tags

        Args:
            text: Text containing references and punctuation
            lang: Language code

        Returns:
            Text with punctuation moved after references
        """
        dots_str = cls.get_dots(lang)

        parsed = wtp.parse(text)
        spans = sorted(tag.span for tag in parsed.get_tags("ref"))

        # Go from last to first so earlier spans stay valid after each edit
        for i in range(len(spans) - 1, -1, -1):
            start, end = spans[i]

            # Punctuation (and spaces) right before the ref
            before = text[:start].rstrip()
            stripped = before.rstrip(dots_str)
            moved = before[len(stripped) :]

            if not moved:
                continue

            # Extend to the end of the consecutive refs (only whitespace between them)
            for next_start, next_end in spans[i + 1 :]:
                if text[end:next_start].strip():
                    break
                end = next_end

            # Put the punctuation after the whole chain, drop the spaces before the first ref
            text = stripped + text[start:end] + moved + text[end:]

        return text


__all__ = [
    "DotsMover",
]
