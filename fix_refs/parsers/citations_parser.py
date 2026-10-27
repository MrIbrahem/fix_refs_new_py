"""
Citation parser for WikiText reference tags
"""

from __future__ import annotations

import logging

import wikitextparser as wtp

from .citation import Citation

logger = logging.getLogger(__name__)


class CitationsParser:
    """Parser for extracting reference tags and citations from WikiText."""

    def get_all_citations(self, text: str) -> list[Citation]:
        """Extract all citation reference tags from text

        Args:
            text: Text containing citation tags

        Returns:
            List of Citation objects
        """
        citations: list[Citation] = []
        parsed = wtp.parse(text)

        for tag in parsed.get_tags():
            if tag.name == "ref":
                citations.append(Citation(tag))

        return citations

    def get_full_refs(self, text: str) -> dict[str, str]:
        """Get mapping of citation names to their full reference tags

        Args:
            text: Text containing citations

        Returns:
            Dictionary mapping citation names to their full tags
        """
        full = {}
        citations = self.get_all_citations(text)

        for cite in citations:
            if cite.contents and cite.name:
                full[cite.name] = cite.tag

        return full

    def get_short_refs(self, text: str) -> list[Citation]:
        """Extract short/empty citations (self-closing tags)

        Args:
            text: Text containing short citations

        Returns:
            List of Citation objects for short references
        """
        citations = []
        parsed = wtp.parse(text)
        for tag in parsed.get_tags():
            if tag.name == "ref" and not tag.contents:
                citations.append(Citation(tag))

        return citations


def get_all_citations(text: str) -> list[Citation]:
    """Legacy wrapper for CitationsParser.get_all_citations."""
    return CitationsParser().get_all_citations(text)


def get_full_refs(text: str) -> dict[str, str]:
    """Legacy wrapper for CitationsParser.get_full_refs."""
    return CitationsParser().get_full_refs(text)


def get_short_refs(text: str) -> list[Citation]:
    """Legacy wrapper for CitationsParser.get_short_refs."""
    return CitationsParser().get_short_refs(text)


__all__ = [
    "CitationsParser",
    "get_all_citations",
    "get_full_refs",
    "get_short_refs",
]
