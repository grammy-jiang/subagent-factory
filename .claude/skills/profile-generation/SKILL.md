# Skill: profile-generation

**Purpose:** Generate or update `profile.yaml` and `provenance-ledger.md` from
interrogation records. Phase 5 of the authoring cycle.

---

## Input

- Interrogation record(s) from source-interrogation
- Subagent package path `subagents/<slug>/`
- Source metadata from `sources/metadata/`

---

## Steps

### 0. Apply importance ranking (Phase 2.5 gate)

Before deriving any field, confirm the candidate units were scored and filtered:

```bash
python -m tools.subagent_factory.score_extracted_units <units.yaml>
```

Derive profile content only from `keep` units. Route `discard` units to the
provenance ledger only. Resolve `review` units with a human decision before use.
Exit non-zero means malformed scores — fix before continuing.

### 1. Resolve profile fields

Apply derivation rules from Phase 5:

| Field | Rule |
|-------|------|
| `slug` | kebab-case, role-based, already established |
| `display_name` | From Q1 — explicit role label or synthesized |
| `role` | One sentence: what, to what, for what reason |
| `when_to_use[]` | Q3 triggers as caller-observable situations (3–6) |
| `when_not_to_use[]` | Q4 exclusions (2+) |
| `inputs.required[]` | Q5 first required artifact/scope |
| `outputs.primary_format` | Q6 canonical deliverable noun |
| `quality_bar[]` | Q7 rewritten as falsifiable checks (3–5) |
| `supported_modes[]` | Q9 only modes with evidence |
| `handoff_rules[]` | Q8 downstream owner |
| `canonical_owner` | Q8+Q17 |
| `forbidden_behaviours[]` | Q10 do-not rules |
| `minimum_useful_output` | Q11 |
| `source_of_truth_policy` | Q8+Q17 |
| `knowledge_partition.*` | Q12–Q16 |

If the source justified a `purpose-review` pattern (see source-interrogation),
embed the `purpose_review` mode from `templates/purpose-review-contract.yaml.j2`,
or emit it as `subagents/<slug>/references/purpose-review-pattern.md` and list it
in `knowledge_partition.references[]`.

### 2. Check profile bloat limits

| Check | Limit |
|-------|-------|
| Total body | Under 800 words |
| Universal rules | Max 12 |
| Rules per mode | Max 3 |
| Procedures in body | No ordered sequence > 2 steps |
| Static tables/checklists | None |
| Platform-specific nouns | Zero |

Move violations to skills or references.

### 3. Write profile.yaml

Use `templates/profile.yaml.j2`. Write to `subagents/<slug>/profile.yaml`.

**YAML-safety rule:** emit every free-text scalar as a folded block scalar
(`>-`). A plain scalar containing a colon-space (`": "`) — e.g.
`- Domain model under review: a diagram` — is parsed as a mapping and breaks the
file. The template encodes this; preserve it when hand-authoring. Constrained
tokens (slug, version, booleans, kebab names) stay inline.

### 4. Write provenance-ledger.md

For every profile field, add a distillation log row:
- field name
- source_id(s)
- QID(s) used
- brief note

Use `templates/provenance-ledger.md.j2`. Write to `subagents/<slug>/provenance-ledger.md`.

### 5. Write CHANGELOG.md

Use `templates/changelog.md.j2`. Write to `subagents/<slug>/CHANGELOG.md`.

### 6. Write README.md

Write brief package README to `subagents/<slug>/README.md`.

### 7. Generate golden tests

Use `templates/golden-tests.yaml.j2`. Write to `subagents/<slug>/tests/golden-tests.yaml`.

### 8. Run Phase 8 self-check

Check #0 is **profile.yaml parses as valid YAML** — verify this first; the
content checks are meaningless on an unparseable file. Then verify the profile
against the remaining Phase 8 checks. Report PASS / WARNING / FAIL.

The authoritative verdict comes from the deterministic
`python -m tools.subagent_factory.cli selfcheck <slug>`, not from a hand
self-assessment. Do not export adapter until that gate returns PASS/WARNING.

---

## Output

- `subagents/<slug>/profile.yaml`
- `subagents/<slug>/provenance-ledger.md`
- `subagents/<slug>/CHANGELOG.md`
- `subagents/<slug>/README.md`
- `subagents/<slug>/tests/golden-tests.yaml`
- Phase 8 self-check verdict
