"""
Redirect detection
"""

from __future__ import annotations

import logging
import re

logger = logging.getLogger(__name__)


class RedirectDetector:
    """Detector for MediaWiki redirect pages."""

    def is_redirect(self, title: str, text: str) -> bool:
        """Check if page is a redirect

        Args:
            title: Page title
            text: Page content

        Returns:
            True if page is a redirect
        """
        return bool(re.match(r"^#(пренасочване|redirect)", text, re.IGNORECASE))


def is_redirect(title: str, text: str) -> bool:
    """Legacy wrapper for RedirectDetector.is_redirect."""
    return RedirectDetector().is_redirect(title, text)


__all__ = [
    "RedirectDetector",
    "is_redirect",
]
