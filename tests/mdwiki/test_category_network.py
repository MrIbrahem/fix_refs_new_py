"""Tests for MDWiki category service (md_catTest.php)

Converted from tests/md_catTest.php and updated for MDWikiCategoryService.
"""

import json
from unittest.mock import MagicMock, patch

import pytest

from fix_refs.mdwiki.category import (
    SKIP_LANGS_CATEGORY,
    MDWikiCategoryService,
)

# Mock Wikidata sitelinks-style data: {"<lang>wiki": {"title": ...}}
MOCK_CATS = {
    "frwiki": {"title": "Catégorie:Traduit de MDWiki"},
    "dewiki": {"title": "Category:Translated from MDWiki (de)"},
    "ruwiki": {"title": "Категория:Статьи, переведённые с MDWiki"},
    "urwiki": {"title": "زمرہ:ایم ڈی وکی سے ترجمہ شدہ"},
}

DEFAULT_CAT = "Category:Translated from MDWiki"


@pytest.fixture
def config_manager(tmp_path):
    """ConfigManager stub whose resources_path points to a temp dir."""
    cm = MagicMock()
    cm.resources_path = tmp_path
    return cm


@pytest.fixture
def service(config_manager, monkeypatch):
    """Service wired to a fake URL getter returning MOCK_CATS (no network)."""
    monkeypatch.setenv("SERVER_NAME", "example.org")
    return MDWikiCategoryService(
        config_manager=config_manager,
        url_getter=lambda url: json.dumps(MOCK_CATS),
    )


class TestAddTranslatedFromMdwiki:
    """Test cases for MDWiki category addition"""

    def test_appends_category_when_conditions_met(self, service):
        text = "This is a sample text"
        result = service.add_translated_from_mdwiki(text, "fr")
        assert result == "This is a sample text\n[[Catégorie:Traduit de MDWiki]]\n"

    def test_does_not_append_when_category_exists(self, service):
        text = "This is a sample text\n[[Category:Translated from MDWiki (de)]]"
        assert service.add_translated_from_mdwiki(text, "de") == text

    def test_handles_multiple_newlines(self, service):
        text = "This is a sample text\n\n"
        result = service.add_translated_from_mdwiki(text, "ru")
        expected = "This is a sample text\n\n\n[[Категория:Статьи, переведённые с MDWiki]]\n"
        assert result == expected

    def test_langs_ur(self, service):
        cat = "زمرہ:ایم ڈی وکی سے ترجمہ شدہ"
        text_no_cat = "This is a sample text\n\n"

        result = service.add_translated_from_mdwiki(text_no_cat, "ur")
        assert result == f"{text_no_cat}\n[[{cat}]]\n"

        # Existing category
        text_with_cat = f"This is a sample text\n\n[[{cat}]]\n"
        assert service.add_translated_from_mdwiki(text_with_cat, "ur") == text_with_cat

        # Fallback category already present (matched by regex, case-insensitive)
        text_with_cat2 = "This is a sample text\n\n[[category:Translated_from_MDWiki]]\n"
        assert service.add_translated_from_mdwiki(text_with_cat2, "ur") == text_with_cat2

    @pytest.mark.parametrize("lang", SKIP_LANGS_CATEGORY)
    def test_skips_configured_languages(self, service, lang):
        text = "This is a sample text"
        assert service.add_translated_from_mdwiki(text, lang) == text

    def test_custom_skip_langs(self, config_manager, monkeypatch):
        monkeypatch.setenv("SERVER_NAME", "example.org")
        svc = MDWikiCategoryService(
            config_manager=config_manager,
            url_getter=lambda url: json.dumps(MOCK_CATS),
            skip_langs=["fr"],
        )
        assert svc.add_translated_from_mdwiki("text", "fr") == "text"
        assert svc.add_translated_from_mdwiki("text", "de").endswith("[[Category:Translated from MDWiki (de)]]\n")

    def test_uses_get_mdwiki_category(self, service):
        """The service method must call its own get_mdwiki_category."""
        with patch.object(service, "get_mdwiki_category", return_value="Cat:X") as m:
            result = service.add_translated_from_mdwiki("text", "xx")
        m.assert_called_once_with("xx")
        assert result == "text\n[[Cat:X]]\n"

    def test_empty_category_not_appended(self, service):
        with patch.object(service, "get_mdwiki_category", return_value=""):
            assert service.add_translated_from_mdwiki("text", "xx") == "text"


class TestGetMdwikiCategory:
    def test_returns_title_for_lang(self, service):
        assert service.get_mdwiki_category("fr") == "Catégorie:Traduit de MDWiki"

    def test_default_when_lang_missing(self, service):
        assert service.get_mdwiki_category("zz") == DEFAULT_CAT

    @pytest.mark.parametrize("lang", SKIP_LANGS_CATEGORY)
    def test_empty_for_skipped_langs(self, service, lang):
        assert service.get_mdwiki_category(lang) == ""

    def test_default_when_title_not_string(self, config_manager, monkeypatch):
        monkeypatch.setenv("SERVER_NAME", "example.org")
        svc = MDWikiCategoryService(
            config_manager=config_manager,
            url_getter=lambda url: json.dumps({"frwiki": {"title": 123}}),
        )
        assert svc.get_mdwiki_category("fr") == DEFAULT_CAT


class TestGetCats:
    def test_local_file_when_no_server_name(self, config_manager, monkeypatch):
        monkeypatch.delenv("SERVER_NAME", raising=False)
        (config_manager.resources_path / "mdwiki_categories.json").write_text(
            json.dumps({"frwiki": {"title": "Local"}}), encoding="utf-8"
        )
        getter = MagicMock()
        svc = MDWikiCategoryService(config_manager=config_manager, url_getter=getter)

        assert svc.get_cats() == {"frwiki": {"title": "Local"}}
        getter.assert_not_called()

    def test_fetches_from_wikidata(self, service):
        assert service.get_cats() == MOCK_CATS

    def test_passes_wikidata_url_to_getter(self, config_manager, monkeypatch):
        monkeypatch.setenv("SERVER_NAME", "example.org")
        getter = MagicMock(return_value=json.dumps(MOCK_CATS))
        svc = MDWikiCategoryService(config_manager=config_manager, url_getter=getter, wikidata_url="https://x.test/api")
        svc.get_cats()
        getter.assert_called_once_with("https://x.test/api")

    @pytest.mark.parametrize("bad_response", [None, "", "not json", "[1, 2, 3]"])
    def test_falls_back_to_local_on_bad_response(self, config_manager, monkeypatch, bad_response):
        monkeypatch.setenv("SERVER_NAME", "example.org")
        (config_manager.resources_path / "mdwiki_categories.json").write_text(
            json.dumps({"fallback": True}), encoding="utf-8"
        )
        svc = MDWikiCategoryService(config_manager=config_manager, url_getter=lambda url: bad_response)
        assert svc.get_cats() == {"fallback": True}


class TestLoadFromLocalFile:
    def test_loads_json(self, config_manager):
        data = {"frwiki": {"title": "Local"}}
        (config_manager.resources_path / "mdwiki_categories.json").write_text(json.dumps(data), encoding="utf-8")
        svc = MDWikiCategoryService(config_manager=config_manager)
        assert svc.load_from_local_file() == data

    def test_missing_file_returns_empty(self, config_manager):
        svc = MDWikiCategoryService(config_manager=config_manager)
        assert svc.load_from_local_file() == {}

    def test_invalid_json_returns_empty(self, config_manager):
        (config_manager.resources_path / "mdwiki_categories.json").write_text("{broken", encoding="utf-8")
        svc = MDWikiCategoryService(config_manager=config_manager)
        assert svc.load_from_local_file() == {}
