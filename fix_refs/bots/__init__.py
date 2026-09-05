"""Core bot functions"""

from __future__ import annotations

import logging

from .add_lang_en_bot import add_lang_en_to_refs
from .fix_missing_refs import fix_missing_refs
from .mini_fixes import mini_fixes, mini_fixes_after_fixing
from .move_dots import move_dots_after_refs
from .redirect import is_redirect
from .remove_duplicate_refs import remove_duplicate_refs_with_attrs

__all__ = [
    "add_lang_en_to_refs",
    "fix_missing_refs",
    "is_redirect",
    "mini_fixes",
    "mini_fixes_after_fixing",
    "move_dots_after_refs",
    "remove_duplicate_refs_with_attrs",
]
