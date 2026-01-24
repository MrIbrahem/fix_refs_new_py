"""
"""
from src.infobox.expend_infobox import do_comments


class TestDoComments:
    """Test cases for infobox expansion"""

    def test_do_comments(self):
        """Test do_comments function"""
        text = """Some text
<!-- Legal data -->
More text
<!-- Clinical data -->
End"""
        result = do_comments(text)
        # Comments should be reformatted with proper spacing
        assert "<!-- Legal data -->" in result
        assert "<!-- Clinical data -->" in result

    def test_do_comments_with_multiple_sections(self):
        """Test do_comments with various comment types"""
        text = """<!-- Names -->
<!-- Clinical data -->
<!-- Legal data -->
<!-- Pharmacokinetic data -->
<!-- Chemical and physical data -->"""
        result = do_comments(text)
        # All comments should still be present
        assert "<!-- Names -->" in result
        assert "<!-- Clinical data -->" in result
        assert "<!-- Legal data -->" in result
