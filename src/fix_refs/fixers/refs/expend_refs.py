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
        """Expand short references with full text from source.
        Refs that already have a body in `text` are never overwritten.
        Args:
            text: Text to fix
            source_text: Source text with full references
        Returns:
            Text with expanded references
        """
        text_loader = WtpRefs.load(text)
        short_refs = text_loader.short_refs

        logger.debug(f"empty refs: {len(short_refs)}")

        if not short_refs:
            return text

        # Only protect existing bodies when a separate source is given.
        # With no source, the text itself is the source (same-text expansion).
        if source_text:
            existing_full_keys = {x.match_key for x in text_loader.full_named_refs}
        else:
            existing_full_keys = set()
            source_text = text

        source_loader = WtpRefs.load(source_text)

        # use match_key to match name and group, (self.name, self.group)
        str_full_refs = {x.match_key: x for x in source_loader.full_named_refs}

        for cite in short_refs:
            if cite.match_key in existing_full_keys:
                logger.debug(f"refs_expand: skip {cite.name}, already has body in text")
                continue

            expanded_ref = str_full_refs.get(cite.match_key)
            if expanded_ref:
                logger.debug(f"refs_expand: {cite.name}")
                text = text.replace(cite.tag_str, expanded_ref.tag_str)

        return text


__all__ = [
    "RefExpander",
]
