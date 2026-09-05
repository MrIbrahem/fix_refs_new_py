"""
Fix missing references by expanding from source text
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from ..config import revisions_path
from ..parsers.citations_parser import get_short_refs
from ..utils.debug import echo_debug, echo_test
from .expend_refs import refs_expand


def get_revision_file_path(mdwiki_revid) -> Path:

    file = revisions_path / f"{mdwiki_revid}/wikitext.txt"

    return file


def find_mdwiki_revid(sourcetitle: str) -> str:
    """Find MDWiki revision ID from JSON file

    Args:
        sourcetitle: Source page title

    Returns:
        MDWiki revision ID or empty string
    """
    json_file = f"{revisions_path}/json_data.json"

    if not Path(json_file).exists():
        return ""

    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data: dict[str, Any] = json.load(f)  # type: ignore

        echo_test(f"url{json_file}")
        echo_test(f"count of data: {len(data)}")

        result = data.get(sourcetitle, "")
        return str(result) if isinstance(result, str) else ""
    except (OSError, json.JSONDecodeError):
        return ""


def get_full_text(sourcetitle: str, mdwiki_revid: int) -> str:
    """Get full text from MDWiki revision

    Args:
        sourcetitle: Source page title
        mdwiki_revid: MDWiki revision ID

    Returns:
        Full text or empty string
    """
    sourcetitle = sourcetitle.replace(" ", "_")

    if mdwiki_revid == 0:
        revid_str = find_mdwiki_revid(sourcetitle)
        mdwiki_revid = int(revid_str) if revid_str.isdigit() else 0

    if mdwiki_revid == 0:
        echo_test(f"empty mdwiki_revid, sourcetitle:({sourcetitle})")
        return ""

    file = get_revision_file_path(mdwiki_revid)

    if not Path(file).exists():
        echo_test(f"file not found: {file}")
        return ""

    echo_test(f"url{file}")

    try:
        with open(file, "r", encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def fix_missing_refs(text: str, sourcetitle: str, mdwiki_revid: int = 0) -> str:
    """Fix missing references by expanding from MDWiki source

    Args:
        text: Text to fix
        sourcetitle: Source page title
        mdwiki_revid: MDWiki revision ID

    Returns:
        Text with missing references expanded
    """
    short_refs = get_short_refs(text)

    echo_debug(f"empty refs: {len(short_refs)}")

    if not short_refs:
        return text

    full_text = get_full_text(sourcetitle, mdwiki_revid)

    if not full_text:
        return text

    text = refs_expand(short_refs, text, full_text)

    return text


__all__ = [
    "get_revision_file_path",
    "find_mdwiki_revid",
    "get_full_text",
    "fix_missing_refs",
]
