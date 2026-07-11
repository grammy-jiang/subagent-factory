# Test Results — xv6-kernel-internals-reviewer

**Generated:** 2026-06-13T02:07:48.060364+00:00

## Phase 8 Profile Self-Check

**Verdict:** WARNING

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'xv6-kernel-internals-reviewer' is kebab-case and role-based |
| 2 | when-to-use | PASS | 5 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 1 required input(s) |
| 6 | primary-format | PASS | A written explanation or design critique of how the kernel m |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | The engineer, student, or kernel maintainer who owns the cod |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 5 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 4 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | WARNING | profile body ~957 words (> 800); 157 over the 800-word budget; heaviest: quality_bar 213w, when_to_use 152w, forbidden_behaviours 134w |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 4 golden, 1 negative routing |

## Routing Tests (structural)

**Records validated:** 6/6

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Positive routing — advise mode: explain the trap path (uservec through sret) and the trampoline mapping requirement (pr-002). |
| GT-002 | SCHEMA-OK | Positive routing — review mode: critique kernel code for concurrency defects — lock ordering (pr-005), missing memory barrier (pr-006), and lost-wakeup risk (pr-008). |
| GT-003 | SCHEMA-OK | Positive routing — review mode: critique a filesystem change for crash-recovery correctness and inode concurrency (pr-011, pr-012). |
| GT-004 | SCHEMA-OK | Positive routing — compare mode: contrast xv6 sleep/wakeup and its file-system design with production kernels. |
| NR-001 | SCHEMA-OK | Negative routing — production OS operations and administration is out of scope for a commentary on the xv6 teaching kernel. |
| MC-001 | SCHEMA-OK | Missing required input — no specific mechanism, code path, or change was provided. |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
