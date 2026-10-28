"""
Citation parser for WikiText reference tags
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from functools import cached_property

import wikitextparser as wtp

from .wtp_temps import WtpTemplates

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

    text: str
    parsed: wtp.WikiText = field(init=False, repr=False)
    tpls: WtpTemplates = field(init=False, repr=False)

    # name -> '<ref name="x">...</ref>'
    full_refs_str: dict[str, str] = field(init=False, default_factory=dict)
    # name -> spans of short refs (no content)
    short_refs_str: dict[str, list[tuple[int, int]]] = field(init=False, default_factory=dict)

    def __post_init__(self):
        self.tpls = WtpTemplates(self.text)
        self.parsed = self.tpls.parsed
        self._collect()

    # ---------- Templates related ----------

    @cached_property
    def tpl_refs(self) -> list[WtpRef]:
        return [r for r in self.all_refs if self.tpls.contains(r.span)]

    @cached_property
    def body_refs(self) -> list[WtpRef]:
        return [r for r in self.all_refs if not self.tpls.contains(r.span)]

    @cached_property
    def tpl_full_refs(self) -> dict[str, str]:
        """Full refs found inside templates only."""
        return self._full_refs_of(self.tpl_refs)

    @cached_property
    def body_full_refs(self) -> dict[str, str]:
        """Full refs found in the body only."""
        return self._full_refs_of(self.body_refs)

    @staticmethod
    def _full_refs_of(refs: list[WtpRef]) -> dict[str, str]:
        out: dict[str, str] = {}
        for r in refs:
            content = r.contents.strip()
            if r.name and content:
                full_str = r.tag.string
                out.setdefault(r.name, full_str)
        return out

    @cached_property
    def body_short_names(self) -> set[str]:
        return {r.name for r in self.body_refs if r.name and r.is_self_closing()}

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
