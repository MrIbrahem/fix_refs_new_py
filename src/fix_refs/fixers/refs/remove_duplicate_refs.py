"""
Remove duplicate references by converting them to named short references
"""

from __future__ import annotations

import logging

from ...parsers.citations_parser import CitationsParser

logger = logging.getLogger(__name__)


class DuplicateRefRemover:
    """Remover for duplicate references by converting subsequent occurrences into self-closing tags."""

    def __init__(self, citations_parser: CitationsParser | None = None) -> None:
        self.citations_parser = citations_parser or CitationsParser()

    def remove(self, text: str) -> str:
        """Remove duplicate references by converting them to self-closing tags

        First occurrence keeps full content, subsequent references become <ref name="..."/>

        Args:
            text: Text containing citations

        Returns:
            Text with duplicate references converted to self-closing tags
        """
        return self.citations_parser.remove_duplicate(text)


__all__ = [
    "DuplicateRefRemover",
]
