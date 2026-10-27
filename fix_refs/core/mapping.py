""" """

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class LangSetting:
    """Per-language fixing options."""

    lang: str
    move_dots: bool = True
    expend_infobox: bool = True
    add_en_lang: bool = False
    add_category: bool = False

    def to_json(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_any(cls, setting: LangSetting | dict[str, Any]) -> LangSetting:
        """Create LangSetting from any input."""
        if isinstance(setting, LangSetting):
            return setting

        return cls(**setting)


__all__ = [
    "LangSetting",
]
