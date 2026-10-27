"""
Infobox expansion functions
"""

from __future__ import annotations

import logging
import re

import wikitextparser as wtp

logger = logging.getLogger(__name__)

COMMENT_PATTERN = re.compile(
    r"\s*\n*\s*(<!-- (Monoclonal antibody data|External links|Names*|Clinical data|Legal data|Legal status|Pharmacokinetic data|Chemical and physical data|Definition and medical uses|Chemical data|\w+ \w+ data|\w+ \w+ \w+ data|\w+ data|\w+ status|Identifiers) -->)\s*\n*",
    re.IGNORECASE,
)


class InfoboxExpander:
    """Expander for WikiText infobox templates and parameters."""

    def do_comments(self, text: str) -> str:
        """Format comments in text."""

        def repl(match: re.Match[str]) -> str:
            return f"\n\n{match.group(1).strip()}\n"

        return COMMENT_PATTERN.sub(repl, text)

    def expend_new(self, main_temp: str) -> str:
        """Expand single template formatting."""
        parsed = wtp.parse(main_temp)
        new_temp = main_temp
        for template in parsed.templates:
            if not template:
                continue
            str_ = template.string
            if str_.strip() != main_temp.strip():
                continue
            template_name = str(template.normal_name()).strip()
            template.name = f"{template_name}\n"
            for arg in template.arguments:
                param = arg.name.rstrip()
                value = arg.value.rstrip()
                newparam = param.ljust(17)
                arg.name = newparam
                arg.value = f"{value}\n"
            new_temp = template.string
            break
        new_temp = self.do_comments(new_temp)
        return new_temp

    def extract_templates_and_params(self, text: str) -> list[dict]:
        """Extract templates and their parameter dictionary from text."""
        result = []
        parsed = wtp.parse(text)
        templates = parsed.templates
        for template in templates:
            if not template:
                continue
            pa_item = template.string
            if not pa_item or pa_item.strip() == "":
                continue
            params = {}
            for param in template.arguments:
                value = str(param.value)
                key = str(param.name)
                key = key.strip()
                params[key] = value
            ficrt = {
                "params": params,
                "item": pa_item,
            }
            result.append(ficrt)
        return result

    def make_section_0(self, title: str, newtext: str) -> str:
        """Extract lead section text (section 0)."""
        if newtext.find("==") != -1:
            section_0 = newtext.split("==")[0]
        else:
            tagg = f"'''{title}'''"
            if newtext.find(tagg) != -1:
                section_0 = newtext.split(tagg)[0]
            else:
                section_0 = newtext
        return section_0

    def expand_infobox_in_text(self, text: str, title: str, section_0: str) -> str:
        """Expand the infobox in the provided text.

        Args:
            text (str): The input text containing the infobox to be expanded.
            title (str): The title of the infobox to be processed.
            section_0 (str): An optional section of text that may contain relevant information.

        Returns:
            str: The modified text with the expanded infobox.
        """
        newtext = text
        if not section_0:
            section_0 = self.make_section_0(title, newtext)
        try:
            title2 = re.escape(title)
        except Exception:
            title2 = title
        newtext = re.sub(r"\}\s*(\'\'\'%s\'\'\')" % title2, r"}\n\n\g<1>", newtext)
        section_0 = re.sub(r"\}\s*(\'\'\'%s\'\'\')" % title2, r"}\n\n\g<1>", section_0)
        tempse_by_u = {}
        tempse = {}
        ingr = self.extract_templates_and_params(section_0)
        u = 0
        for temp in ingr:
            u += 1
            params, template = temp["params"], temp["item"]
            if len(params) > 4 and section_0.find(f">{template}") == -1:
                tempse_by_u[u] = temp
                tempse[u] = len(template)
        main_temp = {}
        if len(tempse_by_u) == 1:
            for _x, v in tempse_by_u.items():
                main_temp = v
        else:
            PP = [[y1, u1] for u1, y1 in tempse.items()]
            PP.sort(reverse=True)
            for _y2, u2 in PP:
                main_temp = tempse_by_u[u2]
                break
        if main_temp != {}:
            main_temp_text = main_temp.get("item", "")
            params = main_temp.get("params", [])
            new_temp = self.expend_new(main_temp_text)
            if new_temp != main_temp_text:
                newtext = newtext.replace(main_temp_text, new_temp)
                newtext = newtext.replace(f"{new_temp}'''", f"{new_temp}\n'''")
        return newtext


__all__ = [
    "InfoboxExpander",
]
