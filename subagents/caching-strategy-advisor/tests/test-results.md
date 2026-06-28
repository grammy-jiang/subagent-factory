# Test Results — caching-strategy-advisor

**Generated:** 2026-06-12T11:09:18.416888+00:00

## Phase 8 Profile Self-Check

**Verdict:** PASS

| # | Check | Level | Detail |
|---|-------|-------|--------|
| 1 | slug | PASS | slug 'caching-strategy-advisor' is kebab-case and role-based |
| 2 | when-to-use | PASS | 6 triggers |
| 3 | when-not-to-use | PASS | 3 exclusions |
| 4 | modes-evidence | INFO | mode source-evidence traceability delegated to profile-reviewer |
| 5 | inputs-required | PASS | 4 required input(s) |
| 6 | primary-format | PASS | Structured advisory covering: (a) viability verdict with bre |
| 7 | mode-output | PASS | every mode states its output |
| 8 | minimum-useful-output | PASS | defined |
| 9 | canonical-owner | PASS | Architectural principles (Atchison 2021) for caching pattern |
| 10 | may-edit-canonical | PASS | false |
| 11 | quality-bar | PASS | 6 evidence-citing checks |
| 12 | forbidden-behaviours | INFO | 6 rules; source traceability delegated to profile-reviewer |
| 13 | no-procedure-in-body | PASS | no ordered procedure detected in body |
| 14 | body-size | PASS | ~711 words |
| 15 | platform-neutral | PASS | core is platform-neutral |
| 16 | provenance-ledger | PASS | present |
| 17 | no-unresolved-conflict | INFO | conflict resolution review delegated to profile-reviewer / Phase 7 merge log |
| 18 | golden-tests | PASS | 3 golden, 1 negative routing |

## Routing Tests (structural)

**Records validated:** 5/5

| Test ID | Status | Description |
|---------|--------|-------------|
| GT-001 | SCHEMA-OK | Advise mode — standard caching viability request with bell-curve access distribution, known service latency, no side effects, and explicit consistency tolerance. Tests P001 (viability gate), P005 (eviction by distribution), P009 (break-even), P003/P004 (consistency), P010 (pattern ownership). |
| GT-002 | SCHEMA-OK | Validate mode — proposed cache design fails the side-effects condition (P002); advisor must decline to endorse and explain the risk. Also exercises P001 (viability gate fails at the side-effects condition). |
| GT-003 | SCHEMA-OK | Compare mode — comparison of cache scaling options when both storage and write throughput are bottlenecks across two geographic regions. Tests P006 (storage vs resource bottleneck diagnosis) and P007 (topology selection). |
| NR-001 | SCHEMA-OK | Negative routing — request for a production Redis configuration file is out of scope; advisor must decline to produce executable artefacts. |
| MC-001 | SCHEMA-OK | Missing required input — caching request with no access-pattern or side-effect information; advisor must warn and request the inputs. Tests P001 (cannot evaluate viability without distribution) and P009 (cannot calculate break-even without Service_Call_Time). |

> Live routing/permission execution requires a Claude invocation; the records above are validated structurally (schema + inventory).
