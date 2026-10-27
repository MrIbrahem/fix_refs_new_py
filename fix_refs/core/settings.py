from __future__ import annotations

import functools
import json
import logging
import os

from ..config import ConfigManager
from ..utils.http import HttpClient

logger = logging.getLogger(__name__)


class SettingsLoader:
    """Loader for language settings from local configuration files or remote server."""

    def __init__(
        self,
        config_manager: ConfigManager | None = None,
        http_client: HttpClient | None = None,
    ) -> None:
        self.config_manager = config_manager or ConfigManager()
        self.http_client = http_client or HttpClient()

    def load_settings_from_file(self) -> dict:
        """Load language settings from local JSON file."""
        file_path = self.config_manager.resources_path / "language_settings.json"
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def load_settings_from_server(self, server_name: str) -> dict:
        """Load language settings from remote API server."""
        url = "http://localhost:9001/api.php?get=language_settings"
        if server_name == "mdwiki.toolforge.org":
            url = "https://mdwiki.toolforge.org/api.php?get=language_settings"

        json_data = self.http_client.get_url(url)

        try:
            data = json.loads(json_data)
        except json.JSONDecodeError:
            data = {}
        return data

    def load_settings(self) -> dict:
        """Load language settings based on environment configuration."""
        server_name = os.environ.get("SERVER_NAME", "")
        if server_name:
            data = self.load_settings_from_server(server_name)
        else:
            data = self.load_settings_from_file()

        results = data.get("results", [])
        new = {}

        for value in results:
            lang_code = value.get("lang_code")
            if lang_code:
                new[lang_code] = value

        return new


def load_settings_from_file() -> dict:
    """Legacy function to load settings from file."""
    return SettingsLoader().load_settings_from_file()


def load_settings_from_server(server_name: str) -> dict:
    """Legacy function to load settings from server."""
    return SettingsLoader().load_settings_from_server(server_name)


@functools.lru_cache(maxsize=1)
def load_settings() -> dict:
    """Legacy function to load settings with caching."""
    return SettingsLoader().load_settings()


__all__ = [
    "SettingsLoader",
    "load_settings_from_file",
    "load_settings_from_server",
    "load_settings",
]
