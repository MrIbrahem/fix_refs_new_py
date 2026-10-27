"""
Armenian-specific bot fixes
"""

from __future__ import annotations

import logging
import re

from .remove_space import RemoveSpace

logger = logging.getLogger(__name__)


class ArmenianBot:
    """Bot for Armenian Wikipedia language-specific fixes."""

    def __init__(self, remove_space: RemoveSpace | None = None) -> None:
        self.remove_space = remove_space or RemoveSpace()

    def remove_spaces_between_ref_and_punctuation(self, text: str) -> str:
        """Remove spaces between ref tags and punctuation

        Args:
            text: WikiText content

        Returns:
            Text with spaces removed
        """
        # Use superset of punctuation across supported languages
        dots = ".,。։।:"
        escaped_punctuation = re.escape(dots)

        # Keep punctuation right after <ref ... /> with no space
        # Pattern: <ref[^>]*/>\s*[punctuation]
        text = re.sub(r"(<ref[^>]*\/>)\s*([" + escaped_punctuation + r"])", r"\1\2", text)

        # Normalize endings: </ref> followed by any punctuation remains attached
        # Pattern: </ref>\s*[punctuation]
        text = re.sub(r"<\/ref>\s*([" + escaped_punctuation + r"])", r"</ref>\1", text)

        return text

    def hy_fixes(self, text: str) -> str:
        """Apply Armenian-specific fixes to text

        Args:
            text: WikiText content

        Returns:
            Fixed text
        """
        text = self.remove_space.remove_spaces_between_last_word_and_beginning_of_ref(text, "hy")
        text = self.remove_spaces_between_ref_and_punctuation(text)
        return text


def remove_spaces_between_ref_and_punctuation(text: str) -> str:
    """Legacy wrapper for ArmenianBot.remove_spaces_between_ref_and_punctuation."""
    return ArmenianBot().remove_spaces_between_ref_and_punctuation(text)


def hy_fixes(text: str) -> str:
    """Legacy wrapper for ArmenianBot.hy_fixes."""
    return ArmenianBot().hy_fixes(text)


__all__ = [
    "ArmenianBot",
    "remove_spaces_between_ref_and_punctuation",
    "hy_fixes",
]
