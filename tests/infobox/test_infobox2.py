"""Tests for infobox2 (infobox2Test.php)

Converted from tests/infoboxes/infobox2Test.php

Note: This test requires the infobox2 Python module which may need to be implemented.
"""
from pathlib import Path
from src.infobox.expend_infobox import expend_new

tests_dir = Path(__file__).parent / "texts_infobox2"


class TestInfobox2:
    """Test cases for infobox2 template processing"""

    def test_expend_new_file_text(self):
        """Test expend_new with file input"""

        with open(tests_dir / "input.txt", 'r', encoding='utf-8') as f:
            text_input = f.read()

        with open(tests_dir / "expected.txt", 'r', encoding='utf-8') as f:
            text_output = f.read()

        result = expend_new(text_input)

        with open(tests_dir / "output.txt", 'w', encoding='utf-8') as f:
            f.write(result)

        # result = result.replace('\r\n', '\n')
        # text_output = text_output.replace('\r\n', '\n')
        assert text_output.strip() == result.strip()
