"""
HTTP client utilities - replaces PHP cURL
"""

from __future__ import annotations

import json
import logging

import requests

logger = logging.getLogger(__name__)

DEFAULT_USER_AGENT = (
    "WikiProjectMed Translation Dashboard/1.0 (https://mdwiki.toolforge.org/; tools.mdwiki@toolforge.org)"
)


class HttpClient:
    """HTTP client for fetching web resources."""

    def __init__(
        self,
        user_agent: str | None = None,
        session: requests.Session | None = None,
    ) -> None:
        self.user_agent = user_agent or DEFAULT_USER_AGENT
        self.session = session or requests.Session()

    def get_url(self, url: str, timeout: int = 5) -> str:
        """Fetch URL content as string.

        Args:
            url: URL to fetch
            timeout: Request timeout in seconds

        Returns:
            Response text as string, empty string on error
        """
        headers = {"User-Agent": self.user_agent}
        try:
            response = self.session.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return str(response.text)
        except requests.RequestException as e:
            logger.debug(f"Request Error: {e}\n{url}")
        return ""

    def get_url_json(self, url: str, timeout: int = 5) -> dict | None:
        """Fetch URL content and parse as JSON.

        Args:
            url: URL to fetch
            timeout: Request timeout in seconds

        Returns:
            Parsed JSON as dictionary, None on error
        """
        headers = {"User-Agent": self.user_agent}
        try:
            response = self.session.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.debug(f"Request Error: {e}\n{url}")
        except (json.JSONDecodeError, ValueError) as e:
            logger.debug(f"JSON Decode Error: {e}\n{url}")
        return None


__all__ = [
    "HttpClient",
]
