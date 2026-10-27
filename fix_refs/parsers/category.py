"""
Category parser for WikiText category tags
"""

from __future__ import annotations

import logging
import re

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

        # Find all [[...]] patterns
        for match in re.finditer(r"\[\[.+?\]\]", text):
            full_match = match.group(0)

            # Extract the word between [[ and :
            prefix_match = re.match(r"\[\[([^\:]+?)\s*:", full_match)
            if prefix_match:
                prefix_word = prefix_match.group(1).strip().lower()
                # Check if it's "category" (case-insensitive)
                if prefix_word == "category":
                    # Extract content after the colon
                    colon_pos = full_match.find(":")
                    if colon_pos > 0:
                        category_content = full_match[colon_pos + 1 : -2]

                        parts = category_content.split("|")
                        category_name = parts[0].strip() if parts else category_content.strip()

                        if category_name:
                            categories[category_name] = full_match

        return categories

    def get_category_list(self, text: str) -> list[str]:
        """Extract category names as a list

        Args:
            text: Text containing category tags

        Returns:
            List of category names
        """
        categories = self.get_categories(text)
        return list(categories.keys())

    def has_category(self, text: str, category_name: str) -> bool:
        """Check if text contains a specific category

        Args:
            text: Text to search
            category_name: Category name to look for

        Returns:
            True if category is present
        """
        categories = self.get_categories(text)
        return category_name in categories


def get_categories(text: str) -> dict[str, str]:
    """Legacy wrapper for CategoryParser.get_categories."""
    return CategoryParser().get_categories(text)


def get_category_list(text: str) -> list[str]:
    """Legacy wrapper for CategoryParser.get_category_list."""
    return CategoryParser().get_category_list(text)


def has_category(text: str, category_name: str) -> bool:
    """Legacy wrapper for CategoryParser.has_category."""
    return CategoryParser().has_category(text, category_name)


__all__ = [
    "CategoryParser",
    "get_categories",
    "get_category_list",
    "has_category",
]
