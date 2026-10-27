import logging

from .wtp_mapping import WtpRefs

logger = logging.getLogger(__name__)


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
