"""
MDWiki category integration service.
"""

from __future__ import annotations

import json
import logging
import os
import re
from typing import Any

from ..config import ConfigManager
from ..utils.http import HttpClient

logger = logging.getLogger(__name__)

# Languages that should not receive the MDWiki translation category
SKIP_LANGS_CATEGORY = ["it", "en", "bg"]


class MDWikiCategoryService:
    """Service for managing, fetching, and integrating MDWiki categories."""

    def __init__(
        self,
        config_manager: ConfigManager | None = None,
        wikidata_url: str = "https://www.wikidata.org/w/rest.php/wikibase/v1/entities/items/Q107014860/sitelinks",
        skip_langs: list[str] | None = None,
        http_client: HttpClient | None = None,
    ) -> None:
        self.http_client = http_client or HttpClient()
        self.config_manager = config_manager or ConfigManager()
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

        data = self.http_client.get_url(self.wikidata_url)

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


__all__ = [
    "MDWikiCategoryService",
]
