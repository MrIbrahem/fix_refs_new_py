"""
Main PageUpdater class
"""

from __future__ import annotations

import logging
from typing import Any

from ..fixers import (
    RefsMover,
    DotsMover,
    DuplicateRefRemover,
    LanguageEnFixer,
    MiniFixes,
    RedirectDetector,
    RefExpander,
)
from ..infobox import InfoboxExpander
from ..lang_bots import LanguageFixerPipeline
from .mapping import LangSetting, PageContext

logger = logging.getLogger(__name__)


class PageUpdater:
    """Stateless page fixer. Create once, call run() for each page."""

    def __init__(
        self,
        move_refs_out_infobox: bool | None = None,
    ) -> None:

        # Injected collaborators
        self.mini_fixer = MiniFixes()
        self.ref_expander = RefExpander()
        self.duplicate_ref_remover = DuplicateRefRemover()
        self.dots_mover = DotsMover()
        self.lang_en_fixer = LanguageEnFixer()
        self.language_pipeline = LanguageFixerPipeline()
        self.infobox_expander = InfoboxExpander()
        self.redirect_detector = RedirectDetector()
        self.move_refs_out_infobox = move_refs_out_infobox if move_refs_out_infobox is not None else True

    # ---------------- Steps (each one updates ctx.text) ----------------
    def _expand_infobox_if_needed(self, ctx: PageContext) -> None:
        if ctx.lang_setting.expend_infobox or ctx.lang_setting.lang == "es":
            ctx.text = self.infobox_expander.expand_infobox_in_text(ctx.text, ctx.title)

    def _apply_refs_fixes(self, ctx: PageContext) -> None:
        if ctx.source_original_text:
            ctx.text = self.ref_expander.run(
                ctx.text,
                source_text=ctx.source_original_text,
            )

        ctx.text = self.duplicate_ref_remover.wtp_remove(ctx.text)
        if self.move_refs_out_infobox:
            ctx.text = RefsMover(ctx.text, True).run()

        if ctx.lang_setting.move_dots:
            ctx.text = self.dots_mover.move_dots_after_refs(ctx.text, ctx.lang_setting.lang)

        if ctx.lang_setting.add_en_lang:
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

    # ---------------- Public API ----------------
    def run(
        self,
        text: str,
        title: str,
        lang_setting: LangSetting | dict[str, Any],
        source_title: str = "",
        mdwiki_revid: int | str = 0,
        source_original_text: str = "",
    ) -> str:
        """
        Run all fixes and return the fixed page content.

        Args:
            text: Page content
            title: Page title
            lang_setting: Per-language options (LangSetting). Defaults to LangSetting().
            source_title: Source page title
            mdwiki_revid: MDWiki revision ID
            source_original_text: Original source page content from mdwiki.org
        """
        ctx = PageContext(
            text=text,
            title=title,
            lang_setting=LangSetting.from_any(lang_setting),
            source_title=source_title,
            mdwiki_revid=int(mdwiki_revid),
            source_original_text=source_original_text,
        )
        logger.info("start fix one page with mdwiki_revid:%s", ctx.mdwiki_revid)

        if self.redirect_detector.is_redirect(ctx.text):
            return ctx.text

        self._expand_infobox_if_needed(ctx)

        ctx.text = self.mini_fixer.fix(
            ctx.text,
            ctx.lang_setting.lang,
        )

        self._apply_refs_fixes(ctx)

        self._apply_language_fixes(ctx)

        ctx.text = self.mini_fixer.mini_fixes_after_fixing(
            ctx.text,
            ctx.lang_setting.lang,
        )

        if not ctx.text.strip():
            return ctx.text_org

        return ctx.text


__all__ = [
    "PageUpdater",
]
