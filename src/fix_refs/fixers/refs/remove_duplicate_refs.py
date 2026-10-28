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
        ref_obj = WtpRefs.load(text)

        seen: set[tuple[str, str]] = set()
        edits: list[tuple[tuple[int, int], str]] = []

        # Walk refs in document order so the first occurrence is the one kept
        for r in sorted(ref_obj.all_refs, key=lambda x: x.span[0]):
            if not r.name or r.is_self_closing():
                continue

            if r.match_key not in seen:
                seen.add(r.match_key)
                continue

            edits.append((r.span, r.to_short()))

        text = ref_obj.parsed.string
        # Apply from the end so earlier spans stay valid
        for (start, end), short in reversed(edits):
            text = text[:start] + short + text[end:]

        logger.info("Replaced %d duplicate refs with short refs", len(edits))
        return text


__all__ = [
    "DuplicateRefRemover",
]
