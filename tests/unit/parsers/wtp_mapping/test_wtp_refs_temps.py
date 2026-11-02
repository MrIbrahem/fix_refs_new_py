from src.fix_refs.parsers.wtp_mapping.wtp_refs_temps import WtpRefsTemps

BASIC = (
    "{{Infobox\n"
    "| a = x<ref name=A>{{cite web|url=http://a}}</ref>\n"
    "| b = y<ref name=A />\n"
    "}}\n"
    "BODY first.<ref name=A /> Second.<ref name=A />\n"
)

# ---------------- WtpRefsTemps ----------------


class TestWtpRefsTemps:
    def test_template_vs_body_split(self):
        refs = WtpRefsTemps.load(BASIC)
        assert len(refs.tpl_refs) == 2
        assert len(refs.body_refs) == 2
        assert list(refs.tpl_full_refs) == ["A"]
        assert refs.body_full_refs == {}
        assert refs.body_short_names == {"A"}
