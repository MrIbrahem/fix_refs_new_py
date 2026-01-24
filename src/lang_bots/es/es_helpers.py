"""
Spanish helper functions
"""

import re
import wikitextparser as wtp
from ...bots.months import make_date_new_val_es
from ...parsers.citations import get_short_citations


def start_end(cite_temp: str) -> bool:
    """Check if string starts with {{ and ends with }}"""
    return cite_temp.startswith("{{") and cite_temp.endswith("}}")


def fix_es_months_in_texts(temp_text: str) -> str:
    """Translate English months to Spanish within template parameters

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
            new_val = make_date_new_val_es(old_val)
            if new_val and new_val.strip() != old_val.strip():
                temp.set_arg(arg.name, new_val)

    return parsed.string


def fix_es_months_in_refs(text: str) -> str:
    """Translate English months to Spanish within citations

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
        ref.contents = fix_es_months_in_texts(contents)
    return parsed.string


def check_short_refs(line: str) -> str:
    """Remove short citations from line

    Args:
        line: Text line

    Returns:
        Line with short citations removed
    """
    shorts = get_short_citations(line)
    for cite in shorts:
        line = line.replace(cite.get_original_text(), "")

    # Remove multiple newlines
    line = re.sub(r'\n+', '\n', line)
    return line


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
    pattern = r'(\{\{\s*(reflist|listaref)\s*\|[^}]*refs\s*=)(.*?)(\}\})'
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)

    new_text = text
    temp_already_in = False

    if match:
        template_start = match.group(1)  # {{Reflist|refs=
        refs_content = match.group(3)     # existing refs content
        template_end = match.group(4)     # }}

        # Clean up existing refs content
        refs_content = check_short_refs(refs_content)

        # Combine existing refs with new refs
        combined_refs = refs_content.strip() + "\n" + line.strip() if refs_content.strip() else line.strip()

        # Replace the template
        # Format: {{Reflist|refs=\n<refs content>}}
        # The }} stays on same line as the last ref to match expected output format
        new_template = f"{template_start}\n{combined_refs}{template_end}"
        new_text = text[:match.start()] + new_template + text[match.end():]
        temp_already_in = True

    # If no template found, add section
    if not temp_already_in:
        section_ref = "\n== Referencias ==\n{{listaref|refs=\n" + line.strip() + "\n}}"
        new_text += section_ref

    return new_text
