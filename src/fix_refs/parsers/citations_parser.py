"""
Citation parser for WikiText reference tags
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
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

    def set_contents(self, new_content: str) -> None:
        """Set citation content"""
        self.tag.contents = new_content

    def get_str_attributes(self) -> str:
        """Get citation options/attributes as a string"""
        tag_str = str(self.tag.string)
        # Find the end of the opening tag: could be ">" or "/>"
        close_idx = tag_str.find(">")
        if close_idx == -1:
            return ""
        attrs_part = tag_str[len("<ref") : close_idx]
        # Strip trailing "/" for self-closing tags
        attrs_part = attrs_part.rstrip(" /")
        return attrs_part.strip()

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
        clone = wtp.Tag(self.tag.string)
        clone.contents = ""
        return clone.string.replace("></ref>", " />")

    @classmethod
    def from_text(cls, ref_text: str) -> WtpRef:
        """Create a WtpRef from a reference tag string"""

        if not ref_text.strip().startswith("<ref"):
            raise ValueError("Not a reference tag")

        if ref_text.count("<ref") != 1:
            raise ValueError("Multiple reference tags")

        tag = wtp.Tag(ref_text)
        return WtpRef.load(tag)

    @classmethod
    def load(cls, ref: wtp.Tag) -> WtpRef:
        return cls(tag=ref)


@dataclass
class WtpRefs:
    """Parser for extracting reference tags and citations from WikiText."""

    text: str = ""
    parsed: wtp.WikiText = field(init=False, repr=False)

    # name -> '<ref name="x">...</ref>'
    full_refs_str: dict[str, str] = field(init=False, default_factory=dict)
    # name -> spans of short refs (no content)
    short_refs_str: dict[str, list[tuple[int, int]]] = field(init=False, default_factory=dict)

    def __post_init__(self):
        self.parsed = wtp.parse(self.text)
        self._collect()

    # ---------- helpers ----------

    @cached_property
    def all_refs(self) -> list[WtpRef]:
        """
        Extract all citation reference tags from text

        Args:
            text: Text containing citation tags

        Returns:
            List of WtpRef objects
        """
        return [WtpRef.load(t) for t in self.parsed.get_tags("ref")]

    # ---------- collecting refs ----------
    def _collect(self):
        for r in self.all_refs:
            if not r.name:
                logger.debug("Skipping unnamed ref at %s", r.span)
                continue

            content = r.contents
            if content.strip():
                full_str = r.tag.string
                self.full_refs_str.setdefault(r.name, full_str)
            else:
                self.short_refs_str.setdefault(r.name, []).append(r.span)

        logger.info(
            "Collected %d full refs and %d short ref names",
            len(self.full_refs_str),
            len(self.short_refs_str),
        )

    def get_all_citations(self, text: str) -> list[WtpRef]:
        return WtpRefs(text).all_refs

    def get_full_refs_str(self, text: str) -> dict[str, str]:
        return WtpRefs(text).full_refs_str

    def get_short_refs(self, text: str) -> list[WtpRef]:
        return [x for x in WtpRefs(text).all_refs if x.is_self_closing()]

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
