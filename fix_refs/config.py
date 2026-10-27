from __future__ import annotations

import logging
import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


@dataclass
class ConfigManager:
    """Manages application paths, environment variables, and configurations."""

    resources_path: Path = field(
        default_factory=lambda: Path(
            os.getenv("RESOURCES_PATH", Path(__file__).parent.parent / "resources")
        ).expanduser()
    )
    revisions_path: Path = field(default_factory=lambda: Path())

    def __post_init__(self) -> None:
        self._load_environment()

        # If revisions_path was not explicitly provided or is default, initialize it relative to resources_path
        if not self.revisions_path or self.revisions_path == Path("."):
            env_value = os.getenv("REVISIONS_PATH") or os.getenv("REVISIONS_DIR") or None
            self.revisions_path = Path(env_value or self.resources_path / "revisions").expanduser()

    def _load_environment(self) -> None:
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

__all__ = [
    "ConfigManager",
]
