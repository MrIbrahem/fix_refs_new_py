"""
Reference expansion utilities
"""

from __future__ import annotations

import logging

from ...parsers.citations_parser import Citation, CitationsParser

logger = logging.getLogger(__name__)


class RefExpander:
    """Expander for replacing short reference tags with full citations."""

    def __init__(self, citations_parser: CitationsParser | None = None) -> None:
        self.citations_parser = citations_parser or CitationsParser()

    def refs_expand(self, short_refs: list[Citation], text: str, alltext: str) -> str:
        """Expand short references with full text from source

        Args:
            short_refs: List of short citation references
            text: Text to fix
            alltext: Source text with full references

        Returns:
            Text with expanded references
        """
        refs = self.citations_parser.get_full_refs(alltext)

        for cite in short_refs:
            name = cite.name
            refe = cite.tag_str

            rr = refs.get(name, "")

            if rr:
                logger.debug(f"refs_expand: {name}")
                text = text.replace(refe, rr)

        return text


__all__ = [
    "RefExpander",
]
