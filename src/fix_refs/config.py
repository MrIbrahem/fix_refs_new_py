from __future__ import annotations

import json
import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


@dataclass
class ConfigManager:
    """Manages application paths, environment variables, and configurations."""

    resources_path: Path
    revisions_path: Path

    @staticmethod
    def _load_environment() -> None:
        """Load environment variables from .env file, with fallback to home directory."""
        try:
            load_dotenv()
        except Exception:
            home_dir = os.getenv("HOME")
            if home_dir:
                load_dotenv(Path(f"{home_dir}/.env"))

    def get_revision_file_path(self, mdwiki_revid: str | int) -> Path:
        file = self.revisions_path / f"{str(mdwiki_revid)}/wikitext.txt"
        return file

    def load_resources_path_json(self, file_name: str) -> dict[str, Any]:
        """Load MDWiki categories from local JSON file.

        Returns:
            Dictionary of MDWiki categories or empty dict if file not found.
        """
        local_file = self.resources_path / file_name

        if not local_file.exists():
            return {}

        try:
            with open(local_file, "r", encoding="utf-8") as f:
                result: dict[str, Any] = json.load(f)  # type: ignore
                return result
        except (OSError, json.JSONDecodeError):
            return {}

    @classmethod
    def load(cls) -> ConfigManager:
        """Create a ConfigManager instance from environment variables."""
        cls._load_environment()

        env_value = os.getenv("REVISIONS_PATH") or os.getenv("REVISIONS_DIR") or None

        resources_path = Path(os.getenv("RESOURCES_PATH", Path(__file__).parent.parent / "resources")).expanduser()
        revisions_path = Path(env_value or resources_path / "revisions").expanduser()

        return cls(
            resources_path=resources_path,
            revisions_path=revisions_path,
        )


__all__ = [
    "ConfigManager",
]
