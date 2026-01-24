"""
Portuguese-specific bot fixes
"""

import re
import wikitextparser as wtp
from ..bots.months import make_date_new_val_pt


def start_end(cite_temp: str) -> bool:
    """Check if string starts with {{ and ends with }}"""
    return cite_temp.startswith("{{") and cite_temp.endswith("}}")


def fix_pt_months_in_texts(temp_text: str) -> str:
    """Translate English months to Portuguese within template parameters

    Args:
        temp_text: Template text (can contain multiple templates)

    Returns:
        Template text with translated months
    """
    parsed = wtp.parse(temp_text)

    for temp in parsed.templates:
        arguments = temp.arguments
        for arg in arguments:
            old_val = arg.value
            new_val = make_date_new_val_pt(old_val)
            if new_val and new_val.strip() != old_val.strip():
                temp.set_arg(arg.name, new_val)

    return parsed.string


def fix_pt_months_in_refs(text: str) -> str:
    """Translate English months to Portuguese within citations

    Args:
        text: Text containing citations

    Returns:
        Text with translated months in citations
    """
    parsed = wtp.parse(text)

    # Get all ref tags
    ref_tags = parsed.get_tags('ref')

    for ref in ref_tags:
        contents = ref.contents
        # Only process if it looks like a template
        if not start_end(contents):
            continue
        ref.contents = fix_pt_months_in_texts(contents)
    return parsed.string


def rm_ref_spaces(newtext: str) -> str:
    """Remove spaces between punctuation and ref tags

    Args:
        newtext: Text to process

    Returns:
        Text with spaces removed
    """
    dot = r"(\.|,|。|।)"
    regline = r"((?:\s*<ref[\s\S]+?(?:<\/ref|\/)>)+)"
    pattern = r'\s*' + dot + r'\s*' + regline
    replacement = r'\1\2'

    newtext = re.sub(pattern, replacement, newtext)

    return newtext


def pt_fixes(text: str) -> str:
    """Apply Portuguese-specific fixes to text

    Args:
        text: WikiText content

    Returns:
        Fixed text
    """
    text = fix_pt_months_in_refs(text)
    text = rm_ref_spaces(text)
    return text
