"""
Remove duplicate references by converting them to named short references
"""

from __future__ import annotations

import logging

from ...parsers.wtp_mapping.wtp_refs import WtpRefs

logger = logging.getLogger(__name__)


class DuplicateRefRemover:
    """Remover for duplicate references by converting subsequent occurrences into self-closing tags."""

    def wtp_remove(self, text: str) -> str:
        """
        Remove duplicate references by converting them to self-closing tags

        First occurrence keeps full content, subsequent references become <ref name="..."/>

        Args:
            text: Text containing citations

        Returns:
            Text with duplicate references converted to self-closing tags
        """
        return WtpRefs.load(text).remove_duplicate()


__all__ = [
    "DuplicateRefRemover",
]
