from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from ...config import ConfigManager
from ...parsers.citations_parser import CitationsParser
from .expend_refs import RefExpander

logger = logging.getLogger(__name__)


class ReferenceExpander:
    """Service for finding MDWiki revisions and expanding missing citations in text."""

    def __init__(self, config_manager: ConfigManager | None = None) -> None:
        """Initialize the reference expander with an optional config manager."""
        self._config_manager = config_manager or ConfigManager.load()
        self._citations_parser = CitationsParser()
        self._ref_expander = RefExpander(self._citations_parser)

    def find_mdwiki_revid(self, sourcetitle: str) -> str:
        """Find MDWiki revision ID from JSON file.

        Args:
            sourcetitle: Source page title.

        Returns:
            MDWiki revision ID or empty string.
        """
        json_file = f"{self._config_manager.revisions_path}/json_data.json"

        if not Path(json_file).exists():
            return ""

        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data: dict[str, Any] = json.load(f)  # type: ignore

            logger.info(f"url{json_file}")
            logger.info(f"count of data: {len(data)}")

            result = data.get(sourcetitle, "")
            return str(result) if isinstance(result, str) else ""
        except (OSError, json.JSONDecodeError):
            return ""

    def get_full_text(self, sourcetitle: str, mdwiki_revid: int) -> str:
        """Get full text from MDWiki revision.

        Args:
            sourcetitle: Source page title.
            mdwiki_revid: MDWiki revision ID.

        Returns:
            Full text or empty string.
        """
        sourcetitle = sourcetitle.replace(" ", "_")

        if mdwiki_revid == 0:
            revid_str = self.find_mdwiki_revid(sourcetitle)
            mdwiki_revid = int(revid_str) if revid_str.isdigit() else 0

        if mdwiki_revid == 0:
            logger.info(f"empty mdwiki_revid, sourcetitle:({sourcetitle})")
            return ""

        file_path = self._config_manager.get_revision_file_path(mdwiki_revid)

        if not Path(file_path).exists():
            logger.info(f"file not found: {file_path}")
            return ""

        logger.info(f"url{file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except OSError:
            return ""

    def fix_missing_refs(self, text: str, sourcetitle: str, mdwiki_revid: int = 0) -> str:
        """Fix missing references by expanding from MDWiki source.

        Args:
            text: Text to fix.
            sourcetitle: Source page title.
            mdwiki_revid: MDWiki revision ID.

        Returns:
            Text with missing references expanded.
        """
        short_refs = self._citations_parser.get_short_refs(text)

        logger.debug(f"empty refs: {len(short_refs)}")

        if not short_refs:
            return text

        full_text = self.get_full_text(sourcetitle, mdwiki_revid)

        if not full_text:
            return text

        expanded_text: str = self._ref_expander.refs_expand(short_refs, text, full_text)
        return expanded_text


__all__ = [
    "ReferenceExpander",
]
