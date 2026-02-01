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
    dots = r".,。।"

    if lang == "hy":
        dots = r".,。։।:"
    # ([\.,。։।:]+)\s*((?:\s*<ref[\s\S]+?(?:<\/ref|\/)>)+)
    regline = r"((?:\s*<ref[\s\S]+?(?:<\/ref|\/)>)+)"

    escaped = re.escape(dots)
    pattern = rf"([{escaped}]+)\s*{regline}"
    replacement = r"\2\1"

    text = re.sub(pattern, replacement, text, flags=re.MULTILINE)

    return text
