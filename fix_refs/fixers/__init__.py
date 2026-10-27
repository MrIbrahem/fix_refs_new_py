"""Core bot functions"""

from __future__ import annotations

from .add_lang_en_bot import LanguageEnFixer, add_lang_en_new, add_lang_en_to_refs
from .fix_images import ImageFixer, remove_missing_images
from .mini_fixes import MiniFixes
from .months import MonthTranslator, fix_months_in_refs
from .move_dots import DotsMover, move_dots_after_refs
from .redirect import RedirectDetector, is_redirect
from .refs import (
    DuplicateRefRemover,
    RefExpander,
    ReferenceExpander,
    RefsMover,
    fix_missing_refs,
    refs_expand,
    refs_expand_work,
    remove_duplicate_refs_with_attrs,
)
from .refs_utils import RefUtils

__all__ = [
    "LanguageEnFixer",
    "ImageFixer",
    "MiniFixes",
    "MonthTranslator",
    "DotsMover",
    "RedirectDetector",
    "DuplicateRefRemover",
    "RefExpander",
    "ReferenceExpander",
    "RefsMover",
    "RefUtils",
    "add_lang_en_new",
    "add_lang_en_to_refs",
    "remove_missing_images",
    "fix_months_in_refs",
    "move_dots_after_refs",
    "is_redirect",
    "fix_missing_refs",
    "refs_expand",
    "refs_expand_work",
    "remove_duplicate_refs_with_attrs",
]
