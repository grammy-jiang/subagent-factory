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
  - installed adapter matches canonical
  - tests exist
  - restricted quote scan passes
"""

import sys
from pathlib import Path

from tools.subagent_factory.validate_metadata import validate_metadata
from tools.subagent_factory.validate_manifest import validate_manifest
from tools.subagent_factory.validate_anchor_index import validate_anchor_index
from tools.subagent_factory.quote_scan import quote_scan


_REPO_ROOT = Path(__file__).parent.parent.parent

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
        # Compare content
        if adapter_path.exists():
            canonical = adapter_path.read_text()
            installed = installed_path.read_text()
            if canonical != installed:
                warn("adapter-sync", "Installed adapter differs from canonical — re-export needed")
    else:
        warn("adapter-installed", f"Installed adapter not found at {installed_path}")

    # 8. Tests
    tests_dir = base / "tests"
    if tests_dir.exists():
        test_files = list(tests_dir.glob("*.yaml")) + list(tests_dir.glob("*.md"))
        if test_files:
            ok("tests", f"{len(test_files)} test file(s) found")
        else:
            warn("tests", "No test files found in tests/")
    else:
        warn("tests", "tests/ directory missing")

    # 9. Quote scan
    quote_findings = quote_scan(base)
    if quote_findings:
        for qf in quote_findings:
            warn("quote-scan", f"{qf['file']}:{qf['line']}: {qf['issue']}")
    else:
        ok("quote-scan", "No potential verbatim quotation found")

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
