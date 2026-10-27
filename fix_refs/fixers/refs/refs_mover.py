import logging
from dataclasses import dataclass, field
from functools import cached_property

import wikitextparser as wtp

logger = logging.getLogger(__name__)


def _inside(span, outer):
    return outer[0] <= span[0] and span[1] <= outer[1]


@dataclass
class WtpTemplates:
    text: str
    parsed: wtp.WikiText = field(init=False, repr=False)

    def __post_init__(self):
        self.parsed = wtp.parse(self.text)

    @cached_property
    def all_spans(self) -> list[tuple[int, int]]:
        return [t.span for t in self.parsed.templates]

    @cached_property
    def ref_spans(self) -> list[tuple[int, int]]:
        return [r.span for r in self.parsed.get_tags("ref")]

    @cached_property
    def top_tpls(self) -> list[tuple[int, int]]:
        """Top-level templates: not inside another template or a ref tag."""
        spans = [
            s for s in self.all_spans
            if not any(o != s and _inside(s, o) for o in self.all_spans)
            and not any(_inside(s, rs) for rs in self.ref_spans)
        ]
        logger.debug("Found %d top-level templates", len(spans))
        return spans

    def contains(self, span) -> bool:
        """Return True if the span is inside a top-level template."""
        return any(_inside(span, t) for t in self.top_tpls)


@dataclass
class WtpRefs:
    text: str
    tpls: WtpTemplates = field(init=False, repr=False)
    parsed: wtp.WikiText = field(init=False, repr=False)

    # name -> '<ref name="x">...</ref>'
    full_refs: dict[str, str] = field(init=False, default_factory=dict)
    # name -> spans of short refs (no content)
    short_refs: dict[str, list[tuple[int, int]]] = field(init=False, default_factory=dict)

    def __post_init__(self):
        self.tpls = WtpTemplates(self.text)
        self.parsed = self.tpls.parsed
        self._collect()

    # ---------- helpers ----------
    @staticmethod
    def get_name(r) -> str:
        return (r.get_attr("name") or "").strip(" \"'")

    @staticmethod
    def make_full(name: str, content: str) -> str:
        return f'<ref name="{name}">{content}</ref>'

    @staticmethod
    def make_short(name: str) -> str:
        return f'<ref name="{name}" />'

    @cached_property
    def all_refs(self) -> list:
        return self.parsed.get_tags("ref")

    @cached_property
    def tpl_refs(self) -> list:
        return [r for r in self.all_refs if self.tpls.contains(r.span)]

    @cached_property
    def body_refs(self) -> list:
        return [r for r in self.all_refs if not self.tpls.contains(r.span)]

    # ---------- collecting refs ----------
    def _collect(self):
        for r in self.all_refs:
            name = self.get_name(r)
            content = (r.contents or "").strip()
            if not name:
                logger.debug("Skipping unnamed ref at %s", r.span)
                continue
            if content:
                self.full_refs.setdefault(name, self.make_full(name, content))
            else:
                self.short_refs.setdefault(name, []).append(r.span)
        logger.info(
            "Collected %d full refs and %d short ref names",
            len(self.full_refs), len(self.short_refs),
        )

    @cached_property
    def tpl_full_refs(self) -> dict[str, str]:
        """Full refs found inside templates only."""
        out = {}
        for r in self.tpl_refs:
            name, content = self.get_name(r), (r.contents or "").strip()
            if name and content:
                out.setdefault(name, self.make_full(name, content))
        return out

    @cached_property
    def body_full_refs(self) -> dict[str, str]:
        """Full refs found in the body only."""
        out = {}
        for r in self.body_refs:
            name, content = self.get_name(r), (r.contents or "").strip()
            if name and content:
                out.setdefault(name, self.make_full(name, content))
        return out

    @cached_property
    def body_short_names(self) -> set[str]:
        return {
            self.get_name(r) for r in self.body_refs
            if self.get_name(r) and not (r.contents or "").strip()
        }


class RefsMover:
    """Moves full refs from templates into the body and shortens them in templates."""

    def __init__(self, text: str, prefer_body_version: bool = False):
        self.text = text
        self.prefer_body_version = prefer_body_version
        self.refs = WtpRefs(text)
        self.placed: set[str] = set()
        self.edits: list[tuple[int, int, str]] = []

    def _plan_body_edits(self):
        """Body: first occurrence becomes full, the rest become short."""
        tpl_full = self.refs.tpl_full_refs
        for r in self.refs.body_refs:
            name = self.refs.get_name(r)
            if name not in tpl_full:
                continue
            if name not in self.placed:
                self.placed.add(name)
                if self.prefer_body_version and (r.contents or "").strip():
                    logger.debug("Keeping body version of ref %r", name)
                    continue
                logger.debug("Placing full ref %r in body at %s", name, r.span)
                self.edits.append((*r.span, tpl_full[name]))
            else:
                logger.debug("Shortening duplicate body ref %r at %s", name, r.span)
                self.edits.append((*r.span, self.refs.make_short(name)))

        unused = set(tpl_full) - self.placed
        for name in unused:
            logger.warning("Ref %r not used in body; left in template", name)

    def _plan_template_edits(self):
        """Templates: shorten only the refs that were placed in the body."""
        for r in self.refs.tpl_refs:
            name = self.refs.get_name(r)
            if name in self.placed:
                logger.debug("Shortening template ref %r at %s", name, r.span)
                self.edits.append((*r.span, self.refs.make_short(name)))

    def _apply_edits(self) -> str:
        """Apply edits from end to start so spans stay valid."""
        text = self.text
        for start, end, new in sorted(self.edits, key=lambda e: e[0], reverse=True):
            text = text[:start] + new + text[end:]
        return text

    def run(self) -> str:
        if not self.refs.tpl_full_refs:
            logger.info("No full refs inside templates; nothing to move")
            return self.text

        self._plan_body_edits()
        self._plan_template_edits()
        logger.info("Applying %d edits", len(self.edits))
        return self._apply_edits()


def move_refs_from_templates(text: str, prefer_body_version: bool = False) -> str:
    return RefsMover(text, prefer_body_version).run()
