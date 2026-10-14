"""Core bot functions"""

from __future__ import annotations

from .expend_refs import refs_expand, refs_expand_work
from .fix_missing_refs import fix_missing_refs
from .remove_duplicate_refs import remove_duplicate_refs_with_attrs

__all__ = [
    "refs_expand",
    "refs_expand_work",
    "fix_missing_refs",
    "remove_duplicate_refs_with_attrs",
]
