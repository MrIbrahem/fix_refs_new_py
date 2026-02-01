"""
Mini fixes for WikiText formatting
"""

import re
from typing import Dict


def fix_sections_titles(text: str, lang: str) -> str:
    """Fix section titles for different languages

    Args:
        text: Text containing section titles
        lang: Language code

    Returns:
        Text with translated section titles
    """
    to_replace: Dict[str, Dict[str, str]] = {
        "hr": {
            "Reference": "Izvori",
            "References": "Izvori",
        },
        "sw": {
            "Reference": "Marejeo",
            "References": "Marejeo",
            "Marejeleo": "Marejeo"
        },
        "ru": {
            "Reference": "Примечания",
            "References": "Примечания",
            "Ссылки": "Примечания"
        }
    }

    if lang not in to_replace:
        return text

    for key, value in to_replace[lang].items():
        k = re.escape(key)
        pattern = rf'(=+)\s*{k}\s*\1'
        replacement = rf'\1 {value} \1'
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    return text


def remove_space_before_ref_tags(text: str, lang: str) -> str:
    """Remove space before reference tags after punctuation

    Args:
        text: Text to fix
        lang: Language code

    Returns:
        Text with spaces removed before ref tags
    """
    pattern = r"\s*(\.|,|。|।)\s*<ref"
    text = re.sub(pattern, r"\1<ref", text, flags=re.IGNORECASE)
    return text


def refs_tags_spaces(text: str) -> str:
    """Remove spaces between reference tags

    Args:
        text: Text containing references

    Returns:
        Text with spaces removed between ref tags
    """
    # Remove spaces between </ref> and <ref>
    text = re.sub(r"</ref>\s*<ref", "</ref><ref", text, flags=re.IGNORECASE)
    # Remove spaces between /> and <ref>
    text = re.sub(r"/>\s*<ref", "/><ref", text, flags=re.IGNORECASE)
    # Remove space between > and <ref> where > is NOT part of <ref>
    # Use negative lookbehind to ensure > is not preceded by <
    text = re.sub(r"(?<!<)>\s*<ref", "><ref", text, flags=re.IGNORECASE)

    return text


def fix_prefix(text: str, lang: str) -> str:
    """Fix language prefix in interwiki links

    Args:
        text: Text with interwiki links
        lang: Language code

    Returns:
        Text with simplified interwiki links
    """
    text = re.sub(r'\[\[:en:', "[[", text)
    text = re.sub(rf'\[\[:{re.escape(lang)}:', "[[", text, flags=re.IGNORECASE)
    return text


def mini_fixes_after_fixing(text: str, lang: str) -> str:
    """Apply fixes after main fixing process

    Args:
        text: Text to fix
        lang: Language code

    Returns:
        Fixed text
    """
    text = re.sub(r'^\s*\n', "\n", text, flags=re.MULTILINE)
    text = fix_prefix(text, lang)
    return text


def mini_fixes(text: str, lang: str) -> str:
    """Apply mini fixes to text

    Args:
        text: Text to fix
        lang: Language code

    Returns:
        Fixed text
    """
    text = refs_tags_spaces(text)
    text = fix_sections_titles(text, lang)
    text = remove_space_before_ref_tags(text, lang)
    return text
