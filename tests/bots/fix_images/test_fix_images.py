"""Tests for fix_images.py

Tests the functionality of checking and removing missing images from Wikimedia Commons.
"""
import pytest
import wikitextparser as wtp

from unittest.mock import patch
from fix_refs.bots.fix_images import (
    check_commons_image_exists,
    check_commons_image_exists_cached,
    remove_missing_infobox_images,
    remove_missing_inline_images,
    remove_missing_images,
    remove_missing_images_cached,
    clear_image_cache,
    _extract_filename_from_wikilink,
)


class TestCheckCommonsImageExists:
    """Test checking if images exist on Wikimedia Commons"""

    @patch('fix_refs.bots.fix_images.get_url_json')
    def test_existing_image(self, mock_get_url_json):
        """Test that existing image returns True"""
        mock_get_url_json.return_value = {"query": {"pages": {"12345": {"title": "File:Example.png"}}}}

        result = check_commons_image_exists("Example.png")
        assert result is True

    @patch('fix_refs.bots.fix_images.get_url_json')
    def test_missing_image(self, mock_get_url_json):
        """Test that missing image returns False"""
        mock_get_url_json.return_value = {"query": {"pages": {"-1": {"missing": ""}}}}

        result = check_commons_image_exists("NonExistent.png")
        assert result is False

    def test_empty_filename(self):
        """Test that empty filename returns False"""
        assert check_commons_image_exists("") is False
        assert check_commons_image_exists("  ") is False

    @patch('fix_refs.bots.fix_images.get_url_json')
    def test_file_prefix_removed(self, mock_get_url_json):
        """Test that File: prefix is properly removed"""
        mock_get_url_json.return_value = {"query": {"pages": {"12345": {"title": "File:Example.png"}}}}

        result = check_commons_image_exists("File:Example.png")
        assert result is True

    @patch('fix_refs.bots.fix_images.get_url_json')
    def test_image_prefix_removed(self, mock_get_url_json):
        """Test that Image: prefix is properly removed"""
        mock_get_url_json.return_value = {"query": {"pages": {"12345": {"title": "File:Example.png"}}}}

        result = check_commons_image_exists("Image:Example.png")
        assert result is True

    @patch('fix_refs.bots.fix_images.get_url_json')
    def test_api_error_returns_true(self, mock_get_url_json):
        """Test that API errors return True to avoid removing valid images"""
        mock_get_url_json.return_value = None

        result = check_commons_image_exists("Example.png")
        assert result is True


class TestCachedImageCheck:
    """Test cached image existence checking"""

    def test_cache_clear(self):
        """Test that cache can be cleared"""
        clear_image_cache()
        # Should not raise any exception

    @patch('fix_refs.bots.fix_images.check_commons_image_exists')
    def test_cache_is_used(self, mock_check):
        """Test that caching reduces API calls"""
        mock_check.return_value = True

        # Clear cache first
        clear_image_cache()

        # First call should hit the API
        result1 = check_commons_image_exists_cached("Example.png")
        assert result1 is True
        assert mock_check.call_count == 1

        # Second call should use cache
        result2 = check_commons_image_exists_cached("Example.png")
        assert result2 is True
        assert mock_check.call_count == 1  # Still 1, not 2


class TestExtractFilenameFromWikilink:
    """Test filename extraction from wikilinks"""

    def test_extract_file_link(self):
        """Test extracting filename from File: wikilink"""
        parsed = wtp.parse("[[File:Example.png|thumb]]")
        wikilink = parsed.wikilinks[0]
        filename = _extract_filename_from_wikilink(wikilink)
        assert filename == "Example.png"

    def test_extract_image_link(self):
        """Test extracting filename from Image: wikilink"""
        parsed = wtp.parse("[[Image:Example.png|thumb]]")
        wikilink = parsed.wikilinks[0]
        filename = _extract_filename_from_wikilink(wikilink)
        assert filename == "Example.png"

    def test_non_file_link(self):
        """Test that non-file links return None"""
        parsed = wtp.parse("[[Article Name]]")
        wikilink = parsed.wikilinks[0]
        filename = _extract_filename_from_wikilink(wikilink)
        assert filename is None

    def test_case_insensitive(self):
        """Test that File/Image prefixes are case-insensitive"""
        parsed = wtp.parse("[[file:Example.png]]")
        wikilink = parsed.wikilinks[0]
        filename = _extract_filename_from_wikilink(wikilink)
        assert filename == "Example.png"


class TestRemoveMissingInlineImages:
    """Test removal of missing inline images"""

    @patch('fix_refs.bots.fix_images.check_commons_image_exists')
    def test_remove_missing_inline_image(self, mock_check):
        """Test that missing inline image is removed"""
        mock_check.return_value = False

        input_text = "Text with [[File:Missing.png|thumb|caption]] here."
        expected = "Text with  here."

        result = remove_missing_inline_images(input_text)
        assert result == expected

    @patch('fix_refs.bots.fix_images.check_commons_image_exists')
    def test_keep_existing_inline_image(self, mock_check):
        """Test that existing inline image is kept"""
        mock_check.return_value = True

        input_text = "Text with [[File:Exists.png|thumb|caption]] here."

        result = remove_missing_inline_images(input_text)
        assert result == input_text

    @patch('fix_refs.bots.fix_images.check_commons_image_exists')
    def test_remove_image_prefix(self, mock_check):
        """Test removal with Image: prefix"""
        mock_check.return_value = False

        input_text = "[[Image:Missing.png|caption]]"
        expected = ""

        result = remove_missing_inline_images(input_text)
        assert result == expected

    @patch('fix_refs.bots.fix_images.check_commons_image_exists')
    def test_keep_non_file_links(self, mock_check):
        """Test that non-file wikilinks are preserved"""
        input_text = "[[Article]] and [[Another Article|label]]"

        result = remove_missing_inline_images(input_text)
        assert result == input_text

    @patch('fix_refs.bots.fix_images.check_commons_image_exists')
    def test_multiple_inline_images(self, mock_check):
        """Test handling multiple inline images"""
        # Wikilinks are processed in reverse order
        # Second file (Exists.png) is checked first - returns True (exists)
        # First file (Missing.png) is checked second - returns False (missing)
        mock_check.side_effect = [True, False]

        input_text = "First [[File:Missing.png|thumb]] and second [[File:Exists.png|thumb]]."
        expected = "First  and second [[File:Exists.png|thumb]]."

        result = remove_missing_inline_images(input_text)
        assert result == expected


class TestRemoveMissingInfoboxImages:
    """Test removal of missing infobox images"""

    @patch('fix_refs.bots.fix_images.check_commons_image_exists')
    def test_empty_missing_infobox_image(self, mock_check):
        """Test that missing infobox image is set to empty"""
        mock_check.return_value = False

        input_text = """{{Infobox\n|name = Example\n|image = Non_existent.png\n|caption = This caption for missing image\n}}"""

        result = remove_missing_infobox_images(input_text)

        # Parse result to check
        parsed = wtp.parse(result)
        template = parsed.templates[0]

        image_arg = None
        caption_arg = None
        for arg in template.arguments:
            if arg.name.strip().lower() == 'image':
                image_arg = arg
            elif arg.name.strip().lower() == 'caption':
                caption_arg = arg

        assert image_arg is not None
        assert image_arg.value.strip() == ''
        assert caption_arg is not None
        assert caption_arg.value.strip() == ''

    @patch('fix_refs.bots.fix_images.check_commons_image_exists')
    def test_keep_existing_infobox_image(self, mock_check):
        """Test that existing infobox image is kept"""
        mock_check.return_value = True

        input_text = """{{Infobox\n|name = Example\n|image = Exists.png\n|caption = Valid caption\n}}"""

        result = remove_missing_infobox_images(input_text)
        assert "Exists.png" in result
        assert "Valid caption" in result

    @patch('fix_refs.bots.fix_images.check_commons_image_exists')
    def test_numbered_image_parameters(self, mock_check):
        """Test handling of image2, image3 parameters"""
        mock_check.return_value = False

        input_text = """{{Infobox\n|image2 = Missing2.png\n|caption2 = Caption 2\n}}"""

        result = remove_missing_infobox_images(input_text)

        parsed = wtp.parse(result)
        template = parsed.templates[0]

        image2_arg = None
        caption2_arg = None
        for arg in template.arguments:
            if arg.name.strip().lower() == 'image2':
                image2_arg = arg
            elif arg.name.strip().lower() == 'caption2':
                caption2_arg = arg

        assert image2_arg is not None
        assert image2_arg.value.strip() == ''
        assert caption2_arg is not None
        assert caption2_arg.value.strip() == ''

    @patch('fix_refs.bots.fix_images.check_commons_image_exists')
    def test_skip_empty_image_values(self, mock_check):
        """Test that already empty image values are skipped"""
        input_text = """{{Infobox\n|image =\n|caption =\n}}"""

        _result = remove_missing_infobox_images(input_text)
        # Should not call the API for empty values
        assert mock_check.call_count == 0

    @patch('fix_refs.bots.fix_images.check_commons_image_exists')
    def test_multiple_templates(self, mock_check):
        """Test handling multiple templates in text"""
        mock_check.side_effect = [False, True]

        input_text = """{{Infobox1\n|image = Missing.png\n}}\n{{Infobox2\n|image = Exists.png\n}}"""

        result = remove_missing_infobox_images(input_text)

        # First template should have empty image value
        assert "|image =" in result and "Missing.png" not in result
        # Second template should retain its image
        assert "Exists.png" in result


class TestRemoveMissingImages:
    """Test main function that handles both infobox and inline images"""

    @patch('fix_refs.bots.fix_images.check_commons_image_exists')
    def test_combined_infobox_and_inline(self, mock_check):
        """Test handling both infobox and inline images"""
        mock_check.return_value = False

        input_text = """{{Infobox|image = Missing1.png\n|caption = Caption 1\n}}\nText with [[File:Missing2.png|thumb]] here."""

        result = remove_missing_images(input_text)

        # Check infobox image is emptied
        parsed = wtp.parse(result)
        template = parsed.templates[0]
        for arg in template.arguments:
            if arg.name.strip().lower() == 'image':
                assert arg.value.strip() == ''

        # Check inline image is removed
        assert "[[File:Missing2.png" not in result

    @patch('fix_refs.bots.fix_images.check_commons_image_exists')
    def test_empty_text(self, mock_check):
        """Test handling empty text"""
        result = remove_missing_images("")
        assert result == ""

    @patch('fix_refs.bots.fix_images.check_commons_image_exists')
    def test_text_without_images(self, mock_check):
        """Test handling text without images"""
        input_text = "This is plain text without any images."
        result = remove_missing_images(input_text)
        assert result == input_text


class TestRemoveMissingImagesCached:
    """Test cached version of remove_missing_images"""

    @patch('fix_refs.bots.fix_images.check_commons_image_exists')
    def test_uses_cache(self, mock_check):
        """Test that cached version uses caching"""
        mock_check.return_value = False

        # Clear cache first
        clear_image_cache()

        input_text = """{{Infobox\n|image = Missing.png\n}}\nText with [[File:Missing.png|thumb]] here."""

        _result = remove_missing_images_cached(input_text)

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
        result = check_commons_image_exists("Wiki.png")
        assert result is True

    def test_real_missing_image(self):
        """Test with a non-existent image"""
        # This filename is unlikely to exist
        result = check_commons_image_exists("NonExistentFile12345xyz.png")
        assert result is False
