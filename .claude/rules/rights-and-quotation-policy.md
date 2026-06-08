# Rights and Quotation Policy

## Source rights classification

Every source must have a rights_status before distillation begins.

| Status | Meaning | Allowed use |
|--------|---------|-------------|
| `open` | Open license (MIT, Apache, CC-BY, public domain) | Quotation and distillation allowed |
| `distillation-only` | Copyrighted, purchased, or fair-use only | Distillation allowed; no verbatim quotation |
| `proprietary/restricted` | Internal, confidential, or restricted license | Minimal distillation only; flag all use |
| `unknown` | Rights not yet determined | Block distillation until resolved |

**Hard rule:** No source enters distillation without rights_status recorded.

## Quotation rules

- `distillation-only` sources: no verbatim quotation anywhere in generated artifacts
- `proprietary/restricted` sources: no quotation, minimal paraphrase, log every reference
- Paraphrase and restructure; do not copy passages of 3+ sentences

## Quote scan

Run `python -m tools.subagent_factory.quote_scan subagents/<slug>` before release.
Any finding of 40+ consecutive source words in output requires manual review.

## Provenance requirement

Every profile field must be traceable to a source and QID in provenance-ledger.md.
No orphan field values.
