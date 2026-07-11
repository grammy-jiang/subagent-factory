# Provenance Ledger — xv6-kernel-internals-reviewer

## Source pack

| Field | Value |
|-------|-------|
| source_id | `a-simple-unix-like-t-20260613000613` |
| Title | xv6: a simple, Unix-like teaching operating system |
| Authors | Russ Cox, Frans Kaashoek, Robert Morris |
| Year | 2019 (October 27, 2019 edition) |
| Type | PDF, 104 pages, 30,768 words |
| sha256 | `f74bc1cb4b0f146d0fdd0d11f878373e35247302d384b956ae53c55c0b393507` |
| Converter | Docling (re-converted 2026-06-13; replaces earlier markitdown conversion) |
| conversion_status | ok |
| is_scanned | False (real text layer) |
| anchor_count | 126 (Docling recovered real ATX headings; markitdown had produced 0) |
| authority | secondary (commentary on the kernel, not the kernel source itself) |
| rights_status | **distillation-only** |

**Rights determination.** The PDF carries a title page with named authors (Cox,
Kaashoek, Morris) and a date but no explicit license, copyright line, or
"all rights reserved" notice anywhere in the converted text. Per the Step 2a
decision tree, an authored work with no explicit license notice is classified at
the conservative floor `distillation-only`: distillation is allowed, verbatim
quotation is not. Absence of a notice is not treated as public domain. This is
not `unknown` — the work is fully attributable (named authors, known teaching
text), so it does not block the pipeline.

## Phase 2.5 importance ranking

Eight candidate units (the book's major subsystem discussions) were scored on the
nine importance dimensions and run through
`tools.subagent_factory.score_extracted_units`
(`tests/importance-scores.yaml`, worksheet `tests/importance-worksheet.md`).

| Unit | Subsystem | Total /45 | Verdict |
|------|-----------|-----------|---------|
| U1 | Concurrency control (locks, ordering, barriers, sleep/wakeup) | 43 | keep |
| U2 | Isolation and the user/kernel boundary | 40 | keep |
| U3 | Page tables and address spaces (RISC-V) | 36 | keep |
| U4 | Traps, interrupts, system calls | 35 | keep |
| U5 | Scheduling and context switching | 37 | keep |
| U6 | Layered file system + crash-recovery logging | 40 | keep |
| U7 | "Real world" production comparisons | 34 | keep |
| U8 | Chapter exercises (CoW fork, superpages, ASLR) | 18 | **discard** |

The seven kept units drive the profile's modes and knowledge partition. U8
(open-ended exercises) is recorded here for provenance only and deliberately kept
out of the profile — they are extension prompts, not settled design guidance.

## Principles summary (v0.3.0)

The 0.3.0 re-author grounds the profile in 12 evidence-backed principles derived
from the Docling-recovered heading anchors (71 claims, 30 evidence records).

| Principle | Topic | Skill mapping |
|-----------|-------|---------------|
| pr-001 | Process isolation triple (ecall, page table, scheduling) | address-space-and-trap-walkthrough |
| pr-002 | Full trap path trace (uservec / usertrap / usertrapret / userret) | address-space-and-trap-walkthrough |
| pr-003 | User-pointer validation through copyinstr/copyin | address-space-and-trap-walkthrough |
| pr-004 | Multi-field invariant coverage by a single lock | kernel-concurrency-review |
| pr-005 | Global lock-acquisition order to prevent deadlock | kernel-concurrency-review |
| pr-006 | Spinlock barrier and interrupt discipline | kernel-concurrency-review |
| pr-007 | Spinlock vs. sleep-lock selection | kernel-concurrency-review |
| pr-008 | Sleep/wakeup lost-wakeup prevention | kernel-concurrency-review |
| pr-009 | Scheduler / context-switch p->lock discipline | kernel-concurrency-review |
| pr-010 | Seven-layer filesystem analytical frame | filesystem-crash-recovery-review |
| pr-011 | Write-ahead logging atomicity (begin_op / end_op) | filesystem-crash-recovery-review |
| pr-012 | Inode-cache two-level locking and known limitations | filesystem-crash-recovery-review |

## Field provenance (profile.yaml → QID → source evidence + principle)

| Profile field | QID | Source evidence | Principle |
|---------------|-----|-----------------|-----------|
| `display_name` | Q1 | Title page; commentary on the xv6 kernel. | — |
| `role` | Q1, Q2 | Book examines how xv6 implements its Unix-like interface; multiplexing, isolation, controlled interaction are the three stated design goals. | pr-001 |
| `when_to_use[0]` | Q3 | Chs. 2–4: process overview, address-space creation, exec, RISC-V trap machinery. | pr-001, pr-002 |
| `when_to_use[1]` | Q3 | Ch. 5 Locking: mutual exclusion, consistent lock order, memory barriers, sleep/wakeup races. | pr-004, pr-005, pr-006, pr-008 |
| `when_to_use[2]` | Q3 | Isolation framing + exec/copyin/copyout safety. | pr-001, pr-003 |
| `when_to_use[3]` | Q3 | Ch. 8 File system: layered design, crash recovery via logging. | pr-010, pr-011 |
| `when_to_use[4]` | Q3 | "Real world" sections contrasting xv6 with BSD/Linux/FreeBSD. | — |
| `when_not_to_use[0]` | Q4 | Book is a design commentary; covers no build/admin workflow. | — |
| `when_not_to_use[1]` | Q4 | Scope is the small xv6 RISC-V feature set. | — |
| `when_not_to_use[2]` | Q4 | Subject is kernel internals, not user-space programming. | — |
| `inputs.required` | Q5 | Every chapter anchors discussion to named source files. | — |
| `outputs.primary_format` | Q6 | Deliverable form is reasoned prose explaining a mechanism and judging correctness. | — |
| `modes[advise]` | Q9 | Pervasive explain/recommend throughout the book. | pr-001..pr-012 |
| `modes[review]` | Q9 | Repeated critique-against-invariant (deadlock, lost wakeup, exec ELF risk). | pr-004, pr-005, pr-006, pr-011 |
| `modes[compare]` | Q9 | "Real world" sections per chapter. | — |
| `quality_bar[0]` | Q7 | Traceability to named mechanisms and principles. | pr-001..pr-012 |
| `quality_bar[1]` | Q7 | Concurrency invariants: multi-field coverage, lock order, barrier, sleep discipline. | pr-004, pr-005, pr-006, pr-007, pr-008 |
| `quality_bar[2]` | Q7 | Trap/isolation: full path trace, user-pointer validation. | pr-001, pr-002, pr-003 |
| `quality_bar[3]` | Q7 | Filesystem: seven-layer model, logging atomicity, inode concurrency. | pr-010, pr-011, pr-012 |
| `quality_bar[4]` | Q7 | xv6-vs-production framed as deliberate simplification. | — |
| `forbidden_behaviours[0]` | Q10 | Book states xv6 gives all processes root and simplifies for teaching. | pr-001 |
| `forbidden_behaviours[1]` | Q10 | CoW fork, demand paging, multi-user protection, orphaned inode recovery named absent or as exercises. | pr-002, pr-012 |
| `forbidden_behaviours[2]` | Q10 | Derived from invariants the book defends. | pr-001, pr-003, pr-005, pr-006, pr-011 |
| `forbidden_behaviours[3]` | Q10 | Faithfulness rule: no claim stronger than its source support. | pr-007 |
| `minimum_useful_output` | Q11 | Smallest useful unit is a grounded mechanism + invariant + principle. | — |
| `handoff_rules`, `canonical_owner` | Q8, Q17 | Code/coursework owner decides; reviewer advises. | — |
| `source_of_truth_policy.precedence` | Q17 | xv6 book + source; pr-001..pr-012 as distillation; production behaviour confirmed against real kernel. | — |
| `knowledge_partition.always_on[0]` | Q12 | Design pillars and trap/page-table framing. | pr-001, pr-002 |
| `knowledge_partition.always_on[1]` | Q12 | Concurrency-control discipline. | pr-004, pr-005, pr-006, pr-007, pr-008 |
| `knowledge_partition.always_on[2]` | Q12 | Filesystem correctness frame. | pr-010, pr-011, pr-012 |
| `knowledge_partition.skills` | Q13 | Detailed procedures extracted to skill bodies. | — |
| `knowledge_partition.references` | Q14 | Reference material: subsystem map, real-world comparisons. | — |

## Mode decision log

- **advise** — assigned. Verb: explain/recommend; deliverable: a reasoned
  explanation of the kernel mechanism. Dominant mode across the whole book.
- **review** — assigned. Verb: critique/evaluate; deliverable: a design critique
  against documented invariants. The book repeatedly judges designs (deadlock,
  lost wakeup, exec ELF risk) and warns where code is unsafe.
- **compare** — assigned. Verb: contrast; deliverable: the documented xv6-vs-real
  distinction. Each chapter's "Real world" section provides this directly.
- **produce, validate, extract, patch-suggest** — NOT assigned. The book explains,
  critiques, and contrasts kernel designs but presents no procedure for drafting a
  kernel from scratch, formally gating against a checklist, extracting structured
  data, or proposing a single bounded patch. No deliverable evidence; withheld per
  the mode-evidence rule.

## Conflicts and gaps

- No multi-source conflict — single source.
- **Evidence gaps:** Q15 (no runtime tool/MCP named by a static commentary);
  Q16 (caller_supplied is empty; inputs.required captures the artifact);
  four unassigned modes above.
- **0.3.0 resolution:** anchor_count was 0 in v0.2.0 (markitdown converter);
  Docling re-conversion recovered 126 real headings, enabling grounding of
  analysis/claims.jsonl (71 claims) and principles/principles.yaml
  (pr-001..pr-012). No prior field decisions are contradicted; the 0.2.0 profile
  rules are now strengthened with explicit principle citations.

## Quotation policy

Rights `distillation-only`: distillation permitted, no verbatim quotation of
the source in generated artifacts. Short evidence fragments in this ledger are
paraphrase or minimal cited phrasing for provenance, kept well under the
40-consecutive-word scan threshold. `quote_scan` must pass clean before release.

## Review schedule

- Cadence: annual (volatility low for the core design ideas).
- Re-review triggers: a new xv6 edition (source-file/line and RISC-V register
  references drift between revisions), or material change in the BSD/Linux/FreeBSD
  behaviour cited in the "Real world" comparisons.

## Version history

| Version | Date | Change | Supersedes |
|---------|------|--------|------------|
| 0.1.0 | 2026-06-09 | Initial derivation from the xv6 book. advise + review + compare modes. | — |
| 0.2.0 | 2026-06-11 | Skill and reference bodies authored (Tier 0; no principle layer). Status: ready. | 0.1.0 |
| 0.3.0 | 2026-06-13 | SUPERSESSION: source re-converted with Docling (126 real headings vs. 0 from markitdown). Profile re-grounded in principles pr-001..pr-012 derived from 71 claims and 30 evidence records. Tier set to 1. quality_bar, always_on, and forbidden_behaviours each cite specific principle IDs. source_id updated to a-simple-unix-like-t-20260613000613. No prior role, modes, skills, or references changed. | 0.2.0 |
| 0.4.0 | 2026-06-15 | Authored examples block (happy-path + failure-recovery) | Adopt the A4 worked-example layer; grounded in existing role/scope, distillation-only |
