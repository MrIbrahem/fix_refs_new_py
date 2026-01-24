"""Tests for Spanish language bot (es_helpers.py)

Converted from tests/es_bots/es_refsTest.php and tests/es_bots/es_monthsTest.php
"""
from src.lang_bots.es.es_refs import mv_es_refs
from src.lang_bots.es.es_helpers import (
    fix_es_months_in_texts,
    fix_es_months_in_refs,
    start_end,
)
from src.bots.months import make_date_new_val_es


class TestEsMonths:
    """Test cases for Spanish month translation"""

    def test_make_date_new_val_es_with_full_date(self):
        """Test converting full date with month to Spanish"""
        assert make_date_new_val_es("July 25, 1975") == "25 de julio de 1975"

    def test_temp_in_wikitexts(self):
        """Test fixing months in references within wikitext"""
        input_text = ('test: <ref name="AHFS2016">{{Citar web|titulo=Charcoal, Activated|url=https://www.drugs.com/monograph/charcoal-activated.html|publicado=The American Society of Health-System Pharmacists|acessodata=8 December 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 December 2016}}</ref>\n'
                      '<ref name="AHFS2016">{{Citar web|acessodata=8 December 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 December 2016}} xxxxxxxxxxxxxxxx {{Webarchive|url=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|date=21 December 2016}}</ref>')

        expected = ('test: <ref name="AHFS2016">{{Citar web|titulo=Charcoal, Activated|url=https://www.drugs.com/monograph/charcoal-activated.html|publicado=The American Society of Health-System Pharmacists|acessodata=8 de diciembre de 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 de diciembre de 2016}}</ref>\n'
                    '<ref name="AHFS2016">{{Citar web|acessodata=8 de diciembre de 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 de diciembre de 2016}} xxxxxxxxxxxxxxxx {{Webarchive|url=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|date=21 de diciembre de 2016}}</ref>')

        result = fix_es_months_in_refs(input_text)
        assert result == expected

    def test_temp_in_ref(self):
        """Test fixing months in single reference"""
        input_text = '<ref name="test" group="notes">{{cite web|date=25  December 2016 |}}</ref>'
        expected = '<ref name="test" group="notes">{{cite web|date=25 de diciembre de 2016|}}</ref>'
        result = fix_es_months_in_refs(input_text)
        assert result == expected


class TestSpanishHelpers:
    """Test cases for Spanish language helpers"""

    # Tests for make_date_new_val_es

    def test_make_date_new_val_es_with_full_date(self):
        """Test converting full date to Spanish format"""
        assert make_date_new_val_es("July 25, 1975") == "25 de julio de 1975"

    def test_make_date_new_val_es_month_year(self):
        """Test converting month and year to Spanish format"""
        assert make_date_new_val_es("January 2023") == "enero de 2023"

    def test_make_date_new_val_es_day_month_year(self):
        """Test converting day month year to Spanish format"""
        assert make_date_new_val_es("10 January, 2023") == "10 de enero de 2023"

    # Tests for fix_es_months_in_texts

    def test_temp_in_templates(self):
        """Test fixing months in templates"""
        input_text = '{{cite web|date=10 January, 2023|}}'
        expected = '{{cite web|date=10 de enero de 2023|}}'
        result = fix_es_months_in_texts(input_text)
        assert result == expected

    def test_temp_in_templates_more(self):
        """Test fixing months in multiple templates"""
        input_text = '{{cite web|date=10 January, 2023|}} {{cite book|time = test|date = 10 de enero de 2023 }}'
        expected = '{{cite web|date=10 de enero de 2023|}} {{cite book|time = test|date = 10 de enero de 2023 }}'
        result = fix_es_months_in_texts(input_text)
        assert result == expected

    def test_fix_months_in_templates_all_months(self):
        """Test translating all months to Spanish"""
        tests = [
            ("{{cite web|date=January 2023|}}", "{{cite web|date=enero de 2023|}}"),
            ("{{cite web|date=February 15, 2023|}}", "{{cite web|date=15 de febrero de 2023|}}"),
            ("{{cite web|date=March 2023|}}", "{{cite web|date=marzo de 2023|}}"),
            ("{{cite web|date=April 5, 2023|}}", "{{cite web|date=5 de abril de 2023|}}"),
            ("{{cite web|date=May 2023|}}", "{{cite web|date=mayo de 2023|}}"),
            ("{{cite web|date=June 20, 2023|}}", "{{cite web|date=20 de junio de 2023|}}"),
            ("{{cite web|date=July 2023|}}", "{{cite web|date=julio de 2023|}}"),
            ("{{cite web|date=August 10, 2023|}}", "{{cite web|date=10 de agosto de 2023|}}"),
            ("{{cite web|date=September 2023|}}", "{{cite web|date=septiembre de 2023|}}"),
            ("{{cite web|date=October 30, 2023|}}", "{{cite web|date=30 de octubre de 2023|}}"),
            ("{{cite web|date=November 2023|}}", "{{cite web|date=noviembre de 2023|}}"),
            ("{{cite web|date=December 25, 2023|}}", "{{cite web|date=25 de diciembre de 2023|}}"),
        ]

        for input_text, expected in tests:
            result = fix_es_months_in_texts(input_text)
            assert result == expected, f"Failed for: {input_text}"

    # Tests for fix_es_months_in_refs

    def test_temp_in_wiki_texts(self):
        """Test fixing months in references within wiki text"""
        input_text = 'test: <ref name="AHFS2016">{{Citar web|titulo=Charcoal, Activated|url=https://www.drugs.com/monograph/charcoal-activated.html|publicado=The American Society of Health-System Pharmacists|acessodata=8 December 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 December 2016}}</ref>\n<ref name="AHFS2016">{{Citar web|acessodata=8 December 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 December 2016}} xxxxxxxxxxxxxxxx {{Webarchive|url=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|date=21 December 2016}}</ref>'
        expected = 'test: <ref name="AHFS2016">{{Citar web|titulo=Charcoal, Activated|url=https://www.drugs.com/monograph/charcoal-activated.html|publicado=The American Society of Health-System Pharmacists|acessodata=8 de diciembre de 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 de diciembre de 2016}}</ref>\n<ref name="AHFS2016">{{Citar web|acessodata=8 de diciembre de 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 de diciembre de 2016}} xxxxxxxxxxxxxxxx {{Webarchive|url=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|date=21 de diciembre de 2016}}</ref>'
        result = fix_es_months_in_refs(input_text)
        assert result == expected

    def test_temp_in_ref(self):
        """Test fixing months in a single reference"""
        input_text = '<ref name="test" group="notes">{{cite web|date=25  December 2016 |}}</ref>'
        expected = '<ref name="test" group="notes">{{cite web|date=25 de diciembre de 2016|}}</ref>'
        result = fix_es_months_in_refs(input_text)
        assert result == expected

    # Tests for utility functions

    def test_start_end(self):
        """Test start_end function"""
        assert start_end("{{template}}") is True
        assert start_end("{{template") is False
        assert start_end("template}}") is False
        assert start_end("template") is False

    def test_mv_es_refs_basic(self):
        """Test mv_es_refs basic functionality"""
        text = 'Some text <ref name="test">{{cite web|date=January 2023}}</ref>'
        result = mv_es_refs(text)

        assert isinstance(result, str)
        assert len(result) > 0
