---
name: research-to-blueprint-and-gap-classification
kind: skill
status: ready
provenance:
  principles:
  - P031
  - P051
  - P091
  - P093
  - P094
  - P125
  - P133
  - P134
  - P135
  - P136
  - P137
  - P139
  - P140
  - P141
  - P142
  - P143
  - P144
  claims:
  - C00013
  - C00019
  - C00075
  - C00076
  - C00020
  - C00077
  - C00078
  - C00005
  - C00006
  - C00015
  - C00016
  - C00028
  - C00029
  - C00021
  - C00017
  - C00018
  - C00022
  - C00023
  - C00024
  - C00027
  - C00030
  - C00031
  - C00035
  - C00036
  - C00037
  source_anchors:
  - 8707406d317e-c0000
  - 8707406d317e-c0001
  - 2a049107e960-c0000
  - 2a049107e960-c0001
  authored_from_digest: 2c50df7877ef0a2594e2969c369dbdd84503b322e7728ed87e0c2a852fd9009d
---

# Research-to-Blueprint Translation & Gap Classification

## Purpose

This skill reviews how a product blueprint (or a research synthesis in the process of
becoming one) translates research findings into product-level content, and how it
classifies and stages the gaps that translation surfaces. It checks that findings become
reusable product primitives rather than a second literature summary (P125); that every
open gap is routed to the right consequence — engineering gaps toward roadmap-sized
product work, academic gaps toward validation or an open question, out-of-scope gaps
toward a stated non-goal (P031); that academic gaps stay out of MVP-0 and Phase 1 unless
the product's whole purpose is to validate them (P051); and that the resulting MVP scope
is staged conservatively rather than expanded on the strength of "we already researched
it" (P136, P137). It reviews and advises on this translation and classification work; it
does not perform the translation itself, write the blueprint's product content, or make
the gap-classification call on the team's behalf.

## When to use

- The caller has a Research-to-Product Translation Map, an Adopt/Adapt/Merge/Defer/Reject
  decision list, or a gap-classification table — or the underlying research synthesis
  those sections should be drawn from — and wants it checked before the blueprint moves
  downstream.
- The caller wants to know whether an academic (open, no-consensus) question has quietly
  become an MVP requirement, or whether an engineering gap was mis-sized into the wrong
  roadmap tier.
- The caller wants the MVP-0 / MVP-1 / safety-baseline / evaluation-baseline / deferred-
  scope split checked for conservatism, especially after a long or gap-heavy research
  round.
- The caller wants to confirm the blueprint's own input-quality and delivery quality gates
  actually ran, rather than assuming a plausible-looking document already passed them.
- The caller is deciding whether a specific capability, workflow, or risk item is
  adequately traceable to evidence, or is quietly resting on an unlabeled assumption.

## Procedure

Work through these checks in order. Each failure is a finding that names the principle,
the location, the trade-off implied, and a concrete remediation — never a rewrite of the
blueprint's prose; remediation is handed back to the blueprint's owner.

1. **Confirm the stage boundary (P091).** Check that the material under review is
   genuinely product-design-from-research work. If a passage is actually doing more
   literature research, choosing a technology stack, designing detailed UX, eliciting
   requirements as user stories, or explaining a single paper, flag it as out of place and
   recommend routing it to that specialized stage instead of folding it into the
   translation.
2. **Confirm the input-quality gate (P093).** Check that input quality was classified
   before any translation started. If the underlying research material is insufficient,
   the correct move was to stop rather than produce a blueprint from thin material; if it
   is merely weak, the missing areas must be recorded as explicit assumptions or open
   questions, not silently filled in with plausible-sounding detail.
3. **Confirm domain scoping (P133).** If the research spans more than one unrelated
   product domain, check that the blueprint scoped itself to the highest-evidence domain
   by default, and that it asked the caller to choose only when multiple domains carried
   comparably strong evidence and would have produced materially different theses.
4. **Confirm extraction and tagging (P134).** Check that mechanisms, methods, patterns,
   benchmarks, assumptions, contradictions, gaps, risks, and architecture hints were
   pulled out and each tagged with its type and a confidence grade before translation
   began. An untagged, ungraded pile of findings is a process gap even when the final
   prose reads smoothly.
5. **Confirm translation into primitives (P125).** Check that each research finding
   became a reusable product primitive — a capability, workflow, policy, conceptual
   component, information object, evaluation requirement, governance rule, risk control,
   user interaction, lifecycle state, or integration surface — rather than a restated
   finding. Where two primitives cover the same ground, flag it and recommend merging them
   before they are composed into a capability or workflow.
6. **Confirm idea resolution (P135).** Check that every major idea carries one explicit,
   conservative decision: ADOPT, ADAPT, MERGE, DEFER, REJECT, or DEFER / VALIDATE. An idea
   with no recorded decision, or an ADOPT resting on thin support, is a finding.
7. **Confirm gap classification (P031).** For every open gap, check it against the right
   consequence: an engineering gap (the field already knows how to solve it in principle,
   it is just not yet productionized at the needed scale, latency, or robustness) becomes
   scoped product work; an academic gap (an open question without consensus) becomes a
   validation requirement or open question, never a feature treated as already solved;
   anything out of scope becomes a stated non-goal. Treating any open gap as solved is a
   hard finding, not a style note.
8. **Confirm the academic-gap MVP boundary (P051).** Check that no academic gap has been
   folded into MVP-0 or Phase 1 unless the product's entire purpose is to answer that
   research question, and that the underlying assumption is carried consistently — into
   the decision record, the risk model, the evaluation strategy, the MVP exclusions, the
   roadmap, and the open questions — rather than named once and then dropped.
9. **Confirm MVP staging and gap-closure pressure (P137, P136).** Check that scope is
   split into MVP-0 (the smallest slice demonstrable end to end), MVP-1 (the first usable
   version), a safety baseline, an evaluation baseline, and deferred scope, with MVP-0 kept
   minimal. Where the material shows a long history of gap-closure rounds, or a readiness
   signal that gaps remain, treat that as pressure to defer or reject speculative scope —
   never as license to expand MVP-0 because the research effort already feels
   substantial.
10. **Confirm traceability.** Check that every major capability cites either a research
    source or a clearly constrained design decision, and that anything without either is
    explicitly labeled a validation-requiring design hypothesis rather than left with a
    blank citation cell. (This check reflects the profile's always-on traceability rule
    for this skill, P138, alongside this skill's own claim set — see Provenance.)
11. **Confirm workflow completeness (P140).** For each major workflow the material
    documents, check that it states a trigger, its inputs, its decision gates, its steps
    or flow, its outputs, its failure modes, and its success criteria. A workflow missing
    any of these is incomplete, not just under-detailed.
12. **Confirm the delivery quality-gate discipline (P094).** Check that quality gates ran
    before the material was treated as final; that any repair pass fixed wording without
    quietly loosening a scope or evidence claim; that repairs were rechecked rather than
    trusted on the first pass; and that repeated gate failure stopped delivery rather than
    shipping anyway. A tech-stack choice, code, a missing required diagram, an unvalidated
    "solved" gap, an omitted risk, uncontrolled routing language, or unstructured essay
    prose is a hard failure, not a suggestion.
13. **Confirm release-gate confidence (P139).** Where a specific release gate rests on
    medium- or low-confidence evidence, check that it stays mandatory only because a
    high-impact risk, the absence of a cheaper control, and an immediate need justify it
    together; otherwise recommend downgrading that gate rather than leaving it as a hard
    blocker on thin support.
14. **Confirm risk treatment (P141).** Check that high-impact risks are named explicitly,
    that mitigations are concrete rather than vague, that safety-critical deferrals are
    written as actual release gates rather than merely noted, and that any risk stemming
    from an unvalidated academic item is flagged as such.
15. **Confirm bookkeeping hygiene (P142, P143, P144).** Check that the topic slug is
    stable and was derived from source metadata, filename, project name, or an explicit
    user slug rather than invented ad hoc; that auto-discovered input candidates are
    recorded with their path, selection status, confidence, and reason; and that decisions
    are kept separate from assumptions, with any high-risk assumption — one that could
    affect security, privacy, the review workflow, a trust boundary, or viability — routed
    to the caller or a downstream review trigger rather than folded silently into a
    decision.

## Inputs

- The blueprint sections under review — typically the source-research interpretation, the
  research-to-product translation map, the Adopt/Adapt/Merge/Defer/Reject decisions, the
  MVP scope, and the open-questions/validation plan — or, when the blueprint is still
  being drafted, the underlying research synthesis report those sections should come from.
- Any structured gap classification (engineering / academic / out-of-scope), if supplied
  separately from the blueprint prose.
- The caller's stated outcome, MVP appetite, and risk tolerance, so severity calls (for
  example, whether to downgrade a release gate) are tied to the caller's actual posture
  rather than a generic default.
- Whatever round-history or gap-closure signal is available (how many prior rounds ran,
  whether gaps remain), since it directly weighs the MVP-staging check.

## Output

A findings list keyed to the principles above: each entry names the specific primitive,
decision, gap, MVP item, workflow, risk, or bookkeeping field at issue, the principle it
fails against, the trade-off the current wording implies, and a concrete remediation the
blueprint's owner can apply. When the caller instead wants advice on a single upcoming
call — how to classify one gap, whether one item belongs in MVP-0 — the output is a single
recommendation in the same form: the principle applied, the assumption it tests, and the
residual trade-off. This skill never rewrites the blueprint's product content itself; it
hands remediation back to the blueprint's owner.

## References

- `../../references/blueprint-principles-index.md` — the package-wide principle index,
  including the neighboring translation and outcomes-over-output principles (for example
  P090, and P125's composition context) that frame this same review alongside the
  blueprint-altitude and build-trap skills.

## Provenance

Grounded in 17 HIGH-confidence principles (P031, P051, P091, P093, P094, P125,
P133–P137, P139–P144), derived from 25 selected claims spanning C00005–C00037 and
C00075–C00078, against the Product Blueprint and Stage-Boundary Skill Contract
(`source_anchors` `8707406d317e-c0000`, `8707406d317e-c0001`). The Lean Startup source
anchors (`2a049107e960-c0000`, `2a049107e960-c0001`) are carried in this skill's
provenance per the package's shared evidence chain. Step 10's traceability check
additionally reflects P138 — the profile's always-on rule for this skill — which sits
outside this skill's own claim set above but is directly on-topic, and is named here
rather than silently folded in.

| Step | Principle(s) | Check |
|---|---|---|
| 1 | P091 | Stage / intent boundary |
| 2 | P093 | Input-quality gate |
| 3 | P133 | Domain scoping |
| 4 | P134 | Extraction & tagging |
| 5 | P125 | Translate to primitives, merge overlaps |
| 6 | P135 | ADOPT / ADAPT / MERGE / DEFER / REJECT |
| 7 | P031 | Engineering / academic / out-of-scope routing |
| 8 | P051 | Academic gaps excluded from MVP-0 / Phase 1 |
| 9 | P137, P136 | MVP staging; gap-closure pressure |
| 10 | P138 (profile always-on) | Traceability to citation or decision |
| 11 | P140 | Workflow completeness |
| 12 | P094 | Delivery quality-gate discipline |
| 13 | P139 | Release-gate confidence |
| 14 | P141 | Risk treatment |
| 15 | P142, P143, P144 | Slug / input-candidate / decision-assumption hygiene |
