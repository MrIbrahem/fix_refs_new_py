"""
Month and date handling for different languages
"""

from __future__ import annotations

import logging
from abc import abstractmethod
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class LangMonth:
    data: dict[str, str] = field(default_factory=dict)

    @abstractmethod
    def format_date(self, day, year, month: str) -> str:
        pass

    @property
    def join_data_keys(self) -> str:
        # data_keys = "January|February|March|April|May|June|July|August|September|October|November|December"
        return "|".join(list(self.data.keys()))

    def translate_month(self, month: str) -> str:
        months_lower = {k.lower(): v for k, v in self.data.items()}
        return months_lower.get(month.lower(), "")

    def translate(self, day: str, year: str, month: str) -> None | str:
        translated_month = self.translate_month(month)
        if translated_month:
            return self.format_date(day, year, translated_month).strip()
        return None


@dataclass
class PortugueseMonth(LangMonth):
    data: dict[str, str] = field(
        default_factory=lambda: {
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
        }
    )

    def format_date(self, day, year, translated_month: str) -> str:
        if day:
            return f"{day} de {translated_month} {year}"

        return f"{translated_month} {year}"


@dataclass
class SpanishMonth(LangMonth):
    data: dict[str, str] = field(
        default_factory=lambda: {
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
        }
    )

    def format_date(self, day: str, year: str, translated_month: str) -> str:
        if day:
            return f"{day} de {translated_month} de {year}"

        return f"{translated_month} de {year}"


@dataclass
class MonthsTranslations:
    langs: dict[str, type[LangMonth]] = field(
        default_factory=lambda: {
            "pt": PortugueseMonth,
            "es": SpanishMonth,
        }
    )

    def load_lang(self, lang) -> None | LangMonth:
        if lang not in self.langs:
            return None

        return self.langs[lang]()


__all__ = [
    "LangMonth",
    "PortugueseMonth",
    "SpanishMonth",
    "MonthsTranslations",
]
