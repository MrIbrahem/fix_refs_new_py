"""
MDWiki category integration
"""

import json
import os
from typing import Any

from ..config import resources_path
from ..utils.http import get_url


def load_from_local_file() -> dict[str, Any]:
    """Load MDWiki categories from local JSON file

    Returns:
        Dictionary of MDWiki categories or empty dict if file not found
    """
    local_file = resources_path / "mdwiki_categories.json"

    if not local_file.exists():
        return {}

    try:
        with open(local_file, "r", encoding="utf-8") as f:
            result: dict[str, Any] = json.load(f)  # type: ignore
            return result
    except (OSError, json.JSONDecodeError):
        return {}


def get_cats() -> dict[str, Any]:
    """Fetch MDWiki categories from Wikidata API with fallback to local file

    Returns:
        Dictionary of MDWiki categories
    """
    server_name = os.environ.get("SERVER_NAME", "")
    if not server_name:
        return load_from_local_file()

    url = "https://www.wikidata.org/w/rest.php/wikibase/v1/entities/items/Q107014860/sitelinks"
    data = get_url(url)

    if not data:
        return load_from_local_file()

    try:
        decoded: Any = json.loads(data)  # type: ignore
        return decoded if isinstance(decoded, dict) else load_from_local_file()
    except json.JSONDecodeError:
        return load_from_local_file()


def get_mdwiki_category(lang: str) -> str:
    """Get MDWiki category name for a specific language

    Args:
        lang: Language code (e.g., 'en', 'es', 'fr')

    Returns:
        Category name or empty string
    """
    skip_langs = ["it", "en"]

    if lang in skip_langs:
        return ""

    cats = get_cats()
    result = cats.get(f"{lang}wiki", {}).get("title", "Category:Translated from MDWiki")
    return str(result) if isinstance(result, str) else "Category:Translated from MDWiki"


def add_translated_from_mdwiki(text: str, lang: str) -> str:
    """Add MDWiki category to text if not already present

    Args:
        text: WikiText content
        lang: Language code

    Returns:
        Text with MDWiki category added if not present
    """
    import re

    skip_langs = ["it", "en", "bg"]

    if lang in skip_langs:
        return text

    if re.search(r":\s*Translated[ _]from[ _]MDWiki\s*\]\]", text, re.IGNORECASE):
        return text

    cat = get_mdwiki_category(lang)

    if cat and cat not in text:
        text += f"\n[[{cat}]]\n"

    return text
