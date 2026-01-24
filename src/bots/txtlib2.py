"""
Template extraction utilities
"""

import wikitextparser as wtp


def extract_templates_and_params(text):
    # ---
    result = []
    # ---
    parsed = wtp.parse(text)
    templates = parsed.templates
    # ---
    for template in templates:
        # ---
        if not template:
            continue
        # ---
        name = template.name.strip()
        # ---
        pa_item = template.string
        # ---
        if not pa_item or pa_item.strip() == "":
            continue
        # ---
        params = {}
        for param in template.arguments:
            value = str(param.value)
            key = str(param.name)
            key = key.strip()
            params[key] = value
        # ---
        namestrip = name
        # ---
        ficrt = {
            "name": f"قالب:{name}",
            "namestrip": namestrip,
            "params": params,
            "item": pa_item,
        }
        # ---
        result.append(ficrt)
    # ---
    return result
