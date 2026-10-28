"""
Tests for Spanish language bot (es_refs.py)
"""

from src.fix_refs.lang_bots.es.es_refs import SpanishRefMover


class TestSpanishRefMover:
    def test_mv_es_refs_basic(self):
        """Test mv_es_refs basic functionality"""
        text = 'Some text <ref name="test">{{cite web|date=January 2023}}</ref>'
        result = SpanishRefMover().mv_es_refs(text)

        assert isinstance(result, str)
        assert len(result) > 0
