from __future__ import annotations

import logging

from ...config import ConfigManager
from .expend_refs import RefExpander

logger = logging.getLogger(__name__)


class ReferenceExpander:
    """Service for finding MDWiki revisions and expanding missing citations in text."""

    def __init__(self, config_manager: ConfigManager | None = None) -> None:
        """Initialize the reference expander with an optional config manager."""
        self.config_manager = config_manager or ConfigManager.load()
        self._ref_expander = RefExpander()

    def fix_missing_refs(
        self,
        text: str,
        sourcetitle: str = "",
        mdwiki_revid: int = 0,
        full_text: str = "",
    ) -> str:
        """Fix missing references by expanding from MDWiki source.

        Args:
            text: Text to fix.
            sourcetitle: Source page title.
            mdwiki_revid: MDWiki revision ID.
            full_text: Original full source page content from mdwiki.org

        Returns:
            Text with missing references expanded.
        """
        full_text = full_text or self.config_manager.get_full_text(sourcetitle, mdwiki_revid)

        if not full_text:
            return text

        return self._ref_expander.run(text, full_text)


__all__ = [
    "ReferenceExpander",
]
