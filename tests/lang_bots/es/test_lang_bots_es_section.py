"""Tests for Spanish section helper (es_section.py)

Converted from tests/es_bots/esSectionTest.php
"""
import pytest
from src.lang_bots.es.es_section_bot import es_section


class TestEsSection:
    """Test cases for Spanish section helper"""

    def test_text_already_has_traducido_ref(self):
        """When text already contains the old template {{Traducido ref|...}}"""
        text = "Some content\n{{Traducido ref|title|oldid=12345}}\nMore content"
        expected = "Some content\n{{Traducido ref|title|oldid=12345}}\nMore content"
        result = es_section("Source Title", text, "12345")
        assert result == expected

    def test_text_already_has_traducido_ref_mdwiki(self):
        """When text already contains the new template {{Traducido ref MDWIKI|...}}"""
        text = "Content here\n{{Traducido ref MDWIKI|en|Title|oldid=12345}}\nEnd"
        result = es_section("Source Title", text, "12345")
        assert result == text

    def test_add_traducido_ref_after_enlaces_externos(self):
        """When no template exists and "Enlaces externos" section is present"""
        text = "Content here\n== Enlaces externos ==\n* [http://example.com Link]\n"
        # Note: The expected output includes the current date, so we'll just check for the template
        result = es_section("Source Title", text, "12345")
        assert "{{Traducido ref MDWiki|en|Source Title|oldid=12345" in result
        assert result.count("== Enlaces externos ==") == 1

    def test_add_enlaces_externos_section_with_traducido_ref(self):
        """When no "Enlaces externos" section exists"""
        text = "Content here\nMore content"
        result = es_section("Source Title", text, "12345")
        assert "{{Traducido ref MDWiki|en|Source Title|oldid=12345" in result
        assert "== Enlaces externos ==" in result

    def test_enlaces_externos_with_extra_spaces(self):
        """When "Enlaces externos" contains extra spaces"""
        text = "Content\n== Enlaces   externos ==\n"
        result = es_section("Source Title", text, "12345")
        assert "== Enlaces   externos ==" in result
        assert "{{Traducido ref MDWiki|en|Source Title|oldid=12345" in result

    def test_empty_text(self):
        """With empty text"""
        text = ""
        result = es_section("Source Title", text, "12345")
        assert "{{Traducido ref MDWiki|en|Source Title|oldid=12345" in result
        assert "== Enlaces externos ==" in result

    def test_traducido_ref_with_spaces(self):
        """When template contains extra spaces inside"""
        text = "{{ Traducido ref | mdwiki | title | oldid=12345 }}"
        result = es_section("Source Title", text, "12345")
        # Should not modify since template already exists
        assert result == text

    def test_es_section_already_has_template(self):
        """Already has template - no change"""
        old_text = "Texto con \n== Enlaces externos ==\n{{Traducido ref MDWiki|en|Título|oldid=111|trad=|fecha=2020}} ya incluido."
        result = es_section("Otro título", old_text, "222")
        assert result == old_text

    def test_es_section_with_external_links(self):
        """Add template after existing external links section"""
        old_text = "Intro.\n== Enlaces externos ==\n\n* [http://example.com Ejemplo]"
        result = es_section("Artículo de prueba", old_text, "123")
        assert "{{Traducido ref MDWiki|en|Artículo de prueba|oldid=123" in result
        assert "== Enlaces externos ==" in result

    def test_es_section_without_external_links(self):
        """Without external links section - should add it"""
        old_text = "Intro sin sección."
        result = es_section("Artículo de prueba", old_text, "321")
        assert "{{Traducido ref MDWiki|en|Artículo de prueba|oldid=321" in result
        assert "== Enlaces externos ==" in result

    def test_es_section(self):
        """With existing external links section"""
        old_text = "Intro sin sección.\n== Enlaces externos ==\n"
        result = es_section("Artículo de prueba", old_text, "321")
        assert "{{Traducido ref MDWiki|en|Artículo de prueba|oldid=321" in result

    def test_already_contains_traducido_ref_template(self):
        """Text already contains Traducido ref template"""
        text = "Some content {{Traducido ref|param=value}} more content"
        expected = "Some content {{Traducido ref|param=value}} more content"
        result = es_section('Source Title', text, '123')
        assert result == expected

    def test_add_after_existing_enlaces_externos(self):
        """Adding template after existing external links section"""
        text = "Content before\n== Enlaces externos ==\nMore content"
        result = es_section('Source Title', text, '123')
        assert "{{Traducido ref MDWiki|en|Source Title|oldid=123" in result
        assert "More content" in result

    def test_append_new_section_when_none_exists(self):
        """Append new section when none exists"""
        text = "No external links section here"
        result = es_section('Source Title', text, '123')
        assert "{{Traducido ref MDWiki|en|Source Title|oldid=123" in result
        assert "== Enlaces externos ==" in result

    def test_multiple_enlaces_externos_sections(self):
        """Multiple "Enlaces externos" sections (should only modify first)"""
        text = "== Enlaces externos ==\nFirst section\n== Enlaces externos ==\nSecond section"
        result = es_section('Source Title', text, '123')
        # Should only add template after first occurrence
        assert result.count("{{Traducido ref MDWiki") == 1
        assert "First section\n== Enlaces externos ==" in result

    def test_case_variations_in_section_header(self):
        """Case variations in "Enlaces externos" """
        text = "== ENLACES EXTERNOS =="
        result = es_section('Source Title', text, '123')
        assert "== ENLACES EXTERNOS ==" in result
        assert "{{Traducido ref MDWiki|en|Source Title|oldid=123" in result

    def test_whitespace_around_section_header(self):
        """Leading/trailing whitespace around section header"""
        text = "  ==   Enlaces externos   ==  "
        result = es_section('test!', text, '520')
        assert "==   Enlaces externos   ==" in result
        assert "{{Traducido ref MDWiki|en|test!|oldid=520" in result

    def test_template_case_insensitive_match(self):
        """Template already exists in lowercase/uppercase variations"""
        text = "Something {{traducido REF mdwiki|Title|oldid=100}} end"
        result = es_section("Source Title", text, "100")
        # Should not modify existing template
        assert result == text

    def test_section_without_newline_after(self):
        """When "Enlaces externos" exists but has no newline after"""
        text = "Intro\n== Enlaces externos =="
        result = es_section("Test", text, "200")
        assert "{{Traducido ref MDWiki|en|Test|oldid=200" in result

    def test_multiple_templates_already_present(self):
        """When template already exists multiple times"""
        text = "{{Traducido ref|one}}\n{{Traducido ref|two}}"
        expected = "{{Traducido ref|one}}\n{{Traducido ref|two}}"
        result = es_section("Source Title", text, "300")
        assert result == expected
