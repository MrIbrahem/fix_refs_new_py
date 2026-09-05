"""
HTTP client utilities - replaces PHP cURL
"""

import json

import requests

from .debug import echo_debug


def get_url(url: str, timeout: int = 5) -> str:
    """Fetch URL content using requests library

    Args:
        url: URL to fetch
        timeout: Request timeout in seconds

    Returns:
        Response text as string, empty string on error
    """
    headers = {
        "User-Agent": "WikiProjectMed Translation Dashboard/1.0 (https://mdwiki.toolforge.org/; tools.mdwiki@toolforge.org)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return str(response.text)  # type: ignore
    except requests.RequestException as e:
        echo_debug(f"Request Error: {e}\n{url}")
    return ""


def get_url_json(url: str, timeout: int = 5) -> dict | None:
    """Fetch URL content and parse as JSON using requests library

    Args:
        url: URL to fetch
        timeout: Request timeout in seconds

    Returns:
        Parsed JSON as dictionary, None on error
    """
    headers = {
        "User-Agent": "WikiProjectMed Translation Dashboard/1.0 (https://mdwiki.toolforge.org/; tools.mdwiki@toolforge.org)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        echo_debug(f"Request Error: {e}\n{url}")
    except (json.JSONDecodeError, ValueError) as e:
        echo_debug(f"JSON Decode Error: {e}\n{url}")
    return None


__all__ = [
    "get_url",
    "get_url_json",
]
