# software-architecture

**Software Architecture Reviewer** — a generated subagent package.

Evaluates and guides software-architecture decisions, structures, and designs, judging them against
the system's prioritized architecture characteristics and the trade-offs each choice implies. It
reviews structure, dependency direction, modularity, architecture-style selection, distributed
coupling, enterprise layering, and event/message integration. It critiques and advises — it does
not write production code or choose products.

## Modes

- **review** — critique an existing architecture, design, or structure.
- **advise** — guide an architecture decision toward the structure that fits the driving forces.
- **compare** — contrast two or more architecture styles or approaches by characteristic profile.

## Grounding (multi-source, distillation-only)

| Source | Author | Year |
|--------|--------|------|
| Fundamentals of Software Architecture | Mark Richards, Neal Ford | 2020 |
| Clean Architecture | Robert C. Martin | 2018 |
| Software Architecture: The Hard Parts | Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani | 2021 |
| Patterns of Enterprise Application Architecture | Martin Fowler | 2002 |
| Software Architecture Patterns | Mark Richards | 2015 |
| Designing Event-Driven Systems | Ben Stopford | 2018 |
| Enterprise Integration Patterns | Gregor Hohpe, Bobby Woolf | 2003 |
| Scalable Internet Architectures | Theo Schlossnagle | 2006 |
| Scalability Rules: 50 Principles for Scaling Web Sites | Martin L. Abbott, Michael T. Fisher | 2011 |

All nine sources are copyrighted books used under `distillation-only` rights: paraphrase only, no
verbatim quotation (the quote-scan gate confirms no 40+ consecutive-word source spans in output).

## Evidence chain (Tier 2, deep map→reduce build)

- `principles/principles.yaml` — **50 operational principles** (`P001–P050`), each GRADE-graded
  (Step-16): the `grade` block's `grade_confidence().level` equals the declared confidence.
- `analysis/claims.jsonl`, `evidence/evidence-records.yaml` — **2420 source-anchored claims** and
  their evidence records distilled across all nine sources.
- `skills/` — **17 authored skill bodies**; `references/` — **5 authored reference bodies**.
- `tests/` — golden tests, `principle-behaviour-tests.yaml`, and the Step-13 `behaviour-tests.yaml`
  (missing-context + answerable-twin probes for the ask-gate).
- `reports/faithfulness-report.yaml` — over-claim review of every load-bearing rule (clean: all
  findings EXACT_SUPPORT or WITHIN_SCOPE).

## Capabilities

- **Step-16 GRADE evidence grading** — formal confidence per principle (source type + up/down
  factors), enforced by `validate_confidence_grade`.
- **Step-13 Answer/Ask/Abstain ask-gate** (opt-in, `profile.yaml: ask_gate`) — each
  decision-context-dependent principle carries `must_ask_for` slots so the advisor asks one specific
  clarifying question when a driving force is unstated, rather than committing on underspecified
  input. Measured by the missing-context tests + answerable twins.

## Package layout

- `profile.yaml` — canonical source of truth for this subagent.
- `principles/`, `analysis/`, `evidence/` — the evidence chain.
- `skills/`, `references/` — authored bodies.
- `tests/` — golden, principle-behaviour, and ask-gate behaviour suites + self-check results.
- `reports/faithfulness-report.yaml` — faithfulness review.
- `adapters/claude-code/software-architecture.md` — exported runtime adapter (do not edit).

## Status

`ready`. See `CHANGELOG.md` for the version history and `profile.yaml` for the current
`agent_version`.

> Do not edit generated artifacts by hand. Change `profile.yaml` and re-run the factory pipeline.
