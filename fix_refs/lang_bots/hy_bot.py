"""
Armenian-specific bot fixes
"""

from __future__ import annotations

import logging
import re

from .remove_space import RemoveSpace

logger = logging.getLogger(__name__)


def remove_spaces_between_ref_and_punctuation(text: str) -> str:
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


def hy_fixes(text: str) -> str:
    """Apply Armenian-specific fixes to text

    Args:
        text: WikiText content

    Returns:
        Fixed text
    """
    text = RemoveSpace().remove_spaces_between_last_word_and_beginning_of_ref(text, "hy")
    text = remove_spaces_between_ref_and_punctuation(text)
    return text


__all__ = [
    "remove_spaces_between_ref_and_punctuation",
    "hy_fixes",
]
