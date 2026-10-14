"""
Main PageFixer class and fix_one_page interface
"""

from __future__ import annotations

from dataclasses import dataclass
import logging

from ..bots import (
    add_lang_en_to_refs,
    fix_missing_refs,
    is_redirect,
    mini_fixes,
    mini_fixes_after_fixing,
    move_dots_after_refs,
    remove_duplicate_refs_with_attrs,
)
from ..infobox import expand_infobox_in_text
from ..lang_bots import apply_language_fixes
from ..mdwiki import add_translated_from_mdwiki

logger = logging.getLogger(__name__)

class PageFixer:
    """Fix Wikipedia page references and formatting.

    Args:
        text: Page content
        title: Page title
        lang: Language code
        move_dots: Whether to move dots after references
        expend_infobox: Whether to expand infobox
        add_en_lang: Whether to add English language parameter to refs
        add_category: Whether to add category for MDWiki translations
        source_title: Source page title
        mdwiki_revid: MDWiki revision ID
    """

    def __init__(
        self,
        *,
        text: str,
        title: str,
        lang: str,
        source_title: str = "",
        mdwiki_revid: int | str = 0,
        move_dots: bool = True,
        expend_infobox: bool = True,
        add_en_lang: bool = False,
        add_category: bool = False,
    ) -> None:
        self.text_org = text
        self.text = text
        self.title = title
        self.lang = lang
        self.move_dots = move_dots
        self.expend_infobox = expend_infobox
        self.add_en_lang = add_en_lang
        self.add_category = add_category
        self.source_title = source_title
        self.mdwiki_revid = int(mdwiki_revid)

    # ------------------------------------------------------------------
    # Steps
    # ------------------------------------------------------------------
    def _expand_infobox_if_needed(self) -> None:
        if self.expend_infobox or self.lang == "es":
            self.text = expand_infobox_in_text(self.text, self.title, "")

    def _apply_basic_fixes(self) -> None:
        self.text = mini_fixes(self.text, self.lang)
        self.text = fix_missing_refs(self.text, self.source_title, self.mdwiki_revid)
        self.text = remove_duplicate_refs_with_attrs(self.text)

    def _move_dots(self) -> None:
        logger.info("move_dots\n")
        self.text = move_dots_after_refs(self.text, self.lang)

    def _add_en_lang(self) -> None:
        logger.info("add_en_lang\n")
        self.text = add_lang_en_to_refs(self.text)

    def _apply_language_fixes(self) -> None:
        fixed = apply_language_fixes(
            self.text, self.title, self.lang, self.source_title, self.mdwiki_revid
        )
        if fixed:
            self.text = fixed
            # Re-expand infobox if language fixes made changes
            self._expand_infobox_if_needed()

    def _add_mdwiki_category(self) -> None:
        if self.add_category:
            self.text = add_translated_from_mdwiki(self.text, self.lang)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def run(self) -> str:
        """Run all fixes and return the fixed page content."""
        logger.info("start fix_one_page with mdwiki_revid:%s", self.mdwiki_revid)

        if is_redirect(self.title, self.text):
            return self.text

        self._expand_infobox_if_needed()
        self._apply_basic_fixes()

        if self.move_dots:
            self._move_dots()

        if self.add_en_lang:
            self._add_en_lang()

        self._apply_language_fixes()
        self._add_mdwiki_category()
        self.text = mini_fixes_after_fixing(self.text, self.lang)

        if not self.text.strip():
            return self.text_org

        return self.text


def fix_one_page(
    *,
    text: str,
    title: str,
    lang: str,
    move_dots: bool = True,
    expend_infobox: bool = True,
    add_en_lang: bool = False,
    add_category: bool = False,
    source_title: str = "",
    mdwiki_revid: int | str = 0,
) -> str:
    """Backward-compatible wrapper around PageFixer."""
    return PageFixer(
        text=text,
        title=title,
        lang=lang,
        move_dots=move_dots,
        expend_infobox=expend_infobox,
        add_en_lang=add_en_lang,
        add_category=add_category,
        source_title=source_title,
        mdwiki_revid=mdwiki_revid,
    ).run()


__all__ = [
    "PageFixer",
    "fix_one_page",
]
