"""Tests for Portuguese language bot (pt_bot.py)

Converted from tests/pt_bots/pt_monthsTest.php
"""
import pytest
from src.lang_bots.pt_bot import (
    fix_pt_months_in_texts,
    fix_pt_months_in_refs,
    rm_ref_spaces,
    start_end
)
from src.bots.months import make_date_new_val_pt


class TestPortugueseBot:
    """Test cases for Portuguese language bot"""

    # Tests for make_date_new_val_pt

    def test_make_date_new_val_pt_full_date(self):
        """Test converting full date to Portuguese format"""
        result = make_date_new_val_pt("25 December 2016")
        assert result == "25 de dezembro 2016"

    def test_make_date_new_val_pt_month_year(self):
        """Test converting month and year to Portuguese format"""
        assert make_date_new_val_pt("January 2023") == "janeiro 2023"

    def test_make_date_new_val_pt_day_month_year(self):
        """Test converting day month year to Portuguese format"""
        assert make_date_new_val_pt("10 January, 2023") == "10 de janeiro 2023"

    # Tests for fix_pt_months_in_texts


class TestPtMonths:
    """Test cases for Portuguese month translation"""

    def test_temp_in_wikitexts(self):
        """Test fixing months in references within wikitext"""
        input_text = ('test: <ref name="AHFS2016">{{Citar web|titulo=Charcoal, Activated|url=https://www.drugs.com/monograph/charcoal-activated.html|publicado=The American Society of Health-System Pharmacists|acessodata=8 December 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 December 2016}}</ref>\n'
                      '<ref name="AHFS2016">{{Citar web|acessodata=8 December 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 December 2016}} xxxxxxxxxxxxxxxx {{Webarchive|url=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|date=21 December 2016}}</ref>')

        expected = ('test: <ref name="AHFS2016">{{Citar web|titulo=Charcoal, Activated|url=https://www.drugs.com/monograph/charcoal-activated.html|publicado=The American Society of Health-System Pharmacists|acessodata=8 de dezembro 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 de dezembro 2016}}</ref>\n'
                    '<ref name="AHFS2016">{{Citar web|acessodata=8 de dezembro 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 de dezembro 2016}} xxxxxxxxxxxxxxxx {{Webarchive|url=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|date=21 de dezembro 2016}}</ref>')

        result = fix_pt_months_in_refs(input_text)
        assert result == expected

    def test_temp_in_ref(self):
        """Test fixing months in single reference"""
        input_text = '<ref name="test" group="notes">{{cite web|date=25  December 2016 |}}</ref>'
        expected = '<ref name="test" group="notes">{{cite web|date=25 de dezembro 2016|}}</ref>'
        result = fix_pt_months_in_refs(input_text)
        assert result == expected

    def test_temp_in_templates(self):
        """Test fixing months in templates"""
        input_text = '{{cite web|date=10 January, 2023|}}'
        expected = '{{cite web|date=10 de janeiro 2023|}}'
        result = fix_pt_months_in_texts(input_text)
        assert result == expected

    def test_temp_in_templates_more(self):
        """Test fixing months in multiple templates"""
        input_text = '{{cite web|date=10 January, 2023|}} {{cite book|time = test|date = 10 de janeiro 2023 }}'
        expected = '{{cite web|date=10 de janeiro 2023|}} {{cite book|time = test|date = 10 de janeiro 2023 }}'
        result = fix_pt_months_in_texts(input_text)
        assert result == expected

    def test_fix_months_in_templates_all_months(self):
        """Test translating all months to Portuguese"""
        tests = [
            ("{{cite web|date=January 2023|}}", "{{cite web|date=janeiro 2023|}}"),
            ("{{cite web|date=February 15, 2023|}}", "{{cite web|date=15 de fevereiro 2023|}}"),
            ("{{cite web|date=March 2023|}}", "{{cite web|date=março 2023|}}"),
            ("{{cite web|date=April 5, 2023|}}", "{{cite web|date=5 de abril 2023|}}"),
            ("{{cite web|date=May 2023|}}", "{{cite web|date=maio 2023|}}"),
            ("{{cite web|date=June 20, 2023|}}", "{{cite web|date=20 de junho 2023|}}"),
            ("{{cite web|date=July 2023|}}", "{{cite web|date=julho 2023|}}"),
            ("{{cite web|date=August 10, 2023|}}", "{{cite web|date=10 de agosto 2023|}}"),
            ("{{cite web|date=September 2023|}}", "{{cite web|date=setembro 2023|}}"),
            ("{{cite web|date=October 30, 2023|}}", "{{cite web|date=30 de outubro 2023|}}"),
            ("{{cite web|date=November 2023|}}", "{{cite web|date=novembro 2023|}}"),
            ("{{cite web|date=December 25, 2023|}}", "{{cite web|date=25 de dezembro 2023|}}"),
        ]

        for input_text, expected in tests:
            result = fix_pt_months_in_texts(input_text)
            assert result == expected, f"Failed for: {input_text}"

    # Tests for fix_pt_months_in_refs

    def test_temp_in_wiki_texts(self):
        """Test fixing months in references within wiki text"""
        input_text = 'test: <ref name="AHFS2016">{{Citar web|titulo=Charcoal, Activated|url=https://www.drugs.com/monograph/charcoal-activated.html|publicado=The American Society of Health-System Pharmacists|acessodata=8 December 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 December 2016}}</ref>\n<ref name="AHFS2016">{{Citar web|acessodata=8 December 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 December 2016}} xxxxxxxxxxxxxxxx {{Webarchive|url=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|date=21 December 2016}}</ref>'
        expected = 'test: <ref name="AHFS2016">{{Citar web|titulo=Charcoal, Activated|url=https://www.drugs.com/monograph/charcoal-activated.html|publicado=The American Society of Health-System Pharmacists|acessodata=8 de dezembro 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 de dezembro 2016}}</ref>\n<ref name="AHFS2016">{{Citar web|acessodata=8 de dezembro 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 de dezembro 2016}} xxxxxxxxxxxxxxxx {{Webarchive|url=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|date=21 de dezembro 2016}}</ref>'
        result = fix_pt_months_in_refs(input_text)
        assert result == expected

    def test_temp_in_ref(self):
        """Test fixing months in a single reference"""
        input_text = '<ref name="test" group="notes">{{cite web|date=25  December 2016 |}}</ref>'
        expected = '<ref name="test" group="notes">{{cite web|date=25 de dezembro 2016|}}</ref>'
        result = fix_pt_months_in_refs(input_text)
        assert result == expected

    # Tests for rm_ref_spaces

    def test_remove_spaces_after_dot_before_ref(self):
        """Test removing spaces after dot before ref"""
        input_text = "This is a sentence . <ref>Reference</ref>"
        expected = "This is a sentence.<ref>Reference</ref>"
        assert rm_ref_spaces(input_text) == expected

    def test_remove_spaces_after_comma_before_ref(self):
        """Test removing spaces after comma before ref"""
        input_text = "Hello , <ref>Ref</ref>"
        expected = "Hello,<ref>Ref</ref>"
        assert rm_ref_spaces(input_text) == expected

    def test_multiple_refs_together(self):
        """Test multiple refs together"""
        input_text = "Sentence . <ref>First</ref> <ref>Second</ref>"
        expected = "Sentence.<ref>First</ref> <ref>Second</ref>"
        assert rm_ref_spaces(input_text) == expected

    def test_no_spaces_should_remain_unchanged(self):
        """Test text without spaces remains unchanged"""
        input_text = "Correct.<ref>Already OK</ref>"
        expected = "Correct.<ref>Already OK</ref>"
        assert rm_ref_spaces(input_text) == expected

    def test_no_ref_no_change(self):
        """Test text without ref remains unchanged"""
        input_text = "This is a sentence . Without ref."
        expected = input_text
        assert rm_ref_spaces(input_text) == expected

    # Tests for utility functions

    def test_start_end(self):
        """Test start_end function"""
        assert start_end("{{template}}") is True
        assert start_end("{{template") is False
        assert start_end("template}}") is False
        assert start_end("template") is False
