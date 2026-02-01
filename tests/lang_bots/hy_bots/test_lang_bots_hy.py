"""Tests for Armenian language bot (hy_bot.py)

Converted from tests/remove_spaceTest.php and tests/remove_space2Test.php
"""
from fix_refs.lang_bots.hy_bot import (
    hy_fixes
)


class TestHyFixes:
    """Test cases for Armenian-specific fixes"""

    def test_hy_fixes_combined(self):
        """Test combined Armenian fixes"""
        input_text = 'Տեքստ  <ref name="TEST" /> ։ Ավելի  <ref name="TEST2" /> :'
        result = hy_fixes(input_text)
        # Both fixes should be applied
        assert '<ref name="TEST" />' in result
        assert '<ref name="TEST2" />' in result
