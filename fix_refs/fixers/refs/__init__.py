"""Core bot functions"""

from __future__ import annotations

from .expend_refs import RefExpander, refs_expand, refs_expand_work
from .fix_missing_refs import ReferenceExpander, fix_missing_refs
from .refs_mover import RefsMover, move_refs_from_templates
from .remove_duplicate_refs import DuplicateRefRemover, remove_duplicate_refs_with_attrs

__all__ = [
    "RefExpander",
    "ReferenceExpander",
    "RefsMover",
    "DuplicateRefRemover",
    "refs_expand",
    "refs_expand_work",
    "fix_missing_refs",
    "move_refs_from_templates",
    "remove_duplicate_refs_with_attrs",
]
