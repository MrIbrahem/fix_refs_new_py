"""
Redirect detection
"""

import re


def page_is_redirect(title: str, text: str) -> bool:
    """Check if page is a redirect

    Args:
        title: Page title
        text: Page content

    Returns:
        True if page is a redirect
    """
    return bool(re.match(r'^#(пренасочване|redirect)', text, re.IGNORECASE))


def is_redirect(title: str, text: str) -> bool:
    """Alias for page_is_redirect

    Args:
        title: Page title
        text: Page content

    Returns:
        True if page is a redirect
    """
    return page_is_redirect(title, text)
