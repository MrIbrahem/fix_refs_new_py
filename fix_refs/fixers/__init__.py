"""Core bot functions"""

from __future__ import annotations

from .add_lang_en_bot import add_lang_en_to_refs
from .mini_fixes import MiniFixes
from .move_dots import move_dots_after_refs
from .redirect import is_redirect
from .refs import (
    ReferenceExpander,
    refs_expand,
    refs_expand_work,
    remove_duplicate_refs_with_attrs,
)

__all__ = [
    "refs_expand",
    "MiniFixes",
    "refs_expand_work",
    "ReferenceExpander",
    "remove_duplicate_refs_with_attrs",
    "add_lang_en_to_refs",
    "is_redirect",
    "move_dots_after_refs",
]
