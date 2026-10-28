"""Tests for expend_refs (expend_refsTest.php)

Converted from tests/fixers/refs/expend_refsTest.php
"""

from src.fix_refs.fixers.refs.expend_refs import RefExpander


class TestExpendRefsWithNameOnly:
    """Test cases for expanding references"""

    def test_refs_expand_work_with_simple_case(self):
        """Test expanding a simple self-closing reference"""
        input_text = '<ref name="ref1">Full content</ref> Text <ref name="ref1"/>'
        expected = '<ref name="ref1">Full content</ref> Text <ref name="ref1">Full content</ref>'
        assert RefExpander().run(input_text) == expected

    def test_refs_expand_work_with_no_matching_ref(self):
        """Test when self-closing ref has no matching full ref"""
        input_text = '<ref name="ref1">Full content</ref> Text <ref name="ref2"/>'
        expected = '<ref name="ref1">Full content</ref> Text <ref name="ref2"/>'
        assert RefExpander().run(input_text) == expected

    def test_refs_expand_work_with_multiple_refs(self):
        """Test expanding multiple different references"""
        input_text = '<ref name="ref1">Content 1</ref> <ref name="ref2">Content 2</ref> Text <ref name="ref1"/> <ref name="ref2"/>'
        expected = '<ref name="ref1">Content 1</ref> <ref name="ref2">Content 2</ref> Text <ref name="ref1">Content 1</ref> <ref name="ref2">Content 2</ref>'
        assert RefExpander().run(input_text) == expected

    def test_refs_expand_work_with_alltext_parameter(self):
        """Test using separate source_text parameter for source of full refs"""
        first = 'Text <ref name="ref1"/>'
        source_text = '<ref name="ref1">Full content</ref>'
        expected = 'Text <ref name="ref1">Full content</ref>'
        assert RefExpander().run(first, source_text) == expected

    def test_refs_expand_work_with_empty_input(self):
        """Test with empty input string"""
        assert RefExpander().run("") == ""

    def test_refs_expand_work_with_no_refs(self):
        """Test with text that has no references"""
        input_text = "No references here"
        assert RefExpander().run(input_text) == input_text

    def test_refs_expand_work_preserves_original_formatting(self):
        """Test that original spacing in content is preserved"""
        input_text = '<ref name="ref1">  Full content  </ref> Text <ref name="ref1"/>'
        expected = '<ref name="ref1">  Full content  </ref> Text <ref name="ref1">  Full content  </ref>'
        assert RefExpander().run(input_text) == expected

    def test_refs_expand_work_with_special_characters(self):
        """Test with special characters in reference content"""
        input_text = '<ref name="ref1">Content with "quotes" & \'apostrophes\'</ref> Text <ref name="ref1"/>'
        expected = '<ref name="ref1">Content with "quotes" & \'apostrophes\'</ref> Text <ref name="ref1">Content with "quotes" & \'apostrophes\'</ref>'
        assert RefExpander().run(input_text) == expected

    def test_refs_expand_work_with_single_quotes_in_name(self):
        """Test with single quotes in ref name attribute"""
        input_text = "<ref name='ref1'>Full content</ref> Text <ref name='ref1'/>"
        expected = "<ref name='ref1'>Full content</ref> Text <ref name='ref1'>Full content</ref>"
        assert RefExpander().run(input_text) == expected

    def test_refs_expand_work_with_mixed_quotes(self):
        """Test with mixed quote styles in name attribute"""
        input_text = "<ref name=\"ref1\">Full content</ref> Text <ref name='ref1'/>"
        expected = '<ref name="ref1">Full content</ref> Text <ref name="ref1">Full content</ref>'
        assert RefExpander().run(input_text) == expected

    def test_refs_expand_work_multiple_same_refs(self):
        """Test multiple self-closing refs with same name"""
        input_text = '<ref name="ref1">Content</ref> A <ref name="ref1"/> B <ref name="ref1"/>'
        expected = '<ref name="ref1">Content</ref> A <ref name="ref1">Content</ref> B <ref name="ref1">Content</ref>'
        assert RefExpander().run(input_text) == expected


class TestExpendRefsWithNameAndGroup:
    """
    Tests for the `group` attribute.
    A self-closing ref is expanded only when BOTH name and group match
    the full ref, regardless of attribute order or quote style.
    """

    # ------------------------------------------------------------------
    # result == input_text

    def test_refs_not_expand_with_same_name_but_different_group(self):
        """Do not expand when the name matches but the group differs"""
        input_text = '<ref name="ref1" group="g1">Content</ref> Text <ref name="ref1" group="g2"/>'
        assert RefExpander().run(input_text) == input_text

    def test_refs_not_expand_when_only_self_closing_has_group(self):
        """Do not expand when the full ref has no group but the self-closing one does"""
        input_text = '<ref name="ref1">Content</ref> Text <ref name="ref1" group="g1"/>'
        assert RefExpander().run(input_text) == input_text

    def test_refs_not_expand_when_only_full_ref_has_group(self):
        """Do not expand when the full ref has a group but the self-closing one does not"""
        input_text = '<ref name="ref1" group="g1">Content</ref> Text <ref name="ref1"/>'
        assert RefExpander().run(input_text) == input_text

    def test_refs_not_expand_with_different_name_and_same_group(self):
        """Do not expand when the group matches but the name differs"""
        input_text = '<ref name="ref1" group="g1">Content</ref> Text <ref name="ref2" group="g1"/>'
        assert RefExpander().run(input_text) == input_text

    def test_refs_not_expand_with_mixed_quotes_and_different_group(self):
        """Do not expand with different quote styles when the group values differ"""
        input_text = "<ref name=\"ref1\" group=\"g1\">Content</ref> Text <ref name='ref1' group='g2'/>"
        assert RefExpander().run(input_text) == input_text

    # ------------------------------------------------------------------
    # result changed

    def test_refs_expand_with_same_name_and_same_group(self):
        """Expand when both name and group match"""
        input_text = '<ref name="ref1" group="g1">Content</ref> Text <ref name="ref1" group="g1"/>'
        expected = '<ref name="ref1" group="g1">Content</ref> Text <ref name="ref1" group="g1">Content</ref>'
        assert RefExpander().run(input_text) == expected

    def test_refs_expand_with_different_attribute_order(self):
        """Expand when the attribute order differs between the full and self-closing refs"""
        input_text = '<ref group="g1" name="ref1">Content</ref> Text <ref name="ref1" group="g1"/>'
        expected = '<ref group="g1" name="ref1">Content</ref> Text <ref group="g1" name="ref1">Content</ref>'
        assert RefExpander().run(input_text) == expected

    def test_refs_expand_with_reversed_attribute_order_on_self_closing(self):
        """Expand when only the self-closing ref has group before name"""
        input_text = '<ref name="ref1" group="g1">Content</ref> Text <ref group="g1" name="ref1"/>'
        expected = '<ref name="ref1" group="g1">Content</ref> Text <ref name="ref1" group="g1">Content</ref>'
        assert RefExpander().run(input_text) == expected

    def test_refs_expand_with_single_quotes_for_name_and_group(self):
        """Expand when name and group both use single quotes"""
        input_text = "<ref name='ref1' group='g1'>Content</ref> Text <ref name='ref1' group='g1'/>"
        expected = "<ref name='ref1' group='g1'>Content</ref> Text <ref name='ref1' group='g1'>Content</ref>"
        assert RefExpander().run(input_text) == expected

    def test_refs_expand_with_mixed_quotes_for_name_and_group(self):
        """Expand when the quote styles differ between the full and self-closing refs"""
        input_text = "<ref name=\"ref1\" group=\"g1\">Content</ref> Text <ref name='ref1' group='g1'/>"
        expected = '<ref name="ref1" group="g1">Content</ref> Text <ref name="ref1" group="g1">Content</ref>'
        assert RefExpander().run(input_text) == expected

    def test_refs_expand_with_mixed_quotes_inside_the_same_tag(self):
        """Expand when name and group use different quote styles within one tag"""
        input_text = "<ref name=\"ref1\" group='g1'>Content</ref> Text <ref name='ref1' group=\"g1\"/>"
        expected = "<ref name=\"ref1\" group='g1'>Content</ref> Text <ref name=\"ref1\" group='g1'>Content</ref>"
        assert RefExpander().run(input_text) == expected

    def test_refs_expand_with_mixed_quotes_and_different_order(self):
        """Expand when both quote style and attribute order differ"""
        input_text = "<ref group=\"g1\" name=\"ref1\">Content</ref> Text <ref name='ref1' group='g1'/>"
        expected = '<ref group="g1" name="ref1">Content</ref> Text <ref group="g1" name="ref1">Content</ref>'
        assert RefExpander().run(input_text) == expected

    def test_refs_expand_same_name_in_different_groups_independently(self):
        """Each self-closing ref receives the content of the full ref in its own group"""
        input_text = (
            '<ref name="n" group="a">A</ref> <ref name="n" group="b">B</ref> '
            'Text <ref name="n" group="a"/> <ref name="n" group="b"/>'
        )
        expected = (
            '<ref name="n" group="a">A</ref> <ref name="n" group="b">B</ref> '
            'Text <ref name="n" group="a">A</ref> <ref name="n" group="b">B</ref>'
        )
        assert RefExpander().run(input_text) == expected

    def test_refs_expand_grouped_and_ungrouped_with_same_name_independently(self):
        """A ref without group and a ref with group sharing a name do not mix"""
        input_text = (
            '<ref name="n">Plain</ref> <ref name="n" group="g">Grouped</ref> '
            'Text <ref name="n"/> <ref name="n" group="g"/>'
        )
        expected = (
            '<ref name="n">Plain</ref> <ref name="n" group="g">Grouped</ref> '
            'Text <ref name="n">Plain</ref> <ref name="n" group="g">Grouped</ref>'
        )
        assert RefExpander().run(input_text) == expected

    def test_refs_expand_multiple_same_refs_with_group(self):
        """Multiple self-closing refs with the same name and group are all expanded"""
        input_text = (
            '<ref name="ref1" group="g1">Content</ref> A <ref name="ref1" group="g1"/> B <ref name="ref1" group="g1"/>'
        )
        expected = (
            '<ref name="ref1" group="g1">Content</ref> A '
            '<ref name="ref1" group="g1">Content</ref> B '
            '<ref name="ref1" group="g1">Content</ref>'
        )
        assert RefExpander().run(input_text) == expected

    def test_refs_expand_with_group_and_alltext_parameter(self):
        """Use source_text as the source of full refs when a group is present"""
        first = 'Text <ref name="ref1" group="g1"/>'
        source_text = '<ref name="ref1" group="g1">Full content</ref>'
        expected = 'Text <ref name="ref1" group="g1">Full content</ref>'
        assert RefExpander().run(first, source_text) == expected

    def test_refs_not_expand_with_group_mismatch_and_alltext_parameter(self):
        """Do not expand from source_text when the group differs"""
        first = 'Text <ref name="ref1" group="g2"/>'
        source_text = '<ref name="ref1" group="g1">Full content</ref>'
        assert RefExpander().run(first, source_text) == first
