"""
Reference expansion utilities
"""

from __future__ import annotations

import logging

from ..parsers.citations_parser import Citation, get_full_refs, get_short_refs
from ..utils.debug import echo_debug


def refs_expand(short_refs: list[Citation], text: str, alltext: str) -> str:
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
        name = cite.name
        refe = cite.tag

        rr = refs.get(name, "")

        if rr:
            echo_debug(f"refs_expand: {name}")
            text = text.replace(refe, rr)

    return text


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
    short_refs = get_short_refs(first)

    for cite in short_refs:
        name = cite.name
        refe = cite.tag

        rr = refs.get(name, "")
        if rr:
            first = first.replace(refe, rr)

    return first


__all__ = [
    "refs_expand",
    "refs_expand_work",
]
