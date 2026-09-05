"""
Remove spaces between words and reference tags
"""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)


def match_it(text: str, charters: str):
    # Build regex equivalent to PHP:
    # /(<\/ref>|\/>)\s*([charters]\s*)$/u
    escaped = re.escape(charters)
    pattern = rf"(</ref>|/>)\s*([{escaped}]\s*)$"
    m = re.search(pattern, text, flags=re.UNICODE)
    if m:
        return m.group(2)
    return None


def get_parts(newtext: str, charters: str):
    # Split by double newlines
    matches = newtext.split("\n\n")
    if len(matches) == 1:
        matches = newtext.split("\r\n\r\n")

    logger.debug(f"count(matches)={len(matches)}")

    new_parts = []
    for p in matches:
        chart = match_it(p, charters)
        if chart:
            new_parts.append([p, chart])

    logger.debug(f"count(new_parts)={len(new_parts)}")
    return new_parts


def remove_spaces_between_last_word_and_beginning_of_ref(newtext: str, lang: str) -> str:
    # Define punctuation marks based on language
    dots = r".,。।"
    if lang == "hy":
        dots = r".,。։।:"

    newtext = re.sub(r">\s*<ref", r"><ref", newtext)

    parts = get_parts(newtext, dots)

    for part, charter in parts:
        logger.debug(f"charter={charter}")

        # Regex equivalent to:
        # /((?:\s*<ref[\s\S]+?(?:<\/ref|\/)>)+)/us
        regline = r"((?:\s*<ref[\s\S]+?(?:</ref|/)>)+)"
        last_ref_matches = re.findall(regline, part, flags=re.UNICODE | re.DOTALL)

        logger.debug(f"count(last_ref)={len(last_ref_matches)}")

        if last_ref_matches:
            ref_text = last_ref_matches[-1]
            end_part = ref_text + charter

            if part.endswith(end_part):
                logger.debug("endswith")

                first_part_clean_end = part[: -len(end_part)]
                first_part_clean_end = first_part_clean_end.rstrip()

                new_part = first_part_clean_end + ref_text.strip() + charter

                newtext = newtext.replace(part, new_part)

    return newtext


__all__ = [
    "remove_spaces_between_last_word_and_beginning_of_ref",
]
