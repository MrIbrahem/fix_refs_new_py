"""
Reference expansion utilities
"""

from __future__ import annotations

import logging


from ...parsers.wtp_mapping import WtpRefs

logger = logging.getLogger(__name__)


class RefExpander:
    """Expander for replacing short reference tags with full citations."""

    def run(self, text: str, source_text: str = "") -> str:
        """Expand short references with full text from source

        Args:
            text: Text to fix
            source_text: Source text with full references

        Returns:
            Text with expanded references
        """
        short_refs = WtpRefs.load(text).short_refs

        logger.debug(f"empty refs: {len(short_refs)}")

        if not short_refs:
            return text

        # if not source_text expend refs in same text
        source_text = source_text or text

        source_loader = WtpRefs.load(source_text)

        str_full_refs = {x.name: x for x in source_loader.full_named_refs}

        for cite in short_refs:
            expanded_ref = str_full_refs.get(cite.name)
            if expanded_ref:
                logger.debug(f"refs_expand: {cite.name}")
                text = text.replace(cite.tag_str, expanded_ref.tag_str)

        return text


__all__ = [
    "RefExpander",
]
