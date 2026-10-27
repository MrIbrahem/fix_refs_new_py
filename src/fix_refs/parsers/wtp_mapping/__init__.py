"""Parsers for WikiText elements"""

from __future__ import annotations

from .wtp_refs import WtpRefs
from .wtp_temps import WtpTemplates

__all__ = [
    "WtpTemplates",
    "WtpRefs",
]
