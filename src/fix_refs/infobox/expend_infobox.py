"""
Infobox expansion functions
"""

from __future__ import annotations

import logging
import re

import wikitextparser as wtp

logger = logging.getLogger(__name__)

# Minimum number of unique params for a template to count as an infobox
MIN_INFOBOX_PARAMS = 4

# Width used to align parameter names
PARAM_NAME_WIDTH = 17

# Section-header comments that must be placed on their own lines
_COMMENT_TITLES = (
    r"Monoclonal antibody data",
    r"External links",
    r"Names*",
    r"Clinical data",
    r"Legal data",
    r"Legal status",
    r"Pharmacokinetic data",
    r"Chemical and physical data",
    r"Definition and medical uses",
    r"Chemical data",
    r"\w+ \w+ data",
    r"\w+ \w+ \w+ data",
    r"\w+ data",
    r"\w+ status",
    r"Identifiers",
)

COMMENT_PATTERN = re.compile(
    r"\s*\n*\s*(<!-- (?:" + "|".join(_COMMENT_TITLES) + r") -->)\s*\n*",
    re.IGNORECASE,
)


class InfoboxExpander:
    """Expander for WikiText infobox templates and parameters."""

    # ------------------------------------------------------------------
    # Formatting helpers
    # ------------------------------------------------------------------
    @staticmethod
    def do_comments(text: str) -> str:
        """Put each known section comment on its own line, surrounded by spacing."""
        return COMMENT_PATTERN.sub(lambda m: f"\n\n{m.group(1).strip()}\n", text)

    @staticmethod
    def _separate_title(text: str, title: str) -> str:
        """Ensure the bold title starts on a new paragraph after a closing brace."""
        title_pattern = re.compile(r"\}\s*('''%s''')" % re.escape(title))
        return title_pattern.sub(r"}\n\n\1", text)

    # ------------------------------------------------------------------
    # Template handling
    # ------------------------------------------------------------------
    def extract_main_template(self, section_0: str) -> dict:
        """Return the longest template in section_0 that has more than 4 params.

        The result is ``{"params": {...}, "item": "<template text>"}``,
        or an empty dict when no template qualifies.
        """
        best: dict = {}
        best_key: tuple[int, int] = (-1, -1)
        order = 0

        for template in wtp.parse(section_0).templates:
            template_str = template.string
            if not template_str.strip():
                continue

            order += 1

            # Templates inside a tag (e.g. <ref>) are not the main infobox
            if f">{template_str}" in section_0:
                continue

            # Later duplicates override earlier ones
            params = {str(p.name).strip(): str(p.value) for p in template.arguments}
            if len(params) <= MIN_INFOBOX_PARAMS:
                continue

            # Longest wins; on ties the later template wins
            key = (len(template_str), order)
            if key > best_key:
                best_key = key
                best = {"params": params, "item": template_str}

        return best

    # ------------------------------------------------------------------
    # Section handling
    # ------------------------------------------------------------------
    @staticmethod
    def extract_lead_section(newtext: str) -> str:
        """Extract the lead section (section 0) using wikitextparser."""
        sections = wtp.parse(newtext).get_sections(include_subsections=False)
        return sections[0].string if sections else newtext

    # ------------------------------------------------------------------
    # Public entry points
    # ------------------------------------------------------------------
    def expend_new(self, main_temp: str) -> str:
        """Expand a single template so each parameter is on its own line."""
        wanted = main_temp.strip()
        new_temp = main_temp

        for template in wtp.parse(main_temp).templates:
            # Only the outer template equal to the whole input is expanded
            if template.string.strip() != wanted:
                continue

            template.name = f"{str(template.normal_name()).strip()}\n"
            for arg in template.arguments:
                arg.name = arg.name.rstrip().ljust(PARAM_NAME_WIDTH)
                arg.value = f"{arg.value.rstrip()}\n"

            new_temp = template.string
            break

        return self.do_comments(new_temp)

    def expand_infobox_in_text(self, text: str, title: str) -> str:
        """Expand the main infobox found in the lead section of ``text``.

        Args:
            text: Full article wikitext.
            title: Article title, used to find the bold lead phrase.

        Returns:
            The text with the main infobox expanded, or the text with only the
            title spacing fixed when no infobox is found.
        """

        newtext = self._separate_title(text, title)
        section_0 = self.extract_lead_section(newtext)

        main_temp = self.extract_main_template(section_0)
        if not main_temp:
            return newtext

        old_temp = main_temp["item"]
        new_temp = self.expend_new(old_temp)
        if new_temp == old_temp:
            return newtext

        newtext = newtext.replace(old_temp, new_temp)
        return newtext.replace(f"{new_temp}'''", f"{new_temp}\n'''")


__all__ = [
    "InfoboxExpander",
]
