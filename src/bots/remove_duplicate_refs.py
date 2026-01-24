"""
Remove duplicate references by converting them to named short references
"""

import re
from typing import Dict, List
from ..parsers.citations import get_citations
from ..bots.attrs_utils import get_attrs
from ..bots.refs_utils import remove_start_end_quotes
from ..utils.debug import echo_debug


def fix_refs_names(text: str) -> str:
    """Fix reference names by normalizing attribute quotes

    Args:
        text: Text containing citations

    Returns:
        Text with normalized citation attributes
    """
    new_text = text
    citations = get_citations(text)

    for citation in citations:
        cite_attrs = citation.get_attributes()
        cite_attrs = cite_attrs.strip() if cite_attrs else ""

        if_in = f"<ref {cite_attrs}>"

        if if_in not in new_text:
            continue

        attrs = get_attrs(cite_attrs)

        if not cite_attrs:
            continue

        new_cite_attrs = ""

        for key, value in attrs.items():
            value2 = remove_start_end_quotes(value)
            new_cite_attrs += f" {key}={value2}"

        new_cite_attrs = new_cite_attrs.strip()
        cite_newtext = f"<ref {new_cite_attrs}>"

        new_text = new_text.replace(if_in, cite_newtext)

    return new_text


def remove_duplicate_refs_with_attrs(text: str) -> str:
    """Remove duplicate references by converting them to self-closing tags

    First occurrence keeps full content, subsequent references become <ref name="..."/>

    Args:
        text: Text containing citations

    Returns:
        Text with duplicate references converted to self-closing tags
    """
    new_text = text
    refs_to_check: Dict[str, str] = {}
    refs: Dict[str, str] = {}
    citations = get_citations(new_text)

    numb = 0

    for citation in citations:
        cite_fulltext = citation.get_original_text()
        cite_attrs = citation.get_attributes()
        cite_attrs = cite_attrs.strip() if cite_attrs else ""

        if not cite_attrs:
            numb += 1
            name = f"autogen_{numb}"
            cite_attrs = f"name='{name}'"

        echo_debug(f"\n cite_attrs: (({cite_attrs}))")

        cite_newtext = f"<ref {cite_attrs} />"

        if cite_attrs in refs:
            new_text = new_text.replace(cite_fulltext, cite_newtext)
        else:
            refs_to_check[cite_newtext] = cite_fulltext
            refs[cite_attrs] = cite_newtext

    for key, value in refs_to_check.items():
        if value not in new_text:
            pattern = re.escape(key)
            new_text = re.sub(pattern, value, new_text, count=1)

    return new_text
