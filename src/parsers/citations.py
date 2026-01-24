"""
Citation parser for WikiText reference tags
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class Citation:
    """Represents a citation reference"""

    content: str
    tag: str
    name: str
    options: str

    def get_original_text(self) -> str:
        """Get the original reference tag"""
        return self.tag

    def get_content(self) -> str:
        """Get citation content"""
        return self.content

    def get_name(self) -> str:
        """Get citation name"""
        return self.name

    def get_attributes(self) -> str:
        """Get citation options/attributes"""
        return self.options

    def to_string(self) -> str:
        """Convert back to reference tag string"""
        return f"<ref {self.options.strip()}>{self.content}</ref>"


def get_name(options: str) -> str:
    """Extract the name attribute from citation options

    Args:
        options: Citation options string

    Returns:
        Extracted name or empty string if not found
    """
    options = options.strip()
    if not options:
        return ""

    pattern = r"name\s*\=\s*[\"']*([^>\"\']*)[\"\']*\s*"
    match = re.search(pattern, options, re.IGNORECASE)

    if not match or not match.group(1):
        return ""

    return match.group(1).strip()


def get_citations(text: str) -> List[Citation]:
    """Extract all citations from text

    Args:
        text: Text containing citations

    Returns:
        List of Citation objects
    """
    citations = []
    pattern = r"<ref([^\/>]*?)>(.+?)<\/ref>"
    matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)

    for options, content in matches:
        ref_tag = f"<ref{options}>{content}</ref>"
        name = get_name(options)
        citation = Citation(
            content=content,
            tag=ref_tag,
            name=name,
            options=options
        )
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
        if cite.name:
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
    pattern = r"<ref ([^\/>]*?)\/\s*>"
    matches = re.findall(pattern, text, re.IGNORECASE | re.DOTALL)

    for options in matches:
        ref_tag = f"<ref {options.strip()}/>"
        name = get_name(options)
        citation = Citation(
            content="",
            tag=ref_tag,
            name=name,
            options=options
        )
        citations.append(citation)

    return citations
