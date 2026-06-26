---
name: refactoring-toward-deeper-insight
kind: skill
status: ready
provenance:
  principles:
  - P002
  - P010
  claims:
  - C022
  - C023
  - C025
  - C060
  - C061
  - C064
  source_anchors:
  - domaindrivendesignqu-20260612231910-h0018
  - domaindrivendesignqu-20260612231910-h0037
  - domaindrivendesignqu-20260612231910-h0039
  authored_from_digest: 53d10a51dea533473ff13859fee1710bdad61d23a13a9fb56f32bd1a6bdfd9ee
---

# Refactoring Toward Deeper Insight

## Purpose

Guide and critique model-level refactoring: the iterative process of making
implicit domain concepts explicit so the model captures the essential structure
of the domain and sheds the superficial. This is distinct from purely technical,
pattern-based code refactoring. It is driven by new insight into the domain — a
relationship that becomes visible, or a concept that was being used only to
explain other concepts and is then recognised as a first-class part of the model.

The reviewer uses this skill to judge two things. First, whether model and code
still correspond: a portion of the software must literally reflect the domain
model, so the mapping between the two is obvious. Refactoring the code to a state
where it no longer expresses the model is a design failure, not progress (P002).
Second, whether the team is doing the second kind of refactoring at all — the
insight-driven kind that produces breakthroughs — or only tidying code while the
model stays shallow (P010).

## When to use

- A refactoring or "clean-up" is proposed and you must judge whether it keeps the
  code expressing the model, or quietly erodes that correspondence.
- The team reports a recurring awkwardness, workaround, or concept that is
  explained verbally but has no class or relationship of its own — a candidate for
  being made explicit.
- A design has stopped changing even though understanding of the domain is still
  growing, suggesting insight is not being fed back into the model.
- You are assessing whether analysis and implementation are being done together,
  or split across people who never reconcile model and code.

## Procedure

1. **Confirm model–code correspondence.** Identify the part of the code that is
   meant to carry the domain model. Check that the mapping is obvious: domain
   concepts appear as named elements, not buried in procedural logic. If the
   central design does not map to the model, the model has little value and the
   software's correctness is suspect (C025).
2. **Treat code changes as model changes.** For each proposed refactoring, ask
   what it does to the model's expression. A change to the code implies a change
   to the model; flag any step that leaves the code less able to state the model
   than before (C023).
3. **Check that modellers and implementers are the same loop.** Verify the people
   refactoring know the model well and feel responsible for its integrity, and
   that modelling and implementation are not happening in isolation from each
   other (C022, P002).
4. **Separate the two kinds of refactoring.** Distinguish technical code-quality
   refactoring from insight-driven refactoring. Confirm the team is also doing
   the second kind: incorporating newly discovered relationships and clearer
   concepts back into the design (C061).
5. **Hunt for implicit concepts.** Look for a concept that is repeatedly used to
   explain other concepts, described in conversation but absent from the model.
   Recommend giving it its own class or relationship — this making-explicit move
   is the primary mechanism of breakthrough insight (C064).
6. **Require domain-expert involvement and iteration.** Sophisticated models are
   developed only through iterative refactoring with continuous domain-expert
   participation. Flag a process that refactors without that involvement (C060).
7. **Keep steps safe and bounded.** Recommend small, controllable steps backed by
   automated tests that verify behaviour is preserved. Flag for caution any step
   that lacks test coverage or that crosses a Bounded Context boundary, where the
   safety of the change can no longer be assumed locally.

## Inputs

- The domain model artifact(s) and the code intended to express them.
- The proposed refactoring or change description.
- Access to, or evidence of, domain-expert involvement in the modelling.

## Output

A structured assessment that states, per proposed change: whether model–code
correspondence is preserved or eroded; whether the change is technical-only or
carries domain insight; any implicit concept that should be made explicit (named,
with where it currently hides); and whether the step is safely bounded (test
coverage present, no unguarded Bounded Context crossing). Each finding names the
specific model element and gives one corrective step.

## References

- `references/refactoring-checklist.md` — the step-by-step checklist form of this
  skill.
- `references/building-block-pattern-summaries.md` — the patterns an explicit
  concept is usually promoted into (Entity, Value Object, Service, etc.).

## Provenance

Distilled from "Domain-Driven Design Quickly" (Avram & Marinescu, InfoQ, 2006),
rights status distillation-only — paraphrased, no verbatim quotation.

- **P002** (model–code correspondence): claims C022 (E012), C023 (E013),
  C025 (E014), anchor h0018 ("Model-Driven Design").
- **P010** (refactoring toward deeper insight): claims C060 (E027), C061 (E028),
  C064 (E029), anchors h0037 ("Continuous Refactoring") and h0039
  ("Bring Key Concepts Into Light").
