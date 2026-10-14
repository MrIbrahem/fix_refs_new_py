"""
Spanish helper functions
"""

from __future__ import annotations

import logging
import re

import wikitextparser as wtp

logger = logging.getLogger(__name__)


def remove_short_refs(text: str) -> str:
    """
    Remove short citations from text
    """
    parsed = wtp.parse(text)
    for tag in parsed.get_tags():
        if tag.name == "ref" and not tag.contents:
            tag.string = ""
    text = parsed.string
    # Remove multiple newlines
    text = re.sub(r"\n+", "\n", text)
    return text


def add_line_to_temp(line: str, text: str) -> str:
    """Add reference line to ref template

    Args:
        line: Reference lines to add
        text: Text containing templates

    Returns:
        Text with references added to template
    """
    # Find templates like {{reflist|...}} or {{listaref|...}}
    # Handle multi-line templates with nested braces by matching until the closing }}
    # that is on its own line or at end of content
    pattern = r"(\{\{\s*(reflist|listaref)\s*\|[^}]*refs\s*=)(.*?)(\}\})"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

    new_text = text
    temp_already_in = False

    if match:
        template_start = match.group(1)  # {{Reflist|refs=
        refs_content = match.group(3)  # existing refs content
        template_end = match.group(4)  # }}

        # Clean up existing refs content
        refs_content = remove_short_refs(refs_content)

        # Combine existing refs with new refs
        combined_refs = refs_content.strip() + "\n" + line.strip() if refs_content.strip() else line.strip()

        # Replace the template
        # Format: {{Reflist|refs=\n<refs content>}}
        # The }} stays on same line as the last ref to match expected output format
        new_template = f"{template_start}\n{combined_refs}{template_end}"
        new_text = text[: match.start()] + new_template + text[match.end() :]
        temp_already_in = True

    # If no template found, add section
    if not temp_already_in:
        section_ref = "\n== Referencias ==\n{{listaref|refs=\n" + line.strip() + "\n}}"
        new_text += section_ref

    return new_text


__all__ = [
    "remove_short_refs",
    "add_line_to_temp",
]
