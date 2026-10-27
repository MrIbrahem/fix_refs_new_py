"""Core bot functions"""

from __future__ import annotations

from .expend_refs import refs_expand, refs_expand_work
from .fix_missing_refs import ReferenceExpander
from .remove_duplicate_refs import remove_duplicate_refs_with_attrs

__all__ = [
    "refs_expand",
    "refs_expand_work",
    "ReferenceExpander",
    "remove_duplicate_refs_with_attrs",
]
