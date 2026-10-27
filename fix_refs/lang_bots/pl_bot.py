"""
Polish-specific bot fixes
"""

from __future__ import annotations

import logging

import wikitextparser as wtp

logger = logging.getLogger(__name__)


class PolishBot:
    """Bot for Polish Wikipedia language-specific fixes."""

    def add_missing_params_to_choroba_infobox(self, text: str) -> str:
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

    def pl_fixes(self, text: str) -> str:
        """Apply Polish-specific fixes to text

        Args:
            text: WikiText content

        Returns:
            Fixed text
        """
        text = self.add_missing_params_to_choroba_infobox(text)
        return text


def add_missing_params_to_choroba_infobox(text: str) -> str:
    """Legacy wrapper for PolishBot.add_missing_params_to_choroba_infobox."""
    return PolishBot().add_missing_params_to_choroba_infobox(text)


def pl_fixes(text: str) -> str:
    """Legacy wrapper for PolishBot.pl_fixes."""
    return PolishBot().pl_fixes(text)


__all__ = [
    "PolishBot",
    "add_missing_params_to_choroba_infobox",
    "pl_fixes",
]
