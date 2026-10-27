"""
Remove duplicate references by converting them to named short references
"""

from __future__ import annotations

import logging

from ...parsers.citations_parser import Citation, CitationsParser

logger = logging.getLogger(__name__)


class DuplicateRefRemover:
    """Remover for duplicate references by converting subsequent occurrences into self-closing tags."""

    def __init__(self, citations_parser: CitationsParser | None = None) -> None:
        self.citations_parser = citations_parser or CitationsParser()

    def remove_duplicate_refs_with_attrs(self, text: str) -> str:
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
        citations: list[Citation] = self.citations_parser.get_all_citations(text)

        numb = 0

        for citation in citations:
            cite_fulltext = citation.tag
            cite_attrs = citation.get_attributes()
            content = citation.contents.strip()

            if not content:
                continue

            if not cite_attrs or not citation.name:
                numb += 1
                name = f"autogen_{numb}"
                citation.ref.attrs["name"] = name
                cite_attrs = citation.get_attributes()

            logger.debug(f"\n cite_attrs: (({cite_attrs}))")

            short_tag = citation.to_string_self_closing()

            if cite_attrs in refs:
                new_text = new_text.replace(cite_fulltext, short_tag)
            else:
                refs_to_check[short_tag] = cite_fulltext
                refs[cite_attrs] = True  # pyright: ignore[reportArgumentType]

        for key, value in refs_to_check.items():
            if value not in new_text:
                # pattern = re.escape(key)
                # new_text = re.sub(pattern, value, new_text, count=1)
                new_text = new_text.replace(key, value, 1)

        return new_text


__all__ = [
    "DuplicateRefRemover",
]
