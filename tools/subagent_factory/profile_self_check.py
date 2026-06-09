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
"""

import re
import sys
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

_BODY_WARN_WORDS = 800
_BODY_FAIL_WORDS = 1000


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
        return {"verdict": "FAIL", "passed": False, "findings": findings}

    try:
        profile = yaml.safe_load(profile_path.read_text(encoding="utf-8")) or {}
    except Exception as e:
        add(0, "FAIL", "profile-parse", f"profile.yaml failed to parse: {e}")
        return {"verdict": "FAIL", "passed": False, "findings": findings}

    slug = str(profile.get("slug", "") or "")
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

    # 1. Role slug is kebab-case and role-based
    if not _SLUG_RE.match(slug):
        add(1, "FAIL", "slug-kebab", f"slug '{slug}' is not kebab-case")
    elif "-" not in slug:
        add(
            1,
            "WARNING",
            "slug-role-based",
            f"slug '{slug}' is a single word; role slugs are usually <domain>-<function>",
        )
    else:
        add(1, "PASS", "slug", f"slug '{slug}' is kebab-case and role-based")

    # 2. when_to_use has 3–6 concrete triggers
    if not 3 <= len(when_to_use) <= 6:
        add(2, "FAIL", "when-to-use", f"when_to_use has {len(when_to_use)} triggers; require 3–6")
    else:
        add(2, "PASS", "when-to-use", f"{len(when_to_use)} triggers")

    # 3. when_not_to_use has 2+ explicit exclusions
    if len(when_not_to_use) < 2:
        add(
            3,
            "FAIL",
            "when-not-to-use",
            f"when_not_to_use has {len(when_not_to_use)} exclusions; require 2+",
        )
    else:
        add(3, "PASS", "when-not-to-use", f"{len(when_not_to_use)} exclusions")

    # 4. Every assigned mode has source evidence (structural proxy + delegated)
    if not modes:
        add(4, "FAIL", "modes-present", "no modes defined in outputs.modes")
    else:
        missing_trigger = [
            m.get("name", "?") for m in modes if not str(m.get("trigger", "")).strip()
        ]
        if missing_trigger:
            add(
                4,
                "WARNING",
                "modes-evidence",
                f"modes missing a trigger (evidence proxy): {', '.join(missing_trigger)}",
            )
        else:
            add(
                4,
                "INFO",
                "modes-evidence",
                "mode source-evidence traceability delegated to profile-reviewer",
            )

    # 5. inputs.required explicit
    if not inputs_required:
        add(5, "FAIL", "inputs-required", "inputs.required is empty")
    else:
        add(5, "PASS", "inputs-required", f"{len(inputs_required)} required input(s)")

    # 6. outputs.primary_format explicit
    if not primary_format:
        add(6, "FAIL", "primary-format", "outputs.primary_format is empty")
    else:
        add(6, "PASS", "primary-format", primary_format[:60])

    # 7. Every mode states its output format
    if modes:
        missing_output = [m.get("name", "?") for m in modes if not str(m.get("output", "")).strip()]
        if missing_output:
            add(
                7,
                "FAIL",
                "mode-output",
                f"modes missing an output contract: {', '.join(missing_output)}",
            )
        else:
            add(7, "PASS", "mode-output", "every mode states its output")

    # 8. minimum_useful_output defined
    if not minimum_useful_output:
        add(8, "FAIL", "minimum-useful-output", "minimum_useful_output is empty")
    else:
        add(8, "PASS", "minimum-useful-output", "defined")

    # 9. canonical_owner named in source_of_truth_policy
    if not canonical_owner:
        add(9, "FAIL", "canonical-owner", "source_of_truth_policy.canonical_owner is empty")
    else:
        add(9, "PASS", "canonical-owner", canonical_owner[:60])

    # 10. may_edit_canonical is false for specialist roles
    if may_edit_canonical in (
        None,
        "",
    ):
        add(10, "FAIL", "may-edit-canonical", "source_of_truth_policy.may_edit_canonical is unset")
    elif _truthy(may_edit_canonical):
        add(
            10,
            "FAIL",
            "may-edit-canonical",
            "may_edit_canonical is true; specialist roles must be false",
        )
    else:
        add(10, "PASS", "may-edit-canonical", "false")

    # 11. quality_bar requires evidence citation
    if not quality_bar:
        add(11, "FAIL", "quality-bar", "quality_bar is empty")
    else:
        qb_text = " ".join(str(q) for q in quality_bar).lower()
        if not any(w in qb_text for w in _EVIDENCE_WORDS):
            add(
                11,
                "WARNING",
                "quality-bar-evidence",
                "no quality_bar check references evidence/source/principle",
            )
        elif len(quality_bar) < 3:
            add(
                11,
                "WARNING",
                "quality-bar",
                f"only {len(quality_bar)} quality_bar checks (expect 3–5)",
            )
        else:
            add(11, "PASS", "quality-bar", f"{len(quality_bar)} evidence-citing checks")

    # 12. forbidden_behaviours present and traceable
    if not forbidden:
        add(12, "FAIL", "forbidden-behaviours", "forbidden_behaviours is empty")
    else:
        add(
            12,
            "INFO",
            "forbidden-behaviours",
            f"{len(forbidden)} rules; source traceability delegated to profile-reviewer",
        )

    # 13. No multi-step workflow in profile body
    # Body fields grouped by section so check 14 can point at the heaviest
    # contributors when the profile is over the word budget. The flattened list
    # is identical to the previous anonymous construction, so check 13 below is
    # byte-for-byte unchanged.
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
    if any(_STEP_RE.search(t) for t in body_fields):
        add(
            13,
            "WARNING",
            "no-procedure-in-body",
            "possible multi-step workflow in profile body; extract to a skill",
        )
    else:
        add(13, "PASS", "no-procedure-in-body", "no ordered procedure detected in body")

    # 14. Profile body under 800 words
    word_count = sum(len(str(t).split()) for t in body_fields)
    if word_count <= _BODY_WARN_WORDS:
        add(14, "PASS", "body-size", f"~{word_count} words")
    else:
        # Over budget: name the heaviest sections so trimming is targeted, not
        # guesswork. (Closing this WARNING is otherwise pure trial-and-error.)
        level = "FAIL" if word_count > _BODY_FAIL_WORDS else "WARNING"
        limit = _BODY_FAIL_WORDS if level == "FAIL" else _BODY_WARN_WORDS
        section_words = {
            name: sum(len(str(t).split()) for t in group) for name, group in body_groups.items()
        }
        top = sorted(section_words.items(), key=lambda kv: kv[1], reverse=True)[:3]
        breakdown = ", ".join(f"{name} {n}w" for name, n in top if n)
        over = word_count - _BODY_WARN_WORDS
        add(
            14,
            level,
            "body-size",
            f"profile body ~{word_count} words (> {limit}); "
            f"{over} over the {_BODY_WARN_WORDS}-word budget; "
            f"heaviest: {breakdown}",
        )

    # 15. No platform-specific paths or tool names in core
    core_text = " ".join(str(t) for t in body_fields).lower()
    hits = sorted({tok for tok in _PLATFORM_FAIL_TOKENS if tok in core_text})
    if hits:
        add(15, "FAIL", "platform-neutral", f"platform-specific tokens in core: {', '.join(hits)}")
    else:
        add(15, "PASS", "platform-neutral", "core is platform-neutral")

    # 16. Provenance ledger exists and is non-trivial
    ledger = base / "provenance-ledger.md"
    if not ledger.exists():
        add(16, "FAIL", "provenance-ledger", "provenance-ledger.md missing")
    elif ledger.stat().st_size < 200:
        add(
            16,
            "WARNING",
            "provenance-ledger",
            "provenance-ledger.md is very small; may be incomplete",
        )
    else:
        add(16, "PASS", "provenance-ledger", "present")

    # 17. No unresolved conflict (delegated — requires merge log)
    add(
        17,
        "INFO",
        "no-unresolved-conflict",
        "conflict resolution review delegated to profile-reviewer / Phase 7 merge log",
    )

    # 18. At least 3 golden tests including 1 negative routing test
    golden, negative = _count_tests(base)
    if golden < 3 or negative < 1:
        add(
            18,
            "FAIL",
            "golden-tests",
            f"found {golden} golden test(s) and {negative} negative routing test(s); "
            f"require 3+ golden and 1+ negative",
        )
    else:
        add(18, "PASS", "golden-tests", f"{golden} golden, {negative} negative routing")

    has_fail = any(f["level"] == "FAIL" for f in findings)
    has_warn = any(f["level"] == "WARNING" for f in findings)
    verdict = "FAIL" if has_fail else ("WARNING" if has_warn else "PASS")
    return {"verdict": verdict, "passed": not has_fail, "findings": findings}


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


def _count_tests(base: Path) -> tuple[int, int]:
    tests_dir = base / "tests"
    golden = 0
    negative = 0
    if not tests_dir.exists():
        return 0, 0
    for tf in tests_dir.glob("*.yaml"):
        try:
            data = yaml.safe_load(tf.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        golden += len(data.get("golden_tests", []) or [])
        negative += len(data.get("negative_routing_tests", []) or [])
    return golden, negative


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
