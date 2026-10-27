# test_refs_mover.py
import logging

from src.fix_refs.fixers.refs.refs_mover import RefsMover
from src.fix_refs.fixers.refs.wtp_mapping import (
    WtpRefs,
    WtpTemplates,
)

BASIC = (
    "{{Infobox\n"
    "| a = x<ref name=A>{{cite web|url=http://a}}</ref>\n"
    "| b = y<ref name=A />\n"
    "}}\n"
    "BODY first.<ref name=A /> Second.<ref name=A />\n"
)


def split_head_body(text: str):
    head, _, body = text.partition("BODY")
    return head, body


def move_refs_from_templates(text: str, prefer_body_version: bool = False) -> str:
    return RefsMover(text, prefer_body_version).run()


# ---------------- WtpTemplates ----------------


class TestWtpTemplates:
    def test_top_tpls_excludes_nested_and_templates_inside_refs(self):
        text = "{{Outer|x={{Inner}}}} text<ref>{{cite web|url=u}}</ref>"
        tpls = WtpTemplates(text)
        assert len(tpls.top_tpls) == 1
        start, end = tpls.top_tpls[0]
        assert text[start:end] == "{{Outer|x={{Inner}}}}"

    def test_contains(self):
        text = "{{T|a<ref name=A>x</ref>}} body<ref name=B>y</ref>"
        tpls = WtpTemplates(text)
        refs = tpls.parsed.get_tags("ref")
        assert tpls.contains(refs[0].span) is True
        assert tpls.contains(refs[1].span) is False

    def test_no_templates(self):
        assert WtpTemplates("plain text").top_tpls == []


# ---------------- WtpRefs ----------------


class TestWtpRefs:
    def test_full_and_short_collection(self):
        refs = WtpRefs(BASIC)
        assert list(refs.full_refs) == ["A"]
        assert refs.full_refs["A"] == '<ref name="A">{{cite web|url=http://a}}</ref>'
        assert len(refs.short_refs["A"]) == 3

    def test_template_vs_body_split(self):
        refs = WtpRefs(BASIC)
        assert len(refs.tpl_refs) == 2
        assert len(refs.body_refs) == 2
        assert list(refs.tpl_full_refs) == ["A"]
        assert refs.body_full_refs == {}
        assert refs.body_short_names == {"A"}

    def test_unnamed_refs_are_skipped(self):
        refs = WtpRefs("{{T|a<ref>no name</ref>}}")
        assert refs.full_refs == {}
        assert refs.short_refs == {}

    def test_name_with_quotes_is_normalized(self):
        refs = WtpRefs("text<ref name='A'>c</ref>")
        assert "A" in refs.full_refs

    def test_helpers(self):
        assert WtpRefs.make_full("A", "c") == '<ref name="A">c</ref>'
        assert WtpRefs.make_short("A") == '<ref name="A" />'


# ---------------- RefsMover ----------------


class TestRefsMover:
    def test_basic_move(self):
        result = move_refs_from_templates(BASIC)
        head, body = split_head_body(result)

        assert '<ref name="A">' not in head
        assert head.count('<ref name="A" />') == 2
        assert body.count('<ref name="A">') == 1
        assert body.index('<ref name="A">') < body.index('<ref name="A" />')
        assert result.count("{{cite web|url=http://a}}") == 1

    def test_works_with_any_template_name(self):
        text = BASIC.replace("Infobox", "Taxobox")
        result = move_refs_from_templates(text)
        head, body = split_head_body(result)
        assert '<ref name="A">' in body
        assert '<ref name="A">' not in head

    def test_no_refs_in_templates_returns_text_unchanged(self):
        text = "{{T|a=1}}\nBody<ref name=A>x</ref><ref name=A />"
        assert move_refs_from_templates(text) == text

    def test_no_templates_returns_text_unchanged(self):
        text = "Just text<ref name=A>x</ref>"
        assert move_refs_from_templates(text) == text

    def test_ref_not_in_body_stays_in_template(self, caplog):
        text = "{{T\n| a = x<ref name=A>full A</ref>\n}}\nBODY no refs here.\n"
        with caplog.at_level(logging.WARNING):
            result = move_refs_from_templates(text)
        assert result == text
        assert "not used in body" in caplog.text

    def test_only_used_refs_are_shortened(self):
        text = "{{T\n| a = x<ref name=A>full A</ref>\n| b = y<ref name=B>full B</ref>\n}}\nBODY text<ref name=A />\n"
        result = move_refs_from_templates(text)
        head, body = split_head_body(result)
        assert '<ref name="A" />' in head
        assert "<ref name=B>full B</ref>" in head  # untouched
        assert '<ref name="A">full A</ref>' in body

    def test_unnamed_ref_in_template_untouched(self):
        text = (
            "{{T\n| a = x<ref>{{cite web|url=u}}</ref>\n| b = y<ref name=A>full A</ref>\n}}\nBODY text<ref name=A />\n"
        )
        result = move_refs_from_templates(text)
        assert "<ref>{{cite web|url=u}}</ref>" in result
        assert result.count('<ref name="A">full A</ref>') == 1

    def test_body_full_version_is_replaced_by_default(self):
        text = (
            "{{T\n| a = x<ref name=A>template version</ref>\n}}\n"
            "BODY text<ref name=A>body version</ref> more<ref name=A />\n"
        )
        result = move_refs_from_templates(text)
        assert "template version" in result
        assert "body version" not in result

    def test_prefer_body_version_keeps_body_full(self):
        text = (
            "{{T\n| a = x<ref name=A>template version</ref>\n}}\n"
            "BODY text<ref name=A>body version</ref> more<ref name=A />\n"
        )
        result = move_refs_from_templates(text, prefer_body_version=True)
        head, body = split_head_body(result)
        assert "template version" not in result
        assert "<ref name=A>body version</ref>" in body
        assert '<ref name="A" />' in head

    def test_duplicate_full_refs_in_body_become_short(self):
        text = (
            "{{T\n| a = x<ref name=A>full A</ref>\n}}\nBODY one<ref name=A>full A</ref> two<ref name=A>full A</ref>\n"
        )
        result = move_refs_from_templates(text)
        _, body = split_head_body(result)
        assert body.count('<ref name="A">full A</ref>') == 1
        assert body.count('<ref name="A" />') == 1

    def test_idempotent(self):
        once = move_refs_from_templates(BASIC)
        twice = move_refs_from_templates(once)
        assert once == twice

    def test_class_and_function_agree(self):
        assert RefsMover(BASIC).run() == move_refs_from_templates(BASIC)

    def test_edits_are_applied_without_corrupting_other_text(self):
        result = move_refs_from_templates(BASIC)
        assert result.startswith("{{Infobox\n| a = x")
        assert result.endswith('Second.<ref name="A" />\n')


# ---------------- Realistic article ----------------

ARTICLE = """{{Infobox aandoening
| naam = Enkelbreuk
| symptomen = pijn<ref name=OI2019>{{cite web |title=Ankle Fractures |url=https://orthoinfo.aaos.org/}}</ref>
| complicaties = x<ref name=OI2019 /><ref name=Stat2019>{{cite journal |last1=Wire |title=Ankle Fractures |pmid=31194464}}</ref>
| diagnose = y<ref name=Stat2019 />
}}
Een '''enkelbreuk''' is een breuk.<ref name=OI2019 /> Symptomen.<ref name=OI2019 /> Complicaties.<ref name=OI2019 /><ref name="Stat2019">{{Citeer journal|achternaam=Wire|pmid=31194464}}</ref>

Oorzaken.<ref name=Stat2019 />

== Referenties ==
{{reflist}}
"""


class TestRealisticArticle:
    def test_each_name_has_exactly_one_full_ref(self):
        result = move_refs_from_templates(ARTICLE)
        assert result.count('<ref name="OI2019">') == 1
        assert result.count('<ref name="Stat2019">') == 1

    def test_infobox_contains_only_short_refs(self):
        result = move_refs_from_templates(ARTICLE)
        infobox_end = result.index("}}\nEen")
        infobox = result[:infobox_end]
        assert "{{cite web" not in infobox
        assert "{{cite journal" not in infobox
        assert '<ref name="OI2019" />' in infobox
        assert '<ref name="Stat2019" />' in infobox

    def test_full_refs_are_in_lead_paragraph(self):
        result = move_refs_from_templates(ARTICLE)
        lead = result.split("\n\n")[0]
        assert '<ref name="OI2019">' in lead
        assert '<ref name="Stat2019">' in lead

    def test_reflist_preserved(self):
        assert "{{reflist}}" in move_refs_from_templates(ARTICLE)
