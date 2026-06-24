"""Deterministic repair for a flaky faithfulness report (re-author reliability).

The faithfulness step occasionally emits ``source_anchors`` that are free-text section
descriptions ("ch4 Traps — RISC-V registers") or dangling ids instead of real anchor ids,
which fails validation and forces a full manual re-author. This repair removes the invalid
entries per finding (keeping the valid ones), so the report validates, and writes the dropped
entries to ``reports/faithfulness-repair.yaml`` so the lost provenance is preserved for review
rather than silently discarded. The finding's verdict/action are never touched.

``source_anchors`` is optional and unbounded in the schema, so dropping to an empty list keeps
the report structurally valid. Deterministic, no LLM.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

from tools.subagent_factory.package_queries import anchor_ids as _anchor_ids
from tools.subagent_factory.validate_faithfulness_report import _ANCHOR_ID_RE


def _is_valid_anchor(a: str, anchors: set[str]) -> bool:
    """Valid = anchor-id-shaped AND present in the index (or index empty → shape-only check)."""
    if not _ANCHOR_ID_RE.search(str(a)):
        return False
    return (a in anchors) if anchors else True


def repair_faithfulness_report(report_path: str | Path, *, write: bool = True) -> dict:
    """Strip invalid ``source_anchors`` from each finding; quarantine them to a sidecar.

    Returns ``{"n_dropped": int, "quarantined": [{finding, rule_ref, dropped}], "changed": bool}``.
    """
    path = Path(report_path)
    base = path.parents[1]  # <base>/reports/faithfulness-report.yaml
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    anchors = _anchor_ids(base)

    quarantined: list[dict] = []
    for i, finding in enumerate(data.get("findings", []) or []):
        original = finding.get("source_anchors", []) or []
        kept = [a for a in original if _is_valid_anchor(a, anchors)]
        for a in original:
            if not _is_valid_anchor(a, anchors):
                quarantined.append(
                    {"finding": i, "rule_ref": finding.get("rule_ref", ""), "dropped": str(a)}
                )
        if kept != original:
            finding["source_anchors"] = kept

    changed = bool(quarantined)
    if write and changed:
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        (base / "reports" / "faithfulness-repair.yaml").write_text(
            yaml.safe_dump({"quarantined": quarantined}, sort_keys=False), encoding="utf-8"
        )
    return {"n_dropped": len(quarantined), "quarantined": quarantined, "changed": changed}


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m tools.subagent_factory.repair_faithfulness_report <report.yaml>")
        sys.exit(1)
    rep = repair_faithfulness_report(sys.argv[1])
    print(f"faithfulness repair: dropped {rep['n_dropped']} invalid anchor ref(s)")
    for q in rep["quarantined"][:15]:
        print(f"  finding[{q['finding']}] {q['rule_ref']}: {q['dropped'][:70]}")


if __name__ == "__main__":
    main()
