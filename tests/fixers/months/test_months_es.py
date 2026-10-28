"""
Tests for months.py for Spanish language
"""

from src.fix_refs.fixers.months import MonthTranslator


class TestMakeDateNewValEs:
    """Test Spanish date wrapper"""

    def test_all_months_spanish(self):
        """Test all months in Spanish with year"""
        months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        for month in months:
            result = MonthTranslator().new_date(f"{month} 2020", "es")
            assert "de 2020" in result

    def test_spanish_month(self):
        """Test Spanish month conversion in full date"""
        result = MonthTranslator().new_date("January 2020", "es")
        assert result == "enero de 2020"

    def test_spanish_full_date_with_de(self):
        """Test Spanish full date uses 'de'"""
        result = MonthTranslator().new_date("January 2020", "es")
        assert "enero de 2020" == result

    def test_spanish_full_date_with_day(self):
        """Test Spanish full date with day"""
        result = MonthTranslator().new_date("15 January 2020", "es")
        assert "15 de enero de 2020" == result

    def test_date_with_full_date(self):
        """Test full date transformation"""
        assert MonthTranslator().new_date("July 25, 1975", "es") == "25 de julio de 1975"

    def test_date_with_month_and_year(self):
        """Test month and year transformation"""
        assert MonthTranslator().new_date("November 2022", "es") == "noviembre de 2022"

    def test_date_with_comma_year(self):
        """Test comma year format"""
        assert MonthTranslator().new_date("January, 2024", "es") == "enero de 2024"

    def test_date_with_day_month_year(self):
        """Test day month year with comma"""
        assert MonthTranslator().new_date("10 March, 2023", "es") == "10 de marzo de 2023"

    def test_date_with_day_month_year_lower(self):
        """Test lowercase month"""
        assert MonthTranslator().new_date("10 march, 2023", "es") == "10 de marzo de 2023"

    def test_date_with_day_month_year_no_comma(self):
        """Test day month year without comma"""
        assert MonthTranslator().new_date("5 May 1999", "es") == "5 de mayo de 1999"

    def test_date_with_month_day_year(self):
        """Test month day year format"""
        assert MonthTranslator().new_date("August 15, 2010", "es") == "15 de agosto de 2010"

    def test_date_with_month_day_year_no_comma(self):
        """Test month day year without comma"""
        assert MonthTranslator().new_date("April 1 2020", "es") == "1 de abril de 2020"

    def test_date_with_single_digit_day(self):
        """Test single digit day"""
        assert MonthTranslator().new_date("June 3, 2005", "es") == "3 de junio de 2005"

    def test_date_with_mixed_case(self):
        """Test uppercase month"""
        assert MonthTranslator().new_date("DECEMBER 20, 2015", "es") == "20 de diciembre de 2015"

    def test_date_with_no_match_returns_original(self):
        """Test non-matching date format"""
        assert MonthTranslator().new_date("Invalid Date", "es") == "Invalid Date"
        assert MonthTranslator().new_date("2023/10/15", "es") == "2023/10/15"

    def test_date_with_empty_input(self):
        """Test empty input"""
        assert MonthTranslator().new_date("", "es") == ""

    def test_date_with_whitespace_only(self):
        """Test whitespace only"""
        assert MonthTranslator().new_date("   ", "es") == ""

    def test_date_with_partial_month_name(self):
        """Test abbreviated month name (no translation)"""
        assert MonthTranslator().new_date("Jan 2023", "es") == "Jan 2023"

    def test_date_with_non_english_month(self):
        """Test non-English month (no translation)"""
        assert MonthTranslator().new_date("يناير 2023", "es") == "يناير 2023"

    def test_date_with_day_month_year_spaces(self):
        """Test extra spaces in input"""
        assert MonthTranslator().new_date("  7   July   2023  ", "es") == "7 de julio de 2023"

    def test_date_with_month_day_year_spaces(self):
        """Test spaces in month day year format"""
        assert MonthTranslator().new_date("September  12,  2023", "es") == "12 de septiembre de 2023"


class TestEsMonthsNewDate:
    """Test cases for Spanish month translation"""

    def test_make_date_new_val_es_with_full_date(self):
        """Test converting full date to Spanish format"""
        assert MonthTranslator().new_date("July 25, 1975", "es") == "25 de julio de 1975"

    def test_make_date_new_val_es_month_year(self):
        """Test converting month and year to Spanish format"""
        assert MonthTranslator().new_date("January 2023", "es") == "enero de 2023"

    def test_make_date_new_val_es_day_month_year(self):
        """Test converting day month year to Spanish format"""
        assert MonthTranslator().new_date("10 January, 2023", "es") == "10 de enero de 2023"


class TestEsMonthsInRefs:
    """Test cases for Spanish month translation"""

    def test_temp_in_wikitexts(self):
        """Test fixing months in references within wikitext"""
        input_text = (
            'test: <ref name="AHFS2016">{{Citar web|titulo=Charcoal, Activated|url=https://www.drugs.com/monograph/charcoal-activated.html|publicado=The American Society of Health-System Pharmacists|acessodata=8 December 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 December 2016}}</ref>\n'
            '<ref name="AHFS2016">{{Citar web|acessodata=8 December 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 December 2016}} xxxxxxxxxxxxxxxx {{Webarchive|url=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|date=21 December 2016}}</ref>'
        )

        expected = (
            'test: <ref name="AHFS2016">{{Citar web|titulo=Charcoal, Activated|url=https://www.drugs.com/monograph/charcoal-activated.html|publicado=The American Society of Health-System Pharmacists|acessodata=8 de diciembre de 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 de diciembre de 2016}}</ref>\n'
            '<ref name="AHFS2016">{{Citar web|acessodata=8 de diciembre de 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 de diciembre de 2016}} xxxxxxxxxxxxxxxx {{Webarchive|url=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|date=21 de diciembre de 2016}}</ref>'
        )

        result = MonthTranslator().fix_months_in_refs(input_text, "es")
        assert result == expected

    def test_temp_in_ref(self):
        """Test fixing months in single reference"""
        input_text = '<ref name="test" group="notes">{{cite web|date=25  December 2016 |}}</ref>'
        expected = '<ref name="test" group="notes">{{cite web|date=25 de diciembre de 2016|}}</ref>'
        result = MonthTranslator().fix_months_in_refs(input_text, "es")
        assert result == expected

    def test_temp_in_wiki_texts(self):
        """Test fixing months in references within wiki text"""
        input_text = 'test: <ref name="AHFS2016">{{Citar web|titulo=Charcoal, Activated|url=https://www.drugs.com/monograph/charcoal-activated.html|publicado=The American Society of Health-System Pharmacists|acessodata=8 December 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 December 2016}}</ref>\n<ref name="AHFS2016">{{Citar web|acessodata=8 December 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 December 2016}} xxxxxxxxxxxxxxxx {{Webarchive|url=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|date=21 December 2016}}</ref>'
        expected = 'test: <ref name="AHFS2016">{{Citar web|titulo=Charcoal, Activated|url=https://www.drugs.com/monograph/charcoal-activated.html|publicado=The American Society of Health-System Pharmacists|acessodata=8 de diciembre de 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 de diciembre de 2016}}</ref>\n<ref name="AHFS2016">{{Citar web|acessodata=8 de diciembre de 2016|urlmorta=live|arquivourl=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|arquivodata=21 de diciembre de 2016}} xxxxxxxxxxxxxxxx {{Webarchive|url=https://web.archive.org/web/20161221011707/https://www.drugs.com/monograph/charcoal-activated.html|date=21 de diciembre de 2016}}</ref>'
        result = MonthTranslator().fix_months_in_refs(input_text, "es")
        assert result == expected

    def test_temp_in_ref2(self):
        """Test fixing months in a single reference"""
        input_text = '<ref name="test" group="notes">{{cite web|date=25  December 2016 |}}</ref>'
        expected = '<ref name="test" group="notes">{{cite web|date=25 de diciembre de 2016|}}</ref>'
        result = MonthTranslator().fix_months_in_refs(input_text, "es")
        assert result == expected


class TestEsMonthsInText:
    """Test cases for Spanish language helpers"""

    def test_temp_in_templates(self):
        """Test fixing months in templates"""
        input_text = "{{cite web|date=10 January, 2023|}}"
        expected = "{{cite web|date=10 de enero de 2023|}}"
        result = MonthTranslator().fix_months_in_texts(input_text, "es")
        assert result == expected

    def test_temp_in_templates_more(self):
        """Test fixing months in multiple templates"""
        input_text = "{{cite web|date=10 January, 2023|}} {{cite book|time = test|date = 10 de enero de 2023 }}"
        expected = "{{cite web|date=10 de enero de 2023|}} {{cite book|time = test|date = 10 de enero de 2023 }}"
        result = MonthTranslator().fix_months_in_texts(input_text, "es")
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
            result = MonthTranslator().fix_months_in_texts(input_text, "es")
            assert result == expected, f"Failed for: {input_text}"
