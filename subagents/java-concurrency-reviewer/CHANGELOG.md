# Changelog — Java Concurrency Reviewer

All notable changes to this subagent are documented here.

## [0.4.0] — 2026-06-15

### Added

- Authored an `examples` block (A4 worked-example slot): one happy-path + one failure-recovery, grounded in the existing role / when_not_to_use / forbidden_behaviours (distillation-only paraphrase). Rendered into the adapter's `## Worked examples` section.

### Changed

- Bumped `agent_version` 0.3.0 → 0.4.0.

## [0.3.0] — 2026-06-11

### Added (Step 8 — skill & reference body authoring)

- **All 14 skill bodies authored** (`skills/<slug>/SKILL.md`) — guarded suspension,
  transactional-method deadlock + resource ordering, BoundedBuffer offer/poll/put/take,
  open-call/split-synchronization, optimistic methods, thread-per-message vs. worker pool,
  latches/barriers, double-checked-locking applicability, cooperative thread-stop, lock-scope
  reduction, priority-inversion diagnosis, ThreadPoolExecutor configuration, ThreadLocal
  confinement, synchronized-vs-concurrent collections. Each carries `## Purpose / When to use /
  Procedure / Inputs / Output / References / Provenance`.
- **All 7 reference bodies authored** (`references/<slug>.md`) — concurrency pattern taxonomy,
  thread API quick reference, thread scheduling overview, executor framework taxonomy, volatile
  usage rules, safety checklist release gate, concurrency overhead taxonomy (plus the
  complementary Lea pattern-taxonomy table). Tables/checklists, no procedure.

### Changed

- **`status`** — `draft` → `ready` (all stubs authored; Step-8 gate satisfied).
- **`agent_version`** — bumped 0.2.1 → 0.3.0.
- **Adapter** — re-exported from the promoted profile.

### Grounding & rights

- Tier 0 package (no principle/claim/evidence layer): every body grounded in the profile
  `always_on` / `quality_bar` / `when_to_use` / `forbidden_behaviours` rules and the two
  `distillation-only` sources (Lea, *Concurrent Programming in Java*, 1997; Oaks & Wong, *Java
  Threads*, 3rd ed. 2004). `provenance.{principles,claims,source_anchors}` empty (not
  drift-tracked); drift baseline stamped via `cli stale --stamp`.

### Self-check

- `validate_skill_authoring`: all 14 skills + 7 references authored. `quote_scan`: PASS (no
  verbatim). Overall verdict: PASS.

---

## [0.2.1] — 2026-06-08

### Changed

- **Profile body condensed** — `role`, `when_to_use`, `when_not_to_use`, `inputs.required`,
  `outputs.modes`, `quality_bar`, `minimum_useful_output`, `forbidden_behaviours`,
  `handoff_rules`, and `source_of_truth_policy.precedence` reworded for concision. Body
  word count reduced ~957 → ~799 to clear the Phase 8 body-size soft limit (< 800 words).
  Editorial only — no change to modes, scope, quality criteria, or forbidden behaviours;
  all technical specifics (hazard categories, wait/notify checklist, volatile rules,
  priority-inversion handling, pattern names) preserved.
- **`agent_version`** — bumped 0.2.0 → 0.2.1.
- **Adapter** — re-exported from condensed profile; installed adapter re-synced.

### Self-check

- Phase 8 body-size: WARNING (~957 words) → PASS (~799 words). Overall verdict: PASS.

---

## [0.2.0] — 2026-06-08

### Phase 7 Multi-Source Merge

Second source ingested: Scott Oaks & Henry Wong, "Java Threads" (O'Reilly, 3rd ed., 2004).
Rights: distillation-only. 20 conflict-log rows resolved; 0 factual contradictions found.

### Added

- **New mode: `patch-suggest`** — justified by Oaks/Wong source evidence (concrete minimal
  corrective code examples: add volatile, shrink lock scope, fix guarded loop,
  switch notify→notifyAll). Source 1 had no evidence for this mode; added per mode-conflict
  rule (keep-both as mode variants).
- **`when_to_use` trigger: scheduling/priority review** — Oaks/Wong Chapter 9 dedicates full
  coverage to thread priority semantics, OS-portability risks, and priority inversion.
  Lea source explicitly deferred on this topic.
- **`when_to_use` trigger: Executor/ThreadPoolExecutor review** — Oaks/Wong Chapter 10
  covers ThreadPoolExecutor, ScheduledThreadPoolExecutor, Callable/Future as primary review
  targets. Lea source (1997) predates java.util.concurrent.
- **`when_not_to_use` exclusion: distributed-system design** — Oaks/Wong makes the in-process
  JVM boundary explicit.
- **`quality_bar` item: scheduling/priority hazard check** — three-case distinction (JVM
  model, OS mapping mismatch, priority inversion via lock contention).
- **`quality_bar` item: thread-pool configuration check** — pool size, queue type, and
  thread-creation cost assessment.
- **`forbidden_behaviours` item: deprecated Thread methods** — Thread.stop(),
  Thread.suspend(), Thread.resume() identified as having race conditions; must not be
  recommended.
- **`forbidden_behaviours` item: volatile misuse** — volatile must not be used as a
  substitute for synchronized for compound operations.
- **4 always-on items**: thread lifecycle states, thread priority model, Executor framework,
  interrupt protocol — all from Oaks/Wong Q12.
- **6 skills**: thread stop pattern, lock scope reduction, priority inversion diagnosis,
  ThreadPoolExecutor configuration, ThreadLocal for per-thread state, concurrent collection
  selection — all from Oaks/Wong Q13.
- **3 references**: thread scheduling overview, Executor framework taxonomy, volatile usage
  rules table — all from Oaks/Wong Q14.
- **caller_supplied item: Swing/AWT** — Swing event-dispatch-thread rule added from
  Oaks/Wong Q16.

### Changed

- **`role` sentence** — merged to cover both design-pattern frame (Lea) and Thread-API /
  Executor frame (Oaks/Wong). Conflict class: framing difference, resolved by absorption.
- **`quality_bar` volatile item** — refined with compound-operation / single-variable
  distinction and array/reference exclusion from Oaks/Wong lines 2192–2235, 4008–4127.
- **`minimum_useful_output`** — "specific field or method at risk" added per Oaks/Wong Q11.
- **`source_of_truth_policy.precedence`** — dual canonical-source authority declared:
  Lea for design patterns/principles; Oaks/Wong for Thread-API and Executor-framework.
- **`sources[]`** — second source record added (oaks-scott-wong-henr-20260608122800).
- **`caller_supplied` Java version item** — Java 5.0 named as the Executor-API inflection
  point (combined from both sources).
- **`outputs.modes` review output** — extended to include priority inversion finding type.
- **`agent_version`** — bumped 0.1.0 → 0.2.0.

### Conflicts Resolved

See `merge-conflict-log.md` for the full 20-row conflict table. Notable resolutions:
1. **Framing difference (C-01, C-17)** — dual frames retained; neither source's organizing
   principle was discarded. Dual canonical-source authority declared in precedence field.
2. **Mode conflict (C-06)** — patch-suggest mode added from source 2; compare mode retained
   from source 1 even though source 2 is silent on it (one-source silence does not justify
   removal).
3. **Volatile precision (C-08)** — source 2's more precise volatile rules (array and
   reference exclusion) were folded in as a refinement of source 1's briefer statement.

---

## [0.1.0] — 2026-06-08

### Added

- Initial generation from source pack
- Sources: Concurrent Programming in Java: Design Principles and Patterns (Doug Lea, 1997)

### Profile

- Role: An expert reviewer and advisor who evaluates Java concurrent code and designs for safety, liveness, and performance...
- Modes: review, advise, compare

### Notes

- Generated by subagent-factory
- Source rights: distillation-only (no verbatim quotation in generated artifacts)
- Evidence gaps logged in provenance-ledger.md (Q8 handoff inference; Q15 MCP empty by design)
- Phase 8 self-check: PASS
