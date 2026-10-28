"""
Move punctuation after reference tags
"""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)


class DotsMover:
    """Fixer for moving punctuation marks after reference tags."""

    @staticmethod
    def move_dots_after_refs_old(text: str, lang: str) -> str:
        """Move punctuation marks after reference tags

        Args:
            text: Text containing references and punctuation
            lang: Language code

        Returns:
            Text with punctuation moved after references
        """
        dots = [
            r".",
            r",",
            r"。",
            r"।",
        ]

        if lang == "hy":
            # dots_str = r".,。։।:"
            dots.append("։")
            dots.append(":")

        dots_str = "".join(dots)
        regline = r"((?:\s*<ref[\s\S]+?(?:<\/ref|\/)>)+)"

        escaped = re.escape(dots_str)
        pattern = rf"([{escaped}]+)\s*{regline}"
        replacement = r"\2\1"

        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)

        return text

    @staticmethod
    def move_dots_after_refs(text: str, lang: str) -> str:
        """Move punctuation marks after reference tags

        Args:
            text: Text containing references and punctuation
            lang: Language code

        Returns:
            Text with punctuation moved after references
        """
        dots = [
            r".",
            r",",
            r"。",
            r"।",
        ]

        if lang == "hy":
            # dots_str = r".,。։।:"
            dots.append("։")
            dots.append(":")

        dots_str = "".join(dots)
        regline = r"((?:\s*<ref[\s\S]+?(?:<\/ref|\/)>)+)"

        escaped = re.escape(dots_str)
        pattern = rf"([{escaped}]+)\s*{regline}"
        replacement = r"\2\1"

        text = re.sub(pattern, replacement, text, flags=re.MULTILINE)

        return text


__all__ = [
    "DotsMover",
]
