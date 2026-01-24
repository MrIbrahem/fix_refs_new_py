"""Tests for remove duplicate references (remove_duplicate_refs.py)

Converted from tests/Bots/remove_duplicate_refsTest.php
"""
import pytest
from src.bots.remove_duplicate_refs import (
    fix_refs_names,
    remove_duplicate_refs_with_attrs
)


class TestRemoveDuplicateRefs:
    """Test cases for removing duplicate references"""

    # Tests for fix_refs_names

    def test_fix_refs_names(self):
        """اختبارات دالة fix_refs_names"""
        tests = [
            # Case: Reference without attributes
            {
                "input": "<ref>Simple reference</ref>",
                "expected": "<ref>Simple reference</ref>"
            },
            # Case: Reference with name attribute in double quotes
            {
                "input": '<ref name="te1">Reference</ref>',
                "expected": '<ref name="te1">Reference</ref>'
            },
            # Case: Reference with name attribute in single quotes
            {
                "input": "<ref name='te2'>Reference</ref>",
                "expected": '<ref name="te2">Reference</ref>'
            },
            # Case: Reference with multiple attributes
            {
                "input": '<ref name="te3" group="notes">Reference</ref>',
                "expected": '<ref name="te3" group="notes">Reference</ref>'
            },
            # Case: Reference with attribute without value
            {
                "input": '<ref name>Reference</ref>',
                "expected": '<ref name="">Reference</ref>'
            },
            # Case: Reference with attribute containing internal quotes
            {
                "input": '<ref name="test\'quote">Reference</ref>',
                "expected": '<ref name="test\'quote">Reference</ref>'
            },
            # Case: Multiple references
            {
                "input": '<ref name="a">Ref1</ref> <ref name=\'b\'>Ref2</ref>',
                "expected": '<ref name="a">Ref1</ref> <ref name="b">Ref2</ref>'
            },
            # Case: Reference with mixed quote types
            {
                "input": '<ref name="te5" group=\'notes\'>Reference</ref>',
                "expected": '<ref name="te5" group="notes">Reference</ref>'
            }
        ]

        for test in tests:
            result = fix_refs_names(test['input'])
            assert result == test['expected'], f"Failed for: {test['input']}"

    # Tests for remove_duplicate_refs_with_attrs

    def test_remove_duplicate_refs(self):
        """اختبارات دالة remove_duplicate_refs_with_attrs"""
        tests = [
            [
                {
                    "input": 'test <ref name="PI2023">{{Cite web|title=DailyMed - SKYCLARYS- omaveloxolone capsule}}</ref> adv <ref name="PI2023" /> 205<ref name="PI2023">{{Cite web|title=DailyMed - SKYCLARYS- omaveloxolone capsule}} any test</ref>',
                    "expected": 'test <ref name="PI2023">{{Cite web|title=DailyMed - SKYCLARYS- omaveloxolone capsule}}</ref> adv <ref name="PI2023" /> 205<ref name="PI2023" />'
                },
            ],
            [
                {
                    "input": 'test <ref name="PI2023">{{Cite web|title=DailyMed - SKYCLARYS- omaveloxolone capsule}}</ref> adv 205<ref name="PI2023">{{Cite web|title=DailyMed - SKYCLARYS- omaveloxolone capsule}} any test</ref>',
                    "expected": 'test <ref name="PI2023">{{Cite web|title=DailyMed - SKYCLARYS- omaveloxolone capsule}}</ref> adv 205<ref name="PI2023" />'
                },
            ],
            # Case: Single reference without name
            [
                {
                    "input": "<ref>Reference without name1</ref>",
                    "expected": '<ref>Reference without name1</ref>'
                }
            ],
            # Case: Two references with same name
            [
                {
                    "input": '<ref name="test">Refs</ref> <ref name="test">Refs</ref>',
                    "expected": '<ref name="test">Refs</ref> <ref name="test" />'
                }
            ],
            # Case: Different references
            [
                {
                    "input": '<ref name="a">Ref1</ref> <ref name="b">Ref2</ref>',
                    "expected": '<ref name="a">Ref1</ref> <ref name="b">Ref2</ref>'
                }
            ],
            # Case: References with multiple attributes
            [
                {
                    "input": '<ref name="test" group="notes">Refs2</ref> <ref name="test" group="notes">Refs2</ref>',
                    "expected": '<ref name="test" group="notes">Refs2</ref> <ref name="test" group="notes" />'
                }
            ],
        ]

        for test_group in tests:
            for test in test_group:
                result = remove_duplicate_refs_with_attrs(test['input'])
                assert result == test['expected'], f"Failed for: {test['input']}"

    def test_remove_group_refs_diff(self):
        """Test removing duplicate refs with group attribute"""
        input_text = '<ref name="test" group="notes">Ref</ref> <ref name="test" group="notes">Ref</ref>'
        expected = '<ref name="test" group="notes">Ref</ref> <ref name="test" group="notes" />'
        result = remove_duplicate_refs_with_attrs(input_text)
        assert result == expected

    def test_remove_med_refs(self):
        """Test removing complex medical references"""
        input_text = '<ref name="PI2023">{{Cite web|title=DailyMed - SKYCLARYS- omaveloxolone capsule|url=https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=f1a1100e-8318-1596-e053-2995a90a533e|website=dailymed.nlm.nih.gov|access-date=24 May 2023|archive-date=1 July 2023|archive-url=https://web.archive.org/web/20230701174203/https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=f1a1100e-8318-1596-e053-2995a90a533e|url-status=live}}</ref> ଅତିକମରେ ୧୬ ବର୍ଷ ବୟସରେ ଏହା ବ୍ଯବହୃତ ହୁଏ ।<ref name="PI2023" /> ଏହା ପାଟିରେ ଦିଆଯାଏ ।<ref name="PI2023">{{Cite web|title=DailyMed - SKYCLARYS- omaveloxolone capsule|url=https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=f1a1100e-8318-1596-e053-2995a90a533e|website=dailymed.nlm.nih.gov|access-date=24 May 2023|archive-date=1 July 2023|archive-url=https://web.archive.org/web/20230701174203/https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=f1a1100e-8318-1596-e053-2995a90a533e|url-status=live}}<cite class="citation web cs1" data-ve-ignore="true">[https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=f1a1100e-8318-1596-e053-2995a90a533e "DailyMed - SKYCLARYS- omaveloxolone capsule"]. \'\'dailymed.nlm.nih.gov\'\'. [https://web.archive.org/web/20230701174203/https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=f1a1100e-8318-1596-e053-2995a90a533e Archived] from the original on 1 July 2023<span class="reference-accessdate">. Retrieved <span class="nowrap">24 May</span> 2023</span>.</cite></ref>'
        expected = '<ref name="PI2023">{{Cite web|title=DailyMed - SKYCLARYS- omaveloxolone capsule|url=https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=f1a1100e-8318-1596-e053-2995a90a533e|website=dailymed.nlm.nih.gov|access-date=24 May 2023|archive-date=1 July 2023|archive-url=https://web.archive.org/web/20230701174203/https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=f1a1100e-8318-1596-e053-2995a90a533e|url-status=live}}</ref> ଅତିକମରେ ୧୬ ବର୍ଷ ବୟସରେ ଏହା ବ୍ଯବହୃତ ହୁଏ ।<ref name="PI2023" /> ଏହା ପାଟିରେ ଦିଆଯାଏ ।<ref name="PI2023" />'
        result = remove_duplicate_refs_with_attrs(input_text)
        assert result == expected

    def test_remove_identical_refs_with_group_attribute(self):
        """Test removing identical refs with group attribute"""
        input_text = '<ref group="notes">Refs3</ref> <ref group="notes">Refs3</ref>'
        expected = '<ref group="notes">Refs3</ref> <ref group="notes" />'
        result = remove_duplicate_refs_with_attrs(input_text)
        assert result == expected
