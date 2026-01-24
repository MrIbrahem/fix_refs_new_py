"""
Template parser for WikiText
"""

import wikitextparser as wtp
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Template:
    """Represents a WikiText template"""

    name: str
    parameters: Dict[str, str] = field(default_factory=dict)
    original_text: str = ""

    def get(self, key: str, default: str = "") -> str:
        """Get a parameter value

        Args:
            key: Parameter name
            default: Default value if not found

        Returns:
            Parameter value or default
        """
        return self.parameters.get(key, default)

    def set(self, key: str, value: str) -> None:
        """Set a parameter value

        Args:
            key: Parameter name
            value: Parameter value
        """
        self.parameters[key] = value

    def to_string(self) -> str:
        """Convert template back to WikiText string

        Returns:
            WikiText template string
        """
        params = []
        # First, collect all positional params (numeric keys in order)
        positional = []
        named = []
        for key, value in self.parameters.items():
            if key.isdigit():
                positional.append((int(key), value))
            else:
                named.append((key, value))

        # Sort positional by their numeric index and output values only
        positional.sort()
        for _, value in positional:
            params.append(value)

        # Then output named params as key=value in insertion order
        for key, value in named:
            if key:
                params.append(f"{key}={value}")
            else:
                params.append(value)

        return f"{{{{{self.name}|{'|'.join(params)}}}}}"

    def get_original_text(self) -> str:
        """Get the original template text

        Returns:
            Original template string
        """
        return self.original_text


def get_template(text: str) -> Optional[Template]:
    """Extract first template from text

    Args:
        text: Text containing template

    Returns:
        Template object or None if not found
    """
    templates = get_templates(text)
    return templates[0] if templates else None


def get_templates(text: str) -> List[Template]:
    """Extract all templates from text

    Args:
        text: Text containing templates

    Returns:
        List of Template objects
    """
    if not text:
        return []

    templates: List[Template] = []

    wikicode = wtp.parse(text)

    for wt_template in wikicode.templates:
        name = wt_template.name.strip()

        parameters: Dict[str, str] = {}

        for i, arg in enumerate(wt_template.arguments):
            arg_name = arg.name.strip() if arg.name else None
            arg_value = arg.value

            if arg_name:
                parameters[arg_name] = arg_value.strip()
            else:
                parameters[str(i)] = arg_value.strip()

        original_text = str(wt_template)
        template = Template(name=name, parameters=parameters, original_text=original_text)
        templates.append(template)

    return templates
