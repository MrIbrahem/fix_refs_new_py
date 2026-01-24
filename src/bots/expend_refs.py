"""
Reference expansion utilities
"""

import re
from typing import Dict, List
from ..parsers.citations import get_short_citations, get_full_refs, Citation
from ..utils.debug import echo_debug


def _refs_expand_work(first: str, alltext: str) -> str:
    """Expand references in first text using full refs from alltext

    Args:
        first: Text with self-closing refs like <ref name="x"/>
        alltext: Text with full refs

    Returns:
        Text with self-closing refs replaced by full refs
    """
    if not alltext:
        return first

    # Pattern to match self-closing refs
    pattern = r'<ref\s+([^>\/]*?)\s*/>'

    # Build mapping from alltext
    refs_map: Dict[str, str] = {}

    for match in re.finditer(pattern, alltext):
        attrs = match.group(1)
        if attrs:
            name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', attrs, re.IGNORECASE)
            if name_match:
                name = name_match.group(1)
                full_ref_pattern = f'<ref\\s+{re.escape(attrs)}\\s*>(.*?)</ref>'
                full_match = re.search(full_ref_pattern, alltext, re.DOTALL | re.IGNORECASE)
                if full_match:
                    refs_map[name] = full_match.group(0)

    if not refs_map:
        return first

    result = first

    for match in re.finditer(pattern, result):
        attrs = match.group(1)

        if attrs:
            name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', attrs, re.IGNORECASE)
            if name_match:
                name = name_match.group(1)
                if name in refs_map:
                    result = result.replace(match.group(0), refs_map[name])

    return result


def refs_expand(short_refs: List[Citation], text: str, alltext: str) -> str:
    """Expand short references with full text from source

    Args:
        short_refs: List of short citation references
        text: Text to fix
        alltext: Source text with full references

    Returns:
        Text with expanded references
    """
    refs = get_full_refs(alltext)

    for cite in short_refs:
        name = cite.get_name()
        refe = cite.get_original_text()

        rr = refs.get(name, "")

        if rr:
            echo_debug(f"refs_expand: {name}")
            text = text.replace(refe, rr)

    return text


def find_empty_short(text: str) -> Dict[str, Citation]:
    """Find short references that have no corresponding full reference

    Args:
        text: Text to search

    Returns:
        Dictionary mapping reference names to short citations
    """
    shorts = get_short_citations(text)
    fulls = get_full_refs(text)
    empty_refs: Dict[str, Citation] = {}

    for cite in shorts:
        name = cite.get_name()

        if name not in fulls:
            empty_refs[name] = cite

    return empty_refs


def refs_expand_work(first: str, alltext: str = "") -> str:
    """Expand short citations with full reference content

    Similar to refs_expand but takes text directly instead of list of citations.
    This matches the PHP API for compatibility.

    Args:
        first: Text to process (may contain short citations)
        alltext: Source text containing full references (if empty, uses first)

    Returns:
        Text with short citations expanded to full references
    """
    if not alltext:
        alltext = first

    refs = get_full_refs(alltext)
    short_refs = get_short_citations(first)

    for cite in short_refs:
        name = cite.get_name()
        refe = cite.get_original_text()

        rr = refs.get(name, "")
        if rr:
            first = first.replace(refe, rr)

    return first
