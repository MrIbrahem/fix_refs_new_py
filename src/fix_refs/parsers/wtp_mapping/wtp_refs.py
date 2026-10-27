""" """

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
    text: str
    tpls: WtpTemplates = field(init=False, repr=False)
    parsed: wtp.WikiText = field(init=False, repr=False)

    # name -> '<ref name="x">...</ref>'
    full_refs: dict[str, str] = field(init=False, default_factory=dict)
    # name -> spans of short refs (no content)
    short_refs: dict[str, list[tuple[int, int]]] = field(init=False, default_factory=dict)

    def __post_init__(self):
        self.tpls = WtpTemplates(self.text)
        self.parsed = self.tpls.parsed
        self._collect()

    # ---------- tag writer ----------
    @staticmethod
    def make_full(content: str, **kwargs) -> str:
        tag = wtp.Tag(f"<ref>{content}</ref>")
        for k, v in kwargs.items():
            tag.set_attr(k, v)
        return tag.string

    @staticmethod
    def make_short(name: str) -> str:
        return f'<ref name="{name}" />'

    @staticmethod
    def _short_from(r: wtp.Tag) -> str:
        """Build a self-closing tag that keeps all original attributes."""
        clone_r = wtp.Tag(r.string)
        clone_r.contents = ""
        result = clone_r.string
        return result.replace("></ref>", " />")

    @staticmethod
    def get_name(r: wtp.Tag) -> str:
        return r.get_attr("name") or ""

    # ---------- helpers ----------

    @cached_property
    def all_refs(self) -> list[wtp.Tag]:
        return self.parsed.get_tags("ref")

    @cached_property
    def tpl_refs(self) -> list:
        return [r for r in self.all_refs if self.tpls.contains(r.span)]

    @cached_property
    def body_refs(self) -> list:
        return [r for r in self.all_refs if not self.tpls.contains(r.span)]

    # ---------- collecting refs ----------
    def _collect(self):
        for r in self.all_refs:
            name = self.get_name(r)
            content = (r.contents or "").strip()
            if not name:
                logger.debug("Skipping unnamed ref at %s", r.span)
                continue
            if content:
                self.full_refs.setdefault(name, self.make_full(content, name=name))
            else:
                self.short_refs.setdefault(name, []).append(r.span)
        logger.info(
            "Collected %d full refs and %d short ref names",
            len(self.full_refs),
            len(self.short_refs),
        )

    @cached_property
    def tpl_full_refs(self) -> dict[str, str]:
        """Full refs found inside templates only."""
        out = {}
        for r in self.tpl_refs:
            name, content = self.get_name(r), (r.contents or "").strip()
            if name and content:
                out.setdefault(name, self.make_full(content, name=name))
        return out

    @cached_property
    def body_full_refs(self) -> dict[str, str]:
        """Full refs found in the body only."""
        out = {}
        for r in self.body_refs:
            name, content = self.get_name(r), (r.contents or "").strip()
            if name and content:
                out.setdefault(name, self.make_full(content, name=name))
        return out

    @cached_property
    def body_short_names(self) -> set[str]:
        return {self.get_name(r) for r in self.body_refs if self.get_name(r) and not (r.contents or "").strip()}

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
            name = self.get_name(r)
            content = (r.contents or "").strip()
            if not name or not content:
                continue

            key = (name, (r.get_attr("group") or ""))
            if key not in seen:
                seen.add(key)
                continue

            edits.append((r.span, self._short_from(r)))

        # Apply from the end so earlier spans stay valid
        for (start, end), short in reversed(edits):
            text = text[:start] + short + text[end:]

        logger.info("Replaced %d duplicate refs with short refs", len(edits))
        return text


__all__ = [
    "WtpRefs",
]
