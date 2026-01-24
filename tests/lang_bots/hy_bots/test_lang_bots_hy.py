"""Tests for Armenian language bot (hy_bot.py)

Converted from tests/remove_spaceTest.php and tests/remove_space2Test.php
"""
import pytest
from src.lang_bots.hy_bot import (
    remove_spaces_between_ref_and_punctuation,
    remove_spaces_between_last_word_and_beginning_of_ref,
    hy_fixes
)


class TestRemoveSpaceBetweenRefAndPunctuation:
    """Test cases for removing spaces between ref tags and punctuation"""

    def test_ref_no_punctuation_after(self):
        """Test ref without punctuation stays unchanged"""
        input_text = 'Sentence <ref name="X1" /> continues here'
        expected = 'Sentence <ref name="X1" /> continues here'
        assert remove_spaces_between_ref_and_punctuation(input_text) == expected

    def test_multiple_spaces_before_punctuation(self):
        """Test removing multiple spaces before punctuation"""
        input_text = 'Sentence <ref name="X2" />     .'
        expected = 'Sentence <ref name="X2" />.'
        assert remove_spaces_between_ref_and_punctuation(input_text) == expected

    def test_closing_ref_double_punctuation(self):
        """Test double punctuation after closing ref"""
        input_text = 'Sentence</ref> .:'
        expected = 'Sentence</ref>.:'
        assert remove_spaces_between_ref_and_punctuation(input_text) == expected

    def test_ref_with_attributes(self):
        """Test ref with multiple attributes"""
        input_text = 'Sentence <ref name="X3" group="note" /> .'
        expected = 'Sentence <ref name="X3" group="note" />.'
        assert remove_spaces_between_ref_and_punctuation(input_text) == expected

    def test_empty_ref_tag(self):
        """Test empty ref tag"""
        input_text = 'Sentence<ref></ref> .'
        expected = 'Sentence<ref></ref>.'
        assert remove_spaces_between_ref_and_punctuation(input_text) == expected

    def test_already_correct_should_stay_same(self):
        """Test already correct spacing stays same"""
        input_text = 'Sentence <ref name="X4" />.'
        expected = 'Sentence <ref name="X4" />.'
        assert remove_spaces_between_ref_and_punctuation(input_text) == expected

    def test_mix_of_colon_types(self):
        """Test different colon types"""
        input_text = 'Sentence <ref name="X5" /> : Another<ref name="X6" /> ：'
        expected = 'Sentence <ref name="X5" />: Another<ref name="X6" /> ：'
        assert remove_spaces_between_ref_and_punctuation(input_text) == expected

    def test_malformed_nested_refs(self):
        """Test malformed nested refs"""
        input_text = 'Sentence <ref><ref /> 。'
        expected = 'Sentence <ref><ref />。'
        assert remove_spaces_between_ref_and_punctuation(input_text) == expected

    def test_remove_space_armenian(self):
        """Test Armenian punctuation (։)"""
        input_text = 'Տեքստ <ref name="NORD2004" /> ։'
        expected = 'Տեքստ <ref name="NORD2004" />։'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'hy') == expected

    def test_remove_space_hindi(self):
        """Test Hindi punctuation (।)"""
        input_text = 'पाठ <ref name="IND2001" /> ।'
        expected = 'पाठ <ref name="IND2001" />।'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'hi') == expected

    def test_remove_space_chinese(self):
        """Test Chinese punctuation (。)"""
        input_text = '文本 <ref name="CN2003" /> 。'
        expected = '文本 <ref name="CN2003" />。'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'zh') == expected

    def test_remove_space_english(self):
        """Test English punctuation (.)"""
        input_text = 'Text <ref name="EN2005" /> .'
        expected = 'Text <ref name="EN2005" />.'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'en') == expected

    def test_remove_space_colon(self):
        """Test colon punctuation"""
        input_text = 'Sentence <ref name="TEST" /> :'
        expected = 'Sentence <ref name="TEST" />:'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'en') == expected

    def test_remove_space_closing_ref_armenian(self):
        """Test Armenian punctuation after closing ref"""
        input_text = 'Տեքստ</ref> ։'
        expected = 'Տեքստ</ref>։'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'hy') == expected

    def test_remove_space_closing_ref_chinese(self):
        """Test Chinese punctuation after closing ref"""
        input_text = '文本</ref> 。'
        expected = '文本</ref>。'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'zh') == expected

    def test_remove_space_closing_ref_english(self):
        """Test English punctuation after closing ref"""
        input_text = 'Text</ref> .'
        expected = 'Text</ref>.'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'en') == expected

    def test_no_space_should_stay_same(self):
        """Test text without extra spaces stays same"""
        input_text = 'Text<ref name="OK" />.'
        expected = 'Text<ref name="OK" />.'
        assert remove_spaces_between_ref_and_punctuation(input_text, 'en') == expected


class TestRemoveSpaceBetweenLastWordAndRef:
    """Test cases for removing spaces between last word and beginning of ref"""

    def test_remove_space_end_basic(self):
        """Test basic space removal before ref"""
        input_text = 'Այն առաջին անգամ արձանագրվել է 1750 թվականին Ամերիկայում գտնվող քահանա Օլիվեր Հարթի օրագրային գրառման մեջ  <ref name="Sc2011">{{Cite book|last=Schachner}}</ref>։'
        expected = 'Այն առաջին անգամ արձանագրվել է 1750 թվականին Ամերիկայում գտնվող քահանա Օլիվեր Հարթի օրագրային գրառման մեջ<ref name="Sc2011">{{Cite book|last=Schachner}}</ref>։'
        result = remove_spaces_between_last_word_and_beginning_of_ref(input_text, 'hy')
        assert result == expected

    def test_remove_space_with_colon(self):
        """Test space removal before ref with colon punctuation"""
        input_text = 'Բուժումը ներառում է [[Թերապիա (բուժում)|օժանդակ միջոցառումներ]] <ref name="NORD2004" /> : Ոսկրային որոշակի անոմալիաներ շտկելու համար կարող է իրականացվել վիրահատություն <ref name="GARD2016" /> :'
        expected = 'Բուժումը ներառում է [[Թերապիա (բուժում)|օժանդակ միջոցառումներ]]<ref name="NORD2004" />: Ոսկրային որոշակի անոմալիաներ շտկելու համար կարող է իրականացվել վիրահատություն<ref name="GARD2016" />:'
        result = remove_spaces_between_last_word_and_beginning_of_ref(input_text, 'hy')
        assert result == expected

    def test_remove_space_multiple_punctuations(self):
        """Test multiple punctuation marks in text"""
        input_text = 'Գոյություն ունի լյարդի ճարպային հիվանդություն <ref name="NIH2016" />։ ՈԱՃՀՀ-ն բաղկացած է <ref name="AFP2013">{{Cite journal}}</ref><ref name="NIH2016" /> Հիմնական ռիսկերից են <ref name="Ant2019" /><ref name="NIH2016" />։'
        expected = 'Գոյություն ունի լյարդի ճարպային հիվանդություն <ref name="NIH2016" />։ ՈԱՃՀՀ-ն բաղկացած է <ref name="AFP2013">{{Cite journal}}</ref><ref name="NIH2016" /> Հիմնական ռիսկերից են <ref name="Ant2019" /><ref name="NIH2016" />։'
        result = remove_spaces_between_last_word_and_beginning_of_ref(input_text, 'hy')
        assert result == expected

    def test_remove_space_end_with_links(self):
        """Test with wiki links"""
        input_text = 'Article text <ref>{{Citar web|Text|author=John|language=en}}</ref> [[Հիպոկրատ|Հիպոկրատի]] test0 <ref name="Os2018" /><ref>{{ref|<!!>}}</ref>։ test1 <ref name="Os2018" /><ref>{{ref|<!!>}}</ref>։'
        expected = 'Article text <ref>{{Citar web|Text|author=John|language=en}}</ref> [[Հիպոկրատ|Հիպոկրատի]] test0 <ref name="Os2018" /><ref>{{ref|<!!>}}</ref>։ test1<ref name="Os2018" /><ref>{{ref|<!!>}}</ref>։'
        result = remove_spaces_between_last_word_and_beginning_of_ref(input_text, 'hy')
        assert result == expected


class TestHyFixes:
    """Test cases for Armenian-specific fixes"""

    def test_hy_fixes_combined(self):
        """Test combined Armenian fixes"""
        input_text = 'Տեքստ  <ref name="TEST" /> ։ Ավելի  <ref name="TEST2" /> :'
        result = hy_fixes(input_text)
        # Both fixes should be applied
        assert '<ref name="TEST" />' in result
        assert '<ref name="TEST2" />' in result
