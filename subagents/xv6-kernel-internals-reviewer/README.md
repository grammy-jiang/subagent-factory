# xv6-kernel-internals-reviewer

Generated Claude Code subagent package — Tier 1.

**Role:** An expert who explains and critiques the internals of a small
Unix-like teaching operating-system kernel (xv6 on RISC-V) — process and memory
multiplexing, isolation, page tables, traps and device drivers, locking and
concurrency control, scheduling and sleep/wakeup, and the layered file system
with crash-recovery logging. Rules are grounded in principles pr-001..pr-012
derived from the Docling-converted source.

## Modes

- **advise** — explain how a kernel mechanism works and why it is designed that
  way, citing the applicable principle.
- **review** — critique existing kernel code or a proposed change against xv6's
  documented invariants (isolation, lock ordering, memory ordering, user-pointer
  validation, on-disk atomicity), each finding tied to a principle ID.
- **compare** — contrast an xv6 design with how a production kernel (BSD, Linux,
  FreeBSD) handles the same problem.

## Source

| | |
|-|-|
| Title | xv6: a simple, Unix-like teaching operating system |
| Authors | Russ Cox, Frans Kaashoek, Robert Morris |
| Year | 2019 |
| Rights | distillation-only (no verbatim quotation) |
| Converter | Docling (re-converted 2026-06-13; 126 headings recovered) |

## Principles

12 evidence-backed principles (pr-001..pr-012) in `principles/principles.yaml`
ground the profile's quality bar, always-on rules, and forbidden behaviours.

| Range | Topic |
|-------|-------|
| pr-001..pr-003 | Process isolation, trap path, user-pointer validation |
| pr-004..pr-009 | Concurrency: locks, ordering, barriers, sleep-lock choice, sleep/wakeup, scheduler |
| pr-010..pr-012 | Filesystem: seven-layer model, write-ahead logging, inode concurrency |

## Status

`ready` — profile, skills, and references are complete. Profile is at version
0.3.0 (Tier 1, re-grounded in principles from Docling re-conversion).

## Layout

```text
profile.yaml                canonical source of truth
provenance-ledger.md        field → QID → source evidence + principle, rights, mode log
interrogation-records.yaml  Q1–Q18 answers from the source
CHANGELOG.md                version history
principles/principles.yaml  pr-001..pr-012 (12 evidence-backed principles)
tests/                      golden tests, importance ranking
skills/                     skill bodies (kernel-concurrency-review,
                            address-space-and-trap-walkthrough,
                            filesystem-crash-recovery-review)
references/                 reference bodies (xv6-subsystem-map,
                            real-world-os-comparisons)
adapters/claude-code/       generated runtime adapter
sources/                    original PDF, converted Markdown, metadata, reports
analysis/                   claims.jsonl (71 claims), claim-importance-scores.yaml
evidence/                   evidence-records.yaml (30 records)
```
