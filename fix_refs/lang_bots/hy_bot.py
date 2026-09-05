"""
Armenian-specific bot fixes
"""

import re

from .remove_space import remove_spaces_between_last_word_and_beginning_of_ref


def str_ends_with(string: str, end_string: str) -> bool:
    """Check if string ends with substring"""
    return string.endswith(end_string)


def str_starts_with(text: str, start: str) -> bool:
    """Check if string starts with substring"""
    return text.startswith(start)


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
    text = remove_spaces_between_last_word_and_beginning_of_ref(text, "hy")
    text = remove_spaces_between_ref_and_punctuation(text)
    return text


__all__ = [
    "str_ends_with",
    "str_starts_with",
    "remove_spaces_between_ref_and_punctuation",
    "hy_fixes",
]
