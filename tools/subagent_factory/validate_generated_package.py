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
"""

import json
import sys
from pathlib import Path

import yaml

from tools.subagent_factory.adapter_policy_scan import adapter_policy_scan
from tools.subagent_factory.classify_tier import classify_tier
from tools.subagent_factory.profile_self_check import profile_self_check
from tools.subagent_factory.prompt_injection_scan import prompt_injection_scan
from tools.subagent_factory.quote_scan import quote_scan
from tools.subagent_factory.validate_anchor_index import validate_anchor_index
from tools.subagent_factory.validate_claims import validate_claims
from tools.subagent_factory.validate_evidence_records import validate_evidence_records
from tools.subagent_factory.validate_faithfulness_report import validate_faithfulness_report
from tools.subagent_factory.validate_manifest import validate_manifest
from tools.subagent_factory.validate_metadata import validate_metadata
from tools.subagent_factory.validate_patch_policy import validate_patch_policy
from tools.subagent_factory.validate_principle_test_coverage import validate_principle_test_coverage
from tools.subagent_factory.validate_principles import validate_principles

_REPO_ROOT = Path(__file__).parent.parent.parent

# Tier-gated artifact registry: ``(rel_path, min_tier, validate_fn)`` where
# ``validate_fn(path) -> list[str]``. The gate validates any entry that is *present*,
# and *requires* it only when the package tier ≥ ``min_tier``. A ``min_tier`` of 99
# means "validate when present, never required yet".
_TIER_ARTIFACTS: list = [
    # Step 1: faithfulness report — present-gated only (promote to min_tier 0 when
    # faithfulness-v0 becomes mandatory at Tier 0).
    ("reports/faithfulness-report.yaml", 99, validate_faithfulness_report),
    # Step 2: atomic claims — required at Tier 1+ (validated whenever present).
    ("analysis/claims.jsonl", 1, validate_claims),
    # Step 3: evidence records — required at Tier 1+ (validated whenever present).
    ("evidence/evidence-records.yaml", 1, validate_evidence_records),
    # Step 4: principles — required at Tier 1+ (validated whenever present).
    ("principles/principles.yaml", 1, validate_principles),
    # Step 5: principle→behaviour coverage — present-gated (keyed on principles.yaml).
    ("principles/principles.yaml", 99, validate_principle_test_coverage),
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

    # 1. Required files
    for fname in REQUIRED_FILES:
        p = base / fname
        if p.exists():
            ok("required-files", f"{fname} present")
        else:
            fail("required-files", f"Missing required file: {fname}")

    # 2. Required directories
    for dname in REQUIRED_DIRS:
        p = base / dname
        if p.exists():
            ok("required-dirs", f"{dname}/ present")
        else:
            warn("required-dirs", f"Missing expected directory: {dname}/")

    # 3. Metadata validation
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
    profile_path = base / "profile.yaml"
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

    # 4. Manifest validation
    manifest_path = base / "source-pack.manifest.yaml"
    if manifest_path.exists():
        errors = validate_manifest(manifest_path)
        if errors:
            for e in errors:
                fail("manifest", e)
        else:
            ok("manifest", "source-pack.manifest.yaml valid")

    # 5. Anchor index validation
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
    reports_dir = base / "sources" / "reports"
    if reports_dir.exists():
        reports = list(reports_dir.glob("*.conversion-report.md"))
        if not reports:
            warn("reports", "No conversion reports found")
        else:
            ok("reports", f"{len(reports)} conversion report(s) found")

    # 7. Adapter check
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
    if (base / "profile.yaml").exists():
        gate = profile_self_check(base)
        gate_fails = [f for f in gate["findings"] if f["level"] == "FAIL"]
        if gate_fails:
            for gf in gate_fails:
                fail("phase8", f"check {gf['num']} {gf['check']}: {gf['message']}")
        else:
            ok("phase8", f"Phase 8 self-check {gate['verdict']}")

    # 10. Quote scan
    quote_findings = quote_scan(base)
    if quote_findings:
        for qf in quote_findings:
            warn("quote-scan", f"{qf['file']}:{qf['line']}: {qf['issue']}")
    else:
        ok("quote-scan", "No potential verbatim quotation found")

    # 11. Prompt-injection scan over ingested source. Advisory triage — WARN, never
    # block: detectors are adaptively breakable and the ~225:1 base rate makes hard
    # blocking flood legit content; the source-safety-reviewer agent triages flags.
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
    for x in adapter_policy_scan(base):
        if x["level"] == "FAIL":
            fail("adapter-policy", f"{x['file']}: {x['issue']}")
        else:
            warn("adapter-policy", f"{x['file']}: {x['issue']}")

    # 13. Patch-safety policy — required when the profile grants a patch/produce mode.
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

    # Tier-gated artifacts: validate any that are present; require those the tier mandates.
    tier = _tier(base)

    # Tier-consistency: the *declared* tier governs which evidence artifacts are
    # required, but classify_tier is the deterministic authority on how content-dense
    # the package actually is (source word count / source count). A package that
    # under-declares its tier — or omits the field, as every pre-evidence-chain package
    # does — silently escapes the Tier-1+ evidence-chain requirement above. Surface that
    # drift. WARN, not FAIL: legacy packages predate the chain and must keep validating
    # (see classify_tier docstring), and the deterministic signal is advisory guidance for
    # the authoring run, which re-runs Step 6.5 and sets the real tier.
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
