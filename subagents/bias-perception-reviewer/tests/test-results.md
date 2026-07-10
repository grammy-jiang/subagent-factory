# Test Results — bias-perception-reviewer

**Generated:** 2026-07-10T11:32:03.318920+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'bias-perception-reviewer' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 4 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A structured review that, per finding, names the bias or pe… |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The analyst and decision-maker hold final authority over th… |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 3 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | WARNING | profile body ~846 words (> 800); 46 over the 800-word budget; heaviest: quality_bar 151w, when_to_use 118w, modes 110w |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 6 golden, 2 negative routing |

## Routing Tests (structural)

**Records validated:** 10/10

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — vivid-analogy anchoring, vague odds, centralized-actor, dismissed evidence |
| GT-002 | SCHEMA-OK | Positive routing — forecast overconfidence, no track record or postmortem |
| GT-003 | SCHEMA-OK | Positive routing — motivated reasoning and belief perseverance |
| GT-004 | SCHEMA-OK | Positive routing — framing and prospect-theory effects in a decision memo |
| GT-005 | SCHEMA-OK | Positive routing — base-rate neglect, conjunction, evidence quality |
| GT-006 | SCHEMA-OK | Positive routing — single mind-set, no alternative hypotheses |
| NR-001 | SCHEMA-OK | Negative routing — request to make the substantive judgment / supply reasons for a foregone conclusion |
| NR-002 | SCHEMA-OK | Negative routing — clinical psychological diagnosis of an individual |
| MC-001 | SCHEMA-OK | Missing context — forecast with no resolution criteria or track record |
| MC-002 | SCHEMA-OK | Missing context — "review for bias" with no analysis or evidence supplied |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
