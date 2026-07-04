---
name: context-and-harness-engineering-reference
kind: reference
status: ready
provenance:
  principles:
  - P058
  - P066
  - P083
  - P084
  - P086
  - P100
  - P105
  - P106
  - P108
  - P109
  - P127
  - P128
  - P129
  - P130
  - P131
  - P141
  - P142
  - P144
  - P146
  - P147
  - P148
  - P149
  claims:
  - C01167
  - C01168
  - C01827
  - C01502
  - C01503
  - C01504
  - C01505
  - C01506
  - C01507
  - C01198
  - C01199
  - C01200
  evidence:
  - E00541
  - E00542
  - E00752
  - E00640
  - E00641
  - E00642
  - E00643
  - E00644
  - E00645
  - E00561
  - E00562
  - E00563
  source_anchors:
  - a0c96ef125b7-c0000
  - f33934784451-c0000
  - a3e5d595f78f-c0000
  - 5e5bb110f00c-c0000
  authored_from_digest: 9c1a4b119cadf5883c814ace551a4353de4063536216300d530419e261db8d38
---

# Reference: context-and-harness-engineering-reference

## Purpose

The context-engineering, tool-design, and harness concepts a skill author should know when a
skill runs inside a long or high-stakes agent loop — how to budget context, design tools, and
reason about the harness/session/sandbox split and evaluation infrastructure. Grounded in P105,
P106, P130, P144, P141.

## Context as a scarce budget

- Treat context as a scarce resource: include enough for reliable behaviour, but prefer the
  smallest high-signal set over broad accumulation [P105].
- Exploit the filesystem model — bundled files cost no context tokens until read — by naming files
  descriptively and organizing by domain or feature so the agent loads only what it needs [P131].
- Rely on live agentic search (traverse the current file tree with grep and reference-following)
  rather than a maintained embedding index [P130].
- Bound and paginate tool/script output to protect the context budget: default to a summary or
  limit, support pagination (offset/range) and filtering [P058].

## Designing tools for agents

- Design tools as clear, non-overlapping, token-efficient contracts with robust behaviour and
  unambiguous parameters, around how a nondeterministic agent perceives choices [P106].
- Use tool input examples to teach conventions a schema cannot express (optional-field patterns,
  nested-object usage, correlated parameters) [P084].
- Use deferred tool discovery for large tool libraries so the model loads only the definitions it
  needs [P066].

## Long-task failure modes

Design explicit mechanisms against the two dominant long-task failure modes — loss of coherence as
the context window fills, and unreliable or over-generous self-assessment of progress [P141].
Avoid irreversible retain/discard context decisions on long-horizon tasks; store context as an
interrogable object outside the window rather than compacting or trimming blindly [P083].

## Harness / session / sandbox virtualization

| Concept | Guidance | Principle |
|---------|----------|-----------|
| Virtualize the agent | separate session (event log), harness (model loop + tool router), and sandbox (code/exec) into independently swappable components | P144 |
| Do not couple them | a single "pet" container that fuses session+harness+sandbox loses the session on container failure and makes failures indistinguishable | P100 |
| Container resources | set a guaranteed allocation and a separate, higher hard-kill limit; never pin both to the same value (zero headroom) | P146 |

## Choosing loop complexity

- Start with the simplest LLM design that solves the task; add agentic complexity only when
  measured outcomes justify the latency, cost, and risk [P108].
- Choose workflows for predictable predefined paths; choose autonomous agents only when flexible,
  model-directed control is needed [P109].
- Use turn-based loops for short, irregular tasks and reduce extra turns with specific prompts and
  explicit verification [P127]. Improve loop output with a clean codebase, accessible docs,
  explicit verification, and independent review [P128]; manage cost by picking the right primitive
  and model, defining stop criteria, and scripting deterministic work [P129].

## Agentic-evaluation infrastructure caveats

- Separate infrastructure-reliability gains from capability gains: added headroom (up to ~3×)
  mainly removes transient-spike failures without making the agent smarter [P086].
- Hold the entire runtime constant when comparing models (same harness, task set, hardware)
  [P147]; publish both recommended per-task resource specs and the enforcement methodology
  [P148]; treat leaderboard differences below ~3 percentage points as within uncertainty until
  the configuration is documented [P149].

## Grounding

Principles: P058, P066, P083, P084, P086, P100, P105, P106, P108, P109, P127, P128, P129, P130, P131,
P141, P142, P144, P146, P147, P148, P149. Distillation-only: no verbatim source quotation.
