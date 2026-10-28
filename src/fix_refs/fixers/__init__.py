"""Core bot functions"""

from __future__ import annotations

from .add_lang_en_bot import LanguageEnFixer
from .fix_images import ImageFixer
from .mini_fixes import MiniFixes
from .months import MonthTranslator
from .move_dots import DotsMover
from .redirect import RedirectDetector
from .refs import (
    DuplicateRefRemover,
    ReferenceExpander,
    RefExpander,
    RefsMover,
)

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
]
