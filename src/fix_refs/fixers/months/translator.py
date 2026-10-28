"""
Month and date handling for different languages
"""

from __future__ import annotations

import logging
import re

import wikitextparser as wtp

from .mapping import MonthsTranslations

logger = logging.getLogger(__name__)


class MonthTranslator:
    """Translator and fixer for dates and English month names in templates and citations."""

    def __init__(self) -> None:
        self.months_translations = MonthsTranslations()

    def _create_patterns(self, data_keys: str) -> list[str]:

        month_part = rf"(?P<m>{data_keys})"

        patterns = [
            rf"^(?:(?P<d>\d{{1,2}})\s+)?{month_part},?\s+(?P<y>\d{{4}})$",
            rf"^{month_part}\s+(?P<d>\d{{1,2}}),?\s+(?P<y>\d{{4}})$",
        ]

        return patterns

    def _start_end(self, cite_temp: str) -> bool:
        """Check if string starts with {{ and ends with }}"""
        return cite_temp.startswith("{{") and cite_temp.endswith("}}")

    def new_date(self, val: str, lang: str = "pt") -> str:
        """Convert English month names to target language

        Args:
            val: Date string with English month
            lang: Target language code ('pt', 'es')

        Returns:
            Date string with translated month name
        """
        lang_item = self.months_translations.load_lang(lang)

        if not lang_item:
            return val

        patterns = self._create_patterns(lang_item.join_data_keys)

        for pattern in patterns:
            match = re.match(pattern, val.strip(), re.IGNORECASE)
            if match:
                result = lang_item.translate(
                    day=match.group("d"),
                    year=match.group("y"),
                    month=match.group("m"),
                )
                if result:
                    return result

        return val.strip()

    def fix_months_in_texts(self, temp_text: str, lang: str) -> str:
        """Translate English months to lang within template parameters

        Args:
            temp_text: Template text (can contain multiple templates)
            lang: Language code

        Returns:
            Template text with translated months
        """
        parsed = wtp.parse(temp_text)

        for temp in parsed.templates:
            arguments = temp.arguments
            for arg in arguments:
                old_val = arg.value
                new_val = self.new_date(old_val, lang)
                if new_val and new_val.strip() != old_val.strip():
                    temp.set_arg(arg.name, new_val)

        return parsed.string

    def fix_months_in_refs(self, text: str, lang: str) -> str:
        """Translate English months to Spanish/Portuguese within citations

        Args:
            text: Text containing citations
            lang: Language code

        Returns:
            Text with translated months in citations
        """
        parsed = wtp.parse(text)

        # Get all ref tags
        ref_tags = parsed.get_tags("ref")

        for ref in ref_tags:
            contents = ref.contents or ""

            # Only process if it looks like a template
            if not self._start_end(contents.strip()):
                continue

            new_contents = self.fix_months_in_texts(contents, lang)
            if new_contents:
                ref.contents = new_contents

        return parsed.string


__all__ = [
    "MonthTranslator",
]
