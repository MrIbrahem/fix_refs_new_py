"""Tests for fix_page (FixpageTest.php)

Converted from tests/FixpageTest.php
"""
import pytest
from pathlib import Path

from src.core.fix_page import fix_one_page


def test_file_ja():
    tests_dir = Path(__file__).parent / "texts/ja"

    with open(tests_dir / "input.txt", 'r', encoding='utf-8') as f:
        text_input = f.read()

    with open(tests_dir / "expected.txt", 'r', encoding='utf-8') as f:
        expected = f.read()

    result = fix_one_page(
        text=text_input,
        title="title",
        lang="ja",
        move_dots=True,
        expend_infobox=True,
        add_en_lang=False,
        source_title="",
        mdwiki_revid=0
    )

    # write output for comparison
    output_file = tests_dir / "output.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)

    # Normalize line endings for comparison
    assert result.strip() == expected.strip()
