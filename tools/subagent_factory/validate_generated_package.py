"""
Validate a generated subagent package.

Checks:
  - required files exist
  - metadata validates per schema
  - manifest validates per schema
  - anchor index validates per schema
  - conversion reports exist
  - profile.yaml exists
  - provenance-ledger.md exists
  - adapter exists (canonical)
  - installed adapter exists and matches canonical (FAIL on mismatch)
  - tests exist (golden-tests.yaml + test-results.md)
  - profile.yaml sources[] trace back to ingested source metadata
  - Phase 8 profile self-check gate passes
  - restricted quote scan passes
  - prompt-injection scan over ingested source (advisory WARN)
  - adapter-policy scan (tool-grant / escalation FAIL; body injection WARN)
  - tier-gated artifacts (e.g. faithfulness report) validated when present
  - skill/reference body authoring (status-gated: FAIL only when status: ready)
  - stale maintenance (authored bodies whose grounding drifted; advisory WARN)

``validate_generated_package`` runs each ``_check_*`` phase below in order; every phase appends its
``{level, check, message}`` findings via the shared ``fail``/``warn``/``ok`` emitters, so the findings
list (and the pass/fail verdict derived from it) is built in phase order.
"""

import json
import sys
from collections.abc import Callable
from pathlib import Path

import yaml

from tools.subagent_factory.adapter_policy_scan import adapter_policy_scan
from tools.subagent_factory.classify_tier import classify_tier
from tools.subagent_factory.compile_invariants import validate_invariant_coverage
from tools.subagent_factory.detect_stale import detect_stale
from tools.subagent_factory.domain_policy import check_domain_policy
from tools.subagent_factory.profile_self_check import profile_self_check
from tools.subagent_factory.prompt_injection_scan import prompt_injection_scan
from tools.subagent_factory.quote_scan import quote_scan
from tools.subagent_factory.validate_adapter_quality import validate_adapter_quality
from tools.subagent_factory.validate_anchor_index import validate_anchor_index
from tools.subagent_factory.validate_behaviour_test_coverage import (
    validate_behaviour_test_coverage,
)
from tools.subagent_factory.validate_claims import validate_claims
from tools.subagent_factory.validate_confidence_grade import validate_confidence_grade
from tools.subagent_factory.validate_evidence_records import validate_evidence_records
from tools.subagent_factory.validate_examples import validate_examples
from tools.subagent_factory.validate_faithfulness_report import validate_faithfulness_report
from tools.subagent_factory.validate_manifest import validate_manifest
from tools.subagent_factory.validate_metadata import validate_metadata
from tools.subagent_factory.validate_patch_policy import validate_patch_policy
from tools.subagent_factory.validate_principle_clusters import validate_principle_clusters
from tools.subagent_factory.validate_principle_graph import validate_principle_graph
from tools.subagent_factory.validate_principle_test_coverage import validate_principle_test_coverage
from tools.subagent_factory.validate_principles import validate_principles
from tools.subagent_factory.validate_skill_authoring import validate_skill_authoring

_REPO_ROOT = Path(__file__).parent.parent.parent

# Each phase appends findings via these emitters: emit(check, message) -> None.
_Emit = Callable[[str, str], None]

# Tier-gated artifact registry: ``(rel_path, min_tier, validate_fn)`` where
# ``validate_fn(path) -> list[str]``. The gate validates any entry that is *present*,
# and *requires* it only when the package tier ≥ ``min_tier``. A ``min_tier`` of 99
# means "validate when present, never required yet".
_TIER_ARTIFACTS: list = [
    # Step 1: faithfulness report — REQUIRED at all tiers. No subagent ships without a
    # faithfulness pass against its source (evidence-protocol: "no over-claimed subagent
    # released"). Promoted from min_tier 99 once every package carried a valid report.
    ("reports/faithfulness-report.yaml", 0, validate_faithfulness_report),
    # Step 2: atomic claims — required at Tier 1+ (validated whenever present).
    ("analysis/claims.jsonl", 1, validate_claims),
    # Step 3: evidence records — required at Tier 1+ (validated whenever present).
    ("evidence/evidence-records.yaml", 1, validate_evidence_records),
    # Step 4: principles — required at Tier 1+ (validated whenever present).
    ("principles/principles.yaml", 1, validate_principles),
    # Step 5: principle→behaviour coverage — required at Tier 1+. Coverage already runs
    # present-gated whenever principles.yaml exists (and Tier 1+ requires it via the
    # validate_principles entry above), so this is self-documenting + belt-and-suspenders:
    # a Tier-1 package without principle-behaviour test coverage cannot validate.
    ("principles/principles.yaml", 1, validate_principle_test_coverage),
    # Step 11 (behaviour-test generation): a generated adversarial suite (golden / negative-routing /
    # missing-context). min_tier 99 = validate-if-present, keyed on the distinct Step-11 filename so
    # the hand-authored golden-tests.yaml packages are untouched; bites only once a package ships a
    # generated behaviour-tests.yaml (schema + oracle-shape + per-principle golden coverage).
    ("tests/behaviour-tests.yaml", 99, validate_behaviour_test_coverage),
    # Step 7 (multi-source synthesis, Phase A/C): cross-source principle clusters + relationship
    # graph. min_tier 99 = validate-if-present, never required yet — they appear only on Tier-2
    # multi-source packages once the LLM-confirm step runs; the deterministic scaffolding is wired
    # now so they are auto-validated the moment they exist.
    ("principles/principle-clusters.json", 99, validate_principle_clusters),
    ("principles/principle-graph.json", 99, validate_principle_graph),
    # Phase 9 (instruction-induction A3/A5): the adapter's must-hold invariant layer must cover
    # every high-confidence profile-rule principle. Non-breaking: skips adapters with no invariant
    # section (pre-feature) and only catches a STALE invariant section once one exists.
    ("principles/principles.yaml", 99, validate_invariant_coverage),
    # Step 16 (K2): GRADE-consistency — a principle carrying a `grade` block must have confidence ==
    # grade_confidence(grade).level. Validate-if-present (min_tier 99): principles without a grade
    # block pass trivially, so it is non-breaking until promotion starts emitting grade factors.
    ("principles/principles.yaml", 99, validate_confidence_grade),
    # Phase 9 (instruction-induction A4): optional worked-example slot. Validate-if-present —
    # profile.yaml always exists so this runs every time, but returns [] unless an `examples` block
    # is present, so the example-less packages pass trivially. When examples ARE present, A4 bites:
    # each must be well-formed and ≥1 must be kind=failure-recovery.
    ("profile.yaml", 99, validate_examples),
]


def _tier(base: Path) -> int:
    """Read the package tier from profile.yaml (default 0).

    Absent ``tier:`` ⇒ Tier 0, so existing packages require no new artifacts. The
    gate validates any tier artifact that is *present* regardless of tier, but only
    *requires* an artifact when the package's tier mandates it.
    """
    profile_path = base / "profile.yaml"
    if not profile_path.exists():
        return 0
    try:
        prof = yaml.safe_load(profile_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return 0
    try:
        return int(prof.get("tier", 0) or 0)
    except (TypeError, ValueError):
        return 0


REQUIRED_FILES = [
    "profile.yaml",
    "provenance-ledger.md",
    "source-pack.manifest.yaml",
    "CHANGELOG.md",
]

REQUIRED_DIRS = [
    "sources/original",
    "sources/markdown",
    "sources/metadata",
    "sources/reports",
]

# sources/original (the raw source bytes) and sources/markdown (the verbatim conversion) carry the
# copyrighted source verbatim. For distillation-only / restricted sources the rights-and-quotation
# policy forbids publishing them, so a rights-clean export legitimately omits these two — their
# absence is then expected, not a warning. The rights-clean dirs (metadata, reports) still warn.
_VERBATIM_SOURCE_DIRS = ("sources/original", "sources/markdown")


def _verbatim_source_withheld(base: Path) -> bool:
    """True if the package's sources are distillation-only / restricted / proprietary, so the verbatim
    ``sources/{original,markdown}`` are intentionally withheld (rights-and-quotation-policy). Unknown
    or fully-open rights → False (keep the warning; openly-licensed sources can be committed)."""
    statuses: list[str] = []
    for mf in (base / "sources" / "metadata").glob("*.metadata.json"):
        try:
            rs = json.loads(mf.read_text(encoding="utf-8")).get("rights_status", "")
        except (OSError, json.JSONDecodeError):
            continue
        statuses.append(str(rs).lower())
    return any(
        any(t in s for t in ("distillation-only", "restricted", "proprietary")) for s in statuses
    )


# 1. Required files
def _check_required_files(base: Path, fail: _Emit, ok: _Emit) -> None:
    for fname in REQUIRED_FILES:
        p = base / fname
        if p.exists():
            ok("required-files", f"{fname} present")
        else:
            fail("required-files", f"Missing required file: {fname}")


# 2. Required directories. sources/{original,markdown} hold the copyrighted source verbatim; a
# rights-clean export of distillation-only/restricted sources omits them by policy, so their
# absence is expected there (OK), not a warning. metadata/reports are rights-clean → still warn.
def _check_required_dirs(base: Path, warn: _Emit, ok: _Emit) -> None:
    verbatim_withheld = _verbatim_source_withheld(base)
    for dname in REQUIRED_DIRS:
        p = base / dname
        if p.exists():
            ok("required-dirs", f"{dname}/ present")
        elif dname in _VERBATIM_SOURCE_DIRS and verbatim_withheld:
            ok(
                "required-dirs",
                f"{dname}/ absent — verbatim source withheld for distillation-only/restricted rights "
                "(rights-clean export)",
            )
        else:
            warn("required-dirs", f"Missing expected directory: {dname}/")


# 3. Metadata validation
def _check_metadata(base: Path, fail: _Emit, warn: _Emit, ok: _Emit) -> None:
    meta_dir = base / "sources" / "metadata"
    if meta_dir.exists():
        meta_files = list(meta_dir.glob("*.metadata.json"))
        if not meta_files:
            warn("metadata", "No metadata files found in sources/metadata/")
        for mf in meta_files:
            errors = validate_metadata(mf)
            if errors:
                for e in errors:
                    fail("metadata", f"{mf.name}: {e}")
            else:
                ok("metadata", f"{mf.name} valid")


# 3b. Profile sources trace back to ingested source metadata.
# profile.yaml's sources[] (source_id + sha256) are the provenance backbone
# required by rights-and-quotation-policy. A derivation that copies a stale
# sha256, points at a source that was never ingested, or leaves the hash
# blank silently breaks traceability — none of the other checks notice.
# The cross-check only runs when source metadata is present (the unit-test
# fixtures omit it); absence is already reported by the required-dirs check.
# Returns the parsed profile (or {}) so the later multisource-synthesis check can reuse it.
def _check_source_provenance(base: Path, fail: _Emit, warn: _Emit, ok: _Emit) -> dict:
    meta_dir = base / "sources" / "metadata"
    profile_path = base / "profile.yaml"
    profile: dict = {}
    if profile_path.exists() and meta_dir.exists():
        meta_sha = {}
        for mf in meta_dir.glob("*.metadata.json"):
            try:
                m = json.loads(mf.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            if m.get("source_id"):
                meta_sha[m["source_id"]] = str(m.get("sha256") or "")
        try:
            profile = yaml.safe_load(profile_path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            profile = {}
        profile_sources = profile.get("sources") or []
        if meta_sha and profile_sources:
            for src in profile_sources:
                sid = str(src.get("source_id") or "")
                sha = str(src.get("sha256") or "")
                if sid not in meta_sha:
                    fail(
                        "source-provenance",
                        f"profile source_id '{sid}' has no ingested metadata "
                        f"(known: {', '.join(sorted(meta_sha)) or 'none'})",
                    )
                elif not sha:
                    warn("source-provenance", f"profile source '{sid}' has an empty sha256")
                elif sha != meta_sha[sid]:
                    fail(
                        "source-provenance",
                        f"profile source '{sid}' sha256 does not match ingested "
                        f"metadata (profile={sha[:12]}…, metadata={meta_sha[sid][:12]}…)",
                    )
                else:
                    ok("source-provenance", f"source '{sid}' traces to ingested metadata")
    return profile


# 4. Manifest validation
def _check_manifest(base: Path, fail: _Emit, ok: _Emit) -> None:
    manifest_path = base / "source-pack.manifest.yaml"
    if manifest_path.exists():
        errors = validate_manifest(manifest_path)
        if errors:
            for e in errors:
                fail("manifest", e)
        else:
            ok("manifest", "source-pack.manifest.yaml valid")


# 5. Anchor index validation
def _check_anchors(base: Path, fail: _Emit, ok: _Emit) -> None:
    anchors_dir = base / "sources" / "anchors"
    if anchors_dir.exists():
        anchor_files = list(anchors_dir.glob("*.anchors.jsonl"))
        for af in anchor_files:
            errors = validate_anchor_index(af)
            if errors:
                for e in errors:
                    fail("anchors", f"{af.name}: {e}")
            else:
                ok("anchors", f"{af.name} valid")


# 6. Conversion reports
def _check_reports(base: Path, warn: _Emit, ok: _Emit) -> None:
    reports_dir = base / "sources" / "reports"
    if reports_dir.exists():
        reports = list(reports_dir.glob("*.conversion-report.md"))
        if not reports:
            warn("reports", "No conversion reports found")
        else:
            ok("reports", f"{len(reports)} conversion report(s) found")


# 7. Adapter check
def _check_adapter(base: Path, slug: str, fail: _Emit, ok: _Emit) -> None:
    adapter_path = base / "adapters" / "claude-code" / f"{slug}.md"
    if adapter_path.exists():
        ok("adapter", f"Canonical adapter {adapter_path.name} present")
    else:
        fail("adapter", f"Canonical adapter missing: {adapter_path}")

    installed_path = _REPO_ROOT / ".claude" / "agents" / "generated" / f"{slug}.md"
    if installed_path.exists():
        ok("adapter-installed", "Installed adapter present")
        # Compare content — installed adapter must match canonical (v0 requirement)
        if adapter_path.exists():
            canonical = adapter_path.read_text()
            installed = installed_path.read_text()
            if canonical != installed:
                fail("adapter-sync", "Installed adapter differs from canonical — re-export needed")
            else:
                ok("adapter-sync", "Installed adapter matches canonical")
    else:
        fail("adapter-installed", f"Installed adapter not found at {installed_path}")


# 8. Tests — golden tests and a test-results record are required (v0 §17)
def _check_tests(base: Path, fail: _Emit, ok: _Emit) -> None:
    tests_dir = base / "tests"
    if not tests_dir.exists():
        fail("tests", "tests/ directory missing")
    else:
        if (tests_dir / "golden-tests.yaml").exists():
            ok("tests", "tests/golden-tests.yaml present")
        else:
            fail("tests", "tests/golden-tests.yaml missing")
        if (tests_dir / "test-results.md").exists():
            ok("test-results", "tests/test-results.md present")
        else:
            fail("test-results", "tests/test-results.md missing — run `cli selfcheck <slug>` first")


# 9. Phase 8 profile self-check gate — any FAIL blocks the package
def _check_phase8(base: Path, fail: _Emit, ok: _Emit) -> None:
    if (base / "profile.yaml").exists():
        gate = profile_self_check(base)
        gate_fails = [f for f in gate["findings"] if f["level"] == "FAIL"]
        if gate_fails:
            for gf in gate_fails:
                fail("phase8", f"check {gf['num']} {gf['check']}: {gf['message']}")
        else:
            ok("phase8", f"Phase 8 self-check {gate['verdict']}")


# 10. Quote scan
def _check_quote_scan(base: Path, warn: _Emit, ok: _Emit) -> None:
    quote_findings = quote_scan(base)
    if quote_findings:
        for qf in quote_findings:
            warn("quote-scan", f"{qf['file']}:{qf['line']}: {qf['issue']}")
    else:
        ok("quote-scan", "No potential verbatim quotation found")


# 11. Prompt-injection scan over ingested source. Advisory triage — WARN, never
# block: detectors are adaptively breakable and the ~225:1 base rate makes hard
# blocking flood legit content; the source-safety-reviewer agent triages flags.
def _check_injection(base: Path, warn: _Emit, ok: _Emit) -> None:
    injection = prompt_injection_scan(base)
    if injection:
        for x in injection:
            warn(
                "injection-scan",
                f"{x['file']}:{x['line']} [{x['family']}/{x['vector']}/{x['severity']}] {x['excerpt']}",
            )
    else:
        ok("injection-scan", "no injection payloads detected in source")


# 12. Adapter-policy scan: tool-grant widening / escalation = FAIL; body injection = WARN.
def _check_adapter_policy(base: Path, fail: _Emit, warn: _Emit) -> None:
    for x in adapter_policy_scan(base):
        if x["level"] == "FAIL":
            fail("adapter-policy", f"{x['file']}: {x['issue']}")
        else:
            warn("adapter-policy", f"{x['file']}: {x['issue']}")


# 13. Patch-safety policy — required when the profile grants a patch/produce mode.
def _check_patch_policy(base: Path, fail: _Emit, ok: _Emit) -> None:
    patch_policy = base / "policy" / "patch-policy.yaml"
    has_patch_mode = False
    if (base / "profile.yaml").exists():
        try:
            _prof = yaml.safe_load((base / "profile.yaml").read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            _prof = {}
        modes = [m.get("name") for m in (_prof.get("outputs", {}) or {}).get("modes", []) or []]
        has_patch_mode = any(m in ("produce", "patch-suggest") for m in modes)
    if patch_policy.exists():
        pp_errs = validate_patch_policy(patch_policy)
        if pp_errs:
            for e in pp_errs:
                fail("patch-policy", f"policy/patch-policy.yaml: {e}")
        else:
            ok("patch-policy", "patch-policy.yaml valid")
    elif has_patch_mode:
        fail(
            "patch-policy",
            "profile grants a patch/produce mode but policy/patch-policy.yaml is missing",
        )


# 14. Domain-adaptation policy (Step-15 J-track) — opt-in per regulated domain.
# Inert unless the profile declares a regulated `domain_risk_category` (finance/legal/medical):
# every technical / non-regulated package has no such field, so this returns [] and Tier-0
# packages are untouched. When set, the package must ship the graded no-advice boundary
# (no-advice forbidden behaviour + defer-to-professional handoff + standing disclaimer).
def _check_domain_policy(base: Path, fail: _Emit, ok: _Emit) -> None:
    if (base / "profile.yaml").exists():
        try:
            _dprof = yaml.safe_load((base / "profile.yaml").read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            _dprof = {}
        dom_errs = check_domain_policy(_dprof)
        if dom_errs:
            for e in dom_errs:
                fail("domain-policy", e)
        elif _dprof.get("domain_risk_category"):
            ok(
                "domain-policy",
                f"regulated domain '{_dprof['domain_risk_category']}' boundary present",
            )


# Tier-consistency: the *declared* tier governs which evidence artifacts are
# required, but classify_tier is the deterministic authority on how content-dense
# the package actually is (source word count / source count). A package that
# under-declares its tier — or omits the field, as every pre-evidence-chain package
# does — silently escapes the Tier-1+ evidence-chain requirement above. Surface that
# drift. WARN, not FAIL: legacy packages predate the chain and must keep validating
# (see classify_tier docstring), and the deterministic signal is advisory guidance for
# the authoring run, which re-runs Step 6.5 and sets the real tier.
# Returns the declared tier (which the tier-artifact + multisource checks below need).
def _check_tier_consistency(base: Path, warn: _Emit, ok: _Emit) -> int:
    tier = _tier(base)
    computed_tier = classify_tier(base)
    if computed_tier > tier:
        warn(
            "tier-consistency",
            f"profile declares tier {tier} but classify_tier computes tier {computed_tier} "
            f"from source size/count; this package likely needs the Tier-{computed_tier} "
            f"evidence chain (claims/evidence/principles). Run Step 6.5 and set "
            f"'tier: {computed_tier}' in profile.yaml.",
        )
    else:
        ok("tier-consistency", f"declared tier {tier} ≥ computed tier {computed_tier}")
    return tier


# Tier-gated artifacts: validate any that are present; require those the tier mandates.
def _check_tier_artifacts(base: Path, tier: int, fail: _Emit, ok: _Emit) -> None:
    for rel, min_tier, vfn in _TIER_ARTIFACTS:
        p = base / rel
        if p.exists():
            errs = vfn(p)
            if errs:
                for e in errs:
                    fail("tier-artifact", f"{rel}: {e}")
            else:
                ok("tier-artifact", f"{rel} valid")
        elif tier >= min_tier:
            fail("tier-artifact", f"tier {tier} requires {rel} (missing)")


# Step 7: multi-source synthesis expected on Tier-2+ packages whose distilled claims genuinely
# span >=2 sources. Keyed on distinct claim source_ids, NOT the manifest source count — a package
# can list 2 sources yet distill claims from only one, in which case there is nothing to fuse and
# flagging it would be a false positive. Advisory (WARN), not FAIL: pre-Step-7 packages lack the
# artifacts; surfacing the gap drives a re-synthesis without breaking them. When present, the tier
# loop above already validated them (min_tier 99 entries).
def _check_multisource(base: Path, profile: dict, tier: int, warn: _Emit, ok: _Emit) -> None:
    claim_sources: set[str] = set()
    _cl_path = base / "analysis" / "claims.jsonl"
    if _cl_path.exists():
        for line in _cl_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                sid = json.loads(line).get("source_id")
            except json.JSONDecodeError:
                continue
            if sid:
                claim_sources.add(str(sid))
    if tier >= 2 and len(claim_sources) >= 2:
        # Step 7 cross-source synthesis is opt-in. A package may explicitly defer it
        # (`multisource_synthesis: deferred` in profile.yaml) — then the absence is an
        # acknowledged decision, not a per-validate WARN that buries real findings.
        synthesis_deferred = (
            str(profile.get("multisource_synthesis", "")).strip().lower() == "deferred"
        )
        for art in ("principle-clusters.json", "principle-graph.json"):
            if (base / "principles" / art).exists():
                ok("multisource-synthesis", f"{art} present")
            elif synthesis_deferred:
                ok("multisource-synthesis", f"{art} deferred (multisource_synthesis: deferred)")
            else:
                warn(
                    "multisource-synthesis",
                    f"Tier-2 multi-source package has no principles/{art} — run Step 7 "
                    "synthesis or set multisource_synthesis: deferred",
                )


# Step 8: skill/reference body authoring — status-gated. FAIL only when the profile
# declares status: ready with an unauthored or invalid skill/reference; otherwise WARN
# (authored N/M). Draft packages (all 15 current ones) only ever WARN here.
def _check_skill_authoring(base: Path, fail: _Emit, warn: _Emit, ok: _Emit) -> None:
    for level, msg in validate_skill_authoring(base):
        if level == "FAIL":
            fail("skill-authoring", msg)
        elif level == "WARN":
            warn("skill-authoring", msg)
        else:
            ok("skill-authoring", msg)


# Adapter output-quality gate: the exported deliverable must be substantive (DO-NOT-EDIT
# header, no stub/placeholder tokens, load-bearing sections present + non-empty). Complements
# the existence + security (adapter-policy) checks above.
def _check_adapter_quality(base: Path, fail: _Emit, warn: _Emit, ok: _Emit) -> None:
    for level, msg in validate_adapter_quality(base):
        if level == "FAIL":
            fail("adapter-quality", msg)
        elif level == "WARN":
            warn("adapter-quality", msg)
        else:
            ok("adapter-quality", msg)


# Step 9: stale maintenance — authored bodies whose grounding (cited principles/claims) has
# drifted since authoring. Advisory only: a stale flag is human-reviewed/re-authored before
# the next release, never a hard release block. STALE/WARN → warn; INFO/OK → ok.
def _check_stale(base: Path, warn: _Emit, ok: _Emit) -> None:
    for level, artifact, reason in detect_stale(base):
        if level in ("STALE", "WARN"):
            warn("stale-maintenance", f"{artifact}: {reason}")
        else:
            ok("stale-maintenance", f"{artifact}: {reason}")


def validate_generated_package(subagent_dir: str | Path) -> dict:
    """
    Run all package validation checks.

    Returns dict: passed (bool), findings list of {level, check, message}
    """
    base = Path(subagent_dir)
    findings = []
    slug = base.name

    def fail(check, msg):
        findings.append({"level": "FAIL", "check": check, "message": msg})

    def warn(check, msg):
        findings.append({"level": "WARN", "check": check, "message": msg})

    def ok(check, msg):
        findings.append({"level": "OK", "check": check, "message": msg})

    _check_required_files(base, fail, ok)
    _check_required_dirs(base, warn, ok)
    _check_metadata(base, fail, warn, ok)
    profile = _check_source_provenance(base, fail, warn, ok)
    _check_manifest(base, fail, ok)
    _check_anchors(base, fail, ok)
    _check_reports(base, warn, ok)
    _check_adapter(base, slug, fail, ok)
    _check_tests(base, fail, ok)
    _check_phase8(base, fail, ok)
    _check_quote_scan(base, warn, ok)
    _check_injection(base, warn, ok)
    _check_adapter_policy(base, fail, warn)
    _check_patch_policy(base, fail, ok)
    _check_domain_policy(base, fail, ok)
    tier = _check_tier_consistency(base, warn, ok)
    _check_tier_artifacts(base, tier, fail, ok)
    _check_multisource(base, profile, tier, warn, ok)
    _check_skill_authoring(base, fail, warn, ok)
    _check_adapter_quality(base, fail, warn, ok)
    _check_stale(base, warn, ok)

    failed = [f for f in findings if f["level"] == "FAIL"]
    passed = len(failed) == 0

    return {"passed": passed, "findings": findings}


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.validate_generated_package subagents/<slug>")
        sys.exit(1)

    result = validate_generated_package(sys.argv[1])
    for f in result["findings"]:
        print(f"[{f['level']:4s}] {f['check']}: {f['message']}")

    print()
    if result["passed"]:
        print("VALIDATION PASSED")
    else:
        failed_count = sum(1 for f in result["findings"] if f["level"] == "FAIL")
        print(f"VALIDATION FAILED — {failed_count} failure(s)")

    sys.exit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()
