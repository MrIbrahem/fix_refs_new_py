"""
fix_refs - WikiText reference/category/template fixer

A Python library to parse and fix references in MediaWiki wikitext.
"""

__version__ = "1.0.0"

from .core.fix_page import fix_refs

__all__ = ["fix_refs"]
