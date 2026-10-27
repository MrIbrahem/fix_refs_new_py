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
from .mapping import LangSetting, PageContext

logger = logging.getLogger(__name__)


class PageUpdater:
    """Stateless page fixer. Create once, call run() for each page."""

    def __init__(
        self,
        mdwiki_category_service: MDWikiCategoryService | None = None,
    ) -> None:

        # Injected collaborators
        self.mini_fixes = MiniFixes()
        self.ref_expander = ReferenceExpander()
        self.duplicate_ref_remover = DuplicateRefRemover()
        self.dots_mover = DotsMover()
        self.lang_en_fixer = LanguageEnFixer()
        self.language_pipeline = LanguageFixerPipeline()
        self.infobox_expander = InfoboxExpander()
        self.redirect_detector = RedirectDetector()
        self.mdwiki_category_service = mdwiki_category_service or MDWikiCategoryService()

    # ---------------- Steps (each one updates ctx.text) ----------------
    def _expand_infobox_if_needed(self, ctx: PageContext) -> None:
        if ctx.lang_setting.expend_infobox or ctx.lang_setting.lang == "es":
            ctx.text = self.infobox_expander.expand_infobox_in_text(ctx.text, ctx.title, "")

    def _apply_basic_fixes(self, ctx: PageContext) -> None:
        lang = ctx.lang_setting.lang
        ctx.text = self.mini_fixes.mini_fixes(ctx.text, lang)
        ctx.text = self.ref_expander.fix_missing_refs(ctx.text, ctx.source_title, ctx.mdwiki_revid)
        ctx.text = self.duplicate_ref_remover.remove_duplicate_refs_with_attrs(ctx.text)

    def _move_dots(self, ctx: PageContext) -> None:
        logger.info("move_dots\n")
        ctx.text = self.dots_mover.move_dots_after_refs(ctx.text, ctx.lang_setting.lang)

    def _add_en_lang(self, ctx: PageContext) -> None:
        logger.info("add_en_lang\n")
        ctx.text = self.lang_en_fixer.add_lang_en_to_refs(ctx.text)

    def _apply_language_fixes(self, ctx: PageContext) -> None:
        fixed = self.language_pipeline.apply_language_fixes(
            ctx.text,
            ctx.title,
            ctx.lang_setting.lang,
            ctx.source_title,
            ctx.mdwiki_revid,
        )
        if fixed:
            ctx.text = fixed
            # Re-expand infobox if language fixes made changes
            self._expand_infobox_if_needed(ctx)

    def _add_mdwiki_category(self, ctx: PageContext) -> None:
        if ctx.lang_setting.add_category:
            ctx.text = self.mdwiki_category_service.add_translated_from_mdwiki(ctx.text, ctx.lang_setting.lang)

    # ---------------- Public API ----------------
    def run(
        self,
        text: str,
        title: str,
        lang_setting: LangSetting | dict[str, Any],
        source_title: str = "",
        mdwiki_revid: int | str = 0,
    ) -> str:
        """
        Run all fixes and return the fixed page content.

        Args:
            text: Page content
            title: Page title
            lang_setting: Per-language options (LangSetting). Defaults to LangSetting().
            source_title: Source page title
            mdwiki_revid: MDWiki revision ID
        """
        ctx = PageContext(
            text=text,
            title=title,
            lang_setting=LangSetting.from_any(lang_setting),
            source_title=source_title,
            mdwiki_revid=int(mdwiki_revid),
        )
        logger.info("start fix one page with mdwiki_revid:%s", ctx.mdwiki_revid)

        if self.redirect_detector.is_redirect(ctx.title, ctx.text):
            return ctx.text

        self._expand_infobox_if_needed(ctx)
        self._apply_basic_fixes(ctx)

        if ctx.lang_setting.move_dots:
            self._move_dots(ctx)

        if ctx.lang_setting.add_en_lang:
            self._add_en_lang(ctx)

        self._apply_language_fixes(ctx)
        self._add_mdwiki_category(ctx)
        ctx.text = self.mini_fixes.mini_fixes_after_fixing(ctx.text, ctx.lang_setting.lang)

        if not ctx.text.strip():
            return ctx.text_org

        return ctx.text


__all__ = [
    "PageUpdater",
]
