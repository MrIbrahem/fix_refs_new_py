"""
Category parser for WikiText category tags
"""

import re
from typing import Dict, List


def get_categories(text: str) -> Dict[str, str]:
    """Extract all categories from text

    Args:
        text: Text containing category tags

    Returns:
        Dictionary mapping category names to their full category tags
    """
    categories: Dict[str, str] = {}

    # Find all [[...]] patterns
    for match in re.finditer(r'\[\[.+?\]\]', text):
        full_match = match.group(0)

        # Extract the word between [[ and :
        prefix_match = re.match(r'\[\[([^\:]+?)\s*:', full_match)
        if prefix_match:
            prefix_word = prefix_match.group(1).strip().lower()
            # Check if it's "category" (case-insensitive)
            if prefix_word == 'category':
                # Extract content after the colon
                colon_pos = full_match.find(':')
                if colon_pos > 0:
                    category_content = full_match[colon_pos+1:-2]

                    parts = category_content.split("|")
                    category_name = parts[0].strip() if parts else category_content.strip()

                    if category_name:
                        categories[category_name] = full_match

    return categories


def get_category_list(text: str) -> List[str]:
    """Extract category names as a list

    Args:
        text: Text containing category tags

    Returns:
        List of category names
    """
    categories = get_categories(text)
    return list(categories.keys())


def has_category(text: str, category_name: str) -> bool:
    """Check if text contains a specific category

    Args:
        text: Text to search
        category_name: Category name to look for

    Returns:
        True if category is present
    """
    categories = get_categories(text)
    return category_name in categories
