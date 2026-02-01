"""
"""
import re
import wikitextparser as wtp


def make_line(refs) -> str:
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


def get_refs(text):
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


def remove_short_refs(text: str) -> str:
    """
    Remove short citations from text
    """
    parsed = wtp.parse(text)
    for tag in parsed.get_tags():
        if tag.name == "ref" and not tag.contents:
            tag.string = ""
    text = parsed.string
    # Remove multiple newlines
    text = re.sub(r'\n+', '\n', text)
    return text


def add_line_to_temp(line, new_text):
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
            value = remove_short_refs(value)
            line = f"{value}\n{line.strip()}"
        # ---
        template.set_arg("refs", f"\n{line}")
        # ---
        new_text = parsed.string
        # ---
        return new_text
    # ---
    return new_text


def mv_es_refs(text):
    # ---
    refs, new_text = get_refs(text)
    # ---
    line = make_line(refs)
    # ---
    new_text = add_line_to_temp(line, new_text)
    # ---
    if new_text.find(line.strip()) == -1:
        return text
    # ---
    return new_text
