"""
Citation parser for WikiText reference tags
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Dict
import wikitextparser as wtp


@dataclass
class Citation:
    """Represents a citation reference"""

    def __init__(self, ref: wtp._tag.Tag) -> None:
        self.ref: wtp._tag.Tag = ref
        self.tag = self.ref.string
        self.contents = self.ref.contents or ""
        self.options = dict(self.ref.attrs)
        self.attrs = self.ref.attrs

    @property
    def name(self) -> str:
        """Get citation name"""
        return self.ref.attrs.get("name", "")

    def get_original_text(self) -> str:
        """Get the original reference tag"""
        return self.tag

    def get_content(self) -> str:
        """Get citation content"""
        return self.contents

    def set_contents(self, new_content: str) -> None:
        """Set citation content"""
        if new_content or self.ref.contents:
            self.ref.contents = new_content

    def get_name(self) -> str:
        """Get citation name"""
        return self.name

    def get_attributes(self) -> str:
        """Get citation options/attributes as a string"""
        tag_str = str(self.ref.string)
        # Find the end of the opening tag: could be ">" or "/>"
        close_idx = tag_str.find(">")
        if close_idx == -1:
            return ""
        attrs_part = tag_str[len("<ref") : close_idx]
        # Strip trailing "/" for self-closing tags
        attrs_part = attrs_part.rstrip(" /")
        return attrs_part.strip()

    def to_string_self_closing(self) -> str:
        """Convert to self-closing tag string"""
        attributes = self.get_attributes()
        if attributes:
            return f"<ref {attributes} />"
        return self.ref.string

    def to_string(self) -> str:
        """Convert back to reference tag string"""
        if self.is_self_closing():
            return self.ref.string.replace("></ref>", " />")

        return self.ref.string

    def is_self_closing(self) -> bool:
        return not self.contents or not self.contents.strip()

    @classmethod
    def from_text(cls, ref_text: str) -> Citation:
        return Citation(wtp._tag.Tag(ref_text))


def get_citations(text: str) -> List[Citation]:
    """Extract all citations from text

    Args:
        text: Text containing citations

    Returns:
        List of Citation objects
    """

    citations = []
    parsed = wtp.parse(text)
    for tag in parsed.get_tags():
        if tag.name == "ref":
            # citations.append(Citation.from_text(tag.string))
            citations.append(Citation(tag))

    return citations


def get_full_refs(text: str) -> Dict[str, str]:
    """Get mapping of citation names to their full reference tags

    Args:
        text: Text containing citations

    Returns:
        Dictionary mapping citation names to their full tags
    """
    full = {}
    citations = get_citations(text)

    for cite in citations:
        if cite.contents and cite.name:
            full[cite.name] = cite.tag

    return full


def get_short_refs(text: str) -> List[Citation]:
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
            citations.append(Citation(tag))

    return citations
