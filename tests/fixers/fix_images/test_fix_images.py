"""Tests for fix_images.py

Tests the functionality of checking and removing missing images from Wikimedia Commons.

ImageFixer is a class that receives its HTTP client through the constructor, so:
- HTTP calls are mocked by injecting a mock client (no patching of module-level functions).
- Internal method calls are mocked by patching the method on the ImageFixer class.
"""

from unittest.mock import MagicMock

import pytest
import wikitextparser as wtp
from src.fix_refs.fixers.fix_images import ImageFixer
from src.fix_refs.utils.http import HttpClient

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def mock_http_client():
    """A mock HttpClient that is injected into ImageFixer."""
    return MagicMock(spec=HttpClient)


@pytest.fixture
def fixer(mock_http_client):
    """An ImageFixer that uses the mocked HttpClient."""
    return ImageFixer(http_client=mock_http_client)


@pytest.fixture
def mock_check(monkeypatch):
    """Replace ImageFixer.check_commons_image_exists on the class.

    Patching on the class affects every instance, including the ones created
    internally by the cached static method.
    """
    mock = MagicMock(return_value=True)
    monkeypatch.setattr(ImageFixer, "check_commons_image_exists", mock)
    return mock


@pytest.fixture(autouse=True)
def clear_cache():
    """The lru_cache is shared at class level, so clear it around every test."""
    ImageFixer().clear_image_cache()
    yield
    ImageFixer().clear_image_cache()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestInit:
    """Test ImageFixer construction"""

    def test_uses_injected_http_client(self, mock_http_client):
        """Test that an injected client is used"""
        assert ImageFixer(http_client=mock_http_client).http_client is mock_http_client

    def test_creates_default_http_client(self):
        """Test that a default HttpClient is created when none is given"""
        assert isinstance(ImageFixer().http_client, HttpClient)


class TestCheckCommonsImageExists:
    """Test checking if images exist on Wikimedia Commons"""

    def test_existing_image(self, fixer, mock_http_client):
        """Test that existing image returns True"""
        mock_http_client.get_url_json.return_value = {"query": {"pages": {"12345": {"title": "File:Example.png"}}}}

        assert fixer.check_commons_image_exists("Example.png") is True

    def test_missing_image(self, fixer, mock_http_client):
        """Test that missing image returns False"""
        mock_http_client.get_url_json.return_value = {"query": {"pages": {"-1": {"missing": ""}}}}

        assert fixer.check_commons_image_exists("NonExistent.png") is False

    def test_empty_filename(self, fixer, mock_http_client):
        """Test that empty filename returns False without calling the API"""
        assert fixer.check_commons_image_exists("") is False
        assert fixer.check_commons_image_exists("  ") is False
        mock_http_client.get_url_json.assert_not_called()

    @pytest.mark.parametrize(
        "filename", ["File:Example.png", "file:Example.png", "Image:Example.png", "image:Example.png"]
    )
    def test_prefix_removed(self, fixer, mock_http_client, filename):
        """Test that File:/Image: prefixes are removed before building the API URL"""
        mock_http_client.get_url_json.return_value = {"query": {"pages": {"12345": {"title": "File:Example.png"}}}}

        assert fixer.check_commons_image_exists(filename) is True

        url = mock_http_client.get_url_json.call_args.args[0]
        assert "File%3AExample.png" in url
        assert "File%3AFile" not in url
        assert "File%3AImage" not in url

    def test_timeout_is_forwarded(self, fixer, mock_http_client):
        """Test that the timeout is passed to the HTTP client"""
        mock_http_client.get_url_json.return_value = {"query": {"pages": {"1": {}}}}

        fixer.check_commons_image_exists("Example.png", timeout=3)

        assert mock_http_client.get_url_json.call_args.kwargs["timeout"] == 3

    def test_api_error_returns_true(self, fixer, mock_http_client):
        """Test that API errors return True to avoid removing valid images"""
        mock_http_client.get_url_json.return_value = None

        assert fixer.check_commons_image_exists("Example.png") is True


class TestCachedImageCheck:
    """Test cached image existence checking"""

    def test_cache_clear(self, fixer):
        """Test that cache can be cleared"""
        fixer.clear_image_cache()
        # Should not raise any exception

    def test_cache_is_used(self, fixer, mock_check):
        """Test that caching reduces API calls"""
        # First call should hit the API
        assert fixer.check_commons_image_exists_cached("Example.png") is True
        assert mock_check.call_count == 1

        # Second call should use cache
        assert fixer.check_commons_image_exists_cached("Example.png") is True
        assert mock_check.call_count == 1  # Still 1, not 2

    def test_cache_clear_resets_cache(self, fixer, mock_check):
        """Test that clearing the cache forces a new API call"""
        fixer.check_commons_image_exists_cached("Example.png")
        fixer.clear_image_cache()
        fixer.check_commons_image_exists_cached("Example.png")

        assert mock_check.call_count == 2


class TestExtractFilenameFromWikilink:
    """Test filename extraction from wikilinks"""

    @pytest.mark.parametrize(
        "wikitext, expected",
        [
            ("[[File:Example.png|thumb]]", "Example.png"),
            ("[[Image:Example.png|thumb]]", "Example.png"),
            ("[[file:Example.png]]", "Example.png"),  # prefix is case-insensitive
            ("[[Article Name]]", None),  # non-file link
        ],
    )
    def test_extract_filename(self, fixer, wikitext, expected):
        """Test extracting filename from File:/Image: wikilinks"""
        wikilink = wtp.parse(wikitext).wikilinks[0]
        assert fixer._extract_filename_from_wikilink(wikilink) == expected


class TestRemoveMissingInlineImages:
    """Test removal of missing inline images"""

    def test_remove_missing_inline_image(self, fixer, mock_check):
        """Test that missing inline image is removed"""
        mock_check.return_value = False

        result = fixer.remove_missing_inline_images("Text with [[File:Missing.png|thumb|caption]] here.")
        assert result == "Text with  here."

    def test_keep_existing_inline_image(self, fixer, mock_check):
        """Test that existing inline image is kept"""
        mock_check.return_value = True

        input_text = "Text with [[File:Exists.png|thumb|caption]] here."
        assert fixer.remove_missing_inline_images(input_text) == input_text

    def test_remove_image_prefix(self, fixer, mock_check):
        """Test removal with Image: prefix"""
        mock_check.return_value = False

        assert fixer.remove_missing_inline_images("[[Image:Missing.png|caption]]") == ""

    def test_keep_non_file_links(self, fixer, mock_check):
        """Test that non-file wikilinks are preserved and never checked"""
        input_text = "[[Article]] and [[Another Article|label]]"

        assert fixer.remove_missing_inline_images(input_text) == input_text
        mock_check.assert_not_called()

    def test_multiple_inline_images(self, fixer, mock_check):
        """Test handling multiple inline images"""
        # Wikilinks are processed in reverse order:
        # the second file (Exists.png) is checked first -> exists
        # the first file (Missing.png) is checked second -> missing
        mock_check.side_effect = [True, False]

        input_text = "First [[File:Missing.png|thumb]] and second [[File:Exists.png|thumb]]."
        expected = "First  and second [[File:Exists.png|thumb]]."

        assert fixer.remove_missing_inline_images(input_text) == expected


def _get_args(text, *names):
    """Return a {name: argument} dict for the first template in the parsed text."""
    template = wtp.parse(text).templates[0]
    found = {}
    for arg in template.arguments:
        name = arg.name.strip().lower()
        if name in names:
            found[name] = arg
    return found


class TestRemoveMissingInfoboxImages:
    """Test removal of missing infobox images"""

    def test_empty_missing_infobox_image(self, fixer, mock_check):
        """Test that missing infobox image and its caption are set to empty"""
        mock_check.return_value = False

        input_text = (
            "{{Infobox\n|name = Example\n|image = Non_existent.png\n|caption = This caption for missing image\n}}"
        )

        args = _get_args(fixer.remove_missing_infobox_images(input_text), "image", "caption")

        assert args["image"].value.strip() == ""
        assert args["caption"].value.strip() == ""

    def test_keep_existing_infobox_image(self, fixer, mock_check):
        """Test that existing infobox image is kept"""
        mock_check.return_value = True

        input_text = "{{Infobox\n|name = Example\n|image = Exists.png\n|caption = Valid caption\n}}"

        result = fixer.remove_missing_infobox_images(input_text)
        assert "Exists.png" in result
        assert "Valid caption" in result

    def test_numbered_image_parameters(self, fixer, mock_check):
        """Test handling of image2, image3 parameters"""
        mock_check.return_value = False

        input_text = "{{Infobox\n|image2 = Missing2.png\n|caption2 = Caption 2\n}}"

        args = _get_args(fixer.remove_missing_infobox_images(input_text), "image2", "caption2")

        assert args["image2"].value.strip() == ""
        assert args["caption2"].value.strip() == ""

    def test_skip_empty_image_values(self, fixer, mock_check):
        """Test that already empty image values are skipped"""
        fixer.remove_missing_infobox_images("{{Infobox\n|image =\n|caption =\n}}")

        # Should not call the API for empty values
        assert mock_check.call_count == 0

    def test_multiple_templates(self, fixer, mock_check):
        """Test handling multiple templates in text"""
        mock_check.side_effect = [False, True]

        input_text = "{{Infobox1\n|image = Missing.png\n}}\n{{Infobox2\n|image = Exists.png\n}}"

        result = fixer.remove_missing_infobox_images(input_text)

        # First template should have empty image value
        assert "|image =" in result and "Missing.png" not in result
        # Second template should retain its image
        assert "Exists.png" in result

    def test_use_cache_flag_uses_cached_check(self, fixer, mock_check):
        """Test that use_cache=True goes through the cached checker"""
        mock_check.return_value = True

        input_text = "{{Infobox1\n|image = Same.png\n}}\n{{Infobox2\n|image = Same.png\n}}"

        fixer.remove_missing_infobox_images(input_text, use_cache=True)

        assert mock_check.call_count == 1


class TestRemoveMissingImages:
    """Test main function that handles both infobox and inline images"""

    def test_combined_infobox_and_inline(self, fixer, mock_check):
        """Test handling both infobox and inline images"""
        mock_check.return_value = False

        input_text = (
            "{{Infobox|image = Missing1.png\n|caption = Caption 1\n}}\nText with [[File:Missing2.png|thumb]] here."
        )

        result = fixer.remove_missing_images(input_text)

        # Check infobox image is emptied
        assert _get_args(result, "image")["image"].value.strip() == ""

        # Check inline image is removed
        assert "[[File:Missing2.png" not in result

    def test_empty_text(self, fixer, mock_check):
        """Test handling empty text"""
        assert fixer.remove_missing_images("") == ""

    def test_text_without_images(self, fixer, mock_check):
        """Test handling text without images"""
        input_text = "This is plain text without any images."

        assert fixer.remove_missing_images(input_text) == input_text
        mock_check.assert_not_called()


class TestRemoveMissingImagesCached:
    """Test cached version of remove_missing_images"""

    def test_uses_cache(self, fixer, mock_check):
        """Test that cached version uses caching"""
        mock_check.return_value = False

        input_text = "{{Infobox\n|image = Missing.png\n}}\nText with [[File:Missing.png|thumb]] here."

        fixer.remove_missing_images_cached(input_text)

        # Should only call API once due to caching
        assert mock_check.call_count == 1


@pytest.mark.network
class TestNetworkImageCheck:
    """Network tests that actually call the Wikimedia Commons API

    These tests are marked with @pytest.mark.network and won't run by default.
    Run with: pytest -m network
    """

    def test_real_existing_image(self):
        """Test with a real existing image on Commons"""
        # This is a well-known file that should exist on Commons
        assert ImageFixer().check_commons_image_exists("Wiki.png") is True

    def test_real_missing_image(self):
        """Test with a non-existent image"""
        # This filename is unlikely to exist
        assert ImageFixer().check_commons_image_exists("NonExistentFile12345xyz.png") is False
