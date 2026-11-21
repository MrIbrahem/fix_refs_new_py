"""
PageFixer.run - WikiText reference/category/template fixer

A Python library to parse and fix references in MediaWiki wikitext.
"""

from __future__ import annotations

from .core import (
    LangSetting,
    PageFixer,
)

# __version__ = "0.1.0"


__all__ = [
    "LangSetting",
    "PageFixer",
]
