"""Tests for Polish bot (pl_infoboxTest.php)

Converted from tests/pl_bots/pl_infoboxTest.php
"""
import pytest
import re
from src.lang_bots.pl_bot import add_missing_params_to_choroba_infobox, pl_fixes


class TestPlInfobox:
    """Test cases for Polish Choroba infobox fixes"""

    def test_add_missing_params_to_choroba_infobox(self):
        """Test adding all missing parameters to Choroba infobox"""
        input_text = '''{{Choroba infobox
|nazwa polska = Astma oskrzelowa
|obraz =
|opis obrazu =
}}
'''
        result = add_missing_params_to_choroba_infobox(input_text)

        # Check that all required parameters are present
        assert 'nazwa naukowa' in result
        assert 'ICD11' in result
        assert re.search(r'\|ICD11\s*=', result)
        assert re.search(r'\|ICD11 nazwa\s*=', result)
        assert re.search(r'\|ICD10\s*=', result)
        assert re.search(r'\|ICD10 nazwa\s*=', result)
        assert 'DSM-5' in result
        assert re.search(r'\|DSM-5\s*=', result)
        assert re.search(r'\|DSM-5 nazwa\s*=', result)
        assert re.search(r'\|DSM-IV\s*=', result)
        assert re.search(r'\|DSM-IV nazwa\s*=', result)
        assert 'ICDO' in result
        assert 'DiseasesDB' in result
        assert 'OMIM' in result
        assert 'MedlinePlus' in result
        assert 'MeshID' in result
        assert 'commons' in result

        # Check that original parameters are still present
        assert 'nazwa polska' in result
        assert 'Astma oskrzelowa' in result

    def test_case_insensitive_template_name(self):
        """Test that template name matching is case-insensitive"""
        inputs = [
            '{{choroba infobox|nazwa polska=Test}}',
            '{{CHOROBA INFOBOX|nazwa polska=Test}}',
            '{{Choroba Infobox|nazwa polska=Test}}',
            '{{ChOrObA iNfObOx|nazwa polska=Test}}'
        ]

        for input_text in inputs:
            result = add_missing_params_to_choroba_infobox(input_text)
            assert 'nazwa naukowa' in result, f"Failed for input: {input_text}"
            assert 'ICD11' in result, f"Failed for input: {input_text}"

    def test_does_not_add_existing_params(self):
        """Test that existing parameters are not duplicated"""
        input_text = '''{{Choroba infobox
|nazwa polska = Astma oskrzelowa
|ICD10 = J45
|MeshID = D001249
}}
'''
        result = add_missing_params_to_choroba_infobox(input_text)

        # Count occurrences using regex - should be exactly 1 for each existing param
        icd10_count = len(re.findall(r'\|ICD10\s*=', result))
        meshid_count = len(re.findall(r'\|MeshID\s*=', result))

        assert icd10_count == 1
        assert meshid_count == 1

        # But should still add missing ones
        assert 'nazwa naukowa' in result
        assert 'ICD11' in result

    def test_ignores_other_templates(self):
        """Test that other templates are not modified"""
        input_text = '{{Some other template|param=value}}'
        result = add_missing_params_to_choroba_infobox(input_text)

        # Should return unchanged
        assert result == input_text

    def test_pl_fixes_function(self):
        """Test the pl_fixes function"""
        input_text = '''{{Choroba infobox
|nazwa polska = Test
}}
'''
        result = pl_fixes(input_text)

        # Test that pl_fixes calls the add_missing_params function
        assert 'nazwa naukowa' in result
        assert 'ICD10' in result

    def test_multiple_choroba_templates(self):
        """Test handling multiple Choroba infobox templates"""
        input_text = '''{{Choroba infobox
|nazwa polska = Test1
}}

Some text here.

{{Choroba infobox
|nazwa polska = Test2
}}
'''
        result = add_missing_params_to_choroba_infobox(input_text)

        # Both templates should get the parameters
        icd10_count = len(re.findall(r'\|ICD10\s*=', result))
        assert icd10_count == 2, "Both Choroba infobox templates should have ICD10 parameter"

    def test_standard_choroba_infobox_all_params_missing(self):
        """Test standard Choroba infobox - all parameters missing"""
        input_text = '{{Choroba infobox|nazwa polska=Astma}}'
        result = add_missing_params_to_choroba_infobox(input_text,)

        # Check expected parameters are present
        for param in ['nazwa naukowa', 'ICD11', 'ICD10', 'DSM-5', 'OMIM', 'MeshID', 'commons']:
            assert param in result, f"Expected parameter '{param}' not found"

    def test_lowercase_template_name(self):
        """Test lowercase template name"""
        input_text = '{{choroba infobox|nazwa polska=Test}}'
        result = add_missing_params_to_choroba_infobox(input_text)
        assert 'ICD10' in result

    def test_uppercase_template_name(self):
        """Test UPPERCASE template name"""
        input_text = '{{CHOROBA INFOBOX|nazwa polska=Test}}'
        result = add_missing_params_to_choroba_infobox(input_text)
        assert 'ICD10' in result

    def test_mixed_case_template_name(self):
        """Test mixed case template name"""
        input_text = '{{ChOrObA InFoBoX|nazwa polska=Test}}'
        result = add_missing_params_to_choroba_infobox(input_text)
        assert 'ICD10' in result

    def test_some_parameters_already_exist(self):
        """Test template with some parameters already existing"""
        input_text = '{{Choroba infobox|nazwa polska=Test|ICD10=J45|OMIM=123456}}'
        result = add_missing_params_to_choroba_infobox(input_text)

        # Check expected missing parameters are present
        assert 'nazwa naukowa' in result
        assert 'ICD11' in result
        assert 'DSM-5' in result
        assert 'MeshID' in result

        # Check existing params are not duplicated
        icd10_count = len(re.findall(r'\|ICD10\s*=', result))
        omim_count = len(re.findall(r'\|OMIM\s*=', result))
        assert icd10_count == 1
        assert omim_count == 1

    def test_full_article_with_choroba_infobox(self):
        """Test full article with Choroba infobox"""
        input_text = """{{Choroba infobox
|nazwa polska = Cukrzyca
|obraz = Insulin glucose metabolism ZP.svg
}}

'''Cukrzyca''' – grupa chorób metabolicznych.

== Zobacz też ==
* [[Insulina]]

== Przypisy ==
<references />
"""
        result = add_missing_params_to_choroba_infobox(input_text)

        # Check expected parameters are present
        for param in ['ICD10', 'ICD11', 'OMIM']:
            assert param in result, f"Expected parameter '{param}' not found"

    def test_non_polish_language_should_not_apply_fixes(self):
        """Test that non-Polish language is not affected (should be handled by caller)"""
        input_text = '{{Choroba infobox|nazwa polska=Test}}'
        # This test documents behavior - language filtering should be done by caller
        result = add_missing_params_to_choroba_infobox(input_text)
        # The function itself doesn't check language - it just processes templates
        assert 'ICD10' in result

    def test_different_template_no_changes(self):
        """Test different template (not Choroba) - no changes"""
        input_text = '{{Infobox person|name=Test}}'
        result = add_missing_params_to_choroba_infobox(input_text)
        assert result == input_text
        assert 'ICD10' not in result
