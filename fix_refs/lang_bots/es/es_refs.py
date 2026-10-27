""" """

from __future__ import annotations

import logging

import wikitextparser as wtp

from .es_helpers import SpanishHelpers

logger = logging.getLogger(__name__)


class SpanishRefMover:
    """Mover for Spanish references into {{listaref}} or {{reflist}} templates."""

    def __init__(self, spanish_helpers: SpanishHelpers | None = None) -> None:
        self.spanish_helpers = spanish_helpers or SpanishHelpers()

    def make_line(self, refs) -> str:
        line = "\n"
        # ---
        for g, gag in refs.items():
            # ---
            for name, ref in gag.items():
                la = f'<ref name="{name}">{ref}</ref>\n'
                if g != "":
                    la = f'<ref group="{g}" name="{name}">{ref}</ref>\n'
                # ---
                line += la
        # ---
        line = line.strip()
        # ---
        return line

    def get_refs(self, text):
        # ---
        parsed = wtp.parse(text)
        tags = parsed.get_tags()
        # ---
        numb = 0
        refs = {}
        # ---
        refs_to_name = {}
        # ---
        for x in tags:
            # ---
            if not x or not x.name:
                continue
            if x.name != "ref":
                continue
            if not x.contents:
                continue
            # ---
            conts = x.contents.strip()
            # ---
            attrs = x.attrs
            # ---
            name = refs_to_name.get(conts) or attrs.get("name", "").strip()
            # ---
            group = attrs.get("group", "").strip()
            # ---
            if group not in refs:
                refs[group] = {}
            # ---
            if not name:
                numb += 1
                name = f"autogen_{numb}"
                x.set_attr("name", name)
            # ---
            if name not in refs[group]:
                refs[group][name] = x.contents
            # ---
            refs_to_name[conts] = name
            # ---
            asas = f'<ref name="{name}" />'
            if group != "":
                asas = f'<ref group="{group}" name="{name}" />'
            # ---
            x.string = asas
        # ---
        new_text = parsed.string
        # ---
        return refs, new_text

    def add_line_to_temp(self, line, new_text):
        # ---
        parsed = wtp.parse(new_text)
        # ---
        for template in reversed(parsed.templates):
            # ---
            if not template:
                continue
            # ---
            template_name = str(template.normal_name()).strip()
            # ---
            if template_name.lower() not in ["reflist", "listaref"]:
                continue
            # ---
            refs_arg = template.get_arg("refs")
            # ---
            value = refs_arg.value.strip() if refs_arg and refs_arg.value.strip() else ""
            # ---
            if refs_arg and value:
                value = self.spanish_helpers.remove_short_refs(value)
                line = f"{value}\n{line.strip()}"
            # ---
            template.set_arg("refs", f"\n{line}")
            # ---
            new_text = parsed.string
            # ---
            return new_text
        # ---
        return new_text

    def mv_es_refs(self, text):
        # ---
        refs, new_text = self.get_refs(text)
        # ---
        line = self.make_line(refs)
        # ---
        new_text = self.add_line_to_temp(line, new_text)
        # ---
        if new_text.find(line.strip()) == -1:
            return text
        # ---
        return new_text


__all__ = [
    "SpanishRefMover",
]
