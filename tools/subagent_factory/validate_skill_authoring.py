"""Validate skill/reference body authoring (Step 8) — status-gated.

Closes the Phase 6 authoring gap: ``generate_stubs`` scaffolds ``skills/<slug>/SKILL.md``
and ``references/<slug>.md`` placeholders, but nothing authors their bodies, so packages
sit at ``status: draft`` forever. This validator is the deterministic enforcement that lets
a package legitimately reach ``status: ready``.

The **status gate** is the non-breaking core:

- profile ``status: ready``  → every declared skill/reference must be authored
  (``status: ready`` frontmatter, no residual stub marker) — any missing/stub one is **FAIL**.
- profile ``status: draft`` (or anything else) → stubs are allowed — a single **WARN**
  summary reports ``authored N/M``; nothing fails.

So the 15 current packages (all ``status: draft``) only ever WARN here.

Independent of the status gate, an **authored** file (one whose frontmatter declares
``status: ready``) that is structurally invalid — bad ``authored-doc-v1`` frontmatter,
dangling ``provenance`` IDs, oversize body, or a leftover ``STATUS: STUB`` / ``TODO: author``
marker — is always a **FAIL**, even inside a draft package, so authored garbage cannot slip in.

Signature is ``(base) -> list[tuple[str, str]]`` of ``(level, message)`` with
``level ∈ {"FAIL", "WARN", "OK"}`` — the gate maps each to its ``fail``/``warn``/``ok`` sink.
Takes the package **base dir** (not a single file): the check spans many files keyed on the
profile's ``status`` + ``knowledge_partition``, like the scan blocks rather than a
``_TIER_ARTIFACTS`` row.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import jsonschema
import yaml

from tools.subagent_factory.generate_stubs import planned_slugs
from tools.subagent_factory.package_queries import (
    anchor_ids as _anchor_ids,
)
from tools.subagent_factory.package_queries import (
    claim_ids as _claim_ids,
)
from tools.subagent_factory.package_queries import (
    principle_ids,
)

_SCHEMA_PATH = Path(__file__).parent.parent.parent / "schemas" / "authored-doc-v1.schema.json"
_STUB_MARKERS = ("STATUS: STUB", "TODO: author")
_MAX_SKILL_LINES = 500  # Phase 6 limit: a skill body stays under 500 lines / 5,000 tokens.


def _load_yaml(path: Path) -> dict:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError):
        return {}


def _evidence_ids(base: Path) -> set[str]:
    data = _load_yaml(base / "evidence" / "evidence-records.yaml")
    return {
        str(e.get("evidence_id"))
        for e in (data.get("evidence_records") or [])
        if e.get("evidence_id")
    }


def _parse_frontmatter(text: str) -> dict | None:
    """Return the parsed YAML frontmatter block, or None if absent/unparseable."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[text.find("\n") + 1 : end]
    try:
        fm = yaml.safe_load(block)
    except yaml.YAMLError:
        return None
    return fm if isinstance(fm, dict) else None


class _IdSets:
    """Lazily-loaded referential ID universes for provenance cross-checks."""

    def __init__(self, base: Path):
        self.principles = principle_ids(base / "principles")
        self.claims = _claim_ids(base)
        self.evidence = _evidence_ids(base)
        self.anchors = _anchor_ids(base)


def _doc_state(path: Path, kind: str, ids: _IdSets, schema) -> tuple[str, list[str]]:
    """Classify one doc as ``missing`` | ``stub`` | ``authored`` | ``stale`` and validate the
    authored ones.

    A file counts as authored content when its frontmatter declares ``status: ready`` (state
    ``authored``) or ``status: stale`` (state ``stale`` — authored but flagged for re-authoring
    by Step 9). Anything else (no frontmatter, ``status: stub``) is ``stub``. The same structural
    + referential checks run on authored and stale docs; errors are returned only for those.
    """
    if not path.exists():
        return "missing", []
    text = path.read_text(encoding="utf-8")
    fm = _parse_frontmatter(text)
    status = str(fm.get("status", "")).lower() if fm else ""
    if not fm or status not in ("ready", "stale"):
        return "stub", []

    errors: list[str] = []
    errors.extend(f"frontmatter: {e.message}" for e in schema.iter_errors(fm))
    if str(fm.get("kind", "")) != kind:
        errors.append(f"frontmatter kind '{fm.get('kind')}' should be '{kind}'")

    prov = fm.get("provenance") or {}
    if isinstance(prov, dict):
        for field, universe in (
            ("principles", ids.principles),
            ("claims", ids.claims),
            ("evidence", ids.evidence),
            ("source_anchors", ids.anchors),
        ):
            for ref in prov.get(field) or []:
                if universe and ref not in universe:
                    errors.append(f"provenance.{field} '{ref}' does not resolve to a real ID")

    body = text[text.find("\n---", 3) + 4 :] if "\n---" in text else text
    for marker in _STUB_MARKERS:
        if marker in body:
            errors.append(f"status: ready but body still contains '{marker}'")
    if kind == "skill":
        if "## Procedure" not in body:
            errors.append("skill body missing a '## Procedure' section")
        n_lines = text.count("\n") + 1
        if n_lines > _MAX_SKILL_LINES:
            errors.append(f"skill body is {n_lines} lines (> {_MAX_SKILL_LINES} limit)")
    return ("stale" if status == "stale" else "authored"), errors


def _check_kind(
    base: Path,
    plan: list[tuple[str, str]],
    kind: str,
    subdir_for,
    ready: bool,
    ids: _IdSets,
    schema,
) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    authored = stubs = missing = stale = 0
    for _entry, slug in plan:
        state, errors = _doc_state(subdir_for(slug), kind, ids, schema)
        if errors:  # an authored/stale file with invalid content always FAILs (even in draft)
            out.extend(("FAIL", f"{kind} '{slug}': {e}") for e in errors)
        if state == "authored" and not errors:
            authored += 1
        elif state == "stale":
            stale += 1
            # Authored but flagged for re-authoring (Step 9). Surface, never FAIL — a stale doc
            # is human-reviewed/re-authored before next release, not a hard release block.
            if not errors:
                out.append(
                    (
                        "WARN",
                        f"{kind} '{slug}' is marked stale; re-author (author-skills) to refresh",
                    )
                )
        elif state == "missing":
            missing += 1
            if ready:
                out.append(
                    ("FAIL", f"{kind} '{slug}' has no file; status: ready requires it authored")
                )
        elif state == "stub":
            stubs += 1
            if ready:
                out.append(
                    ("FAIL", f"{kind} '{slug}' is still a stub; status: ready requires it authored")
                )

    total = len(plan)
    if total == 0:
        return out
    if not ready and (stubs or missing):
        out.append(
            (
                "WARN",
                f"{kind}s authored {authored}/{total} ({stubs} stub, {missing} missing, "
                f"{stale} stale); run `author-skills {base.name}` then set profile status: ready",
            )
        )
    elif authored == total:
        out.append(("OK", f"all {total} {kind}s authored"))
    return out


def validate_skill_authoring(subagent_dir: str | Path) -> list[tuple[str, str]]:
    """Return ``[(level, message)]`` with level ∈ {FAIL, WARN, OK}. Empty = nothing to check."""
    base = Path(subagent_dir)
    profile_path = base / "profile.yaml"
    if not profile_path.exists():
        return []
    profile = _load_yaml(profile_path)
    ready = str(profile.get("status", "draft")).lower() == "ready"
    skill_plan, ref_plan = planned_slugs(profile)
    if not skill_plan and not ref_plan:
        return []

    try:
        schema = jsonschema.Draft202012Validator(
            json.loads(_SCHEMA_PATH.read_text(encoding="utf-8"))
        )
    except (OSError, json.JSONDecodeError) as e:
        return [("FAIL", f"authored-doc schema load error: {e}")]

    ids = _IdSets(base)
    out: list[tuple[str, str]] = []
    out += _check_kind(
        base, skill_plan, "skill", lambda s: base / "skills" / s / "SKILL.md", ready, ids, schema
    )
    out += _check_kind(
        base, ref_plan, "reference", lambda s: base / "references" / f"{s}.md", ready, ids, schema
    )
    return out


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.validate_skill_authoring subagents/<slug>")
        sys.exit(1)
    findings = validate_skill_authoring(sys.argv[1])
    for level, msg in findings:
        print(f"[{level:4s}] {msg}")
    sys.exit(1 if any(level == "FAIL" for level, _ in findings) else 0)


if __name__ == "__main__":
    main()
