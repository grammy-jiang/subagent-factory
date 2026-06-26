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
import re
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

# A frontmatter block that opened a fence but failed to parse — distinct from "no frontmatter
# at all" (None). A present-but-unparseable frontmatter is a fail-closed signal, not a stub.
_FRONTMATTER_CORRUPT = object()

# The closing frontmatter fence must be a full line (``^---$``, optional trailing whitespace),
# so a ``---`` appearing mid-line inside a value does not truncate parsing early. ``\r?`` before
# each newline tolerates CRLF line endings (a Windows-authored doc must not silently read as
# having no closing fence — that would fail-close a valid doc and, in adapter_policy_scan, blind
# the tool-grant scan).
_FENCE_CLOSE = re.compile(r"\r?\n---[ \t]*(?:\r?\n|$)")

# Recognise an *opening* fence even when preceded by a UTF-8 BOM and/or leading blank lines /
# whitespace, so such a doc is not misread as "no frontmatter" → stub. A genuinely fence-less
# doc (no leading ``---`` line at all) does not match and stays a legit stub. ``\r?`` tolerates a
# CRLF after the opening ``---``.
_FENCE_OPEN = re.compile(r"\A﻿?\s*---[ \t]*\r?\n")


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


def _parse_frontmatter(text: str):
    """Classify and parse the leading YAML frontmatter block.

    Returns one of:
    - ``None`` — no frontmatter at all (no opening fence): a legitimate stub.
    - ``_FRONTMATTER_CORRUPT`` — an opening fence is present but the block cannot be cleanly
      closed+parsed to a mapping (no closing fence, unparseable YAML, or non-mapping): a
      fail-closed signal (must FAIL, never silently demote to stub).
    - ``dict`` — the parsed frontmatter mapping.

    A leading UTF-8 BOM and/or leading blank lines/whitespace before the opening ``---`` are
    tolerated (so they do not masquerade as "no frontmatter"). The closing fence must be a full
    line (``^---$``) so a ``---`` embedded inside a value does not truncate the block early.
    "Opened a fence but couldn't cleanly close+parse it" is uniformly the corrupt/fail path.
    """
    open_m = _FENCE_OPEN.match(text)
    if open_m is None:
        return None
    # Opening fence found; everything from here must close+parse cleanly or fail closed.
    m = _FENCE_CLOSE.search(text, open_m.end() - 1)
    if m is None:
        return _FRONTMATTER_CORRUPT
    block = text[open_m.end() : m.start()]
    try:
        fm = yaml.safe_load(block)
    except yaml.YAMLError:
        return _FRONTMATTER_CORRUPT
    if fm is None:
        # An empty frontmatter block declares no status → treat as a (legit) stub.
        return None
    return fm if isinstance(fm, dict) else _FRONTMATTER_CORRUPT


def split_frontmatter(text: str) -> tuple[object, str]:
    """``(_parse_frontmatter(text), body)`` from ONE anchored fence split.

    The body boundary is the closing fence ``_parse_frontmatter`` used (a full ``^---$`` line
    anchored after the BOM/blank-tolerant opening fence), so a ``---`` line embedded inside a
    frontmatter value or in the body cannot truncate the split early. Callers that both read the
    frontmatter and rewrite the body (e.g. detect_stale --stamp) MUST use this rather than a
    private re-split, so the read path and the rewrite path can never disagree and corrupt a file.
    Body is ``""`` when there is no frontmatter or the block is unparseable/unclosed.
    """
    result = _parse_frontmatter(text)
    open_m = _FENCE_OPEN.match(text)
    if open_m is None:
        return result, ""
    close = _FENCE_CLOSE.search(text, open_m.end() - 1)
    if close is None:
        return result, ""
    return result, text[close.end() :]


def _source_loadable(path: Path, loader) -> bool:
    """True iff a provenance source file exists and parses cleanly.

    Distinguishes a *legitimately empty* universe (source present and parseable, just declares no
    ids) from a *failed-to-load* universe (file missing, or present-but-unparseable). The id-helper
    functions swallow both into an empty set, so the cross-check cannot tell them apart on its own;
    this re-derives the load status so a citation against a non-loadable source can fail closed.
    """
    if not path.exists():
        return False
    try:
        loader(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError, json.JSONDecodeError):
        return False
    return True


def _yaml_loadable(text: str) -> None:
    # The YAML provenance sources (principles, evidence) are mappings. A document that parses to a
    # non-mapping (top-level list/scalar) is the wrong shape: the id helpers raise on ``.get`` and
    # an empty universe would otherwise pass references unchecked. Treat it as not-loadable so the
    # cross-check fails closed. (An empty/whitespace doc → None is tolerated as a legit empty source.)
    loaded = yaml.safe_load(text)
    if loaded is not None and not isinstance(loaded, dict):
        raise yaml.YAMLError("expected a top-level mapping")


def _jsonl_loadable(text: str) -> None:
    for line in text.splitlines():
        line = line.strip()
        if line:
            json.loads(line)


def _safe_ids(fn) -> set[str]:
    """Call an id-collecting helper, mapping any parse/IO/shape error to an empty universe.

    ``AttributeError``/``TypeError`` cover a source that *parses* but to the wrong shape (e.g. a
    top-level list/scalar where a mapping is expected): the helper then raises on ``.get``. Such a
    source must yield an empty universe + a non-loadable verdict (so a citation against it FAILs
    closed) rather than crashing the validator.
    """
    try:
        return fn()
    except (OSError, yaml.YAMLError, json.JSONDecodeError, AttributeError, TypeError):
        return set()


def _anchors_loadable(base: Path) -> bool:
    """Anchors live in many ``*.anchors.jsonl`` files; loadable iff the dir exists and every
    present file parses."""
    anchors_dir = base / "sources" / "anchors"
    if not anchors_dir.exists():
        return False
    files = list(anchors_dir.glob("*.anchors.jsonl"))
    if not files:
        return False
    return all(_source_loadable(af, _jsonl_loadable) for af in files)


class _IdSets:
    """Lazily-loaded referential ID universes for provenance cross-checks.

    Alongside each id universe we record whether its *source* was loadable — present and
    parseable — so the cross-check can fail closed when a doc cites provenance of a kind whose
    source is missing or corrupt (an empty universe would otherwise pass every reference).
    """

    def __init__(self, base: Path):
        # The id helpers do not all guard parse errors; a corrupt source must yield an empty
        # universe here (the `loadable` map below records the failure so the cross-check fails
        # closed) rather than letting the exception escape the validator.
        self.principles = _safe_ids(lambda: principle_ids(base / "principles"))
        self.claims = _safe_ids(lambda: _claim_ids(base))
        self.evidence = _safe_ids(lambda: _evidence_ids(base))
        self.anchors = _safe_ids(lambda: _anchor_ids(base))
        self.loadable = {
            "principles": _source_loadable(base / "principles" / "principles.yaml", _yaml_loadable),
            "claims": _source_loadable(base / "analysis" / "claims.jsonl", _jsonl_loadable),
            "evidence": _source_loadable(
                base / "evidence" / "evidence-records.yaml", _yaml_loadable
            ),
            "source_anchors": _anchors_loadable(base),
        }


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
    # Present-but-unparseable frontmatter is a fail-closed signal: a doc that opened a fence but
    # whose YAML is corrupt must FAIL, not silently demote to a stub and skip its content checks.
    if fm is _FRONTMATTER_CORRUPT:
        return "authored", ["frontmatter present but unparseable (corrupt YAML frontmatter)"]
    status = str(fm.get("status", "")).lower() if isinstance(fm, dict) else ""
    if not isinstance(fm, dict) or status not in ("ready", "stale"):
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
            refs = list(prov.get(field) or [])
            if not refs:
                continue
            # Fail closed: if the doc cites provenance of a kind whose source failed to load
            # (missing or unparseable), the empty universe must not pass the refs unchecked.
            if not ids.loadable.get(field, False):
                errors.append(
                    f"provenance.{field} cited but its source did not load "
                    f"(missing or unparseable) — cannot verify references"
                )
                continue
            for ref in refs:
                if ref not in universe:
                    errors.append(f"provenance.{field} '{ref}' does not resolve to a real ID")

    # Split off the frontmatter so body checks (markers, section, line count) see only the body,
    # via the shared anchored split (same closing fence _parse_frontmatter used).
    _, body = split_frontmatter(text)
    for marker in _STUB_MARKERS:
        if marker in body:
            errors.append(f"status: ready but body still contains '{marker}'")
    if kind == "skill":
        if "## Procedure" not in body:
            errors.append("skill body missing a '## Procedure' section")
        n_lines = body.count("\n") + 1  # the limit is on the skill BODY, not the whole file
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
