"""Tests for adding English language parameter (add_lang_en.py)

Converted from tests/en_lang_paramTest.php
"""
import pytest
from src.bots.add_lang_en_bot import add_lang_en_to_refs


class TestAddLangEn:
    """Test cases for adding English language parameter to references"""

    def test_add_lang_en_simple_ref(self):
        """Test adding language=en to simple reference"""
        input_text = "<ref>{{Citar web|Some text}}</ref> {{temp|test=1}}"
        expected = "<ref>{{Citar web|Some text|language=en}}</ref> {{temp|test=1}}"
        result = add_lang_en_to_refs(input_text)
        assert result == expected

    def test_add_lang_en_existing_language(self):
        """Test not modifying existing language parameter"""
        input_text = "<ref>{{Citar web|Text|language=fr}}</ref>"
        expected = "<ref>{{Citar web|Text|language=fr}}</ref>"
        result = add_lang_en_to_refs(input_text)
        assert result == expected

    def test_add_lang_en_empty_ref(self):
        """Test handling empty reference"""
        input_text = "<ref></ref>"
        expected = "<ref></ref>"
        result = add_lang_en_to_refs(input_text)
        assert result == expected

    def test_add_lang_en_with_existing_params(self):
        """Test adding language with existing parameters"""
        input_text = " {{temp|test=1}} <ref>{{Citar web|Text|author=John}}</ref>"
        expected = " {{temp|test=1}} <ref>{{Citar web|Text|author=John|language=en}}</ref>"
        result = add_lang_en_to_refs(input_text)
        assert result == expected

    def test_add_lang_malformed_ref(self):
        """Test fixing malformed language parameter"""
        input_text = "<ref>{{Citar web|Text|language = }}</ref> {{temp|test=1}}"
        expected = "<ref>{{Citar web|Text|language =en}}</ref> {{temp|test=1}}"
        result = add_lang_en_to_refs(input_text)
        assert result == expected

    def test_add_lang_en_arabic(self):
        """Test not overwriting Arabic language"""
        input_text = "<ref>{{Citar web|Text|language=ar}}</ref>"
        expected = "<ref>{{Citar web|Text|language=ar}}</ref>"
        result = add_lang_en_to_refs(input_text)
        assert result == expected

    def test_add_lang_en_no_change_needed(self):
        """Test reference already has language=en"""
        input_text = " {{temp|test=1}} <ref>{{Citar web|Text|language=en}}</ref>"
        expected = " {{temp|test=1}} <ref>{{Citar web|Text|language=en}}</ref>"
        result = add_lang_en_to_refs(input_text)
        assert result == expected

    def test_add_lang_multiple_refs(self):
        """Test adding language to multiple references"""
        input_text = "<ref>{{Cite web|text1}}</ref> Some text <ref>{{Cite web|text2}}</ref>"
        expected = "<ref>{{Cite web|text1|language=en}}</ref> Some text <ref>{{Cite web|text2|language=en}}</ref>"
        result = add_lang_en_to_refs(input_text)
        assert result == expected

    def test_add_lang_mixed_refs(self):
        """Test mixed references with and without language"""
        input_text = "<ref>{{Cite|no lang}}</ref> <ref>{{Cite|language=es}}</ref> <ref>{{Cite|another}}</ref>"
        expected = "<ref>{{Cite|no lang|language=en}}</ref> <ref>{{Cite|language=es}}</ref> <ref>{{Cite|another|language=en}}</ref>"
        result = add_lang_en_to_refs(input_text)
        assert result == expected

    def test_add_lang_mixed_refs_hy(self):
        """Test mixed references with and without language"""
        input_text = """'''Լյարդի ճարպային հիվանդությունը''' ( '''ԼՃՀ''' ), որը հայտնի է նաև որպես '''լյարդի ստեատոզ''', վիճակ է, որի դեպքում [[Լյարդ|լյարդում]] կուտակվում է ավելորդ [[ճարպ]] <ref name="NIH2016">{{Cite web|title=Nonalcoholic Fatty Liver Disease & NASH|url=https://www.niddk.nih.gov/health-information/liver-disease/nafld-nash/all-content|website=National Institute of Diabetes and Digestive and Kidney Diseases|access-date=7 November 2018|date=November 2016|archive-date=9 January 2020|archive-url=https://web.archive.org/web/20200109183351/https://www.niddk.nih.gov/health-information/liver-disease/nafld-nash/all-content|url-status=live}}</ref>։ Հաճախ ախտանիշներ չկան կամ քիչ են<ref name="NIH2016" /><ref name="Sin2017">{{Cite journal|last=Singh|first=S|last2=Osna|first2=NA|last3=Kharbanda|first3=KK|title=Treatment options for alcoholic and non-alcoholic fatty liver disease: A review.|journal=World Journal of Gastroenterology|date=28 September 2017|volume=23|issue=36|pages=6549–6570|doi=10.3748/wjg.v23.i36.6549|pmid=29085205|pmc=5643281}}</ref>։ Երբեմն կարող է լինել հոգնածություն կամ ցավ [[Որովայն|որովայնի]] վերին աջ մասում<ref name="NIH2016" />։ Բարդություններից կարող են լինել [[Լյարդի ցիռոզ|ցիռոզը]], [[Լյարդի քաղցկեղ|լյարդի քաղցկեղը]] և կերակրափողի լայնացած երակները<ref name="NIH2016" /><ref name="Ant2019">{{Cite journal|last=Antunes|first=C|last2=Azadfard|first2=M|last3=Gupta|first3=M|title=Fatty Liver|date=January 2019|pmid=28723021|journal=StatPearls}}</ref>։"""
        expected = """'''Լյարդի ճարպային հիվանդությունը''' ( '''ԼՃՀ''' ), որը հայտնի է նաև որպես '''լյարդի ստեատոզ''', վիճակ է, որի դեպքում [[Լյարդ|լյարդում]] կուտակվում է ավելորդ [[ճարպ]] <ref name="NIH2016">{{Cite web|title=Nonalcoholic Fatty Liver Disease & NASH|url=https://www.niddk.nih.gov/health-information/liver-disease/nafld-nash/all-content|website=National Institute of Diabetes and Digestive and Kidney Diseases|access-date=7 November 2018|date=November 2016|archive-date=9 January 2020|archive-url=https://web.archive.org/web/20200109183351/https://www.niddk.nih.gov/health-information/liver-disease/nafld-nash/all-content|url-status=live|language=en}}</ref>։ Հաճախ ախտանիշներ չկան կամ քիչ են<ref name="NIH2016" /><ref name="Sin2017">{{Cite journal|last=Singh|first=S|last2=Osna|first2=NA|last3=Kharbanda|first3=KK|title=Treatment options for alcoholic and non-alcoholic fatty liver disease: A review.|journal=World Journal of Gastroenterology|date=28 September 2017|volume=23|issue=36|pages=6549–6570|doi=10.3748/wjg.v23.i36.6549|pmid=29085205|pmc=5643281|language=en}}</ref>։ Երբեմն կարող է լինել հոգնածություն կամ ցավ [[Որովայն|որովայնի]] վերին աջ մասում<ref name="NIH2016" />։ Բարդություններից կարող են լինել [[Լյարդի ցիռոզ|ցիռոզը]], [[Լյարդի քաղցկեղ|լյարդի քաղցկեղը]] և կերակրափողի լայնացած երակները<ref name="NIH2016" /><ref name="Ant2019">{{Cite journal|last=Antunes|first=C|last2=Azadfard|first2=M|last3=Gupta|first3=M|title=Fatty Liver|date=January 2019|pmid=28723021|journal=StatPearls|language=en}}</ref>։"""
        result = add_lang_en_to_refs(input_text)
        assert result == expected
