# Quote scan — verified run (rights gate)

Round-1 review finding **F6**: the packaged `quote_scan` PASS was vacuous. All three sources are
`distillation-only` and their text is withheld from the package (`sources/markdown/` is absent by
design), so with nothing to compare against the gate could not run — `validate_generated_package`
reports that honestly as
`[WARN] quote-scan: rights NOT verified — 3 restricted source(s) but no source text available`.

This file records a scan that **did** run, against the warm map-reduce cache the package was built
from, so the rights-clean claim carries evidence rather than an unrunnable gate.

## Run

- Re-run at **agent_version 1.3.0** (round-1 review, F5) — same command, same cache keys, same result
  (`{"findings": [], "restricted": 3, "scanned": true}`), now covering the 1.3.0 profile prose, the
  corrected persuasion skill body, the two skills carrying new boundary pointers, the three skills
  carrying new `description` trigger clauses, and the reordered principles index. The verified-clean
  version below is therefore 1.3.0, not the 1.1.0 recorded when this file was first written.
- Date: 2026-07-27
- Command (equivalent):
  `quote_scan_report("subagents/presentation-design-advisor", cache_root="<repo>/cache/book-extracts")`
- Source text loaded from the content-addressed cache modules keyed by the manifest `sha256`:

| source_id | sha256 (cache key) | words compared |
|-----------|--------------------|----------------|
| alley-craft-of-scien-8c1a058e | 8c1a058e8c77e0ed6cb571b40badbcc387eb11b206271f102592e2df26c2a7e9 | 86,055 |
| duarte-resonate-dc2fdbd7 | dc2fdbd73adeab13db76178f3c804bcd08dcfaecf176ab057831770b3e64588b | 53,313 |
| duarte-slideology-e1324c7e | e1324c7e36782f0cd5467259ebcb3dd6f3b1da94df944f8a06949f62d4da069b | 41,539 |

## Result

```
{"findings": [], "restricted": 3, "scanned": true}
```

**PASS — no verbatim quotation found.** Every generated markdown artifact in the package (profile-derived
prose, 14 skills, 2 references, ledger, changelog, adapter) was compared against the normalised source
text of all three restricted sources; no run of 40+ consecutive source words survives anywhere, which is
the threshold `.claude/rules/rights-and-quotation-policy.md` sets for manual review.

The scan covers the package **as of agent_version 1.3.0** (first run at 1.1.0, when the 14 skill bodies
were re-authored; re-run unchanged at 1.3.0).

## Why validate still WARNs

The cache lives outside the package (`<repo>/cache/book-extracts/`, not committed) and is absent in a
clean checkout, so `validate_generated_package` cannot reach it and correctly refuses to call the gate
"clean" when it could not run. That WARN is a statement about the checkout, not about this package; this
file is the evidence for the checkout that had the cache warm.
