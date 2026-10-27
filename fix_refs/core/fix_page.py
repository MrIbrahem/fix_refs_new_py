"""
Main PageUpdater class
"""

from __future__ import annotations

import logging
from typing import Any

from ..fixers import (
    DotsMover,
    DuplicateRefRemover,
    LanguageEnFixer,
    MiniFixes,
    RedirectDetector,
    ReferenceExpander,
)
from ..infobox import InfoboxExpander
from ..lang_bots import LanguageFixerPipeline
from ..mdwiki import MDWikiCategoryService
from .mapping import LangSetting

logger = logging.getLogger(__name__)


class PageUpdater:
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
        mini_fixes: MiniFixes | None = None,
        ref_expander: ReferenceExpander | None = None,
        duplicate_ref_remover: DuplicateRefRemover | None = None,
        dots_mover: DotsMover | None = None,
        lang_en_fixer: LanguageEnFixer | None = None,
        language_pipeline: LanguageFixerPipeline | None = None,
        infobox_expander: InfoboxExpander | None = None,
        redirect_detector: RedirectDetector | None = None,
        mdwiki_category_service: MDWikiCategoryService | None = None,
    ) -> None:
        self.text_org = text
        self.text = text
        self.title = title
        self.lang_setting = LangSetting.from_any(lang_setting)
        self.source_title = source_title
        self.mdwiki_revid = int(mdwiki_revid)

        # Injected collaborators
        self.mini_fixes = mini_fixes or MiniFixes()
        self.ref_expander = ref_expander or ReferenceExpander()
        self.duplicate_ref_remover = duplicate_ref_remover or DuplicateRefRemover()
        self.dots_mover = dots_mover or DotsMover()
        self.lang_en_fixer = lang_en_fixer or LanguageEnFixer()
        self.language_pipeline = language_pipeline or LanguageFixerPipeline()
        self.infobox_expander = infobox_expander or InfoboxExpander()
        self.redirect_detector = redirect_detector or RedirectDetector()
        self.mdwiki_category_service = mdwiki_category_service or MDWikiCategoryService()

    # ------------------------------------------------------------------
    # Steps
    # ------------------------------------------------------------------
    def _expand_infobox_if_needed(self) -> None:
        if self.lang_setting.expend_infobox or self.lang_setting.lang == "es":
            self.text = self.infobox_expander.expand_infobox_in_text(self.text, self.title, "")

    def _apply_basic_fixes(self) -> None:
        self.text = self.mini_fixes.mini_fixes(self.text, self.lang_setting.lang)
        self.text = self.ref_expander.fix_missing_refs(self.text, self.source_title, self.mdwiki_revid)
        self.text = self.duplicate_ref_remover.remove_duplicate_refs_with_attrs(self.text)

    def _move_dots(self) -> None:
        logger.info("move_dots\n")
        self.text = self.dots_mover.move_dots_after_refs(self.text, self.lang_setting.lang)

    def _add_en_lang(self) -> None:
        logger.info("add_en_lang\n")
        self.text = self.lang_en_fixer.add_lang_en_to_refs(self.text)

    def _apply_language_fixes(self) -> None:
        fixed = self.language_pipeline.apply_language_fixes(
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
            self.text = self.mdwiki_category_service.add_translated_from_mdwiki(self.text, self.lang_setting.lang)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run(self) -> str:
        """Run all fixes and return the fixed page content."""
        logger.info("start fix one page with mdwiki_revid:%s", self.mdwiki_revid)

        if self.redirect_detector.is_redirect(self.title, self.text):
            return self.text

        self._expand_infobox_if_needed()
        self._apply_basic_fixes()

        if self.lang_setting.move_dots:
            self._move_dots()

        if self.lang_setting.add_en_lang:
            self._add_en_lang()

        self._apply_language_fixes()
        self._add_mdwiki_category()
        self.text = self.mini_fixes.mini_fixes_after_fixing(self.text, self.lang_setting.lang)

        if not self.text.strip():
            return self.text_org

        return self.text


__all__ = [
    "PageUpdater",
]
