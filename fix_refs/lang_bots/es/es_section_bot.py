"""
Spanish section helper
"""

import re
from datetime import datetime


def es_section(source_title: str, text: str, mdwiki_revid: str) -> str:
    """Add Traducido ref template to Spanish text

    Args:
        source_title: Source page title
        text: WikiText content
        mdwiki_revid: MDWiki revision ID

    Returns:
        Text with Traducido ref template added
    """
    # If template already exists (any variant), return as-is
    if re.search(r'\{\{\s*Traducido\s*ref(?:\s*MDWiki)?\s*\|', text, re.IGNORECASE):
        return text

    # Get current date
    date = datetime.now().strftime("%d de %B de %Y")

    # Create translation template
    # Use {{{{ and }}}} for literal {{ and }} in f-strings
    temp = f"{{{{Traducido ref MDWiki|en|{source_title}|oldid={mdwiki_revid}|trad=|fecha={date}}}}}"

    # Insert after "== Enlaces externos ==" if it exists, otherwise append
    if re.search(r'==\s*Enlaces\s*externos\s*==', text, re.IGNORECASE):
        text = re.sub(
            r'(==\s*Enlaces\s*externos\s*==)',
            r'\1\n' + temp + '\n',
            text,
            flags=re.IGNORECASE,
            count=1
        )
    else:
        text += f"\n== Enlaces externos ==\n{temp}\n"

    return text
