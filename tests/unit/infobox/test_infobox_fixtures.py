""" """

from pathlib import Path

from src.fix_refs.infobox.expend_infobox import InfoboxExpander

tests_dir = Path(__file__).parent / "example1"


class TestInfobox2:
    """Test cases for infobox2 template processing"""

    def write_fixture(self, name: str, text: str):
        path = Path(__file__).parent / "fixtures" / name

        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

    def load_fixture(self, name: str) -> str:
        path = Path(__file__).parent / "fixtures" / name
        assert path.exists(), f"Fixture file missing: {path}"

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        assert content is not None, f"Unable to read fixture file: {path}"
        return content

    def test_expend_new_file_text(self):
        """Test _expend_new with file input"""

        source = self.load_fixture("example1/input.txt")
        expected = self.load_fixture("example1/expected.txt")

        result = InfoboxExpander()._expend_new(source)

        self.write_fixture("example1/output.txt", result)

        assert expected.strip() == result.strip()

    def test_expend_new_simple_template(self):
        """Test _expend_new with a simple template"""
        # Test with basic template
        source = self.load_fixture("example2/input.txt")
        expected = self.load_fixture("example2/expected.txt")

        result = InfoboxExpander()._expend_new(source).strip()
        assert result == expected.strip()

        self.write_fixture("example2/output.txt", result)
