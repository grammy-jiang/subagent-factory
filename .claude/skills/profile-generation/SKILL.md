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

Verify profile against all 18 checks in Phase 8.
Report PASS / WARNING / FAIL.
Do not export adapter until PASS.

---

## Output

- `subagents/<slug>/profile.yaml`
- `subagents/<slug>/provenance-ledger.md`
- `subagents/<slug>/CHANGELOG.md`
- `subagents/<slug>/README.md`
- `subagents/<slug>/tests/golden-tests.yaml`
- Phase 8 self-check verdict
