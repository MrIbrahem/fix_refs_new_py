"""
Reference expansion utilities
"""

from typing import Dict, List
from ..parsers.citations import get_short_citations, get_full_refs, Citation
from ..utils.debug import echo_debug


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
