"""
Month and date handling for different languages
"""

from __future__ import annotations

import logging
import re

import wikitextparser as wtp

logger = logging.getLogger(__name__)


def new_date(val: str, lang: str = "pt") -> str:
    """Convert English month names to target language

    Args:
        val: Date string with English month
        lang: Target language code ('pt', 'es')

    Returns:
        Date string with translated month name
    """
    months_translations: dict[str, dict[str, str]] = {
        "pt": {
            "January": "janeiro",
            "February": "fevereiro",
            "March": "março",
            "April": "abril",
            "May": "maio",
            "June": "junho",
            "July": "julho",
            "August": "agosto",
            "September": "setembro",
            "October": "outubro",
            "November": "novembro",
            "December": "dezembro",
        },
        "es": {
            "January": "enero",
            "February": "febrero",
            "March": "marzo",
            "April": "abril",
            "May": "mayo",
            "June": "junio",
            "July": "julio",
            "August": "agosto",
            "September": "septiembre",
            "October": "octubre",
            "November": "noviembre",
            "December": "diciembre",
        },
    }

    if lang not in months_translations:
        return val.strip()

    months_lower = {k.lower(): v for k, v in months_translations[lang].items()}

    month_part = r"(?P<m>January|February|March|April|May|June|July|August|September|October|November|December)"
    patterns = [
        rf"^(?:(?P<d>\d{{1,2}})\s+)?{month_part},?\s+(?P<y>\d{{4}})$",
        rf"^{month_part}\s+(?P<d>\d{{1,2}}),?\s+(?P<y>\d{{4}})$",
    ]

    for pattern in patterns:
        match = re.match(pattern, val.strip(), re.IGNORECASE)
        if match:
            day = match.group("d")
            month = match.group("m").lower()
            year = match.group("y")
            translated_month = months_lower.get(month, "")

            if translated_month:
                if lang == "es":
                    return f"{day} de {translated_month} de {year}".strip() if day else f"{translated_month} de {year}"
                else:
                    return f"{day} de {translated_month} {year}".strip() if day else f"{translated_month} {year}"

    return val.strip()


def fix_months_in_texts(temp_text: str, lang: str) -> str:
    """
    Translate English months to lang within template parameters

    Args:
        temp_text: Template text (can contain multiple templates)

    Returns:
        Template text with translated months
    """
    parsed = wtp.parse(temp_text)

    for temp in parsed.templates:
        arguments = temp.arguments
        for arg in arguments:
            old_val = arg.value
            new_val = new_date(old_val, lang)
            if new_val and new_val.strip() != old_val.strip():
                temp.set_arg(arg.name, new_val)

    return parsed.string


def start_end(cite_temp: str) -> bool:
    """Check if string starts with {{ and ends with }}"""
    return cite_temp.startswith("{{") and cite_temp.endswith("}}")


def fix_months_in_refs(text: str, lang: str) -> str:
    """Translate English months to Spanish within citations

    Args:
        text: Text containing citations

    Returns:
        Text with translated months in citations
    """
    parsed = wtp.parse(text)

    # Get all ref tags
    ref_tags = parsed.get_tags("ref")

    for ref in ref_tags:
        contents = ref.contents or ""
        # Only process if it looks like a template
        if not start_end(contents):
            continue
        ref.contents = fix_months_in_texts(contents, lang)
    return parsed.string


__all__ = [
    "fix_months_in_texts",
    "fix_months_in_refs",
]
