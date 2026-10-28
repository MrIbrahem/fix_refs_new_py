"""
Unit tests for wtp_mapping module.
"""

from pathlib import Path

import wikitextparser as wtp

from src.fix_refs.parsers.wtp_mapping import WtpRefs, WtpRef


class TestWtpRef:
    def test_basic(self):
        text = "<ref name = PI2022></ref>"
        result = WtpRef.from_text(text)
        assert result.name == "PI2022"
        assert result.is_self_closing() is True

    def test_for_bug(self):
        """
        BUG: WtpRef.from_text("<ref name = PI2022/>").name == "PI2022/" this should be fixed in WtpRef to become "PI2022"
        This bug already solved in wikitextparser>0.55
        """
        wtp_tag = wtp.Tag("<ref name = PI2022/>")
        # assert wtp_tag.attrs["name"] == "PI2022/"
        assert wtp_tag.attrs["name"] == "PI2022"

        wtp_tag = wtp.Tag("<ref name=PI2022/>")
        # this should be fixed in WtpRef to become "PI2022"
        # assert wtp_tag.attrs["name"] == "PI2022/"
        assert wtp_tag.attrs["name"] == "PI2022"


class TestGetAllRefs:
    """Tests for WtpRefs.load(text).all_refs function"""

    def test_single_full_ref_no_name(self):
        text = "Some text<ref>A basic citation</ref> more text"
        result = WtpRefs.load(text).all_refs

        assert len(result) == 1
        assert result[0].contents == "A basic citation"
        assert result[0].tag_str == "<ref>A basic citation</ref>"
        assert result[0].name == ""

    def test_single_full_ref_with_name(self):
        text = '<ref name="smith2020">Smith, J. (2020)</ref>'
        result = WtpRefs.load(text).all_refs

        assert len(result) == 1
        assert result[0].contents == "Smith, J. (2020)"
        assert result[0].name == "smith2020"
        assert result[0].attrs["name"] == "smith2020"
        assert result[0].tag_str == text

    def test_multiple_full_refs(self):
        text = "Text<ref>First</ref> more<ref>Second</ref>"
        result = WtpRefs.load(text).all_refs

        assert len(result) == 2
        assert result[0].contents == "First"
        assert result[1].contents == "Second"

    def test_multiple_named_refs_with_text_between(self):
        text = '<ref name="ref1">Content 1</ref> Text <ref name="ref2">Content 2</ref>'
        result = WtpRefs.load(text).all_refs

        assert len(result) == 2
        assert [c.name for c in result] == ["ref1", "ref2"]
        assert [c.contents for c in result] == ["Content 1", "Content 2"]
        assert result[0].tag_str == '<ref name="ref1">Content 1</ref>'

    def test_not_excludes_self_closing_refs(self):
        text = 'Text<ref name="a">Full ref</ref> and<ref name="a" /> a short ref'
        result = WtpRefs.load(text).all_refs

        assert len(result) == 2
        assert result[0].contents == "Full ref"
        assert result[0].name == "a"

    def test_no_refs_returns_empty_list(self):
        result = WtpRefs.load("Just some plain text without any refs").all_refs

        assert result == []

    def test_empty_text_returns_empty_list(self):
        result = WtpRefs.load("").all_refs

        assert result == []

    def test_ref_with_extra_attributes(self):
        text = '<ref name="foo" group="note">Some content</ref>'
        result = WtpRefs.load(text).all_refs

        assert len(result) == 1
        assert result[0].name == "foo"
        assert result[0].attrs["name"] == "foo"
        assert result[0].attrs["group"] == "note"

    def test_ref_name_is_stripped(self):
        text = '<ref name=" spaced ">Content</ref>'
        result = WtpRefs.load(text).all_refs

        assert len(result) == 1
        assert result[0].name == "spaced"

    def test_nested_markup_inside_ref(self):
        text = "<ref>See [[Some Page|the page]] for {{cite web|url=example.com}} details</ref>"
        result = WtpRefs.load(text).all_refs

        assert len(result) == 1
        assert "[[Some Page|the page]]" in result[0].contents
        assert "{{cite web|url=example.com}}" in result[0].contents

    def test_multiline_ref_content(self):
        text = "<ref>Line one\nLine two\nLine three</ref>"
        result = WtpRefs.load(text).all_refs

        assert len(result) == 1
        assert result[0].contents == "Line one\nLine two\nLine three"

    def test_duplicate_names_both_returned(self):
        text = '<ref name="dup">First</ref> text <ref name="dup">Second</ref>'
        result = WtpRefs.load(text).all_refs

        assert len(result) == 2
        assert [c.contents for c in result] == ["First", "Second"]
        assert all(c.name == "dup" for c in result)


class TestGetShortRefs:
    """Tests for WtpRefs.load(text).short_refs function"""

    def test_single_short_ref(self):
        text = '<ref name="smith2020" />'
        result = WtpRefs.load(text).short_refs

        assert len(result) == 1
        assert result[0].name == "smith2020"
        assert result[0].contents == ""
        assert result[0].tag_str == '<ref name="smith2020" />'

    def test_multiple_short_refs(self):
        # Mixes the "/>" and " />" self-closing styles
        text = 'Text<ref name="a"/> more<ref name="b" />'
        result = WtpRefs.load(text).short_refs

        assert len(result) == 2
        assert {c.name for c in result} == {"a", "b"}
        assert all(c.contents == "" for c in result)

    def test_excludes_full_refs(self):
        text = '<ref name="full">Full content</ref><ref name="short" />'
        result = WtpRefs.load(text).short_refs

        assert len(result) == 1
        assert result[0].name == "short"

    def test_no_refs_returns_empty_list(self):
        result = WtpRefs.load("No refs in this text").short_refs

        assert result == []

    def test_empty_text_returns_empty_list(self):
        result = WtpRefs.load("").short_refs

        assert result == []

    def test_short_ref_without_name(self):
        text = "<ref />"
        result = WtpRefs.load(text).short_refs

        assert len(result) == 1
        assert result[0].name == ""
        assert result[0].contents == ""

    def test_short_ref_name_is_stripped(self):
        text = '<ref name=" spaced " />'
        result = WtpRefs.load(text).short_refs

        assert len(result) == 1
        assert result[0].name == "spaced"

    def test_short_ref_with_extra_attributes(self):
        text = '<ref name="foo" group="note" />'
        result = WtpRefs.load(text).short_refs

        assert len(result) == 1
        assert result[0].attrs["name"] == "foo"
        assert result[0].attrs["group"] == "note"

    def test_no_space_before_self_close(self):
        text = '<ref name="tight"/>'
        result = WtpRefs.load(text).short_refs

        assert len(result) == 1
        assert result[0].name == "tight"
        assert result[0].tag_str == '<ref name="tight"/>'


def get_full_refs_str(text: str) -> dict[str, str]:
    # return WtpRefs.load(text).full_refs_str
    return {x.name: x.tag_str for x in WtpRefs.load(text).full_refs}


class TestGetFullRefs:
    """Tests for get_full_refs_str function"""

    def test_single_named_ref(self):
        text = '<ref name="smith2020">Smith, J. (2020)</ref>'
        result = get_full_refs_str(text)

        assert result == {"smith2020": '<ref name="smith2020">Smith, J. (2020)</ref>'}

    def test_multiple_named_refs(self):
        text = '<ref name="a">First</ref> text <ref name="b">Second</ref>'
        result = get_full_refs_str(text)

        assert set(result.keys()) == {"a", "b"}
        assert result["a"] == '<ref name="a">First</ref>'
        assert result["b"] == '<ref name="b">Second</ref>'

    def test_unnamed_refs_excluded(self):
        text = '<ref>No name here</ref><ref name="named">Has name</ref>'
        result = get_full_refs_str(text)

        assert list(result.keys()) == ["named"], f"Unexpected keys: {list(result.keys())}"

    def test_self_closing_refs_excluded(self):
        text = '<ref name="full">Full ref</ref><ref name="short" />'
        result = get_full_refs_str(text)

        assert list(result.keys()) == ["full"], f"Unexpected keys: {list(result.keys())}"

    def test_short_ref_before_full_ref_with_same_name(self):
        # A short ref appearing first must not shadow the full definition
        text = '<ref name="ref2"/><ref name="ref1">Content 1</ref> <ref name="ref2">Content 2</ref>'
        result = get_full_refs_str(text)

        assert len(result) == 2
        assert result["ref1"] == '<ref name="ref1">Content 1</ref>'
        assert result["ref2"] == '<ref name="ref2">Content 2</ref>'

    def test_only_short_refs_returns_empty_dict(self):
        result = get_full_refs_str('<ref name="ref2"/>')

        assert result == {}

    def test_no_refs_returns_empty_dict(self):
        result = get_full_refs_str("Plain text, no refs at all")

        assert result == {}

    def test_empty_text_returns_empty_dict(self):
        result = get_full_refs_str("")

        assert result == {}

    def test_duplicate_names_last_occurrence_wins(self):
        text = '<ref name="dup">First</ref> text <ref name="dup">Second</ref>'
        result = get_full_refs_str(text)

        assert result == {"dup": '<ref name="dup">Second</ref>'}


class TestGetShortAndFullRefs:
    def load_fixture(self, name: str) -> str:
        path = Path(__file__).parent / "data" / name
        assert path.exists(), f"Fixture file missing: {path}"

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        assert content is not None, f"Unable to read fixture file: {path}"
        return content

    def test_refs(self) -> None:
        source = self.load_fixture("source-1.wiki")

        full_refs = {x.name: x.tag_str for x in WtpRefs.load(source).full_refs}

        assert set(full_refs.keys()) == {
            "",
            "AHFS2022",
            "BNF81",
            "EMA",
            "EMC",
            "EPAR2022",
            "Lin",
            "MSR",
            "Minkovsky",
            "PI2022",
            "TGA",
            "WHO22nd",
        }

        short_refs = WtpRefs.load(source).short_refs
        short_refs_by_name = {x.name: x for x in short_refs}

        assert set(short_refs_by_name.keys()) == {
            "AHFS2022",
            "BNF81",
            "EMA",
            "EMC",
            "EPAR2022",
            "Lin",
            "Minkovsky",
            "PI2022",
            "TGA",
            "not_exists_ref_should_be_deleted",
        }

        assert len(full_refs) == 11, f"Unexpected number of full refs: {len(full_refs)}"
        assert len(short_refs) == 22, f"Unexpected number of short refs: {len(short_refs)}"

        assert len(set(full_refs.keys())) == 11, f"Unexpected number of unique full refs: {len(full_refs)}"
