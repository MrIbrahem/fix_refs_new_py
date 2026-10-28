"""Parsers for WikiText elements"""

from __future__ import annotations

from .category import CategoryParser
from .wtp_mapping import WtpRef, WtpRefs, WtpRefsTemps, WtpTemplates

__all__ = [
    "WtpRefsTemps",
    "WtpRef",
    "WtpTemplates",
    "WtpRefs",
    "CategoryParser",
]
