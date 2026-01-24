"""Tests for remove_space (remove_spaceTest.php)

Converted from tests/remove_spaceTest.php
"""
import pytest
from src.lang_bots.hy_bot import remove_spaces_between_last_word_and_beginning_of_ref


class TestRemoveSpace:
    """Test cases for removing spaces between text and refs"""

    def test_remove_space_end_3rd_file(self):
        """Test removing spaces in text with multiple refs"""
        input_text = '''            Article text <ref>{{Citar web|Text|author=John|language=en}}</ref> [[Հիպոկրատ|Հիպոկրատի]] test0 <ref name="Os2018" /><ref>{{ref
            |<!!>
            }}</ref>։ test1 <ref name="Os2018" /><ref>{{ref
            |<!!>
            }}</ref>։
        '''
        expected = '''            Article text <ref>{{Citar web|Text|author=John|language=en}}</ref> [[Հիպոկրատ|Հիպոկրատի]] test0 <ref name="Os2018" /><ref>{{ref
            |<!!>
            }}</ref>։ test1<ref name="Os2018" /><ref>{{ref
            |<!!>
            }}</ref>։
        '''
        result = remove_spaces_between_last_word_and_beginning_of_ref(input_text, 'hy')
        assert result == expected

    def test_remove_space_end_4th_file(self):
        """Test removing spaces in Armenian text with multiple refs"""
        input_text = '''            Հետծննդյան հոգեբանական խանգարումը հանդիպում է 1000 ծննդաբերությունից 1-2-ի մոտ։ <ref name="Os2018" /><ref name="Li2018" /> Տարբեր [[Մշակույթ|մշակույթներում]] և [[Դասակարգային կառուցվածք|սոցիալական դասերում]] գները նման են թվում։ <ref name="Luc2021" /> Ավելի հաճախ այն հանդիպում է հայտնի կամ նոր սկսվող երկբևեռ խանգարման համատեքստում, որը հայտնի է որպես հետծննդյան երկբևեռ խանգարում : <ref name="Luc2021" /> Այս վիճակը նկարագրվել է դեռևս մ.թ.ա. 400 թվականից [[Հիպոկրատ|Հիպոկրատի]] կողմից ։ <ref name="Os2018" />
        '''
        expected = '''            Հետծննդյան հոգեբանական խանգարումը հանդիպում է 1000 ծննդաբերությունից 1-2-ի մոտ։ <ref name="Os2018" /><ref name="Li2018" /> Տարբեր [[Մշակույթ|մշակույթներում]] և [[Դասակարգային կառուցվածք|սոցիալական դասերում]] գները նման են թվում։ <ref name="Luc2021" /> Ավելի հաճախ այն հանդիպում է հայտնի կամ նոր սկսվող երկբևեռ խանգարման համատեքստում, որը հայտնի է որպես հետծննդյան երկբևեռ խանգարում : <ref name="Luc2021" /> Այս վիճակը նկարագրվել է դեռևս մ.թ.ա. 400 թվականից [[Հիպոկրատ|Հիպոկրատի]] կողմից ։ <ref name="Os2018" />
        '''
        result = remove_spaces_between_last_word_and_beginning_of_ref(input_text, 'hy')
        assert result == expected

    def test_remove_space_end_5th_file(self):
        """Test removing spaces with keyword before ref"""
        input_text = '''            Article text <ref>{{Citar web|Text|author=John|language=en}}</ref> [[Հիպոկրատ|Հիպոկրատի]] կողմից <ref name="Os2018" /><ref>{{ref
            |<!!>
            }}</ref>։ կողմից <ref name="Os2018" /><ref>{{ref
            |zz
            }}</ref>։

            == test ==
        '''
        expected = '''            Article text <ref>{{Citar web|Text|author=John|language=en}}</ref> [[Հիպոկրատ|Հիպոկրատի]] կողմից <ref name="Os2018" /><ref>{{ref
            |<!!>
            }}</ref>։ կողմից<ref name="Os2018" /><ref>{{ref
            |zz
            }}</ref>։

            == test ==
        '''
        result = remove_spaces_between_last_word_and_beginning_of_ref(input_text, 'hy')
        assert result == expected

    def test_remove_space_end_1(self):
        """Test removing spaces in complex Armenian text"""
        input_text = 'Հետծննդյան հոգեբանական խանգարումը հանդիպում է 1000 ծննդաբերությունից 1-2-ի մոտ։ <ref name="Os2018" /><ref name="Li2018" /> Տարբեր [[Մշակույթ|մշակույթներում]] և [[Դասակարգային կառուցվածք|սոցիալական դասերում]] գները նման են թվում։ <ref name="Luc2021" /> Ավելի հաճախ այն հանդիպում է հայտնի կամ նոր սկսվող երկբևեռ խանգարման համատեքստում, որը հայտնի է որպես հետծննդյան երկբևեռ խանգարում : <ref name="Luc2021" /> Այս վիճակը նկարագրվել է դեռևս մ.թ.ա. 400 թվականից [[Հիպոկրատ|Հիպոկրատի]] կողմից  <ref name="Os2018" />։'
        expected = 'Հետծննդյան հոգեբանական խանգարումը հանդիպում է 1000 ծննդաբերությունից 1-2-ի մոտ։ <ref name="Os2018" /><ref name="Li2018" /> Տարբեր [[Մշակույթ|մշակույթներում]] և [[Դասակարգային կառուցվածք|սոցիալական դասերում]] գները նման են թվում։ <ref name="Luc2021" /> Ավելի հաճախ այն հանդիպում է հայտնի կամ նոր սկսվող երկբևեռ խանգարման համատեքստում, որը հայտնի է որպես հետծննդյան երկբևեռ խանգարում : <ref name="Luc2021" /> Այս վիճակը նկարագրվել է դեռևս մ.թ.ա. 400 թվականից [[Հիպոկրատ|Հիպոկրատի]] կողմից<ref name="Os2018" />։'
        result = remove_spaces_between_last_word_and_beginning_of_ref(input_text, 'hy')
        assert result == expected

    def test_part_3(self):
        """Test removing spaces before ref with Armenian text"""
        input_text = 'Այն առաջին անգամ արձանագրվել է 1750 թվականին Ամերիկայում գտնվող քահանա Օլիվեր Հարթի օրագրային գրառման մեջ  <ref name="Sc2011">{{Cite book|last=Schachner|first=Lawrence A.|last2=Hansen|first2=Ronald C.|title=Pediatric Dermatology E-Book|date=2011|publisher=Elsevier Health Sciences|isbn=978-0723436652|page=598|url=https://books.google.com/books?id=tAlGLYplkacC&pg=PA598|language=en|url-status=live|archive-url=https://web.archive.org/web/20171105195802/https://books.google.com/books?id=tAlGLYplkacC&pg=PA598|archive-date=November 5, 2017}}</ref>։'
        expected = 'Այն առաջին անգամ արձանագրվել է 1750 թվականին Ամերիկայում գտնվող քահանա Օլիվեր Հարթի օրագրային գրառման մեջ<ref name="Sc2011">{{Cite book|last=Schachner|first=Lawrence A.|last2=Hansen|first2=Ronald C.|title=Pediatric Dermatology E-Book|date=2011|publisher=Elsevier Health Sciences|isbn=978-0723436652|page=598|url=https://books.google.com/books?id=tAlGLYplkacC&pg=PA598|language=en|url-status=live|archive-url=https://web.archive.org/web/20171105195802/https://books.google.com/books?id=tAlGLYplkacC&pg=PA598|archive-date=November 5, 2017}}</ref>։'
        result = remove_spaces_between_last_word_and_beginning_of_ref(input_text, 'hy')
        assert result == expected

    def test_part_4(self):
        """Test removing spaces in complex medical text with multiple refs"""
        input_text = 'Գոյություն ունի լյարդի ճարպային հիվանդության երկու տեսակ՝ ոչ ալկոհոլային ճարպային լյարդի հիվանդություն (ՈԱՃՀ) և ալկոհոլային լյարդի հիվանդություն <ref name="NIH2016" />։ ՈԱՃՀՀ-ն բաղկացած է պարզ ճարպային լյարդից և ոչ ալկոհոլային ստեատոհեպատիտից (ՈԱՃՀ): <ref name="AFP2013">{{Cite journal|last=Iser|first=D|last2=Ryan|first2=M|title=Fatty liver disease—a practical guide for GPs.|journal=Australian Family Physician|date=July 2013|volume=42|issue=7|pages=444–7|pmid=23826593}}</ref><ref name="NIH2016" /> Հիմնական ռիսկերից են [[Էթիլ սպիրտ|ալկոհոլը]], [[Տիպ 2 շաքարային դիաբետ|2-րդ տիպի շաքարախտը]] և [[Ճարպակալում|ճարպակալումը]] <ref name="Ant2019" /><ref name="NIH2016" />։ Այլ ռիսկի գործոններից են որոշակի դեղամիջոցները, ինչպիսիք են [[Գլյուկոկորտիկոիդներ|գլյուկոկորտիկոիդները]] և [[Հեպատիտ C|հեպատիտ C-ն]] : <ref name="NIH2016" /> Անհասկանալի է, թե ինչու են ոչ ալկոհոլային ճարպային լյարդի հիվանդություն ունեցող որոշ մարդիկ զարգացնում պարզ ճարպային լյարդ, իսկ մյուսները՝ ոչ ալկոհոլային հեպատիտ: <ref name="NIH2016" /> Ախտորոշումը հիմնված է [[Անամնեզ|բժշկական պատմության]] վրա, որը հաստատվում է արյան անալիզներով, բժշկական պատկերագրական հետազոտություններով և երբեմն լյարդի բիոպսիայով <ref name="NIH2016" />։'
        expected = 'Գոյություն ունի լյարդի ճարպային հիվանդության երկու տեսակ՝ ոչ ալկոհոլային ճարպային լյարդի հիվանդություն (ՈԱՃՀ) և ալկոհոլային լյարդի հիվանդություն <ref name="NIH2016" />։ ՈԱՃՀՀ-ն բաղկացած է պարզ ճարպային լյարդից և ոչ ալկոհոլային ստեատոհեպատիտից (ՈԱՃՀ): <ref name="AFP2013">{{Cite journal|last=Iser|first=D|last2=Ryan|first2=M|title=Fatty liver disease—a practical guide for GPs.|journal=Australian Family Physician|date=July 2013|volume=42|issue=7|pages=444–7|pmid=23826593}}</ref><ref name="NIH2016" /> Հիմնական ռիսկերից են [[Էթիլ սպիրտ|ալկոհոլը]], [[Տիպ 2 շաքարային դիաբետ|2-րդ տիպի շաքարախտը]] և [[Ճարպակալում|ճարպակալումը]] <ref name="Ant2019" /><ref name="NIH2016" />։ Այլ ռիսկի գործոններից են որոշակի դեղամիջոցները, ինչպիսիք են [[Գլյուկոկորտիկոիդներ|գլյուկոկորտիկոիդները]] և [[Հեպատիտ C|հեպատիտ C-ն]] : <ref name="NIH2016" /> Անհասկանալի է, թե ինչու են ոչ ալկոհոլային ճարպային լյարդի հիվանդություն ունեցող որոշ մարդիկ զարգացնում պարզ ճարպային լյարդ, իսկ մյուսները՝ ոչ ալկոհոլային հեպատիտ: <ref name="NIH2016" /> Ախտորոշումը հիմնված է [[Անամնեզ|բժշկական պատմության]] վրա, որը հաստատվում է արյան անալիզներով, բժշկական պատկերագրական հետազոտություններով և երբեմն լյարդի բիոպսիայով<ref name="NIH2016" />։'
        result = remove_spaces_between_last_word_and_beginning_of_ref(input_text, 'hy')
        assert result == expected
