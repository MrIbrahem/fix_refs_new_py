"""Tests for SettingsLoader in fix_refs/core/settings.py"""

from fix_refs.core.settings import SettingsLoader


class TestSettingsLoader:
    """Unit tests for SettingsLoader class."""

    def test_load_settings_from_file(self):
        loader = SettingsLoader()
        settings = loader.load_settings_from_file()
        assert isinstance(settings, dict)

    def test_load_settings(self):
        loader = SettingsLoader()
        settings = loader.load_settings()
        assert isinstance(settings, dict)
        # Verify language settings format if loaded
        if "es" in settings:
            assert settings["es"].get("lang_code") == "es"
