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

    def overwrite_all_refs(self, text: str, source_text: str) -> str:
        """
        Overwrite full refs in `text` with the refs from `source_text`.

        A ref in `text` is replaced only when it has a body and a source
        ref with the same (name, group) key exists. Short (self-closing)
        refs are left untouched; use `run` to expand them.

        Args:
            text: Text whose refs should be overwritten
            source_text: Text holding the authoritative full refs
        Returns:
            Text with matching refs overwritten
        """
        if not text or not source_text:
            return text

        text_loader = WtpRefs.load(text)
        source_loader = WtpRefs.load(source_text)

        # Only named full refs can be matched reliably
        source_refs = WtpRefs.list_wtpref_to_dict(source_loader.full_named_refs)

        if not source_refs:
            return text

        # Collect replacements as (start, end, new_string) using spans
        replacements: list[tuple[int, int, str]] = []

        for ref in text_loader.full_named_refs:
            new_ref = source_refs.get(ref.match_key)
            if not new_ref:
                continue

            # Skip refs that are already identical
            if new_ref.tag_str == ref.tag_str:
                continue

            start, end = ref.span
            replacements.append((start, end, new_ref.tag_str))
            logger.debug(f"refs_overwrite: {ref.name}")

        # Apply from the end so earlier spans stay valid
        for start, end, new_str in sorted(replacements, reverse=True):
            text = text[:start] + new_str + text[end:]

        return text

    def fix_and_overwrite(
        self,
        text: str,
        source_text: str = "",
        overwrite: bool = False,
    ) -> str:
        """Expand short references with full text from source.

        Args:
            text: Text to fix
            source_text: Source text with full references
            overwrite: If True, full refs in `text` that match a full ref
                in `source_text` (same name+group) are replaced by the
                source version. Ignored when no `source_text` is given.
        Returns:
            Text with expanded (and optionally overwritten) references
        """
        # Step 1: overwrite existing full refs
        if overwrite and source_text:
            text = self.overwrite_all_refs(text, source_text)

        # Step 2: expand short refs
        text = self.run(text, source_text)

        return text

__all__ = [
    "RefExpander",
]
