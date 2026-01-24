"""Tests for move_dots (move_dots.py)

Converted from tests/mv_dots_afterTest.php and tests/mv_dots_beforeTest.php
"""
import pytest
from src.bots.move_dots import move_dots_after_refs


class TestMoveDotsAfter:
    """Test cases for moving dots after references"""

    def test_move_dots_after_single_dot(self):
        input_text = "This is a sentence。<ref>Reference 1</ref>"
        expected = "This is a sentence<ref>Reference 1</ref>。"
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_multiple_dots(self):
        input_text = "First sentence. Second sentence.<ref>Reference 1</ref>"
        expected = "First sentence. Second sentence<ref>Reference 1</ref>."
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_multiple_refs(self):
        input_text = "Text।<ref>Ref1</ref><ref>Ref2</ref>"
        expected = "Text<ref>Ref1</ref><ref>Ref2</ref>।"
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_no_dot(self):
        input_text = "Text<ref>Reference</ref>"
        expected = "Text<ref>Reference</ref>"
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_different_punctuation(self):
        input_text = "Text, <ref>Reference</ref>"
        expected = "Text<ref>Reference</ref>,"
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_with_whitespace(self):
        input_text = "Text.  <ref>Reference</ref>"
        expected = "Text<ref>Reference</ref>."
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_self_closing_ref(self):
        input_text = "Text.<ref name=\"ref1\" />"
        expected = "Text<ref name=\"ref1\" />."
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_multiple_refs_with_whitespace(self):
        input_text = "Text. <ref>Ref1</ref> <ref>Ref2</ref>"
        expected = "Text<ref>Ref1</ref> <ref>Ref2</ref>."
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_not_before_refs(self):
        input_text = "This is a sentence. This is another sentence<ref>Reference</ref>"
        expected = "This is a sentence. This is another sentence<ref>Reference</ref>"
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_multiple_punctuation(self):
        input_text = "Text.,<ref>Reference</ref>"
        expected = "Text<ref>Reference</ref>.,"
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_empty_text(self):
        assert move_dots_after_refs("", 'en') == ""

    def test_move_dots_after_no_references(self):
        input_text = "This is a sentence."
        expected = "This is a sentence."
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_complex_refs(self):
        input_text = "Text.<ref name=\"ref1\" group=\"group1\">Reference content</ref>"
        expected = "Text<ref name=\"ref1\" group=\"group1\">Reference content</ref>."
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_nested_tags(self):
        input_text = "Text.<ref>Reference with <i>italic</i> text</ref>"
        expected = "Text<ref>Reference with <i>italic</i> text</ref>."
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_chinese_punctuation(self):
        input_text = "这是句子。<ref>参考文献1</ref>"
        expected = "这是句子<ref>参考文献1</ref>。"
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_devanagari_punctuation(self):
        input_text = "यह वाक्य है।<ref>संदर्भ 1</ref>"
        expected = "यह वाक्य है<ref>संदर्भ 1</ref>।"
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_armenian_multiple_punctuation(self):
        input_text = "Տեքստ.,<ref>Հղում</ref>"
        expected = "Տեքստ<ref>Հղում</ref>.,"
        assert move_dots_after_refs(input_text, 'hy') == expected

    def test_move_dots_at_end_of_text(self):
        input_text = "Text.<ref>Reference</ref>"
        expected = "Text<ref>Reference</ref>."
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_multiple_instances(self):
        input_text = "First sentence.<ref>Ref1</ref> Second sentence.<ref>Ref2</ref>"
        expected = "First sentence<ref>Ref1</ref>. Second sentence<ref>Ref2</ref>."
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_only_punctuation(self):
        input_text = ".<ref>Reference</ref>"
        expected = "<ref>Reference</ref>."
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_dot_with_space(self):
        input_text = "Text. <ref>Reference</ref>"
        expected = "Text<ref>Reference</ref>."
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_comma_with_space(self):
        input_text = "Text, <ref>Reference</ref>"
        expected = "Text<ref>Reference</ref>,"
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_dot_no_space(self):
        input_text = "Text.<ref>Reference</ref>"
        expected = "Text<ref>Reference</ref>."
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_comma_no_space(self):
        input_text = "Text,<ref>Reference</ref>"
        expected = "Text<ref>Reference</ref>,"
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_dot_with_multiple_refs(self):
        input_text = "Text.<ref>Ref1</ref><ref>Ref2</ref>"
        expected = "Text<ref>Ref1</ref><ref>Ref2</ref>."
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_dot_with_multiple_refs_and_spaces(self):
        input_text = "Text. <ref>Ref1</ref> <ref>Ref2</ref>"
        expected = "Text<ref>Ref1</ref> <ref>Ref2</ref>."
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_dot_with_multiple_refs_and_spaces_and_text(self):
        input_text = "Text. Some text <ref>Ref1</ref> More text <ref>Ref2</ref>"
        expected = "Text. Some text <ref>Ref1</ref> More text <ref>Ref2</ref>"
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_dot_with_multiple_refs_and_spaces_and_text_and_dot(self):
        input_text = "Text. Some text. <ref>Ref1</ref> More text. <ref>Ref2</ref>"
        expected = "Text. Some text<ref>Ref1</ref>. More text<ref>Ref2</ref>."
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_dot_with_multiple_refs_and_spaces_and_text_and_dot_and_comma(self):
        input_text = "Text, Some text. <ref>Ref1</ref> More text, <ref>Ref2</ref>"
        expected = "Text, Some text<ref>Ref1</ref>. More text<ref>Ref2</ref>,"
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_dot_with_multiple_refs_and_spaces_and_text_and_dot_and_comma_and_dot(self):
        input_text = "Text. Some text, <ref>Ref1</ref> More text. <ref>Ref2</ref>"
        expected = "Text. Some text<ref>Ref1</ref>, More text<ref>Ref2</ref>."
        assert move_dots_after_refs(input_text, 'en') == expected

    def test_move_dots_after_hy(self):
        input_text = 'Հետծննդյան հոգեբանական խանգարումը հանդիպում է 1000 ծննդաբերությունից 1-2-ի մոտ։ <ref name="Os2018" /><ref name="Li2018" /> Տարբեր [[Մշակույթ|մշակույթներում]] և [[Դասակարգային կառուցվածք|սոցիալական դասերում]] գները նման են թվում։ <ref name="Luc2021" /> Ավելի հաճախ այն հանդիպում է հայտնի կամ նոր սկսվող երկբևեռ խանգարման համատեքստում, որը հայտնի է որպես հետծննդյան երկբևեռ խանգարում : <ref name="Luc2021" /> Այս վիճակը նկարագրվել է դեռևս մ.թ.ա. 400 թվականից [[Հիպոկրատ|Հիպոկրատի]] կողմից ։ <ref name="Os2018" />\r\n\r\n== test =="'
        expected = 'Հետծննդյան հոգեբանական խանգարումը հանդիպում է 1000 ծննդաբերությունից 1-2-ի մոտ<ref name="Os2018" /><ref name="Li2018" />։ Տարբեր [[Մշակույթ|մշակույթներում]] և [[Դասակարգային կառուցվածք|սոցիալական դասերում]] գները նման են թվում<ref name="Luc2021" />։ Ավելի հաճախ այն հանդիպում է հայտնի կամ նոր սկսվող երկբևեռ խանգարման համատեքստում, որը հայտնի է որպես հետծննդյան երկբևեռ խանգարում <ref name="Luc2021" />: Այս վիճակը նկարագրվել է դեռևս մ.թ.ա. 400 թվականից [[Հիպոկրատ|Հիպոկրատի]] կողմից <ref name="Os2018" />։\r\n\r\n== test =="'
        assert move_dots_after_refs(input_text, 'hy') == expected

    def test_part1(self):
        input_text = '[[Category:Translated from MDWiki]] ռետինոիդներ. <ref name="NORD2006" /><ref name="Gli2017" />'
        expected = '[[Category:Translated from MDWiki]] ռետինոիդներ<ref name="NORD2006" /><ref name="Gli2017" />.'
        assert move_dots_after_refs(input_text, 'hy') == expected

    def test_part2(self):
        input_text = '[[Category:Translated from MDWiki]] ռետինոիդներ, <ref name="NORD2006" /><ref name="Gli2017" />'
        expected = '[[Category:Translated from MDWiki]] ռետինոիդներ<ref name="NORD2006" /><ref name="Gli2017" />,'
        assert move_dots_after_refs(input_text, 'hy') == expected
