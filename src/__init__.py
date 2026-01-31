"""
fix_one_page - WikiText reference/category/template fixer

A Python library to parse and fix references in MediaWiki wikitext.
"""

__version__ = "1.0.0"

from .core.fix_page import fix_one_page
from .core import DoChangesToText1
__all__ = ["fix_one_page", "DoChangesToText1"]
