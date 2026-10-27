"""
Main PageFixer class
"""

from __future__ import annotations

import logging
from typing import Any

from .fix_page import PageUpdater
from .mapping import LangSetting

logger = logging.getLogger(__name__)


class PageFixer:
    """Fix Wikipedia page references and formatting.

    Args:
        text: Page content
        title: Page title
        lang_setting: Per-language options (LangSetting). Defaults to LangSetting().
        source_title: Source page title
        mdwiki_revid: MDWiki revision ID
    """

    def __init__(
        self,
        *,
        text: str,
        title: str,
        lang_setting: LangSetting | dict[str, Any],
        source_title: str = "",
        mdwiki_revid: int | str = 0,
    ) -> None:
        self.text_org = text
        self.text = text
        self.title = title
        self.lang_setting = LangSetting.from_any(lang_setting)
        self.source_title = source_title
        self.mdwiki_revid = int(mdwiki_revid)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run(self) -> str:
        """Run all fixes and return the fixed page content."""
        return PageUpdater().run(
            text=self.text,
            title=self.title,
            lang_setting=self.lang_setting,
            source_title=self.source_title,
            mdwiki_revid=self.mdwiki_revid,
        )


__all__ = [
    "PageFixer",
]
