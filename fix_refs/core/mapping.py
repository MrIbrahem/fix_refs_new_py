""" """

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass, field
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


@dataclass
class PageContext:
    """Per-page data and the working text shared by all steps."""

    text: str
    title: str
    lang_setting: LangSetting
    source_title: str = ""
    mdwiki_revid: int = 0
    text_org: str = field(init=False)

    def __post_init__(self) -> None:
        # Keep the untouched original so we can fall back to it
        self.text_org = self.text


__all__ = [
    "LangSetting",
    "PageContext",
]
