"""
Portuguese-specific bot fixes
"""

from __future__ import annotations

import logging
import re

from ..fixers.months import fix_months_in_refs

logger = logging.getLogger(__name__)


def rm_ref_spaces(newtext: str) -> str:
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


def pt_fixes(text: str) -> str:
    """Apply Portuguese-specific fixes to text

    Args:
        text: WikiText content

    Returns:
        Fixed text
    """
    text = fix_months_in_refs(text, "pt")
    text = rm_ref_spaces(text)
    return text


__all__ = [
    "rm_ref_spaces",
    "pt_fixes",
]
