"""
Polish-specific bot fixes
"""

import wikitextparser as wtp


def add_missing_params_to_choroba_infobox(text: str) -> str:
    """Add missing medical code parameters to Choroba infobox templates

    Args:
        text: WikiText content

    Returns:
        Text with missing parameters added
    """
    parsed = wtp.parse(text)

    params_to_add = [
        "nazwa naukowa",
        "ICD11",
        "ICD11 nazwa",
        "ICD10",
        "ICD10 nazwa",
        "DSM-5",
        "DSM-5 nazwa",
        "DSM-IV",
        "DSM-IV nazwa",
        "ICDO",
        "DiseasesDB",
        "OMIM",
        "MedlinePlus",
        "MeshID",
        "commons",
    ]

    for template in parsed.templates:
        template_name = template.name.strip()
        if template_name.lower() == "choroba infobox":
            existing_params = {arg.name.strip().lower() for arg in template.arguments}
            for param_name in params_to_add:
                if param_name.lower() not in existing_params:
                    template.set_arg(param_name, "")

    return parsed.string


def pl_fixes(text: str) -> str:
    """Apply Polish-specific fixes to text

    Args:
        text: WikiText content

    Returns:
        Fixed text
    """
    text = add_missing_params_to_choroba_infobox(text)
    return text
