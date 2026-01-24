"""Tests for remove_space2 (remove_space2Test.php)

Converted from tests/remove_space2Test.php
"""
import pytest
from src.lang_bots.hy_bot import remove_spaces_between_ref_and_punctuation


class TestRemoveSpace2Extra:
    """Extra test cases for remove_space2"""

    def test_ref_no_punctuation_after(self):
        """Test with ref tag followed by text (no punctuation)"""
        input_text = 'Sentence <ref name="X1" /> continues here'
        expected = 'Sentence <ref name="X1" /> continues here'
        assert remove_spaces_between_ref_and_punctuation(input_text) == expected

    def test_multiple_spaces_before_punctuation(self):
        """Test removing multiple spaces before punctuation"""
        input_text = 'Sentence <ref name="X2" />     .'
        expected = 'Sentence <ref name="X2" />.'
        assert remove_spaces_between_ref_and_punctuation(input_text) == expected

    def test_closing_ref_double_punctuation(self):
        """Test with double punctuation after closing ref"""
        input_text = 'Sentence</ref> .:'
        expected = 'Sentence</ref>.:'  # space removed only before the first dot
        assert remove_spaces_between_ref_and_punctuation(input_text) == expected

    def test_ref_with_attributes(self):
        """Test with ref tag containing multiple attributes"""
        input_text = 'Sentence <ref name="X3" group="note" /> .'
        expected = 'Sentence <ref name="X3" group="note" />.'
        assert remove_spaces_between_ref_and_punctuation(input_text) == expected

    def test_empty_ref_tag(self):
        """Test with empty ref tag"""
        input_text = 'Sentence<ref></ref> .'
        expected = 'Sentence<ref></ref>.'
        assert remove_spaces_between_ref_and_punctuation(input_text) == expected

    def test_already_correct_should_stay_same(self):
        """Test text that is already correctly formatted"""
        input_text = 'Sentence <ref name="X4" />.'
        expected = 'Sentence <ref name="X4" />.'
        assert remove_spaces_between_ref_and_punctuation(input_text) == expected

    def test_mix_of_colon_types(self):
        """Test with different colon types"""
        input_text = 'Sentence <ref name="X5" /> : Another<ref name="X6" /> ：'
        expected = 'Sentence <ref name="X5" />: Another<ref name="X6" /> ：'
        assert remove_spaces_between_ref_and_punctuation(input_text) == expected

    def test_malformed_nested_refs(self):
        """Test with malformed nested refs"""
        input_text = 'Sentence <ref><ref /> 。'
        expected = 'Sentence <ref><ref />。'
        assert remove_spaces_between_ref_and_punctuation(input_text) == expected


class TestRemoveSpace2(TestRemoveSpace2Extra):
    """Main test cases for remove_space2"""

    def test_remove_space_end_1(self):
        """Test Armenian text with multiple refs"""
        input_text = 'Բուժումը ներառում է [[Թերապիա (բուժում)|օժանդակ միջոցառումներ]], ինչպիսիք են գանգի պաշտպանիչ սարքը և ատամնաբուժական խնամքը <ref name="NORD2004" /> : Ոսկրային որոշակի անոմալիաներ շտկելու համար կարող է իրականացվել վիրահատություն <ref name="GARD2016" /> : Կյանքի տևողությունը, ընդհանուր առմամբ, նորմալ է<ref name="Yo2002">{{Cite book|last=Young|first=Ian D.|title=Genetics for Orthopedic Surgeons: The Molecular Genetic Basis of Orthopedic Disorders|date=2002|publisher=Remedica|isbn=9781901346428|page=92|url=https://books.google.com/books?id=QyVsI5b2zJoC&pg=PT52|language=en|url-status=live|archive-url=https://web.archive.org/web/20161103235838/https://books.google.ca/books?id=QyVsI5b2zJoC&pg=PT52|archive-date=2016-11-03}}</ref>։'
        expected = 'Բուժումը ներառում է [[Թերապիա (բուժում)|օժանդակ միջոցառումներ]], ինչպիսիք են գանգի պաշտպանիչ սարքը և ատամնաբուժական խնամքը <ref name="NORD2004" />: Ոսկրային որոշակի անոմալիաներ շտկելու համար կարող է իրականացվել վիրահատություն <ref name="GARD2016" />: Կյանքի տևողությունը, ընդհանուր առմամբ, նորմալ է<ref name="Yo2002">{{Cite book|last=Young|first=Ian D.|title=Genetics for Orthopedic Surgeons: The Molecular Genetic Basis of Orthopedic Disorders|date=2002|publisher=Remedica|isbn=9781901346428|page=92|url=https://books.google.com/books?id=QyVsI5b2zJoC&pg=PT52|language=en|url-status=live|archive-url=https://web.archive.org/web/20161103235838/https://books.google.ca/books?id=QyVsI5b2zJoC&pg=PT52|archive-date=2016-11-03}}</ref>։'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'hy') == expected

    def test_remove_space_armenian(self):
        """Test Armenian text with Armenian punctuation"""
        input_text = 'Տեքստ <ref name="NORD2004" /> ։'
        expected = 'Տեքստ <ref name="NORD2004" />։'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'hy') == expected

    def test_remove_space_hindi(self):
        """Test Hindi text with Hindi punctuation"""
        input_text = 'पाठ <ref name="IND2001" /> ।'
        expected = 'पाठ <ref name="IND2001" />।'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'hi') == expected

    def test_remove_space_chinese(self):
        """Test Chinese text with Chinese punctuation"""
        input_text = '文本 <ref name="CN2003" /> 。'
        expected = '文本 <ref name="CN2003" />。'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'zh') == expected

    def test_remove_space_english(self):
        """Test English text with English punctuation"""
        input_text = 'Text <ref name="EN2005" /> .'
        expected = 'Text <ref name="EN2005" />.'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'en') == expected

    def test_remove_space_colon(self):
        """Test with colon punctuation"""
        input_text = 'Sentence <ref name="TEST" /> :'
        expected = 'Sentence <ref name="TEST" />:'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'en') == expected

    def test_remove_space_closing_ref_armenian(self):
        """Test closing ref tag with Armenian punctuation"""
        input_text = 'Տեքստ</ref> ։'
        expected = 'Տեքստ</ref>։'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'hy') == expected

    def test_remove_space_closing_ref_chinese(self):
        """Test closing ref tag with Chinese punctuation"""
        input_text = '文本</ref> 。'
        expected = '文本</ref>。'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'zh') == expected

    def test_remove_space_closing_ref_english(self):
        """Test closing ref tag with English punctuation"""
        input_text = 'Text</ref> .'
        expected = 'Text</ref>.'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'en') == expected

    def test_remove_space_closing_ref_colon(self):
        """Test closing ref tag with colon"""
        input_text = 'Sentence</ref> :'
        expected = 'Sentence</ref>:'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'en') == expected

    def test_no_space_should_stay_same(self):
        """Test text without spaces stays the same"""
        input_text = 'Text<ref name="OK" />.'
        expected = 'Text<ref name="OK" />.'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'en') == expected

    def test_multiple_refs_same_line_armenian(self):
        """Test multiple refs on same line with Armenian text"""
        input_text = 'Նախադասություն <ref name="N1" /> ։ Հաջորդը <ref name="N2" /> :'
        expected = 'Նախադասություն <ref name="N1" />։ Հաջորդը <ref name="N2" />:'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'hy') == expected

    def test_multiple_refs_same_line_chinese(self):
        """Test multiple refs on same line with Chinese text"""
        input_text = '句子 <ref name="C1" /> 。 然后 <ref name="C2" /> :'
        expected = '句子 <ref name="C1" />。 然后 <ref name="C2" />:'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'zh') == expected

    def test_closing_ref_multiple_marks(self):
        """Test closing ref with multiple punctuation marks"""
        input_text = 'Text</ref> ։ More text</ref> . And again</ref> :'
        expected = 'Text</ref>։ More text</ref>. And again</ref>:'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'en') == expected

    def test_long_mixed_paragraph(self):
        """Test long paragraph with mixed languages"""
        input_text = ('Բուժումը ներառում է [[Therapy|թերապիա]] <ref name="NORD2004" /> ։ Կյանքի տևողությունը նորմալ է<ref name="Yo2002">{{Cite book}}</ref> ։ '
            'النص العربي <ref name="AR2020" /> : والنهاية طبيعية<ref name="AR2021" /> . '
            'Chinese 文本<ref name="CN1" /> 。 Final<ref name="EN1" /> :')

        expected = ('Բուժումը ներառում է [[Therapy|թերապիա]] <ref name="NORD2004" />։ Կյանքի տևողությունը նորմալ է<ref name="Yo2002">{{Cite book}}</ref>։ '
            'النص العربي <ref name="AR2020" />: والنهاية طبيعية<ref name="AR2021" />. '
            'Chinese 文本<ref name="CN1" />。 Final<ref name="EN1" />:')

        assert remove_spaces_between_ref_and_punctuation(input_text, 'multi') == expected

    def test_no_spaces_remain_unchanged(self):
        """Test text without spaces remains unchanged"""
        input_text = 'Sentence<ref name="OK" />: Another</ref>. End</ref>։'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'multi') == input_text
