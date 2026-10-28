"""Parsers for WikiText elements"""

from __future__ import annotations

from .wtp_refs import WtpRefs, WtpRef
from .wtp_temps import WtpTemplates
from .wtp_refs_temps import WtpRefsTemps

__all__ = [
    "WtpRefsTemps",
    "WtpRef",
    "WtpTemplates",
    "WtpRefs",
]
