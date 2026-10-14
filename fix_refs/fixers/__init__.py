"""Core bot functions"""

from __future__ import annotations

from .add_lang_en_bot import add_lang_en_to_refs
from .mini_fixes import mini_fixes, mini_fixes_after_fixing
from .move_dots import move_dots_after_refs
from .redirect import is_redirect
from .refs import (
    fix_missing_refs,
    refs_expand,
    refs_expand_work,
    remove_duplicate_refs_with_attrs,
)

__all__ = [
    "refs_expand",
    "refs_expand_work",
    "fix_missing_refs",
    "remove_duplicate_refs_with_attrs",
    "add_lang_en_to_refs",
    "is_redirect",
    "mini_fixes",
    "mini_fixes_after_fixing",
    "move_dots_after_refs",
]
