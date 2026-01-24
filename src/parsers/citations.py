"""
Citation parser for WikiText reference tags
"""

import re
import wikitextparser as wtp
from dataclasses import dataclass
from typing import Any, List, Dict


@dataclass
class Citation:
    """Represents a citation reference"""

    ref: Any

    # content=tag.contents,
    # tag=tag.string,
    # name=tag.attrs.get("name", ""),
    # options=tag.attrs
    def get_original_text(self) -> str:
        """Get the original reference tag"""
        return self.tag

    def get_content(self) -> str:
        """Get citation content"""
        return self.ref.contents

    def set_contents(self, new_content: str) -> None:
        """Set citation content"""
        if new_content or self.ref.contents:
            self.ref.contents = new_content

    def get_name(self) -> str:
        """Get citation name"""
        return self.ref.attrs.get("name", "")

    @property
    def tag(self) -> str:
        """Get citation string"""
        return self.ref.string

    @property
    def cite(self) -> str:
        return self.ref

    @property
    def content(self) -> str:
        """Get citation content"""
        return self.get_content()

    @property
    def name(self) -> str:
        """Get citation name"""
        return self.get_name()

    def get_attributes(self) -> str:
        """Get citation options/attributes"""
        return str(self.ref.attrs)

    def to_string(self) -> str:
        """Convert back to reference tag string"""
        # return f"<ref {self.options.strip()}>{self.content}</ref>"
        text = self.ref.string
        # if text like `<ref name="Zip2015"></ref>` change to self-closing tag
        if self.content == "":
            text = text.replace("></ref>", " />")

        return text

    @property
    def options(self) -> str:
        """Get citation options/attributes"""
        return self.get_attributes()


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
            citation = Citation(ref=tag)
            citations.append(citation)

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
        if cite.content and cite.name:
            full[cite.name] = cite.tag

    return full


def get_short_citations(text: str) -> List[Citation]:
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
            citation = Citation(ref=tag)
            citations.append(citation)

    return citations
