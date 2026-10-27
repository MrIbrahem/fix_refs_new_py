"""
Main PageFixer class
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from typing import Any

from ..fixers import (
    ReferenceExpander,
    MiniFixes,
    add_lang_en_to_refs,
    is_redirect,
    move_dots_after_refs,
    remove_duplicate_refs_with_attrs,
)
from ..infobox import expand_infobox_in_text
from ..lang_bots import apply_language_fixes
from ..mdwiki import MDWikiCategoryService

logger = logging.getLogger(__name__)


@dataclass
class LangSetting:
    """Per-language fixing options."""

    lang: str
    move_dots: bool = True
    expend_infobox: bool = True
    add_en_lang: bool = False
    add_category: bool = False

    def to_json(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_any(cls, setting: LangSetting | dict[str, Any]) -> LangSetting:
        """Create LangSetting from any input."""
        if isinstance(setting, LangSetting):
            return setting

        return cls(**setting)


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
    # Steps
    # ------------------------------------------------------------------
    def _expand_infobox_if_needed(self) -> None:
        if self.lang_setting.expend_infobox or self.lang_setting.lang == "es":
            self.text = expand_infobox_in_text(self.text, self.title, "")

    def _apply_basic_fixes(self) -> None:
        self.text = MiniFixes().mini_fixes(self.text, self.lang_setting.lang)
        self.text = ReferenceExpander().fix_missing_refs(self.text, self.source_title, self.mdwiki_revid)
        self.text = remove_duplicate_refs_with_attrs(self.text)

    def _move_dots(self) -> None:
        logger.info("move_dots\n")
        self.text = move_dots_after_refs(self.text, self.lang_setting.lang)

    def _add_en_lang(self) -> None:
        logger.info("add_en_lang\n")
        self.text = add_lang_en_to_refs(self.text)

    def _apply_language_fixes(self) -> None:
        fixed = apply_language_fixes(
            self.text,
            self.title,
            self.lang_setting.lang,
            self.source_title,
            self.mdwiki_revid,
        )
        if fixed:
            self.text = fixed
            # Re-expand infobox if language fixes made changes
            self._expand_infobox_if_needed()

    def _add_mdwiki_category(self) -> None:
        if self.lang_setting.add_category:
            self.text = MDWikiCategoryService().add_translated_from_mdwiki(self.text, self.lang_setting.lang)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run(self) -> str:
        """Run all fixes and return the fixed page content."""
        logger.info("start fix one page with mdwiki_revid:%s", self.mdwiki_revid)

        if is_redirect(self.title, self.text):
            return self.text

        self._expand_infobox_if_needed()
        self._apply_basic_fixes()

        if self.lang_setting.move_dots:
            self._move_dots()

        if self.lang_setting.add_en_lang:
            self._add_en_lang()

        self._apply_language_fixes()
        self._add_mdwiki_category()
        self.text = MiniFixes().mini_fixes_after_fixing(self.text, self.lang_setting.lang)

        if not self.text.strip():
            return self.text_org

        return self.text


__all__ = [
    "LangSetting",
    "PageFixer",
]
