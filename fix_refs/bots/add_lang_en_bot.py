"""
Add English language parameter to references
"""

import wikitextparser as wtp
from ..utils.debug import echo_debug


def add_lang_en_new(temp_text: str) -> str:
    """Add language parameter to templates

    Args:
        temp_text: Text containing templates

    Returns:
        Text with language parameter added
    """
    wikicode = wtp.parse(temp_text.strip())

    for wt_template in wikicode.templates:
        language_arg = wt_template.get_arg('language')
        if not language_arg or not language_arg.value.strip():
            wt_template.set_arg('language', 'en')

    new_text = wikicode.string
    return new_text


def add_lang_en_to_refs(text: str) -> str:
    """Add English language parameter to all references in text

    Args:
        text: Text containing references

    Returns:
        Text with language parameter added to references
    """
    echo_debug("\n add_lang_en_to_refs:\n")
    parsed = wtp.parse(text)

    # Get all ref tags
    ref_tags = parsed.get_tags('ref')

    for ref in ref_tags:
        contents = ref.contents
        # Only process if it looks like a template
        if not (contents.startswith("{{") and contents.endswith("}}")):
            continue

        # Access templates inside this ref tag
        inner_templates = ref.templates

        for temp in inner_templates:
            # Add language parameter if needed
            language_arg = temp.get_arg('language')
            if not language_arg or not language_arg.value.strip():
                temp.set_arg('language', 'en')
            break  # Only process the first template

    return parsed.string
