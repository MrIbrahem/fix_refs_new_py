"""
PageFixer.run - WikiText reference/category/template fixer

A Python library to parse and fix references in MediaWiki wikitext.
"""

from __future__ import annotations

__version__ = "0.1.0"

from .core import (
    LangSetting,
    PageFixer,
)

__all__ = [
    "LangSetting",
    "PageFixer",
]
