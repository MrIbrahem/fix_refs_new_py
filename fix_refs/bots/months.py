"""
Month and date handling for different languages
"""

import re
from typing import Dict, Optional


def new_date(val: str, lang: str = 'pt') -> str:
    """Convert English month names to target language

    Args:
        val: Date string with English month
        lang: Target language code ('pt', 'es')

    Returns:
        Date string with translated month name
    """
    months_translations: Dict[str, Dict[str, str]] = {
        'pt': {
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
        'es': {
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
            day = match.group('d')
            month = match.group('m').lower()
            year = match.group('y')
            translated_month = months_lower.get(month, "")

            if translated_month:
                if lang == 'es':
                    return f"{day} de {translated_month} de {year}".strip() if day else f"{translated_month} de {year}"
                else:
                    return f"{day} de {translated_month} {year}".strip() if day else f"{translated_month} {year}"

    return val.strip()


def make_date_new_val_pt(val: str) -> str:
    """Convert date to Portuguese format

    Args:
        val: Date string with English month

    Returns:
        Date string with Portuguese month
    """
    return new_date(val, 'pt')


def make_date_new_val_es(val: str) -> str:
    """Convert date to Spanish format

    Args:
        val: Date string with English month

    Returns:
        Date string with Spanish month
    """
    return new_date(val, 'es')
