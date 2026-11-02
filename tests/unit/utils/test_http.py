"""Tests for HttpClient class in fix_refs/utils/http.py"""

from src.fix_refs.utils.http import HttpClient


class TestHttpClient:
    """Unit tests for HttpClient class."""

    def test_init_defaults(self):
        client = HttpClient()
        assert "WikiProjectMed" in client.user_agent
        assert client.session is not None

    def test_init_custom_user_agent(self):
        client = HttpClient(user_agent="CustomAgent/1.0")
        assert client.user_agent == "CustomAgent/1.0"

    def test_get_url_error_returns_empty_string(self):
        client = HttpClient()
        # Invalid scheme / URL should handle error gracefully
        result = client.get_url("http://invalid.domain.that.does.not.exist.123456789")
        assert result == ""

    def test_get_url_json_error_returns_none(self):
        client = HttpClient()
        result = client.get_url_json("http://invalid.domain.that.does.not.exist.123456789")
        assert result is None
