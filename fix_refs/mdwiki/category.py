"""
MDWiki category integration service.
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any
from collections.abc import Callable

from ..config import ConfigManager
from ..utils.http import get_url

logger = logging.getLogger(__name__)

# Languages that should not receive the MDWiki translation category
SKIP_LANGS_CATEGORY = ["it", "en", "bg"]


class MDWikiCategoryService:
    """Service for managing, fetching, and integrating MDWiki categories."""

    def __init__(
        self,
        config_manager: ConfigManager | None = None,
        url_getter: Callable[[str], str | None] | None = None,
        wikidata_url: str = "https://www.wikidata.org/w/rest.php/wikibase/v1/entities/items/Q107014860/sitelinks",
        skip_langs: list[str] | None = None,
    ) -> None:
        self.config_manager = config_manager or ConfigManager()
        self.url_getter = url_getter or get_url
        self.wikidata_url = wikidata_url
        self.skip_langs = skip_langs or SKIP_LANGS_CATEGORY

    def load_from_local_file(self) -> dict[str, Any]:
        """Load MDWiki categories from local JSON file.

        Returns:
            Dictionary of MDWiki categories or empty dict if file not found.
        """
        local_file = self.config_manager.resources_path / "mdwiki_categories.json"

        if not local_file.exists():
            return {}

        try:
            with open(local_file, "r", encoding="utf-8") as f:
                result: dict[str, Any] = json.load(f)  # type: ignore
                return result
        except (OSError, json.JSONDecodeError):
            return {}

    def get_cats(self) -> dict[str, Any]:
        """Fetch MDWiki categories from Wikidata API with fallback to local file.

        Returns:
            Dictionary of MDWiki categories.
        """
        server_name = os.environ.get("SERVER_NAME", "")
        if not server_name:
            return self.load_from_local_file()

        data = self.url_getter(self.wikidata_url)

        if not data:
            return self.load_from_local_file()

        try:
            decoded: Any = json.loads(data)  # type: ignore
            return decoded if isinstance(decoded, dict) else self.load_from_local_file()
        except json.JSONDecodeError:
            return self.load_from_local_file()

    def get_mdwiki_category(self, lang: str) -> str:
        """Get MDWiki category name for a specific language.

        Args:
            lang: Language code (e.g., 'en', 'es', 'fr').

        Returns:
            Category name or empty string.
        """
        if lang in self.skip_langs:
            return ""

        cats = self.get_cats()
        result = cats.get(f"{lang}wiki", {}).get("title", "Category:Translated from MDWiki")
        return str(result) if isinstance(result, str) else "Category:Translated from MDWiki"

    def add_translated_from_mdwiki(self, text: str, lang: str) -> str:
        """Add MDWiki category to text if not already present.

        Args:
            text: WikiText content.
            lang: Language code.

        Returns:
            Text with MDWiki category added if not present.
        """
        if lang in self.skip_langs:
            return text

        if re.search(r":\s*Translated[ _]from[ _]MDWiki\s*\]\]", text, re.IGNORECASE):
            return text

        cat = self.get_mdwiki_category(lang)

        if cat and cat not in text:
            text += f"\n[[{cat}]]\n"

        return text


# Default service instance for legacy functions
_default_service = MDWikiCategoryService()


def load_from_local_file() -> dict[str, Any]:
    """Legacy entry point. Use MDWikiCategoryService.load_from_local_file instead."""
    return _default_service.load_from_local_file()


def get_cats() -> dict[str, Any]:
    """Legacy entry point. Use MDWikiCategoryService.get_cats instead."""
    return _default_service.get_cats()


def get_mdwiki_category(lang: str) -> str:
    """Legacy entry point. Use MDWikiCategoryService.get_mdwiki_category instead."""
    return _default_service.get_mdwiki_category(lang)


def add_translated_from_mdwiki(text: str, lang: str) -> str:
    """Legacy entry point. Use MDWikiCategoryService.add_translated_from_mdwiki instead."""
    return _default_service.add_translated_from_mdwiki(text, lang)


__all__ = [
    "MDWikiCategoryService",
    "load_from_local_file",
    "get_cats",
    "get_mdwiki_category",
    "add_translated_from_mdwiki",
]
