"""
Citation parser for WikiText reference tags
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from functools import cached_property

import wikitextparser as wtp

logger = logging.getLogger(__name__)


@dataclass
class WtpRef:
    """Represents a citation reference"""

    tag: wtp.Tag

    @property
    def attrs(self) -> dict[str, str]:
        return self.tag.attrs

    @property
    def tag_str(self) -> str:
        return self.tag.string

    @property
    def contents(self) -> str:
        return self.tag.contents or ""

    @property
    def name(self) -> str:
        """Get citation name"""
        return self.tag.attrs.get("name", "").strip()

    def is_self_closing(self) -> bool:
        return not self.tag.contents or not self.tag.contents.strip()

    @property
    def group(self) -> str:
        return (self.tag.get_attr("group") or "").strip()

    @property
    def span(self) -> tuple[int, int]:
        return self.tag.span

    def to_short(self) -> str:
        """Build a self-closing tag that keeps all original attributes."""
        clone = wtp.Tag(self.tag_str)
        clone.contents = ""
        return clone.string.replace("></ref>", " />")

    @classmethod
    def load(cls, ref: wtp.Tag) -> WtpRef:
        return cls(tag=ref)


@dataclass
class WtpRefs:
    """Parser for extracting reference tags and citations from WikiText."""

    parsed: wtp.WikiText

    @classmethod
    def load(
        cls,
        text: str = "",
        parsed: wtp.WikiText | None = None,
    ) -> WtpRefs:
        return cls(
            parsed=parsed or wtp.parse(text),
        )

    # ---------- helpers ----------

    @cached_property
    def all_refs(self) -> list[WtpRef]:
        """Extract all citation reference tags from text"""
        return [WtpRef.load(t) for t in self.parsed.get_tags("ref")]

    @property
    def full_refs(self) -> list[WtpRef]:
        return [x for x in self.all_refs if not x.is_self_closing()]

    @property
    def full_named_refs(self) -> list[WtpRef]:
        return [x for x in self.full_refs if x.name]

    @property
    def short_refs(self) -> list[WtpRef]:
        return [x for x in self.all_refs if x.is_self_closing()]

    def remove_duplicate(self) -> str:
        """Replace repeated full refs with self-closing refs.

        The first occurrence of each (name, group) keeps its content;
        every later one with content becomes <ref name="..." />.
        Unnamed refs are left untouched.
        Returns the new text (self.text is not modified).
        """
        text = self.parsed.string
        seen: set[tuple[str, str]] = set()
        edits: list[tuple[tuple[int, int], str]] = []

        # Walk refs in document order so the first occurrence is the one kept
        for r in sorted(self.all_refs, key=lambda x: x.span[0]):
            if not r.name or r.is_self_closing():
                continue

            key = (r.name, r.group)
            if key not in seen:
                seen.add(key)
                continue

            edits.append((r.span, r.to_short()))

        # Apply from the end so earlier spans stay valid
        for (start, end), short in reversed(edits):
            text = text[:start] + short + text[end:]

        logger.info("Replaced %d duplicate refs with short refs", len(edits))
        return text


__all__ = [
    "WtpRef",
    "WtpRefs",
]
