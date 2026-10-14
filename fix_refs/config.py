from __future__ import annotations

import logging
import os
from pathlib import Path

from dataclasses import dataclass, field
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

@dataclass
class ConfigManager:
    """Manages application paths, environment variables, and configurations."""

    resources_path: Path = field(default_factory=lambda: Path(os.getenv("RESOURCES_PATH", Path(__file__).parent.parent / "resources")).expanduser())
    revisions_path: Path = field(default_factory=lambda: Path())

    def __post_init__(self) -> None:
        self._load_environment()

        # If revisions_path was not explicitly provided or is default, initialize it relative to resources_path
        if not self.revisions_path or self.revisions_path == Path('.'):
            self.revisions_path = Path(os.getenv("REVISIONS_PATH", self.resources_path / "revisions")).expanduser()

    def _load_environment(self) -> None:
        """Load environment variables from .env file, with fallback to home directory."""
        try:
            load_dotenv()
        except Exception:
            home_dir = os.getenv("HOME")
            if home_dir:
                load_dotenv(Path(f"{home_dir}/.env"))

# Create an instance of the dataclass
config = ConfigManager()

__all__ = [
    "ConfigManager",
    "config",
]
