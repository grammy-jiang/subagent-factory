# Provenance Ledger — Java Concurrency Reviewer

**Subagent slug:** `java-concurrency-reviewer`
**Profile version:** 0.2.0
**Generated:** 2026-06-08T00:00:00+00:00

---

## Source Registry

| ID | Title | Author | Year | Authority | Rights | Volatility | Review cadence |
|----|-------|--------|------|-----------|--------|------------|----------------|
| concurrent-programmi-20260608115137 | Concurrent Programming in Java: Design Principles and Patterns | Doug Lea | 1997 | secondary | distillation-only | low | annual |
| oaks-scott-wong-henr-20260608122800 | Java Threads | Scott Oaks & Henry Wong | 2004 | secondary | distillation-only | low | annual |

**Rights note:** distillation-only throughout for both sources. No verbatim quotation from
either source is permitted in any generated artifact. All prose is original paraphrase;
all code suggestions must be original derivations, not copied from the source texts.

---

## Distillation Log

### Version 0.1.0 decisions (SUPERSEDED WHERE NOTED — kept visible per policy)

| Field | Source IDs | QIDs | Notes |
|-------|-----------|------|-------|
| `slug` | concurrent-programmi-20260608115137 | Q1 | Derived from display name as kebab-case role label |
| `display_name` | concurrent-programmi-20260608115137 | Q1 | Taken directly from q1_display_name |
| `role` | concurrent-programmi-20260608115137 | Q1, Q2 | v0.1.0: synthesised from q1_role and q2_job; paraphrased. SUPERSEDED at 0.2.0 — see below. |
| `when_to_use` (5 triggers) | concurrent-programmi-20260608115137 | Q3 | Five triggers from q3_triggers; line refs 857, 1430–1431, 2083, 10013–10014, 81, 1758, 3747, 4229, 2847–2860, 2891–2906, 3041–3042, 4770, 5289–5304, 5619–5621, 7078–7082, 9890, 9937. SUPERSEDED at 0.2.0 — two triggers added; originals retained. |
| `when_not_to_use` (3 exclusions) | concurrent-programmi-20260608115137 | Q4 | Three exclusions; line refs 1002, 2506, 4553, 5570, 5574, 4864–4868, 9327–9329. SUPERSEDED at 0.2.0 — one exclusion strengthened, one added. |
| `inputs.required` | concurrent-programmi-20260608115137 | Q5, Q16 | Concrete code or design artefact; context about concurrent role. SUPERSEDED at 0.2.0 — volatile fields and Executor config added to enumeration. |
| `outputs.primary_format` | concurrent-programmi-20260608115137 | Q6 | Canonical deliverable noun from q6_primary_deliverable. SUPERSEDED at 0.2.0 — extended to include patch-suggest output. |
| `outputs.modes` (review, advise, compare) | concurrent-programmi-20260608115137 | Q9 | Three modes; line refs 1124, 9937, 1758, 2749, 2847, 81, 1563, 4770, 5302, 9883, 8281–8282, 2807–2808, 4770–4771, 5619–5622, 3470, 3797. SUPERSEDED at 0.2.0 — patch-suggest mode added; review mode output extended. |
| `quality_bar` (5 items) | concurrent-programmi-20260608115137 | Q7 | Five quality marks; line refs 1430–1431, 1932–1940, 10013–10026, 952, 2083–2085, 3948, 3046–3047, 1758, 3343, 4229, 9883, 2847–2860, 3041–3042, 2122–2123, 3470, 3748. SUPERSEDED at 0.2.0 — volatile item refined; two items added; total: 7. |
| `minimum_useful_output` | concurrent-programmi-20260608115137 | Q11 | From q11_minimum_output. SUPERSEDED at 0.2.0 — "specific field or method at risk" added from source 2. |
| `forbidden_behaviours` (4 items) | concurrent-programmi-20260608115137 | Q10 | Four do-not rules; line refs 3046–3047, 4864–4868, 1002, 2083–2085, 2122–2123. SUPERSEDED at 0.2.0 — two items added from source 2; total: 6. |
| `handoff_rules` | concurrent-programmi-20260608115137 | Q8 | From q8_handoff; evidence gap noted — downstream role inferred (line 9880). UNCHANGED at 0.2.0. |
| `source_of_truth_policy.canonical_owner` | concurrent-programmi-20260608115137 | Q8, Q17 | Developer/tech lead per q8_handoff. UNCHANGED at 0.2.0. |
| `source_of_truth_policy.may_edit_canonical` | concurrent-programmi-20260608115137 | Q8 | Specialist role confirmed — reviewer does not own canonical code. UNCHANGED at 0.2.0. |
| `source_of_truth_policy.precedence` | concurrent-programmi-20260608115137 | Q17 | From q17_source_of_truth. SUPERSEDED at 0.2.0 — dual-source authority added. |
| `knowledge_partition.always_on` (8 items) | concurrent-programmi-20260608115137 | Q12 | Eight invariant concepts; line refs 1430–1434, 1932–1940, 1842–1844, 2847–2858, 2902–2903, 2122–2123, 3748, 1563, 2020, 2037–2038, 1435, 1983–1985, 952, 3046–3047, 3948. SUPERSEDED at 0.2.0 — four items added; total: 12. |
| `knowledge_partition.skills` (8 items) | concurrent-programmi-20260608115137 | Q13 | Eight skills; line refs 2842–2858, 3126–3147, 2083–2134, 3179–3298, 3470–3479, 8480, 3884–3945, 3948, 4770–4771, 5619–5622, 7809, 8584, 9738–9746, 9731–9783. SUPERSEDED at 0.2.0 — six skills added; total: 14. |
| `knowledge_partition.references` (4 items) | concurrent-programmi-20260608115137 | Q14 | Four references; line refs 4229, 1423–1490, 9937, 996–999. SUPERSEDED at 0.2.0 — three references added; total: 7. |
| `knowledge_partition.mcp` | concurrent-programmi-20260608115137 | Q15 | Empty by design; source makes no reference to external tool retrieval. UNCHANGED at 0.2.0. |
| `knowledge_partition.caller_supplied` (3 items) | concurrent-programmi-20260608115137 | Q16 | Three caller-supplied items; line ref 9622 for java.util.concurrent. SUPERSEDED at 0.2.0 — Java version item refined; Swing/AWT item added; total: 4. |

---

### Version 0.2.0 additions and refinements (from source 2: oaks-scott-wong-henr-20260608122800)

| Field | Source IDs | QIDs | Notes |
|-------|-----------|------|-------|
| `role` (merged) | concurrent-programmi-20260608115137, oaks-scott-wong-henr-20260608122800 | Q1, Q2 (both) | Merged role sentence combines design-pattern frame (source 1) and Thread-API/Executor frame (source 2). Conflict class: framing difference — resolved by absorption. See merge-conflict-log.md C-20. |
| `when_to_use` trigger: scheduling/priority review | oaks-scott-wong-henr-20260608122800 | Q3 | Source 2 Chapter 9 coverage; lines 7626–7932. Source 1 explicitly deferred on priority scheduling. Conflict: source 2 adds. See C-02. |
| `when_to_use` trigger: Executor/ThreadPoolExecutor review | oaks-scott-wong-henr-20260608122800 | Q3 | Source 2 Chapter 10 coverage; lines 8346–8435. Source 1 (1997) predates java.util.concurrent. Conflict: source 2 adds. See C-03. |
| `when_not_to_use`: distributed-system exclusion | oaks-scott-wong-henr-20260608122800 | Q4 | Source 2 Preface lines 206–215, Chapter scope lines 297–357. Source 1 silent on this boundary. Conflict: source 2 adds. See C-05. |
| `when_not_to_use`: OS/JVM scheduler tuning (strengthened) | concurrent-programmi-20260608115137, oaks-scott-wong-henr-20260608122800 | Q4 (both) | Both sources agree on this exclusion; source 2 adds rationale. Conflict: agreement with refinement. See C-04. |
| `inputs.required` (volatile fields, Executor config enumerated) | oaks-scott-wong-henr-20260608122800 | Q5 | Preface lines 184–215. Additive detail from source 2 scope. |
| `outputs.modes` — patch-suggest (new) | oaks-scott-wong-henr-20260608122800 | Q9 | Source 2 provides concrete minimal corrective examples (volatile done flag lines 1531/1781/2024; lock scope reduction lines 2141–2162; guarded-loop fix lines 3425–3445; notify→notifyAll Chapter 4). Source 1 has no evidence for this mode. Mode-conflict rule applied: keep both. See C-06. |
| `outputs.modes` — review (output extended) | oaks-scott-wong-henr-20260608122800 | Q9 | Review mode output now includes priority inversion finding type, derived from source 2 Chapter 9. |
| `quality_bar` — volatile precision (refined) | oaks-scott-wong-henr-20260608122800 | Q7 | Lines 2192–2235, 4008–4127. Source 2 adds compound-operation / single-variable distinction and array/reference exclusion. Conflict: refinement. See C-08. |
| `quality_bar` — scheduling/priority hazard check (new) | oaks-scott-wong-henr-20260608122800 | Q7 | Lines 7737–7932. Three-case distinction: JVM model, OS mapping mismatch, priority inversion. Conflict: source 2 adds. See C-09. |
| `quality_bar` — thread-pool configuration check (new) | oaks-scott-wong-henr-20260608122800 | Q7 | Lines 8346–8435, Chapter 14. Pool size, queue type, thread-creation cost. Conflict: source 2 adds. See C-10. |
| `minimum_useful_output` (specific field/method added) | oaks-scott-wong-henr-20260608122800 | Q11 | Lines 1116–1127, 2192–2197, 3454–3463. Conflict: source 2 refines. See C-19. |
| `forbidden_behaviours` — deprecated Thread methods (new) | oaks-scott-wong-henr-20260608122800 | Q10 | Lines 1462. Source 1 predates widespread deprecation. Conflict: source 2 adds. See C-11. |
| `forbidden_behaviours` — volatile misuse (new) | oaks-scott-wong-henr-20260608122800 | Q10 | Lines 2210–2215. Conflict: source 2 adds. See C-12. |
| `source_of_truth_policy.precedence` (dual authority) | concurrent-programmi-20260608115137, oaks-scott-wong-henr-20260608122800 | Q17 (both) | Dual canonical sources with complementary scope. Conflict: framing difference — resolved by dual-precedence statement. See C-17. |
| `knowledge_partition.always_on` — thread lifecycle states (new) | oaks-scott-wong-henr-20260608122800 | Q12 | Chapter 2 outline line 86, lines 1392–1400. Conflict: source 2 adds. See C-13. |
| `knowledge_partition.always_on` — interrupt protocol (new) | oaks-scott-wong-henr-20260608122800 | Q12 | Lines 1620–1640. Conflict: source 2 adds. See C-14. |
| `knowledge_partition.always_on` — Executor framework (new) | oaks-scott-wong-henr-20260608122800 | Q12 | Lines 8346–8435, Chapter 10 outline lines 335–338. Conflict: source 2 adds. See C-15. |
| `knowledge_partition.always_on` — thread priority model (new) | oaks-scott-wong-henr-20260608122800 | Q12 | Lines 7737–7932. Conflict: source 2 adds. See C-16. |
| `knowledge_partition.skills` — thread stop pattern (new) | oaks-scott-wong-henr-20260608122800 | Q13 | Lines 1531–1640. |
| `knowledge_partition.skills` — lock scope reduction (new) | oaks-scott-wong-henr-20260608122800 | Q13 | Lines 2141–2162. |
| `knowledge_partition.skills` — priority inversion diagnosis (new) | oaks-scott-wong-henr-20260608122800 | Q13 | Lines 7897–7932, 6499–6508. |
| `knowledge_partition.skills` — ThreadPoolExecutor configuration (new) | oaks-scott-wong-henr-20260608122800 | Q13 | Chapter 10 outline lines 130–137, lines 8346–8435. |
| `knowledge_partition.skills` — ThreadLocal for per-thread state (new) | oaks-scott-wong-henr-20260608122800 | Q13 | Lines 5020–5084. |
| `knowledge_partition.skills` — concurrent collections selection (new) | oaks-scott-wong-henr-20260608122800 | Q13 | Chapter 8 outline lines 120–123, lines 6927–7528. |
| `knowledge_partition.references` — thread scheduling overview (new) | oaks-scott-wong-henr-20260608122800 | Q14 | Lines 7737–7932. |
| `knowledge_partition.references` — Executor framework taxonomy (new) | oaks-scott-wong-henr-20260608122800 | Q14 | Chapter 10–11 outline lines 129–143. |
| `knowledge_partition.references` — volatile usage rules table (new) | oaks-scott-wong-henr-20260608122800 | Q14 | Lines 2192–2235, 4061–4127. |
| `knowledge_partition.caller_supplied` — Java version refined | concurrent-programmi-20260608115137, oaks-scott-wong-henr-20260608122800 | Q16 (both) | Java 5.0 named as Executor-API inflection point. Source 2 Preface lines 219–227. Conflict: refinement. See C-18. |
| `knowledge_partition.caller_supplied` — Swing/AWT (new) | oaks-scott-wong-henr-20260608122800 | Q16 | Chapter 7 outline lines 115–119. Swing event-dispatch-thread rule. |
| `sources[]` — second source entry | oaks-scott-wong-henr-20260608122800 | — | Added Oaks/Wong source record to sources array with rights: distillation-only. |

---

## Generated Artifacts

| Artifact | Type | Path | Notes |
|----------|------|------|-------|
| profile.yaml | canonical profile | `subagents/java-concurrency-reviewer/profile.yaml` | |
| provenance-ledger.md | provenance log | `subagents/java-concurrency-reviewer/provenance-ledger.md` | |
| CHANGELOG.md | version history | `subagents/java-concurrency-reviewer/CHANGELOG.md` | |
| README.md | package readme | `subagents/java-concurrency-reviewer/README.md` | |
| tests/golden-tests.yaml | routing and output tests | `subagents/java-concurrency-reviewer/tests/golden-tests.yaml` | |
| merge-conflict-log.md | Phase 7 conflict log | `subagents/java-concurrency-reviewer/merge-conflict-log.md` | |

---

## Version History

| Version | Date | Changes | Sources involved |
|---------|------|---------|-----------------|
| 0.1.0 | 2026-06-08 | Initial generation | concurrent-programmi-20260608115137 |
| 0.2.0 | 2026-06-08 | Phase 7 multi-source merge: added patch-suggest mode; added scheduling/priority and Executor triggers; added 4 always-on items; added 6 skills; added 3 references; added 2 forbidden behaviours; refined volatile quality-bar item; added 2 quality-bar items; dual canonical-source authority declared; 20 conflict-log rows resolved | concurrent-programmi-20260608115137, oaks-scott-wong-henr-20260608122800 |
| 0.4.0 | 2026-06-15 | Authored examples block (happy-path + failure-recovery) | Adopt the A4 worked-example layer; grounded in existing role/scope, distillation-only |

---

## Open Questions

- Q8 handoff: the Lea source does not name a specific downstream recipient role; the
  description "developer or tech lead who owns the concurrent code" is inferred from
  the book's framing of code review as a developer learning and improvement activity
  (line 9880). The Oaks/Wong source concurs — the audience is developers who correct
  their own programs (Preface lines 188–215). This value remains a reasonable inference.

- Q15 MCP: neither source describes a tool-retrieval or external lookup workflow; mcp
  list is empty by design.

---

## Conflict Log Reference

Full conflict table with 20 rows is in
`subagents/java-concurrency-reviewer/merge-conflict-log.md`.
No factual contradictions between sources were found. All resolutions are additive or
refinements. No source 1 content was silently removed.
