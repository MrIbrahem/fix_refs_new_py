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
        text_loader = WtpRefs.load(text)
        short_refs = text_loader.short_refs

        logger.debug(f"empty refs: {len(short_refs)}")

        if not short_refs:
            return text

        # If source_text is provided externally, don't overwrite references that already
        # have full bodies defined in text
        existing_full_keys: set[tuple[str, str]] = set()
        if source_text:
            existing_full_keys = {x.match_key for x in text_loader.full_named_refs}

        # if not source_text expend refs in same text
        source_text = source_text or text

        source_loader = WtpRefs.load(source_text)

        # use match_key to match name and group, (self.name, self.group)
        str_full_refs = {x.match_key: x for x in source_loader.full_named_refs}

        edits: list[tuple[int, int, str]] = []
        for cite in short_refs:
            if cite.match_key in existing_full_keys:
                continue
            expanded_ref = str_full_refs.get(cite.match_key)
            if expanded_ref:
                logger.debug(f"refs_expand: {cite.name}")
                edits.append((cite.span[0], cite.span[1], expanded_ref.tag_str))

        # Apply edits in reverse order so character offsets remain valid
        for start, end, replacement in sorted(edits, key=lambda e: e[0], reverse=True):
            text = text[:start] + replacement + text[end:]

        return text


__all__ = [
    "RefExpander",
]
