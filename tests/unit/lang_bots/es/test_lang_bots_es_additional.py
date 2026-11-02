"""Tests for Spanish bot additional tests (esTest.php, es_months_new_valueTest.php)

Converted from tests/es_bots/esTest.php and tests/es_bots/es_months_new_valueTest.php
"""

import re

from src.fix_refs.fixers.months import MonthTranslator
from src.fix_refs.lang_bots.es.es_bot import SpanishTemplateFixer


def fix_temps_wrap(text: str) -> str:
    """Wrapper function that combines _fix_temps and fix_months_in_refs(result, "es")"""
    result = SpanishTemplateFixer()._fix_temps(text)
    result = MonthTranslator().fix_months_in_refs(result, "es")
    result = re.sub(r"\s*=\s*", "=", result)
    return result


class TestEsTest:
    """Test cases for Spanish bot template transformation"""

    def test_fix_temps_and_months_1(self):
        """Test template transformation with journal citation"""
        old = "{{cite journal|vauthors=Dowd SE|title=Confirmation |journal=Applied |volume=64 |issue=9 |pages=3332–5 |year=1998 |pmid=9726879 |pmc=106729 |doi=10|bibcode=1|url-status=dead}}"
        new = "{{cita publicación|vauthors=Dowd SE|título=Confirmation|journal=Applied|volumen=64|issue=9|páginas=3332–5|año=1998|pmid=9726879|pmc=106729|doi=10|bibcode=1}}"
        assert fix_temps_wrap(old) == new

    def test_fix_temps_and_months_2(self):
        """Test template transformation inside ref tag"""
        old = "hi!. <ref name=Doed1998>{{cite journal|vauthors=Dowd SE|title=Confirmation |journal=Applied |volume=64 |issue=9 |pages=3332–5 |year=1998 |pmid=9726879 |pmc=106729 |doi=10|bibcode=1}}</ref> dodo"
        new = "hi!. <ref name=Doed1998>{{cita publicación|vauthors=Dowd SE|título=Confirmation|journal=Applied|volumen=64|issue=9|páginas=3332–5|año=1998|pmid=9726879|pmc=106729|doi=10|bibcode=1}}</ref> dodo"
        assert fix_temps_wrap(old) == new

    def test_fix_temps_and_months_3(self):
        """Test template transformation with multiple authors"""
        old = "hi!. <ref name=Doed1998>{{cite journal |vauthors=Dowd SE, Gerba CP, Pepper IL |title=Confirmation of the Human-Pathogenic Microsporidia Enterocytozoon bieneusi, Encephalitozoon intestinalis, and Vittaforma corneae in Water |journal=Applied and Environmental Microbiology |volume=64 |issue=9 |pages=3332–5 |year=1998 |pmid=9726879 |pmc=106729 |doi=10.1128/AEM.64.9.3332-3335.1998|bibcode=1998ApEnM..64.3332D }}</ref>yemen"
        new = "hi!. <ref name=Doed1998>{{cita publicación|vauthors=Dowd SE, Gerba CP, Pepper IL|título=Confirmation of the Human-Pathogenic Microsporidia Enterocytozoon bieneusi, Encephalitozoon intestinalis, and Vittaforma corneae in Water|journal=Applied and Environmental Microbiology|volumen=64|issue=9|páginas=3332–5|año=1998|pmid=9726879|pmc=106729|doi=10.1128/AEM.64.9.3332-3335.1998|bibcode=1998ApEnM..64.3332D}}</ref>yemen"
        assert fix_temps_wrap(old) == new

    def test_fix_temps_and_months_4(self):
        """Test template transformation with web citation"""
        old = "<ref>{{cite journal|vauthors=Dowd SE|title=Confirmation|url-status=dead}} {{cite web |title=CDC - DPDx - Microsporidiosis |url=https://www.cdc.gov/dpdx/microsporidiosis/index.html |website=www.cdc.gov |accessdate=11 December 2024 |language=en-us |date=29 May 2019}}</ref>"
        new = "<ref>{{cita publicación|vauthors=Dowd SE|título=Confirmation}} {{cita web|título=CDC - DPDx - Microsporidiosis|url=https://www.cdc.gov/dpdx/microsporidiosis/index.html|sitioweb=www.cdc.gov|fechaacceso=11 de diciembre de 2024|idioma=en-us|fecha=29 de mayo de 2019}}</ref>"
        assert fix_temps_wrap(old) == new

    def test_fix_temps_and_months_5(self):
        """Test date transformation"""
        old = "<ref>{{cite journal |date=July 25, 1975}} {{cite journal |date=May 25, 1975}}</ref>"
        new = "<ref>{{cita publicación|fecha=25 de julio de 1975}} {{cita publicación|fecha=25 de mayo de 1975}}</ref>"
        assert fix_temps_wrap(old) == new

    def test_fix_temps_and_months_6(self):
        """Test archive date transformation"""
        old = "<ref>{{cite web |access-date=10 January 2022 |archive-date=9 January 2021}} {{Webarchive|url=https://web.archive.org/web/20221014134136/https://books.google.ca/books?id=4gznEkPjNJMC&pg=PA640|date=10 December 2022}}</ref>"
        new = "<ref>{{cita web|fechaacceso=10 de enero de 2022|fechaarchivo=9 de enero de 2021}} {{Webarchive|url=https://web.archive.org/web/20221014134136/https://books.google.ca/books?id=4gznEkPjNJMC&pg=PA640|date=10 de diciembre de 2022}}</ref>"
        assert fix_temps_wrap(old) == new

    def test_fix_temps_and_months_with_month(self):
        """Test month transformation in date"""
        old = "<ref>{{cite journal|title=Study|journal=Nature|date=January 2005|pages=20–25}}</ref>"
        new = "<ref>{{cita publicación|título=Study|journal=Nature|fecha=enero de 2005|páginas=20–25}}</ref>"
        assert fix_temps_wrap(old) == new

    def test_fix_temps_and_months_different_template(self):
        """Test book template transformation"""
        old = "{{cite book|title=Medical Book|year=2010|pages=100–105}}"
        new = "{{cita libro|título=Medical Book|año=2010|páginas=100–105}}"
        assert fix_temps_wrap(old) == new

    def test_fix_temps_and_months_no_change(self):
        """Test text without templates or English months"""
        old = "Texto sin plantillas ni meses en inglés."
        new = "Texto sin plantillas ni meses en inglés."
        assert fix_temps_wrap(old) == new

    def test_fix_temps_inside_ref(self):
        """Test already Spanish template inside ref"""
        old = "<ref name=OI2018>{{cita web|título=Shoulder Trauma (Fractures and Dislocations)|url=https://orthoinfo.aaos.org/en/diseases--conditions/shoulder-trauma-fractures-and-dislocations/|sitioweb=OrthoInfo - AAOS|fechaacceso=7 de noviembre de 2018|fechaarchivo=19 de diciembre de 2019|urlarchivo=https://web.archive.org/web/20191219132225/https://orthoinfo.aaos.org/en/diseases--conditions/shoulder-trauma-fractures-and-dislocations/}}</ref>"
        new = "<ref name=OI2018>{{cita web|título=Shoulder Trauma (Fractures and Dislocations)|url=https://orthoinfo.aaos.org/en/diseases--conditions/shoulder-trauma-fractures-and-dislocations/|sitioweb=OrthoInfo - AAOS|fechaacceso=7 de noviembre de 2018|fechaarchivo=19 de diciembre de 2019|urlarchivo=https://web.archive.org/web/20191219132225/https://orthoinfo.aaos.org/en/diseases--conditions/shoulder-trauma-fractures-and-dislocations/}}</ref>"
        assert fix_temps_wrap(old) == new

    def test_fix_temps_with_webarchive_temp(self):
        """Test with Webarchive template"""
        old = "<ref name=OI2018>{{cita web|título=Shoulder Trauma (Fractures and Dislocations)|url=https://orthoinfo.aaos.org/en/diseases--conditions/shoulder-trauma-fractures-and-dislocations/|sitioweb=OrthoInfo - AAOS|fechaacceso=7 de noviembre de 2018|fechaarchivo=19 de diciembre de 2019|urlarchivo=https://web.archive.org/web/20191219132225/https://orthoinfo.aaos.org/en/diseases--conditions/shoulder-trauma-fractures-and-dislocations/}} {{Webarchive|url=https://web.archive.org/web/20191219132225/https://orthoinfo.aaos.org/en/diseases--conditions/shoulder-trauma-fractures-and-dislocations/|date=19 de diciembre de 2019}}</ref>"
        new = "<ref name=OI2018>{{cita web|título=Shoulder Trauma (Fractures and Dislocations)|url=https://orthoinfo.aaos.org/en/diseases--conditions/shoulder-trauma-fractures-and-dislocations/|sitioweb=OrthoInfo - AAOS|fechaacceso=7 de noviembre de 2018|fechaarchivo=19 de diciembre de 2019|urlarchivo=https://web.archive.org/web/20191219132225/https://orthoinfo.aaos.org/en/diseases--conditions/shoulder-trauma-fractures-and-dislocations/}} {{Webarchive|url=https://web.archive.org/web/20191219132225/https://orthoinfo.aaos.org/en/diseases--conditions/shoulder-trauma-fractures-and-dislocations/|date=19 de diciembre de 2019}}</ref>"
        assert fix_temps_wrap(old) == new

    def test_fix_temps_alone(self):
        """Test template without ref tags"""
        # The input is already a Spanish template, so it should remain unchanged
        # (except for whitespace normalization)
        old = "{{cita web|título=Shoulder Trauma (Fractures and Dislocations)|url=https://orthoinfo.aaos.org/en/diseases--conditions/shoulder-trauma-fractures-and-dislocations/|sitioweb=OrthoInfo - AAOS|fechaacceso=7 de noviembre de 2018|fechaarchivo=19 de diciembre de 2019|urlarchivo=https://web.archive.org/web/20191219132225/https://orthoinfo.aaos.org/en/diseases--conditions/shoulder-trauma-fractures-and-dislocations/}}"
        new = "{{cita web|título=Shoulder Trauma (Fractures and Dislocations)|url=https://orthoinfo.aaos.org/en/diseases--conditions/shoulder-trauma-fractures-and-dislocations/|sitioweb=OrthoInfo - AAOS|fechaacceso=7 de noviembre de 2018|fechaarchivo=19 de diciembre de 2019|urlarchivo=https://web.archive.org/web/20191219132225/https://orthoinfo.aaos.org/en/diseases--conditions/shoulder-trauma-fractures-and-dislocations/}}"
        assert fix_temps_wrap(old) == new
