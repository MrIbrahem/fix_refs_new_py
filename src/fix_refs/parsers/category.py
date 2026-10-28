"""
Category parser for WikiText category tags
"""

from __future__ import annotations

import logging

import wikitextparser as wtp

logger = logging.getLogger(__name__)


class CategoryParser:
    """Parser for extracting and checking MediaWiki category tags in text."""

    def get_categories(self, text: str) -> dict[str, str]:
        """Extract all categories from text

        Args:
            text: Text containing category tags

        Returns:
            Dictionary mapping category names to their full category tags
        """
        categories: dict[str, str] = {}

        wikilinks: list[wtp.WikiLink] = wtp.parse(text).wikilinks

        for link in wikilinks:
            # link.target is the part before the "|", e.g. "Category:Foo"
            prefix, sep, name = link.target.partition(":")

            # Skip links without a namespace prefix, and leading-colon links
            # such as [[:Category:Foo]], which are plain links, not categorizations
            if not sep or prefix.strip().lower() != "category":
                continue

            category_name = name.strip()
            if category_name:
                # link.string is the full tag, e.g. "[[Category:Foo|sortkey]]"
                categories[category_name] = link.string

        return categories

    def has_category(self, text: str, category_name: str) -> bool:
        """Check if text contains a specific category

        Args:
            text: Text to search
            category_name: Category name to look for

        Returns:
            True if category is present
        """
        return category_name in self.get_categories(text)


__all__ = [
    "CategoryParser",
]
