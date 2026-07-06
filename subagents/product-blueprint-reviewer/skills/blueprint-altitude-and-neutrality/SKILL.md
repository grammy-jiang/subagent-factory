---
name: blueprint-altitude-and-neutrality
kind: skill
status: ready
provenance:
  principles:
  - P030
  - P058
  - P090
  - P092
  - P096
  - P101
  - P126
  - P127
  - P128
  - P129
  - P130
  - P131
  - P138
  - P146
  - P169
  claims:
  - C00011
  - C00014
  - C00072
  - C00073
  - C00096
  - C00101
  - C00113
  - C00001
  - C00002
  - C00033
  - C00034
  - C00091
  - C00117
  - C00119
  - C00124
  - C00025
  - C00032
  - C00007
  - C00008
  - C00009
  - C00010
  - C00026
  - C00039
  - C00074
  source_anchors:
  - 8707406d317e-c0000
  - 8707406d317e-c0001
  - 2a049107e960-c0000
  - 2a049107e960-c0001
  authored_from_digest: 935ff7577576db32a9381560abb3d8153469a0cc0082843832dd96b51be78f12
---

# Blueprint Altitude and Implementation Neutrality

## Purpose

Hold a product blueprint at the correct altitude: implementation-neutral product
primitives, expressed through neutral logical component names that describe
responsibility boundaries rather than an implementation, anchored in a
research-backed thesis rather than a restated literature review, and delivered as
an ordered, parseable, traceable Markdown artifact that a downstream
technical-design stage can act on without re-reading the source research (P090,
P126, P127, P128, P129, P130, P131, P030, P169, P058, P096, P101, P092, P146,
P138).

## When to use

- The blueprint (or a research synthesis being turned into one) may name a
  specific technology, vendor, deployment model, code, schema, package, ticket,
  or build task, and its altitude needs checking (P030).
- The blueprint's logical component names need checking against being — or
  already having become — source-code modules, classes, services, or deployable
  units, and its logical-architecture section needs checking against silently
  doing the downstream architecture document's job (P169, P058, P096).
- A technology-property claim (enforcement, security, immutability, provider
  neutrality) appears and needs checking against what the named technology
  actually delivers (P101).
- The blueprint's thesis, ordered section structure, navigation, or capability
  citations need checking against drifting into a second literature summary or
  losing traceability (P090, P126, P127, P128, P130, P131, P138).
- The blueprint's artifact-contract fields or output filename convention need
  checking against the shared controlled vocabulary and format (P092, P146,
  P129).

## Procedure

1. **Scan for implementation leakage (P030).**
   - Look for concrete technology, vendor, deployment, code, schema, package,
     ticket, or build-task specifics anywhere in the blueprint.
   - Classify what you find into two tiers: language that hard-names a specific
     product, vendor, or deployment model (rewrite outright), versus
     runtime-leaning language that is not yet a hard failure but must still be
     surfaced rather than silently accepted (rephrase to its purpose, or record
     it as a flagged assumption for the downstream technical-design handoff).
   - Apply a simple test: if the sentence still conveys its constraint once the
     specific product/vendor/deployment name is replaced by the responsibility
     it serves, replace it; if the sentence cannot be stated at all without
     naming that specific product, vendor, or deployment model, it belongs to a
     later technical-design stage, not this blueprint.
   - When a term sits between the two tiers, classify it conservatively (treat
     it as the stricter tier) rather than assuming it is harmless.

2. **Rewrite flagged language as product primitives (P030).**
   - Never simply delete a flagged requirement — restate it as the conceptual
     responsibility it protects (a capability, workflow, policy, information
     object, governance rule, risk control, user interaction, lifecycle state,
     or integration surface).
   - Keep the rewrite traceable to what triggered the flag, so a reader can see
     what was changed and why, not just that a fixed version was substituted.

3. **Check neutral component naming and architecture altitude (P169, P058,
   P096).**
   - Confirm every named logical component is used only to express a
     responsibility boundary or ownership area — never as a de facto
     source-code module, class, service, or deployable unit. Flag any
     component name that has already been given a concrete implementation
     shape.
   - Confirm the blueprint does not map every conceptual component onto its own
     separate service by default; decomposition and ownership belong in
     higher-level views, and a component- or deployment-level view is
     warranted only when a specific trigger calls for it.
   - Because a downstream architecture document will independently need its
     own ordered sections, structural views, responsibility matrices,
     technology-decision rationale, and decision-record coverage for
     high-impact choices, confirm the blueprint's architecture section sets
     the *intent* for that work rather than pre-empting or duplicating it —
     flag any blueprint content that is really doing the architecture stage's
     job.

4. **Check technology-property claims (P101).**
   - If any statement — in the blueprint itself or in an architecture artifact
     under joint review — attributes a property such as enforcement, security,
     immutability, or provider-neutrality to a named technology, confirm the
     technology actually delivers that property; downgrade or remove the claim
     if it overstates what the technology provides.

5. **Check the thesis is research-backed product content, not a rehash of the
   literature (P090, P126, P127, P128).**
   - Confirm findings are expressed as product primitives, workflows,
     architecture intent, MVP scope, evaluation, and handoff material — not as
     restated research findings. A section that still reads like a literature
     summary is exactly what this check exists to catch.
   - Confirm the thesis leads with the primary research-backed mechanism or
     architecture, not a conditional or secondary one, and that actors and
     domains stay aligned with that thesis; confirm metadata is copied from
     the source material rather than invented.
   - Where a structured or machine-readable artifact and the Markdown research
     report disagree, confirm the Markdown report was treated as authoritative
     and the conflict was disclosed — flag any place the blueprint silently
     followed the structured artifact instead.
   - Confirm the blueprint is usable as a handoff: a downstream technical
     designer should be able to choose a stack and plan an implementation from
     it without re-reading the original research.

6. **Check the ordered structure and parseable navigation (P130, P131, P138).**
   - Confirm the full ordered section sequence is present — from the executive
     thesis through the traceability appendix — and flag any missing or
     reordered section.
   - Confirm a linked contents section exists, at least one workflow-level
     diagram and one architecture-level diagram are present, decision- and
     risk-bearing content is in tables, and citations are traceable back to
     the source report.
   - Confirm every major capability traces to a citation or an explicit,
     constrained design decision; anything that does not must be labelled a
     design hypothesis requiring validation — flag any blank citation.

7. **Check artifact-contract hygiene (P092, P146).**
   - Confirm the shared contract fields are present using the controlled
     vocabulary: identity and generation metadata, what was consumed,
     decisions, assumptions, open questions, recommended next stage,
     quality-gate status, and a stated reason wherever a field is marked
     not-applicable.
   - Where the blueprint's own section already carries an equivalent field,
     flag any duplicated boilerplate and recommend mapping to the existing
     section instead of adding a redundant one.

8. **Check the output artifact form (P129).**
   - Confirm the blueprint exists as a single, slug-named product-blueprint
     Markdown document; if file output is unavailable, confirm the full
     blueprint was still produced inline together with the recommended
     filename.

## Inputs

- The blueprint text under review (or the in-progress draft), section by
  section.
- Where available, the source research report it was derived from, so
  authority conflicts and thesis alignment can be checked, and any
  structured/JSON artifact it also consumed.

## Output

A findings list, one entry per flagged item, each naming: the offending
text or section, the principle it violates (cited inline, e.g. "P030, P169"),
its severity tier, and the concrete product-primitive rewrite or fix. Where a
step finds nothing to flag, state that the altitude holds for that check
rather than leaving it silent, so an unreviewed section cannot be mistaken for
a clean one.

## References

- `../../references/blueprint-principles-index.md`

## Provenance

Every check in this skill traces to this package's own principles P030, P058,
P090, P092, P096, P101, P126, P127, P128, P129, P130, P131, P138, P146, and
P169, their derived claims, and the product-blueprint-and-stage-boundary skill
contract source anchors recorded above; nothing here goes beyond that
grounding.
