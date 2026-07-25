"""Deterministic Phase 8 profile self-check gate.

Implements the structurally-checkable subset of the 18 Phase 8 checks from
``docs/subagent-authoring-process-cycle.md``. This is the gate the process
mandates before adapter generation ("Do not generate adapters until gate
passes"). Judgement-heavy checks that cannot be verified deterministically
(source-evidence traceability, unresolved-conflict detection) are reported as
INFO and delegated to the ``profile-reviewer`` agent.

Verdict:
  FAIL    — at least one FAIL finding; adapter export must be blocked.
  WARNING — no FAIL but at least one WARNING.
  PASS    — all checks pass.

Structure: ``profile_self_check`` loads the profile, extracts its fields into a ``Fields`` bag, then
runs the checks in the ``_CHECKS`` registry in order. Each check receives its own ordinal ``num``
(so the number lives in exactly one place — the registry) and appends finding(s) via the shared
``add`` emitter, so the findings list — consumed by the CLI, ``test-results.md``, and tests — is
built in check order.
"""

import re
import sys
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

import yaml

_SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

# Unambiguous platform contamination that must never appear in the neutral core.
_PLATFORM_FAIL_TOKENS = [
    ".claude",
    ".github",
    ".codex",
    "claude code",
    "claude-code",
    "copilot",
    "mcpservers",
    "permissionmode",
    "disallowedtools",
    "subagent_type",
]

# Heuristic for an ordered multi-step workflow leaking into the profile body.
_STEP_RE = re.compile(r"(?:^|\s)(?:step\s*\d|\d\.\s|\bfirst\b.+?\bthen\b)", re.IGNORECASE)

# A sibling package this agent routes work to, named inline as a slug
# (e.g. "belongs to research-writing-advisor"). Used by the router-description check.
_SIBLING_RE = re.compile(r"\b([a-z0-9]+(?:-[a-z0-9]+)*-(?:advisor|reviewer))\b")

# Wording that signals a quality-bar check demands evidence/citation.
_EVIDENCE_WORDS = (
    "evidence",
    "cite",
    "citation",
    "source",
    "principle",
    "reference",
    "named",
    "specific",
    "traceable",
)

# A Tier-1 profile grounds quality_bar in promoted principles by citing their
# IDs (``[P-006]``, ``P-009/P-010``) rather than the literal word "principle";
# claim (``CL-016``) and evidence-record (``EV-005``) IDs are also valid
# groundings. Recognise these so a correctly-grounded Tier-1 profile is not
# flagged for "no evidence reference". The factory's own workers emit IDs in
# both the hyphenated (``P-006``) and compact (``P001``) styles, so the hyphen
# is optional here — otherwise a profile grounded in ``[P001]`` is falsely
# flagged despite being correctly cited.
_ID_CITATION_RE = re.compile(r"\b(?:P|CL|EV)-?\d", re.IGNORECASE)

_BODY_WARN_WORDS = 800
_BODY_FAIL_WORDS = 1000

# Each check appends ``{num, level, check, message}`` findings via this emitter.
_Emit = Callable[[int, str, str, str], None]


@dataclass(frozen=True)
class Fields:
    """Typed field bag extracted once from the profile, consumed by the checks.

    Constructing this (the "extract" responsibility) is separated from running the
    checks (the "use" responsibility); see ``_extract_fields``.
    """

    base: Path
    slug: str
    router_description: str
    handoff_rules: list
    when_to_use: list
    when_not_to_use: list
    inputs_required: list
    primary_format: str
    modes: list
    quality_bar: list
    minimum_useful_output: str
    forbidden: list
    canonical_owner: str
    may_edit_canonical: object
    body_groups: dict
    body_fields: list


# A check receives its own ordinal ``num`` (the single home of the number), the
# extracted ``Fields`` bag, and the shared ``add`` emitter.
_Check = Callable[[int, Fields, _Emit], None]


def _trunc(text: str, limit: int = 60) -> str:
    """Truncate for table cells with an explicit ellipsis, never mid-word silently."""
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


# Role slug is kebab-case and role-based
def _check_slug(num: int, f: Fields, add: _Emit) -> None:
    slug = f.slug
    if not _SLUG_RE.match(slug):
        add(num, "FAIL", "slug-kebab", f"slug '{slug}' is not kebab-case")
    elif "-" not in slug:
        add(
            num,
            "WARNING",
            "slug-role-based",
            f"slug '{slug}' is a single word; role slugs are usually <domain>-<function>",
        )
    else:
        add(num, "PASS", "slug", f"slug '{slug}' is kebab-case and role-based")


# when_to_use has 3–6 concrete triggers
def _check_when_to_use(num: int, f: Fields, add: _Emit) -> None:
    when_to_use = f.when_to_use
    if not 3 <= len(when_to_use) <= 6:
        add(num, "FAIL", "when-to-use", f"when_to_use has {len(when_to_use)} triggers; require 3–6")
    else:
        add(num, "PASS", "when-to-use", f"{len(when_to_use)} triggers")


# when_not_to_use has 2+ explicit exclusions
def _check_when_not_to_use(num: int, f: Fields, add: _Emit) -> None:
    when_not_to_use = f.when_not_to_use
    if len(when_not_to_use) < 2:
        add(
            num,
            "FAIL",
            "when-not-to-use",
            f"when_not_to_use has {len(when_not_to_use)} exclusions; require 2+",
        )
    else:
        add(num, "PASS", "when-not-to-use", f"{len(when_not_to_use)} exclusions")


# Every assigned mode has source evidence (structural proxy + delegated)
def _check_modes_evidence(num: int, f: Fields, add: _Emit) -> None:
    modes = f.modes
    if not modes:
        add(num, "FAIL", "modes-present", "no modes defined in outputs.modes")
    else:
        missing_trigger = [
            m.get("name", "?") for m in modes if not str(m.get("trigger", "")).strip()
        ]
        if missing_trigger:
            add(
                num,
                "WARNING",
                "modes-evidence",
                f"modes missing a trigger (evidence proxy): {', '.join(missing_trigger)}",
            )
        else:
            add(
                num,
                "INFO",
                "modes-evidence",
                "mode source-evidence traceability delegated to profile-reviewer",
            )


# inputs.required explicit
def _check_inputs_required(num: int, f: Fields, add: _Emit) -> None:
    inputs_required = f.inputs_required
    if not inputs_required:
        add(num, "FAIL", "inputs-required", "inputs.required is empty")
    else:
        add(num, "PASS", "inputs-required", f"{len(inputs_required)} required input(s)")


# outputs.primary_format explicit
def _check_primary_format(num: int, f: Fields, add: _Emit) -> None:
    primary_format = f.primary_format
    if not primary_format:
        add(num, "FAIL", "primary-format", "outputs.primary_format is empty")
    else:
        add(num, "PASS", "primary-format", _trunc(primary_format))


# Every mode states its output format
def _check_mode_output(num: int, f: Fields, add: _Emit) -> None:
    modes = f.modes
    if modes:
        missing_output = [m.get("name", "?") for m in modes if not str(m.get("output", "")).strip()]
        if missing_output:
            add(
                num,
                "FAIL",
                "mode-output",
                f"modes missing an output contract: {', '.join(missing_output)}",
            )
        else:
            add(num, "PASS", "mode-output", "every mode states its output")


# minimum_useful_output defined
def _check_minimum_useful_output(num: int, f: Fields, add: _Emit) -> None:
    minimum_useful_output = f.minimum_useful_output
    if not minimum_useful_output:
        add(num, "FAIL", "minimum-useful-output", "minimum_useful_output is empty")
    else:
        add(num, "PASS", "minimum-useful-output", "defined")


# canonical_owner named in source_of_truth_policy
def _check_canonical_owner(num: int, f: Fields, add: _Emit) -> None:
    canonical_owner = f.canonical_owner
    if not canonical_owner:
        add(num, "FAIL", "canonical-owner", "source_of_truth_policy.canonical_owner is empty")
    else:
        add(num, "PASS", "canonical-owner", _trunc(canonical_owner))


# may_edit_canonical is false for specialist roles
def _check_may_edit_canonical(num: int, f: Fields, add: _Emit) -> None:
    may_edit_canonical = f.may_edit_canonical
    if may_edit_canonical in (
        None,
        "",
    ):
        add(num, "FAIL", "may-edit-canonical", "source_of_truth_policy.may_edit_canonical is unset")
    elif _truthy(may_edit_canonical):
        add(
            num,
            "FAIL",
            "may-edit-canonical",
            "may_edit_canonical is true; specialist roles must be false",
        )
    else:
        add(num, "PASS", "may-edit-canonical", "false")


# quality_bar requires evidence citation
def _check_quality_bar(num: int, f: Fields, add: _Emit) -> None:
    quality_bar = f.quality_bar
    if not quality_bar:
        add(num, "FAIL", "quality-bar", "quality_bar is empty")
    else:
        qb_text = " ".join(str(q) for q in quality_bar).lower()
        if not any(w in qb_text for w in _EVIDENCE_WORDS) and not _ID_CITATION_RE.search(qb_text):
            add(
                num,
                "WARNING",
                "quality-bar-evidence",
                "no quality_bar check references evidence/source/principle",
            )
        elif len(quality_bar) < 3:
            add(
                num,
                "WARNING",
                "quality-bar",
                f"only {len(quality_bar)} quality_bar checks (expect 3–5)",
            )
        else:
            add(num, "PASS", "quality-bar", f"{len(quality_bar)} evidence-citing checks")


# forbidden_behaviours present and traceable
def _check_forbidden(num: int, f: Fields, add: _Emit) -> None:
    forbidden = f.forbidden
    if not forbidden:
        add(num, "FAIL", "forbidden-behaviours", "forbidden_behaviours is empty")
    else:
        add(
            num,
            "INFO",
            "forbidden-behaviours",
            f"{len(forbidden)} rules; source traceability delegated to profile-reviewer",
        )


# No multi-step workflow in profile body
def _check_no_procedure(num: int, f: Fields, add: _Emit) -> None:
    if any(_STEP_RE.search(t) for t in f.body_fields):
        add(
            num,
            "WARNING",
            "no-procedure-in-body",
            "possible multi-step workflow in profile body; extract to a skill",
        )
    else:
        add(num, "PASS", "no-procedure-in-body", "no ordered procedure detected in body")


# Profile body under 800 words
def _check_body_size(num: int, f: Fields, add: _Emit) -> None:
    body_fields = f.body_fields
    word_count = sum(len(str(t).split()) for t in body_fields)
    if word_count <= _BODY_WARN_WORDS:
        add(num, "PASS", "body-size", f"~{word_count} words")
    else:
        # Over budget: name the heaviest sections so trimming is targeted, not
        # guesswork. (Closing this WARNING is otherwise pure trial-and-error.)
        level = "FAIL" if word_count > _BODY_FAIL_WORDS else "WARNING"
        limit = _BODY_FAIL_WORDS if level == "FAIL" else _BODY_WARN_WORDS
        section_words = {
            name: sum(len(str(t).split()) for t in group) for name, group in f.body_groups.items()
        }
        top = sorted(section_words.items(), key=lambda kv: kv[1], reverse=True)[:3]
        breakdown = ", ".join(f"{name} {n}w" for name, n in top if n)
        over = word_count - _BODY_WARN_WORDS
        add(
            num,
            level,
            "body-size",
            f"profile body ~{word_count} words (> {limit}); "
            f"{over} over the {_BODY_WARN_WORDS}-word budget; "
            f"heaviest: {breakdown}",
        )


# Routing signal survives export
def _check_router_description(num: int, f: Fields, add: _Emit) -> None:
    """Warn when the adapter's routing string would silently lose scope.

    The adapter frontmatter ``description`` is what the runtime routes on. Absent a
    ``router_description``, ``export_claude_agent`` composes it as
    ``role — Use when: <trigger[0..1]> — Not for: <exclusion[0]>``, which keeps only the
    first two triggers and the first exclusion. For an agent with more triggers, more
    exclusions, or a sibling it hands work to, the dropped text is exactly the signal a
    router needs — so the loss is invisible at runtime and nothing else catches it.
    """
    if f.router_description:
        add(num, "PASS", "router-description", "authored routing description present")
        return

    dropped_triggers = max(0, len(f.when_to_use) - 2)
    dropped_exclusions = max(0, len(f.when_not_to_use) - 1)
    siblings = sorted(
        {
            tok
            for text in list(f.when_not_to_use) + list(f.handoff_rules)
            for tok in _SIBLING_RE.findall(str(text))
            if tok != f.slug
        }
    )
    if not (dropped_triggers or dropped_exclusions or siblings):
        add(num, "PASS", "router-description", "composed description is lossless")
        return

    lost = []
    if dropped_triggers:
        lost.append(f"{dropped_triggers} of {len(f.when_to_use)} triggers")
    if dropped_exclusions:
        lost.append(f"{dropped_exclusions} of {len(f.when_not_to_use)} exclusions")
    if siblings:
        lost.append(f"hand-off to {', '.join(siblings)}")
    add(
        num,
        "WARNING",
        "router-description",
        "no router_description; the composed adapter description drops "
        + "; ".join(lost)
        + " — author router_description so routing sees the full remit",
    )


# No platform-specific paths or tool names in core
def _check_platform_neutral(num: int, f: Fields, add: _Emit) -> None:
    core_text = " ".join(str(t) for t in f.body_fields).lower()
    hits = sorted({tok for tok in _PLATFORM_FAIL_TOKENS if tok in core_text})
    if hits:
        add(num, "FAIL", "platform-neutral", f"platform-specific tokens in core: {', '.join(hits)}")
    else:
        add(num, "PASS", "platform-neutral", "core is platform-neutral")


# Provenance ledger exists and is non-trivial
def _check_provenance_ledger(num: int, f: Fields, add: _Emit) -> None:
    ledger = f.base / "provenance-ledger.md"
    if not ledger.exists():
        add(num, "FAIL", "provenance-ledger", "provenance-ledger.md missing")
    elif ledger.stat().st_size < 200:
        add(
            num,
            "WARNING",
            "provenance-ledger",
            "provenance-ledger.md is very small; may be incomplete",
        )
    else:
        add(num, "PASS", "provenance-ledger", "present")


# No unresolved conflict (delegated — requires merge log)
def _check_no_unresolved_conflict(num: int, f: Fields, add: _Emit) -> None:
    add(
        num,
        "INFO",
        "no-unresolved-conflict",
        "conflict resolution review delegated to profile-reviewer / Phase 7 merge log",
    )


# At least 3 golden tests including 1 negative routing test
def _check_golden_tests(num: int, f: Fields, add: _Emit) -> None:
    golden, negative, misplaced_hint = _count_tests(f.base)
    if golden < 3 or negative < 1:
        add(
            num,
            "FAIL",
            "golden-tests",
            f"found {golden} golden test(s) and {negative} negative routing test(s); "
            f"require 3+ golden and 1+ negative" + misplaced_hint,
        )
    else:
        add(num, "PASS", "golden-tests", f"{golden} golden, {negative} negative routing")


# The single home of each check's ordinal. Add or reorder here only — the number
# is passed into the check, so it lives in exactly one place.
_CHECKS: list[tuple[int, _Check]] = [
    (1, _check_slug),
    (2, _check_when_to_use),
    (3, _check_when_not_to_use),
    (4, _check_modes_evidence),
    (5, _check_inputs_required),
    (6, _check_primary_format),
    (7, _check_mode_output),
    (8, _check_minimum_useful_output),
    (9, _check_canonical_owner),
    (10, _check_may_edit_canonical),
    (11, _check_quality_bar),
    (12, _check_forbidden),
    (13, _check_no_procedure),
    (14, _check_body_size),
    (15, _check_platform_neutral),
    (16, _check_provenance_ledger),
    (17, _check_no_unresolved_conflict),
    (18, _check_golden_tests),
    # Appended, not inserted: the ordinals are referenced by existing reports and tests, so a
    # new check takes the next number rather than renumbering the established ones.
    (19, _check_router_description),
]


def _result(findings: list[dict]) -> dict:
    """Verdict from collected findings: FAIL > WARNING > PASS."""
    has_fail = any(f["level"] == "FAIL" for f in findings)
    has_warn = any(f["level"] == "WARNING" for f in findings)
    verdict = "FAIL" if has_fail else ("WARNING" if has_warn else "PASS")
    return {"verdict": verdict, "passed": not has_fail, "findings": findings}


def profile_self_check(subagent_dir: str | Path) -> dict:
    """Run the deterministic Phase 8 gate on a generated package.

    Returns dict: ``verdict`` (PASS/WARNING/FAIL), ``passed`` (verdict != FAIL),
    and ``findings`` — a list of ``{num, level, check, message}``.
    """
    base = Path(subagent_dir)
    findings: list[dict] = []

    def add(num, level, check, message):
        findings.append({"num": num, "level": level, "check": check, "message": message})

    profile_path = base / "profile.yaml"
    if not profile_path.exists():
        add(0, "FAIL", "profile-exists", f"profile.yaml not found at {profile_path}")
        return _result(findings)

    try:
        profile = yaml.safe_load(profile_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as e:
        add(0, "FAIL", "profile-parse", f"profile.yaml failed to parse: {e}")
        return _result(findings)

    fields = _extract_fields(profile, base)
    for num, check in _CHECKS:
        check(num, fields, add)

    return _result(findings)


def _extract_fields(profile: dict, base: Path) -> Fields:
    """Build the typed ``Fields`` bag the checks consume (the "construct" step).

    Separated from ``profile_self_check`` so the orchestrator only dispatches checks
    and the field-derivation logic lives in one place.
    """
    slug = str(profile.get("slug", "") or "")
    router_description = " ".join(str(profile.get("router_description", "") or "").split())
    handoff_rules = _as_list(profile.get("handoff_rules"))
    when_to_use = _as_list(profile.get("when_to_use"))
    when_not_to_use = _as_list(profile.get("when_not_to_use"))
    inputs_required = _as_list(profile.get("inputs", {}).get("required"))
    outputs = profile.get("outputs", {}) or {}
    primary_format = str(outputs.get("primary_format", "") or "").strip()
    modes = outputs.get("modes", []) or []
    quality_bar = _as_list(profile.get("quality_bar"))
    minimum_useful_output = str(profile.get("minimum_useful_output", "") or "").strip()
    forbidden = _as_list(profile.get("forbidden_behaviours"))
    sot = profile.get("source_of_truth_policy", {}) or {}
    canonical_owner = str(sot.get("canonical_owner", "") or "").strip()
    may_edit_canonical = sot.get("may_edit_canonical", None)

    # Body fields grouped by section so check 14 can point at the heaviest contributors when the
    # profile is over the word budget. The flattened list feeds checks 13/14/15 identically.
    body_groups = {
        "role": [str(profile.get("role", ""))],
        "when_to_use": when_to_use,
        "when_not_to_use": when_not_to_use,
        "inputs.required": inputs_required,
        "outputs.primary_format": [primary_format],
        "minimum_useful_output": [minimum_useful_output],
        "modes": [f"{m.get('trigger', '')} {m.get('output', '')}" for m in modes],
        "quality_bar": quality_bar,
        "forbidden_behaviours": forbidden,
        "handoff_rules": _as_list(profile.get("handoff_rules")),
        "precedence": [str(sot.get("precedence", ""))],
    }
    body_fields = [t for group in body_groups.values() for t in group]

    return Fields(
        base=base,
        slug=slug,
        router_description=router_description,
        handoff_rules=handoff_rules,
        when_to_use=when_to_use,
        when_not_to_use=when_not_to_use,
        inputs_required=inputs_required,
        primary_format=primary_format,
        modes=modes,
        quality_bar=quality_bar,
        minimum_useful_output=minimum_useful_output,
        forbidden=forbidden,
        canonical_owner=canonical_owner,
        may_edit_canonical=may_edit_canonical,
        body_groups=body_groups,
        body_fields=body_fields,
    )


def _as_list(value) -> list:
    if value is None:
        return []
    if isinstance(value, list):
        return [v for v in value if str(v).strip()]
    return [value] if str(value).strip() else []


def _truthy(value) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("true", "yes", "1")


# Top-level keys under which the gate recognizes test collections.
_RECOGNIZED_TEST_KEYS = ("golden_tests", "negative_routing_tests", "missing_context_tests")

# Sibling test artifacts that live in tests/ but carry their own schema (and their
# own validator) — they are NOT golden-tests files and must not be diagnosed as
# "misplaced" golden tests. A Tier-1 package legitimately ships
# tests/principle-behaviour-tests.yaml (principle-behaviour-tests-v1) alongside
# golden-tests.yaml; its `principle_behaviour_tests` list carries `test_id` items
# and would otherwise trip the misplaced-key hint with actively wrong advice
# ("move these into golden_tests"). Recognized by declared `schema_version`.
_SIBLING_TEST_SCHEMAS = frozenset({"principle-behaviour-tests-v1"})


def _looks_like_test_list(value) -> bool:
    """True when value is a list whose items look like test definitions."""
    return isinstance(value, list) and any(
        isinstance(item, dict) and "test_id" in item for item in value
    )


def _count_tests(base: Path) -> tuple[int, int, str]:
    """Count golden + negative routing tests, and diagnose misplaced ones.

    Returns ``(golden, negative, hint)``. ``hint`` is empty unless a tests file
    parks test definitions under an unrecognized top-level key (e.g. a ``tests:``
    list with per-item ``mode``/``routing_type`` — a common derivation defect).
    Without the hint such a file is silently counted as zero tests and the gate
    FAILs with a confusing "found 0" message rather than pointing at the schema.
    """
    tests_dir = base / "tests"
    golden = 0
    negative = 0
    misplaced: list[str] = []
    if not tests_dir.exists():
        return 0, 0, ""
    for tf in sorted(tests_dir.glob("*.yaml")):
        try:
            data = yaml.safe_load(tf.read_text(encoding="utf-8")) or {}
        except (yaml.YAMLError, OSError):
            continue
        if not isinstance(data, dict):
            continue
        golden += len(data.get("golden_tests", []) or [])
        negative += len(data.get("negative_routing_tests", []) or [])
        # A sibling test artifact (e.g. principle-behaviour-tests.yaml) declares its
        # own schema and is validated elsewhere — it carries no golden/negative tests
        # and must not be reported as misplaced golden tests.
        if data.get("schema_version") in _SIBLING_TEST_SCHEMAS:
            continue
        for key, value in data.items():
            if key in _RECOGNIZED_TEST_KEYS:
                continue
            if _looks_like_test_list(value):
                misplaced.append(f"{tf.name}: {len(value)} test(s) under unrecognized key '{key}'")
    hint = ""
    if misplaced:
        hint = (
            "; misplaced test definitions — "
            + "; ".join(misplaced)
            + ". Expected top-level keys golden_tests / negative_routing_tests / "
            "missing_context_tests (see templates/golden-tests.yaml.j2)"
        )
    return golden, negative, hint


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.profile_self_check subagents/<slug>")
        sys.exit(1)

    result = profile_self_check(sys.argv[1])
    for f in result["findings"]:
        print(f"[{f['level']:7s}] {f['num']:>2}. {f['check']}: {f['message']}")

    print()
    print(f"Phase 8 verdict: {result['verdict']}")
    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
