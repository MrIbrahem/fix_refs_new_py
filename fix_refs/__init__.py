"""
fix_one_page - WikiText reference/category/template fixer

A Python library to parse and fix references in MediaWiki wikitext.
"""

__version__ = "0.1.0"

from .core.fix_page import fix_one_page

__all__ = [
    "fix_one_page",
]
