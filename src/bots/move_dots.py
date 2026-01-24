"""
Move punctuation after reference tags
"""

import re


def move_dots_after_refs(text: str, lang: str) -> str:
    """Move punctuation marks after reference tags

    Args:
        text: Text containing references and punctuation
        lang: Language code

    Returns:
        Text with punctuation moved after references
    """
    dot = r"\.,。।"

    if lang == "hy":
        dot = r"\.,。։।:"

    regline = r"((?:\s*<ref[\s\S]+?(?:<\/ref|\/)>)+)"
    pattern = rf"([{dot}]+)\s*{regline}"
    replacement = r"\2\1"

    text = re.sub(pattern, replacement, text, flags=re.MULTILINE)

    return text
