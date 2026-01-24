"""
HTTP client utilities - replaces PHP cURL
"""

import requests
from typing import Optional
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
        'User-Agent': 'WikiProjectMed Translation Dashboard/1.0 (https://mdwiki.toolforge.org/; tools.mdwiki@toolforge.org)'
    }

    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return str(response.text)  # type: ignore
    except requests.RequestException as e:
        echo_debug(f"Request Error: {e}\n{url}")
        return ""
