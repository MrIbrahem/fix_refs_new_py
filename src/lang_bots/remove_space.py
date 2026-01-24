"""

"""

import re


def match_it(text, charters):
    charters = re.escape(charters)
    m = re.search(rf'(</ref>|\/>)\s*([{charters}]\s*)$', text, flags=re.UNICODE)
    if m:
        return m.group(2)
    return None


def get_parts(newtext, charters):
    pattern = r'(.+?)(\n\n|\Z)'
    parts = re.findall(pattern, newtext, re.DOTALL)
    # ---
    new_parts = []
    # ---
    print(f"{len(parts)=}")
    # ---
    for p in parts:
        chart = match_it(p[0], charters)
        if chart:
            new_parts.append((p[0], chart))
    # ---
    print(f"{len(new_parts)=}")
    # ---
    return new_parts


def remove_spaces_between_last_word_and_beginning_of_ref(newtext: str, lang: str) -> str:

    # Define punctuation marks based on language
    dots = r".,。।"

    if lang == "hy":
        dots = r".,。।։:"

    newtext = re.sub(r">\s*<ref", r"><ref", newtext)

    parts = get_parts(newtext, dots)
    # ---
    for part, charter in parts:
        # ---
        # print([part])
        print(f"{charter=}")
        # ---
        regline = r"((?:\s*<ref[\s\S]+?(?:<\/ref|\/)>)+)"
        # ---
        # find last ref group
        last_ref = re.findall(regline, part, re.DOTALL)
        # ---
        print(f"{len(last_ref)=}")
        # ---
        if last_ref:
            # ---
            ref_text = last_ref[-1]
            # ---
            end_part = f"{ref_text}{charter}"
            # ---
            if part.endswith(end_part):
                # ---
                print("endswith ")
                # ---s
                new_part = part.split(end_part)[0].strip() + f"{ref_text.strip()}{charter}"
                # ---
                newtext = newtext.replace(part, new_part)

    return newtext


__all__ = [
    "remove_spaces_between_last_word_and_beginning_of_ref",
]
