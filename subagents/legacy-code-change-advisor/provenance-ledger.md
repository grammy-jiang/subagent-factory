# Provenance Ledger — Legacy Code Change Advisor

Canonical profile: `subagents/legacy-code-change-advisor/profile.yaml`
Tier: 1 (single content-dense source, 131,673 words)

## Source Registry

| source_id | title | author | year | rights_status | sha256 (prefix) |
|-----------|-------|--------|------|---------------|-----------------|
| robert-c-martin-seri-e072e493 | Working Effectively with Legacy Code | Michael C. Feathers | 2005 | distillation-only | e072e493… |

Source-pack note: the PDF carries an explicit copyright notice ("All rights
reserved. … Copyright © 2005 Pearson Education, Inc., Publishing as Prentice Hall
PTR"). Rights resolved to `distillation-only` per the Step 2a decision tree
(authored, copyrighted work; distillation allowed, no verbatim quotation).
Converted with Docling (1207 anchors).

## Distillation Log

The Tier-1 evidence chain was run before profile derivation:

1. **Interrogation** (`interrogation-records.yaml`) — Q1–Q18 from the source.
2. **Claims** (`analysis/claims.jsonl`) — 24 atomic claims (C001–C024), each
   source-anchored to real heading anchors; validated by `validate_claims`.
3. **Evidence records** (`evidence/evidence-records.yaml`) — one record per claim
   (E001–E024) with strength/support level; validated by `validate_evidence_records`.
4. **Importance scores** (`analysis/claim-importance-scores.yaml`) — all 24 units
   scored ≥32/45 (verdict keep); validated by `cli score`.
5. **Principles** (`principles/principles.yaml`) — 12 operational principles
   (P01–P12) promoted from the claims; validated by `validate_principles`.
6. **Profile** — every rule grounds in a principle ID (P01–P12).

Key field derivations:

| Profile field | Grounded in | Source anchor(s) |
|---------------|-------------|------------------|
| role / always_on Legacy Code Change Algorithm | P02 ← C003 | h0035–h0040 |
| Cover and Modify over Edit and Pray | P01 ← C001, C002 | h0012, h0028 |
| sensing vs separation; fake objects | P03 ← C004, C024 | h0043, h0049 |
| seam definition, enabling point, seam types | P04 ← C005–C008 | h0076, h0086, h0100, h0119 |
| characterization tests + no moral authority | P05, P06 ← C009–C013 | h0530, h0539, h0569 |
| Method Use Rule | P07 ← C012 | h0539 |
| Sprout / Wrap Method & Class | P08 ← C014–C017, C023 | h0168, h0182, h0197, h0207, h0040 |
| conservative dependency breaking | P09 ← C018 | h0034 |
| unit-test speed/isolation | P10 ← C019 | h0030 |
| effect reasoning + pinch points | P11 ← C020, C021 | h0466, h0522 |
| Extract Interface | P12 ← C022 | h0990 |

## Conflict Log

No multi-source conflicts (single source). No internal contradictions found; the
one hedged claim (C008, object-seam preference) is carried as medium confidence
and is not asserted as a mandate in the profile.

## Generated Artifacts

- `profile.yaml` (canonical), `adapters/claude-code/legacy-code-change-advisor.md`,
  `.claude/agents/generated/legacy-code-change-advisor.md` (exported)
- `tests/golden-tests.yaml`, `tests/principle-behaviour-tests.yaml`,
  `tests/test-results.md`
- `reports/faithfulness-report.yaml` (Tier-1, vs evidence records; no CONTRADICTED)
- `policy/patch-policy.yaml` (patch-suggest mode → suggest-only default)

## Version History

- **0.1.0** (2026-06-15) — Initial authoring from a single distillation-only
  source via the Tier-1 evidence chain. Modes: advise, review, extract,
  patch-suggest. Status: draft (skill/reference bodies are stubs).

## Open Questions

- Technique applicability to languages published after 2005 (Go, Rust, Kotlin,
  TypeScript) is an evidence gap; the caller supplies the language for filtering.
- Dated tool references (JUnit/CppUnit/FIT versions, IDE refactoring support) in
  Ch 5 may no longer reflect current tooling; annual review recommended.
