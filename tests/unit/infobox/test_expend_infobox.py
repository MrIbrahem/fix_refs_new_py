"""Tests for infobox expansion (expend_infobox.py)

Converted from tests/infoboxes/infoboxTest.php and tests/infoboxes/infobox2Test.php.
Goal: 100% line + branch coverage of ``InfoboxExpander``.

Run with:
    pytest test_expend_infobox.py \
        --cov=src.fix_refs.infobox.expend_infobox --cov-branch --cov-report=term-missing
"""

import pytest
from src.fix_refs.infobox import expend_infobox as module
from src.fix_refs.infobox.expend_infobox import InfoboxExpander

# Five unique params -> qualifies as an infobox (threshold is "more than 4").
FIVE_PARAMS = "{{Infobox drug|a=1|b=2|c=3|d=4|e=5}}"


@pytest.fixture
def expander() -> InfoboxExpander:
    return InfoboxExpander()


# ----------------------------------------------------------------------
# do_comments
# ----------------------------------------------------------------------
class TestDoComments:
    """Test cases for section-comment formatting"""

    def test_do_comments(self, expander: InfoboxExpander) -> None:
        """Test do_comments function"""
        text = """Some text\n<!-- Legal data -->\nMore text\n<!-- Clinical data -->\nEnd"""
        result = expander.do_comments(text)
        # Comments should be reformatted with proper spacing
        assert "<!-- Legal data -->" in result
        assert "<!-- Clinical data -->" in result

    def test_do_comments_with_multiple_sections(self, expander: InfoboxExpander) -> None:
        """Test do_comments with various comment types"""
        text = """<!-- Names -->\n<!-- Clinical data -->\n<!-- Legal data -->\n<!-- Pharmacokinetic data -->\n<!-- Chemical and physical data -->"""
        result = expander.do_comments(text)
        # All comments should still be present
        assert "<!-- Names -->" in result
        assert "<!-- Clinical data -->" in result
        assert "<!-- Legal data -->" in result

    @pytest.mark.parametrize(
        "title",
        [
            "Monoclonal antibody data",
            "External links",
            "Name",
            "Names",
            "Clinical data",
            "Legal data",
            "Legal status",
            "Pharmacokinetic data",
            "Chemical and physical data",
            "Definition and medical uses",
            "Chemical data",
            "Identifiers",
            # Generic patterns
            "Foo data",
            "Foo bar data",
            "Foo bar baz data",
            "Foo status",
        ],
    )
    def test_each_known_title_gets_own_line(self, expander, title):
        result = expander.do_comments(f"x\n<!-- {title} -->\ny")
        assert result == f"x\n\n<!-- {title} -->\ny"

    def test_exact_spacing_collapses_surrounding_whitespace(self, expander: InfoboxExpander) -> None:
        result = expander.do_comments("x   \n\n  <!-- Legal data -->   \n\n\ny")
        assert result == "x\n\n<!-- Legal data -->\ny"

    def test_case_insensitive_and_case_preserved(self, expander: InfoboxExpander) -> None:
        result = expander.do_comments("x<!-- legal DATA -->y")
        assert result == "x\n\n<!-- legal DATA -->\ny"

    @pytest.mark.parametrize(
        "text",
        [
            "plain text without comments",
            "<!-- Something else -->",
            "",
        ],
    )
    def test_unknown_or_missing_comments_unchanged(self, expander, text):
        assert expander.do_comments(text) == text


# ----------------------------------------------------------------------
# _separate_title
# ----------------------------------------------------------------------
class TestSeparateTitle:
    def test_title_after_closing_brace_moves_to_new_paragraph(self):
        result = InfoboxExpander._separate_title("{{x}}'''Title''' is a drug", "Title")
        assert result == "{{x}}\n\n'''Title''' is a drug"

    def test_whitespace_between_brace_and_title_is_normalized(self):
        result = InfoboxExpander._separate_title("{{x}}\n'''Title''' is", "Title")
        assert result == "{{x}}\n\n'''Title''' is"

    def test_title_is_regex_escaped(self):
        result = InfoboxExpander._separate_title("{{x}}'''C++ (drug)'''", "C++ (drug)")
        assert result == "{{x}}\n\n'''C++ (drug)'''"

    def test_no_match_leaves_text_unchanged(self):
        text = "{{x}}'''Other''' is"
        assert InfoboxExpander._separate_title(text, "Title") == text


# ----------------------------------------------------------------------
# extract_text_before_triple_single_quote
# ----------------------------------------------------------------------
class TestExtractTextBeforeTripleSingleQuote:
    def test_stops_at_first_line_starting_with_triple_quote(self, expander: InfoboxExpander) -> None:
        text = "{{a}}\nmore\n'''Title''' rest\nlater"
        assert expander.extract_text_before_triple_single_quote(text) == "{{a}}\nmore\n"

    def test_triple_quote_on_first_line_returns_empty(self, expander: InfoboxExpander) -> None:
        assert expander.extract_text_before_triple_single_quote("'''Title''' x") == ""

    def test_no_matching_line_returns_whole_text(self, expander: InfoboxExpander) -> None:
        text = "line one\nline two"
        assert expander.extract_text_before_triple_single_quote(text) == text

    def test_triple_quote_mid_line_is_ignored(self, expander: InfoboxExpander) -> None:
        text = "x '''bold'''\ny"
        assert expander.extract_text_before_triple_single_quote(text) == text


# ----------------------------------------------------------------------
# extract_main_template
# ----------------------------------------------------------------------
class TestExtractMainTemplate:
    def test_returns_params_and_item(self, expander: InfoboxExpander) -> None:
        result = expander.extract_main_template(FIVE_PARAMS)
        assert result["item"] == FIVE_PARAMS
        assert result["params"] == {"a": "1", "b": "2", "c": "3", "d": "4", "e": "5"}

    def test_no_templates_returns_empty_dict(self, expander: InfoboxExpander) -> None:
        assert expander.extract_main_template("just text") == {}

    def test_four_params_is_below_threshold(self, expander: InfoboxExpander) -> None:
        assert expander.extract_main_template("{{x|a=1|b=2|c=3|d=4}}") == {}

    def test_template_after_bold_title_line_is_ignored(self, expander: InfoboxExpander) -> None:
        text = "'''Title''' is a drug.\n" + FIVE_PARAMS
        assert expander.extract_main_template(text) == {}

    def test_template_inside_ref_tag_is_skipped(self, expander: InfoboxExpander) -> None:
        text = "<ref>{{cite web|a=1|b=2|c=3|d=4|e=5}}</ref>"
        assert expander.extract_main_template(text) == {}

    def test_longest_template_wins_when_it_comes_second(self, expander: InfoboxExpander) -> None:
        short = "{{Short|a=1|b=2|c=3|d=4|e=5}}"
        long_ = "{{Longer name|a=1|b=2|c=3|d=4|e=5|f=6}}"
        result = expander.extract_main_template(f"{short}\n{long_}")
        assert result["item"] == long_

    def test_longest_template_wins_when_it_comes_first(self, expander: InfoboxExpander) -> None:
        short = "{{Short|a=1|b=2|c=3|d=4|e=5}}"
        long_ = "{{Longer name|a=1|b=2|c=3|d=4|e=5|f=6}}"
        result = expander.extract_main_template(f"{long_}\n{short}")
        assert result["item"] == long_

    def test_duplicate_param_names_later_value_wins(self, expander: InfoboxExpander) -> None:
        result = expander.extract_main_template("{{x|a=1|a=2|b=3|c=4|d=5|e=6}}")
        assert result["params"]["a"] == "2"

    def test_duplicate_names_count_once_towards_threshold(self, expander: InfoboxExpander) -> None:
        # 5 arguments but only 4 unique names
        assert expander.extract_main_template("{{x|a=1|a=2|b=3|c=4|d=5}}") == {}

    def test_nested_template_does_not_replace_outer(self, expander: InfoboxExpander) -> None:
        inner = "{{inner|p=1|q=2|r=3|s=4|t=5}}"
        text = f"{{{{outer|a=1|b=2|c=3|d=4|e={inner}}}}}"
        result = expander.extract_main_template(text)
        assert result["item"] == text
        assert result["params"]["e"] == inner


# ----------------------------------------------------------------------
# extract_lead_section
# ----------------------------------------------------------------------
class TestExtractLeadSection:
    def test_make_section_0(self):
        """Test extract_lead_section function"""
        text = "Some text before\n==Section==\nContent after"
        result = InfoboxExpander.extract_lead_section(text)
        assert result == "Some text before\n"

        # Test without sections
        text2 = "Just some text"
        result2 = InfoboxExpander.extract_lead_section(text2)
        assert result2 == text2

    def test_subsections_are_excluded(self):
        text = "lead\n==A==\nx\n===B===\ny"
        assert InfoboxExpander.extract_lead_section(text) == "lead\n"

    def test_empty_text(self):
        assert InfoboxExpander.extract_lead_section("") == ""


# ----------------------------------------------------------------------
# _expend_new
# ----------------------------------------------------------------------
class TestExpendNew:
    def test_expend_new_simple_template(self):
        """Test _expend_new with a simple template"""
        # Test with basic template
        result = InfoboxExpander()._expend_new("{{test}}")
        assert result == "{{test\n}}"

    def test_named_params_are_aligned_one_per_line(self, expander: InfoboxExpander) -> None:
        result = expander._expend_new("{{Infobox drug|name=Test|a=1}}")
        assert result.startswith("{{Infobox drug\n|name")
        assert result.endswith("\n}}")
        assert "|name" + " " * 13 + "=Test\n" in result
        assert "|a" + " " * 16 + "=1\n" in result

    def test_positional_params_are_not_padded(self, expander: InfoboxExpander) -> None:
        result = expander._expend_new("{{t|one|two}}")
        assert result == "{{t\n|one\n|two\n}}"

    def test_trailing_whitespace_in_values_is_trimmed(self, expander: InfoboxExpander) -> None:
        result = expander._expend_new("{{t|a=x   \n}}")
        assert "|a" + " " * 16 + "=x\n}}" in result

    def test_only_whole_template_is_expanded(self, expander: InfoboxExpander) -> None:
        # Two sibling templates: neither equals the whole input, so no change.
        text = "{{a}} {{b}}"
        assert expander._expend_new(text) == text

    def test_section_comments_are_put_on_their_own_line(self, expander: InfoboxExpander) -> None:
        result = expander._expend_new("{{Infobox drug|a=1<!-- Legal data -->|b=2}}")
        assert "\n\n<!-- Legal data -->\n" in result


# ----------------------------------------------------------------------
# expand_infobox_in_text
# ----------------------------------------------------------------------
class TestExpandInfoboxInText:
    def test_expend_infobox_basic(self):
        """Test expend_infobox with basic infobox"""
        text = """{{Infobox drug|name=Test}}\nSome content"""
        result = InfoboxExpander().expand_infobox_in_text(text, "TestPage")
        assert isinstance(result, str)
        assert len(result) > 0
        # Only one param -> not a main infobox -> text is returned as is
        assert result == text

    def test_no_infobox_only_fixes_title_spacing(self, expander: InfoboxExpander) -> None:
        text = "{{short|a=1}}'''Title''' is a drug."
        result = expander.expand_infobox_in_text(text, "Title")
        assert result == "{{short|a=1}}\n\n'''Title''' is a drug."

    def test_full_expansion(self, expander: InfoboxExpander) -> None:
        text = "{{Infobox drug|name=Test|a=1|b=2|c=3|d=4}}'''Test''' is a drug.\n\n==Section==\nBody"
        result = expander.expand_infobox_in_text(text, "Test")

        assert result.startswith("{{Infobox drug\n|name")
        assert "|name" + " " * 13 + "=Test\n" in result
        assert "|d" + " " * 16 + "=4\n}}\n\n'''Test''' is a drug." in result
        assert result.endswith("==Section==\nBody")

    def test_bold_phrase_not_matching_title_gets_newline_after_infobox(self, expander: InfoboxExpander) -> None:
        # Title mismatch -> _separate_title does nothing, so the final
        # replace() must insert the newline between "}}" and "'''".
        text = "{{Infobox drug|name=Test|a=1|b=2|c=3|d=4}}'''Other''' is a drug."
        result = expander.expand_infobox_in_text(text, "Test")
        assert "\n}}\n'''Other''' is a drug." in result

    def test_already_expanded_infobox_is_returned_unchanged(self, expander: InfoboxExpander) -> None:
        text = "{{Infobox drug\n|name             =Test\n|a                =1\n|b                =2\n|c                =3\n|d                =4\n}}\n\n'''Test''' is a drug."
        assert expander.expand_infobox_in_text(text, "Test") == text

    def test_infobox_after_triple_single_quote(self, expander: InfoboxExpander) -> None:
        text = "'''Test''' is a drug.\n\n{{Infobox drug|name=Test|a=1|b=2|c=3|d=4}}"
        assert expander.expand_infobox_in_text(text, "Test") == text


def test_module_exports():
    assert module.__all__ == ["InfoboxExpander"]
