"""
Reference expansion utilities
"""

from __future__ import annotations

import logging

from ...parsers.wtp_mapping import WtpRef, WtpRefs

logger = logging.getLogger(__name__)


class RefExpander:
    """Expander for replacing short reference tags with full citations."""

    def refs_expand(self, short_refs: list[WtpRef], text: str, alltext: str) -> str:
        """Expand short references with full text from source

        Args:
            short_refs: List of short citation references
            text: Text to fix
            alltext: Source text with full references

        Returns:
            Text with expanded references
        """
        full_refs = WtpRefs.load(alltext).full_refs
        full_refs_str = {x.name: x.tag_str for x in full_refs}

        for cite in short_refs:
            name = cite.name
            refe = cite.tag_str

            rr = full_refs_str.get(name, "")

            if rr:
                logger.debug(f"refs_expand: {name}")
                text = text.replace(refe, rr)

        return text


__all__ = [
    "RefExpander",
]
