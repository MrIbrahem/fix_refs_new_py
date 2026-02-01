"""
Bulgarian-specific bot fixes
"""

import re


def bg_section(text: str, sourcetitle: str, mdwiki_revid: int) -> str:
    """Add Bulgarian translation template to text

    Template: {{Превод от|mdwiki|{sourcetitle}|{mdwiki_revid}}}

    Args:
        text: WikiText content
        sourcetitle: Source page title
        mdwiki_revid: MDWiki revision ID

    Returns:
        Text with translation template added
    """
    # Check if translation template already exists
    pattern = r'\{\{\s*Превод\s*от\s*\|'
    if re.search(pattern, text, re.IGNORECASE):
        return text

    # Create translation template
    temp = f"{{{{Превод от|mdwiki|{sourcetitle}|{mdwiki_revid}}}}}\n"

    # Insert before first [[Категория: or [[Category: if found, otherwise append
    category_pattern = r'\[\[(Категория|Category):'
    match = re.search(category_pattern, text, re.IGNORECASE)

    if match:
        pos = match.start()
        text = text[:pos] + temp + text[pos:]
    else:
        if text:
            text += "\n\n" + temp
        else:
            text = "\n" + temp

    return text


def bg_fixes(text: str, source_title: str, mdwiki_revid: int) -> str:
    """Apply Bulgarian-specific fixes to text

    Args:
        text: WikiText content
        source_title: Source page title
        mdwiki_revid: MDWiki revision ID

    Returns:
        Fixed text
    """
    # Add translation template
    text = bg_section(text, source_title, mdwiki_revid)

    # Remove [[Category:Translated from MDWiki]] (Bulgarian pages don't need it)
    text = re.sub(
        r'\[\[\s*(Категория|Category)\s*:\s*Translated from MDWiki\s*\]\]',
        '',
        text,
        flags=re.IGNORECASE
    )

    return text
