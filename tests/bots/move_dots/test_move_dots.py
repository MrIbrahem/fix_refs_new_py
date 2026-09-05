"""Tests for move_dots (move_dots.py)

Converted from tests/mv_dots_afterTest.php and tests/mv_dots_beforeTest.php
"""


from fix_refs.bots.move_dots import move_dots_after_refs


def test_move_dots_after_single_dot():
    input_text = "This is a sentence。<ref>Reference 1</ref>"
    expected = "This is a sentence<ref>Reference 1</ref>。"
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_multiple_dots():
    input_text = "First sentence. Second sentence.<ref>Reference 1</ref>"
    expected = "First sentence. Second sentence<ref>Reference 1</ref>."
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_multiple_refs():
    input_text = "Text।<ref>Ref1</ref><ref>Ref2</ref>"
    expected = "Text<ref>Ref1</ref><ref>Ref2</ref>।"
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_no_dot():
    input_text = "Text<ref>Reference</ref>"
    expected = "Text<ref>Reference</ref>"
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_different_punctuation():
    input_text = "Text, <ref>Reference</ref>"
    expected = "Text<ref>Reference</ref>,"
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_with_whitespace():
    input_text = "Text.  <ref>Reference</ref>"
    expected = "Text<ref>Reference</ref>."
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after__closing_ref():
    input_text = 'Text.<ref name="ref1" />'
    expected = 'Text<ref name="ref1" />.'
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_multiple_refs_with_whitespace():
    input_text = "Text. <ref>Ref1</ref> <ref>Ref2</ref>"
    expected = "Text<ref>Ref1</ref> <ref>Ref2</ref>."
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_not_before_refs():
    input_text = "This is a sentence. This is another sentence<ref>Reference</ref>"
    expected = "This is a sentence. This is another sentence<ref>Reference</ref>"
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_multiple_punctuation():
    input_text = "Text.,<ref>Reference</ref>"
    expected = "Text<ref>Reference</ref>.,"
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_empty_text():
    assert move_dots_after_refs("", "en") == ""


def test_move_dots_after_no_references():
    input_text = "This is a sentence."
    expected = "This is a sentence."
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_complex_refs():
    input_text = 'Text.<ref name="ref1" group="group1">Reference content</ref>'
    expected = 'Text<ref name="ref1" group="group1">Reference content</ref>.'
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_nested_tags():
    input_text = "Text.<ref>Reference with <i>italic</i> text</ref>"
    expected = "Text<ref>Reference with <i>italic</i> text</ref>."
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_chinese_punctuation():
    input_text = "这是句子。<ref>参考文献1</ref>"
    expected = "这是句子<ref>参考文献1</ref>。"
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_devanagari_punctuation():
    input_text = "यह वाक्य है।<ref>संदर्भ 1</ref>"
    expected = "यह वाक्य है<ref>संदर्भ 1</ref>।"
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_armenian_multiple_punctuation():
    input_text = "Տեքստ.,<ref>Հղում</ref>"
    expected = "Տեքստ<ref>Հղում</ref>.,"
    assert move_dots_after_refs(input_text, "hy") == expected


def test_move_dots_at_end_of_text():
    input_text = "Text.<ref>Reference</ref>"
    expected = "Text<ref>Reference</ref>."
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_multiple_instances():
    input_text = "First sentence.<ref>Ref1</ref> Second sentence.<ref>Ref2</ref>"
    expected = "First sentence<ref>Ref1</ref>. Second sentence<ref>Ref2</ref>."
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_only_punctuation():
    input_text = ".<ref>Reference</ref>"
    expected = "<ref>Reference</ref>."
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_dot_with_space():
    input_text = "Text. <ref>Reference</ref>"
    expected = "Text<ref>Reference</ref>."
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_comma_with_space():
    input_text = "Text, <ref>Reference</ref>"
    expected = "Text<ref>Reference</ref>,"
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_dot_no_space():
    input_text = "Text.<ref>Reference</ref>"
    expected = "Text<ref>Reference</ref>."
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_comma_no_space():
    input_text = "Text,<ref>Reference</ref>"
    expected = "Text<ref>Reference</ref>,"
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_dot_with_multiple_refs():
    input_text = "Text.<ref>Ref1</ref><ref>Ref2</ref>"
    expected = "Text<ref>Ref1</ref><ref>Ref2</ref>."
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_dot_with_multiple_refs_and_spaces():
    input_text = "Text. <ref>Ref1</ref> <ref>Ref2</ref>"
    expected = "Text<ref>Ref1</ref> <ref>Ref2</ref>."
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_dot_with_multiple_refs_and_spaces_and_text():
    input_text = "Text. Some text <ref>Ref1</ref> More text <ref>Ref2</ref>"
    expected = "Text. Some text <ref>Ref1</ref> More text <ref>Ref2</ref>"
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_dot_with_multiple_refs_and_spaces_and_text_and_dot():
    input_text = "Text. Some text. <ref>Ref1</ref> More text. <ref>Ref2</ref>"
    expected = "Text. Some text<ref>Ref1</ref>. More text<ref>Ref2</ref>."
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_dot_with_multiple_refs_and_spaces_and_text_and_dot_and_comma():
    input_text = "Text, Some text. <ref>Ref1</ref> More text, <ref>Ref2</ref>"
    expected = "Text, Some text<ref>Ref1</ref>. More text<ref>Ref2</ref>,"
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_dot_with_multiple_refs_and_spaces_and_text_and_dot_and_comma_and_dot():
    input_text = "Text. Some text, <ref>Ref1</ref> More text. <ref>Ref2</ref>"
    expected = "Text. Some text<ref>Ref1</ref>, More text<ref>Ref2</ref>."
    assert move_dots_after_refs(input_text, "en") == expected


def test_move_dots_after_hy():
    input_text = 'Հետծննդյան հոգեբանական խանգարումը հանդիպում է 1000 ծննդաբերությունից 1-2-ի մոտ։ <ref name="Os2018" /><ref name="Li2018" /> Տարբեր [[Մշակույթ|մշակույթներում]] և [[Դասակարգային կառուցվածք|սոցիալական դասերում]] գները նման են թվում։ <ref name="Luc2021" /> Ավելի հաճախ այն հանդիպում է հայտնի կամ նոր սկսվող երկբևեռ խանգարման համատեքստում, որը հայտնի է որպես հետծննդյան երկբևեռ խանգարում : <ref name="Luc2021" /> Այս վիճակը նկարագրվել է դեռևս մ.թ.ա. 400 թվականից [[Հիպոկրատ|Հիպոկրատի]] կողմից ։ <ref name="Os2018" />\r\n\r\n== test =="'
    expected = 'Հետծննդյան հոգեբանական խանգարումը հանդիպում է 1000 ծննդաբերությունից 1-2-ի մոտ<ref name="Os2018" /><ref name="Li2018" />։ Տարբեր [[Մշակույթ|մշակույթներում]] և [[Դասակարգային կառուցվածք|սոցիալական դասերում]] գները նման են թվում<ref name="Luc2021" />։ Ավելի հաճախ այն հանդիպում է հայտնի կամ նոր սկսվող երկբևեռ խանգարման համատեքստում, որը հայտնի է որպես հետծննդյան երկբևեռ խանգարում <ref name="Luc2021" />: Այս վիճակը նկարագրվել է դեռևս մ.թ.ա. 400 թվականից [[Հիպոկրատ|Հիպոկրատի]] կողմից <ref name="Os2018" />։\r\n\r\n== test =="'
    assert move_dots_after_refs(input_text, "hy") == expected


def test_part1():
    input_text = '[[Category:Translated from MDWiki]] ռետինոիդներ. <ref name="NORD2006" /><ref name="Gli2017" />'
    expected = '[[Category:Translated from MDWiki]] ռետինոիդներ<ref name="NORD2006" /><ref name="Gli2017" />.'
    assert move_dots_after_refs(input_text, "hy") == expected


def test_part2():
    input_text = '[[Category:Translated from MDWiki]] ռետինոիդներ, <ref name="NORD2006" /><ref name="Gli2017" />'
    expected = '[[Category:Translated from MDWiki]] ռետինոիդներ<ref name="NORD2006" /><ref name="Gli2017" />,'
    assert move_dots_after_refs(input_text, "hy") == expected


def test_part5():
    input_text = """text part 1 <ref name="NIH2016" />։ text part 2: <ref name="AFP2013">{{Cite journal|last=Iser|first=D|last2=Ryan|first2=M|title=Fatty liver disease—a practical guide for GPs.|journal=Australian Family Physician|date=July 2013|volume=42|issue=7|pages=444–7|pmid=23826593}}</ref><ref name="NIH2016" /> some text [[links|label]] other [[text]] <small>text</small> <ref name="Ant2019" /><ref name="NIH2016" />։ hello!! [[2020|hi]] և [[Հեպատիտ C|հեպատիտ C-ն]] : <ref name="NIH2016" /> random texts: <ref name="NIH2016" /> last part <ref name="NIH2016" />։"""
    expected = """text part 1 <ref name="NIH2016" />։ text part 2<ref name="AFP2013">{{Cite journal|last=Iser|first=D|last2=Ryan|first2=M|title=Fatty liver disease—a practical guide for GPs.|journal=Australian Family Physician|date=July 2013|volume=42|issue=7|pages=444–7|pmid=23826593}}</ref><ref name="NIH2016" />: some text [[links|label]] other [[text]] <small>text</small> <ref name="Ant2019" /><ref name="NIH2016" />։ hello!! [[2020|hi]] և [[Հեպատիտ C|հեպատիտ C-ն]] <ref name="NIH2016" />: random texts<ref name="NIH2016" />: last part <ref name="NIH2016" />։"""
    assert move_dots_after_refs(input_text, "hy") == expected
