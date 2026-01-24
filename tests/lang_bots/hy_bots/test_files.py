"""Tests for remove_space (remove_spaceTest.php)

Converted from tests/remove_spaceTest.php
"""
import pytest
from pathlib import Path
from src.lang_bots.hy_bot import remove_spaces_between_last_word_and_beginning_of_ref


def test_file_text_1():
    """Test with file input for Spanish references"""
    tests_dir = Path(__file__).parent / "remove_space_texts/1"

    with open(tests_dir / "input.txt", 'r', encoding='utf-8') as f:
        text_input = f.read()

    with open(tests_dir / "expected.txt", 'r', encoding='utf-8') as f:
        expected = f.read()

    # result = mv_es_refs(text_input)
    result = remove_spaces_between_last_word_and_beginning_of_ref(text_input, "hy")

    # write output for comparison
    output_file = tests_dir / "output.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)

    # Normalize line endings for comparison
    assert result.strip() == expected.strip()


def test_file_text_2():
    """Test with file input for Spanish references"""
    tests_dir = Path(__file__).parent / "remove_space_texts/2"

    with open(tests_dir / "input.txt", 'r', encoding='utf-8') as f:
        text_input = f.read()

    with open(tests_dir / "expected.txt", 'r', encoding='utf-8') as f:
        expected = f.read()

    # result = mv_es_refs(text_input)
    result = remove_spaces_between_last_word_and_beginning_of_ref(text_input, "hy")

    # write output for comparison
    output_file = tests_dir / "output.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)

    # Normalize line endings for comparison
    assert result.strip() == expected.strip()
