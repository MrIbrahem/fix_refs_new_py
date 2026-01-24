"""Tests for Spanish references (es_refsTest.php)

Converted from tests/es_bots/es_refsTest.php
"""
from pathlib import Path
from src.lang_bots.es.es_refs import mv_es_refs
from src.lang_bots.es.es_bot import fix_es


class TestEsRefs:
    """Test cases for Spanish reference moving"""

    def test_file_text_1(self):
        """Test with file input for Spanish references"""
        tests_dir = Path(__file__).parent / "mv_es_refs_texts/1"

        with open(tests_dir / "input.txt", 'r', encoding='utf-8') as f:
            text_input = f.read()

        with open(tests_dir / "expected.txt", 'r', encoding='utf-8') as f:
            expected = f.read()

        # result = mv_es_refs(text_input)
        result = fix_es(text_input)

        # write output for comparison
        output_file = tests_dir / "output.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)

        # Normalize line endings for comparison
        assert result.strip() == expected.strip()

    def test_file_text_2(self):
        """Test with file input for Spanish references"""
        tests_dir = Path(__file__).parent / "mv_es_refs_texts/2"

        with open(tests_dir / "input.txt", 'r', encoding='utf-8') as f:
            text_input = f.read()

        with open(tests_dir / "expected.txt", 'r', encoding='utf-8') as f:
            expected = f.read()

        # result = mv_es_refs(text_input)
        result = fix_es(text_input)

        # write output for comparison
        output_file = tests_dir / "output.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)

        # Normalize line endings for comparison
        assert result.strip() == expected.strip()
