"""Shared claim/evidence IO for the deterministic re-anchoring tools.

``reanchor_by_heading`` and ``reanchor_claims`` both load the package's claims, recompute each
claim's ``source_anchors``, then persist the claims and mirror the new anchors onto the 1:1 evidence
records. That load + write-back is identical between them and lives here. (The per-tool anchor
loaders differ in shape — ranked windows vs heading tokens vs line pairs — and stay in their modules;
the "set of all anchor ids" query is ``package_queries.anchor_ids``.)
"""

from __future__ import annotations

import json
from pathlib import Path

import yaml


def load_claims(base: Path) -> list[dict]:
    """Parse ``<base>/analysis/claims.jsonl`` into a list of claim records (blank lines skipped)."""
    path = base / "analysis" / "claims.jsonl"
    return [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]


def write_claims_and_propagate(
    base: Path, claims: list[dict], chosen_by_claim: dict[str, list[str]]
) -> None:
    """Persist re-anchored claims, then mirror each claim's new ``source_anchors`` onto its evidence.

    Writes ``<base>/analysis/claims.jsonl`` from ``claims``, then — if ``<base>/evidence/
    evidence-records.yaml`` exists — sets each record's ``source_anchors`` to ``chosen_by_claim`` by
    matching ``claim_id`` (evidence inherits its claim's anchors 1:1). No-op for evidence if absent.
    """
    (base / "analysis" / "claims.jsonl").write_text(
        "\n".join(json.dumps(c, ensure_ascii=False) for c in claims) + "\n", encoding="utf-8"
    )
    ev_path = base / "evidence" / "evidence-records.yaml"
    if ev_path.exists():
        ev = yaml.safe_load(ev_path.read_text(encoding="utf-8")) or {}
        for r in ev.get("evidence_records", []) or []:
            cid = r.get("claim_id")
            if cid in chosen_by_claim:
                r["source_anchors"] = chosen_by_claim[cid]
        ev_path.write_text(
            yaml.safe_dump(ev, sort_keys=False, allow_unicode=True), encoding="utf-8"
        )
