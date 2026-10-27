"""
Citation parser for WikiText reference tags
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import wikitextparser as wtp


logger = logging.getLogger(__name__)


@dataclass
class Citation:
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

    def make_short(self) -> str:
        """Convert to self-closing tag string"""
        attributes = self.get_str_attributes()
        if attributes:
            return f"<ref {attributes} />"
        return self.tag.string

    def to_string(self) -> str:
        """Convert back to reference tag string"""
        if self.is_self_closing():
            return self.tag.string.replace("></ref>", " />")

        return self.tag.string

    def is_self_closing(self) -> bool:
        return not self.tag.contents or not self.tag.contents.strip()

    @classmethod
    def from_text(cls, ref_text: str) -> Citation:
        """Create a Citation from a reference tag string"""

        if not ref_text.strip().startswith("<ref"):
            raise ValueError("Not a reference tag")

        if ref_text.count("<ref") != 1:
            raise ValueError("Multiple reference tags")

        tag = wtp.Tag(ref_text)
        return Citation.load(tag)

    @classmethod
    def load(cls, ref: wtp.Tag) -> Citation:
        return cls(tag=ref)


class CitationsParser:
    """Parser for extracting reference tags and citations from WikiText."""

    def get_all_citations(self, text: str) -> list[Citation]:
        """Extract all citation reference tags from text

        Args:
            text: Text containing citation tags

        Returns:
            List of Citation objects
        """
        citations: list[Citation] = []
        parsed = wtp.parse(text)

        for tag in parsed.get_tags():
            if tag.name == "ref":
                # citations.append(Citation.from_text(tag.string))
                citations.append(Citation.load(tag))

        return citations

    def get_full_refs(self, text: str) -> dict[str, str]:
        """Get mapping of citation names to their full reference tags

        Args:
            text: Text containing citations

        Returns:
            Dictionary mapping citation names to their full tags
        """
        full = {}
        citations = self.get_all_citations(text)

        for cite in citations:
            if cite.contents and cite.name:
                full[cite.name] = cite.tag_str

        return full

    def get_short_refs(self, text: str) -> list[Citation]:
        """Extract short/empty citations (self-closing tags)

        Args:
            text: Text containing short citations

        Returns:
            List of Citation objects for short references
        """
        citations = []
        parsed = wtp.parse(text)
        for tag in parsed.get_tags():
            if tag.name == "ref" and not tag.contents:
                # citations.append(Citation.from_text(tag.string))
                citations.append(Citation.load(tag))

        return citations

    def remove_duplicate(self, text: str) -> str:
        """Remove duplicate references by converting them to self-closing tags

        First occurrence keeps full content, subsequent references become <ref name="..."/>

        Args:
            text: Text containing citations

        Returns:
            Text with duplicate references converted to self-closing tags
        """
        new_text = text
        refs_to_check: dict[str, str] = {}
        refs: dict[str, str] = {}
        citations: list[Citation] = self.get_all_citations(text)

        numb = 0

        for citation in citations:
            cite_fulltext = citation.tag_str
            cite_attrs = citation.get_str_attributes()
            content = citation.contents.strip()

            if not content:
                continue

            if not cite_attrs or not citation.name:
                numb += 1
                name = f"autogen_{numb}"
                citation.tag.attrs["name"] = name
                cite_attrs = citation.get_str_attributes()

            logger.debug(f"\n cite_attrs: (({cite_attrs}))")

            short_tag = citation.make_short()

            if cite_attrs in refs:
                new_text = new_text.replace(cite_fulltext, short_tag)
            else:
                refs_to_check[short_tag] = cite_fulltext
                refs[cite_attrs] = True  # pyright: ignore[reportArgumentType]

        for key, value in refs_to_check.items():
            if value not in new_text:
                new_text = new_text.replace(key, value, 1)

        return new_text


__all__ = [
    "Citation",
    "CitationsParser",
]
