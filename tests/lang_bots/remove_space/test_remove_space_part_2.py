"""Tests for remove_space (remove_spaceTest.php)

Converted from tests/remove_spaceTest.php
"""

from fix_refs.lang_bots.hy_bot import remove_spaces_between_ref_and_punctuation
from fix_refs.lang_bots.remove_space import remove_spaces_between_last_word_and_beginning_of_ref


def test_remove_space_end_3rd_file():
    """Test removing spaces in text with multiple refs"""
    input_text = """            Article text <ref>{{Citar web|Text|author=John|language=en}}</ref> [[Հիպոկրատ|Հիպոկրատի]] test0 <ref name="Os2018" /><ref>{{ref
        |<!!>
        }}</ref>։ test1 <ref name="Os2018" /><ref>{{ref
        |<!!>
        }}</ref>։
    """
    expected = """            Article text <ref>{{Citar web|Text|author=John|language=en}}</ref> [[Հիպոկրատ|Հիպոկրատի]] test0 <ref name="Os2018" /><ref>{{ref
        |<!!>
        }}</ref>։ test1<ref name="Os2018" /><ref>{{ref
        |<!!>
        }}</ref>։
    """
    result = remove_spaces_between_last_word_and_beginning_of_ref(input_text, "hy")
    assert result == expected


def test_remove_space_end_5th_file() -> None:
    """Test removing spaces with keyword before ref"""
    input_text = """
        Article text <ref>{{Citar web|Text|author=John|language=en}}</ref> [[Հիպոկրատ|Հիպոկրատի]] կողմից <ref name="Os2018" /><ref>{{ref
        |<!!>
        }}</ref>։ կողմից <ref name="Os2018" /><ref>{{ref
        |zz
        }}</ref>։

        == test ==
    """
    expected = """
        Article text <ref>{{Citar web|Text|author=John|language=en}}</ref> [[Հիպոկրատ|Հիպոկրատի]] կողմից <ref name="Os2018" /><ref>{{ref
        |<!!>
        }}</ref>։ կողմից<ref name="Os2018" /><ref>{{ref
        |zz
        }}</ref>։

        == test ==
    """
    result = remove_spaces_between_last_word_and_beginning_of_ref(input_text, "hy")
    assert result == expected


def test_remove_space_end_with_links():
    """Test with wiki links"""
    input_text = 'Article text <ref>{{Citar web|Text|author=John|language=en}}</ref> [[Հիպոկրատ|Հիպոկրատի]] test0 <ref name="Os2018" /><ref>{{ref|<!!>}}</ref>։ test1 <ref name="Os2018" /><ref>{{ref|<!!>}}</ref>։'
    expected = 'Article text <ref>{{Citar web|Text|author=John|language=en}}</ref> [[Հիպոկրատ|Հիպոկրատի]] test0 <ref name="Os2018" /><ref>{{ref|<!!>}}</ref>։ test1<ref name="Os2018" /><ref>{{ref|<!!>}}</ref>։'
    result = remove_spaces_between_last_word_and_beginning_of_ref(input_text, "hy")
    assert result == expected


def test_remove_space_with_colon():
    """Test space removal before ref with colon punctuation"""
    input_text = 'Բուժումը ներառում է [[Թերապիա (բուժում)|օժանդակ միջոցառումներ]] <ref name="NORD2004" /> : Ոսկրային որոշակի անոմալիաներ շտկելու համար կարող է իրականացվել վիրահատություն <ref name="GARD2016" /> :'
    expected = 'Բուժումը ներառում է [[Թերապիա (բուժում)|օժանդակ միջոցառումներ]] <ref name="NORD2004" />: Ոսկրային որոշակի անոմալիաներ շտկելու համար կարող է իրականացվել վիրահատություն<ref name="GARD2016" />:'

    result = remove_spaces_between_ref_and_punctuation(input_text)
    result = remove_spaces_between_last_word_and_beginning_of_ref(result, "hy")

    assert result == expected


def test_part_4():
    """Test removing spaces in complex medical text with multiple refs"""
    input_text = 'Գոյություն ունի լյարդի ճարպային հիվանդության երկու տեսակ՝ ոչ ալկոհոլային ճարպային լյարդի հիվանդություն (ՈԱՃՀ) և ալկոհոլային լյարդի հիվանդություն <ref name="NIH2016" />։ ՈԱՃՀՀ-ն բաղկացած է պարզ ճարպային լյարդից և ոչ ալկոհոլային ստեատոհեպատիտից (ՈԱՃՀ): <ref name="AFP2013">{{Cite journal|last=Iser|first=D|last2=Ryan|first2=M|title=Fatty liver disease—a practical guide for GPs.|journal=Australian Family Physician|date=July 2013|volume=42|issue=7|pages=444–7|pmid=23826593}}</ref><ref name="NIH2016" /> Հիմնական ռիսկերից են [[Էթիլ սպիրտ|ալկոհոլը]], [[Տիպ 2 շաքարային դիաբետ|2-րդ տիպի շաքարախտը]] և [[Ճարպակալում|ճարպակալումը]] <ref name="Ant2019" /><ref name="NIH2016" />։ Այլ ռիսկի գործոններից են որոշակի դեղամիջոցները, ինչպիսիք են [[Գլյուկոկորտիկոիդներ|գլյուկոկորտիկոիդները]] և [[Հեպատիտ C|հեպատիտ C-ն]] : <ref name="NIH2016" /> Անհասկանալի է, թե ինչու են ոչ ալկոհոլային ճարպային լյարդի հիվանդություն ունեցող որոշ մարդիկ զարգացնում պարզ ճարպային լյարդ, իսկ մյուսները՝ ոչ ալկոհոլային հեպատիտ: <ref name="NIH2016" /> Ախտորոշումը հիմնված է [[Անամնեզ|բժշկական պատմության]] վրա, որը հաստատվում է արյան անալիզներով, բժշկական պատկերագրական հետազոտություններով և երբեմն լյարդի բիոպսիայով <ref name="NIH2016" />։'
    expected = 'Գոյություն ունի լյարդի ճարպային հիվանդության երկու տեսակ՝ ոչ ալկոհոլային ճարպային լյարդի հիվանդություն (ՈԱՃՀ) և ալկոհոլային լյարդի հիվանդություն <ref name="NIH2016" />։ ՈԱՃՀՀ-ն բաղկացած է պարզ ճարպային լյարդից և ոչ ալկոհոլային ստեատոհեպատիտից (ՈԱՃՀ): <ref name="AFP2013">{{Cite journal|last=Iser|first=D|last2=Ryan|first2=M|title=Fatty liver disease—a practical guide for GPs.|journal=Australian Family Physician|date=July 2013|volume=42|issue=7|pages=444–7|pmid=23826593}}</ref><ref name="NIH2016" /> Հիմնական ռիսկերից են [[Էթիլ սպիրտ|ալկոհոլը]], [[Տիպ 2 շաքարային դիաբետ|2-րդ տիպի շաքարախտը]] և [[Ճարպակալում|ճարպակալումը]] <ref name="Ant2019" /><ref name="NIH2016" />։ Այլ ռիսկի գործոններից են որոշակի դեղամիջոցները, ինչպիսիք են [[Գլյուկոկորտիկոիդներ|գլյուկոկորտիկոիդները]] և [[Հեպատիտ C|հեպատիտ C-ն]] : <ref name="NIH2016" /> Անհասկանալի է, թե ինչու են ոչ ալկոհոլային ճարպային լյարդի հիվանդություն ունեցող որոշ մարդիկ զարգացնում պարզ ճարպային լյարդ, իսկ մյուսները՝ ոչ ալկոհոլային հեպատիտ: <ref name="NIH2016" /> Ախտորոշումը հիմնված է [[Անամնեզ|բժշկական պատմության]] վրա, որը հաստատվում է արյան անալիզներով, բժշկական պատկերագրական հետազոտություններով և երբեմն լյարդի բիոպսիայով<ref name="NIH2016" />։'
    result = remove_spaces_between_last_word_and_beginning_of_ref(input_text, "hy")
    assert result == expected


def test_remove_space_multiple_punctuations():
    """Test multiple punctuation marks in text"""
    input_text = 'Գոյություն ունի լյարդի ճարպային հիվանդություն <ref name="NIH2016" />։ ՈԱՃՀՀ-ն բաղկացած է <ref name="AFP2013">{{Cite journal}}</ref><ref name="NIH2016" /> Հիմնական ռիսկերից են <ref name="Ant2019" /><ref name="NIH2016" />։'
    expected = 'Գոյություն ունի լյարդի ճարպային հիվանդություն <ref name="NIH2016" />։ ՈԱՃՀՀ-ն բաղկացած է <ref name="AFP2013">{{Cite journal}}</ref><ref name="NIH2016" /> Հիմնական ռիսկերից են<ref name="Ant2019" /><ref name="NIH2016" />։'
    result = remove_spaces_between_last_word_and_beginning_of_ref(input_text, "hy")
    assert result == expected
