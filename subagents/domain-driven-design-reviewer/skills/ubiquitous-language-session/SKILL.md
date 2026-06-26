---
name: ubiquitous-language-session
kind: skill
status: ready
provenance:
  principles:
  - P001
  claims:
  - C013
  - C014
  - C015
  source_anchors:
  - domaindrivendesignqu-20260612231910-h0013
  - domaindrivendesignqu-20260612231910-h0014
  authored_from_digest: f44120abb3f17c2f8902dc59533104849ec21894a3594f8115e476023eb69d11
---

# Ubiquitous Language Session

## Purpose

Run or critique a working session whose goal is establishing and maintaining
a single language — grounded in the domain model — that every team member
uses consistently in speech, written documents, diagrams, and code. The
reviewer uses this skill to detect language drift: situations where terms
carry different meanings across conversation, design artifacts, and code
identifiers, causing domain knowledge to go uncaptured or become unreliable.

The Ubiquitous Language is not merely a naming convention. It is the
vehicle through which domain knowledge is reliably shared: when discussion
terminology diverges from code terminology, the most precise expressions of
domain understanding exist only transiently and are never captured
(C013, P001).

## When to use

- Code identifiers, diagram labels, or written documents use terminology
  that does not match the words domain experts use when describing the
  domain — language drift is active or suspected (P001).
- A new domain is being modeled and the primary concepts have not yet been
  given stable, agreed-upon names.
- A review finding implicates naming inconsistency: a class or method name
  does not correspond to the model concept it is meant to express.
- A change to the domain model is under consideration and the reviewer must
  confirm that any language change will propagate to the model, and vice
  versa (C014, P001).

## Procedure

### Phase 1 — Anchor the language on the model

1. Identify the domain model artifact being used as the backbone
   (class diagram, written design doc, or code domain layer). Confirm
   it is the current authoritative representation of the domain concepts.

2. Establish that the same terms must appear in all communication forms:
   spoken discussion, written documents, diagrams, and code. Any term
   used in speech but absent from the code — or present in code but
   unknown to domain experts — is a gap to resolve (C013).

### Phase 2 — Surface and map candidate terms

3. In a session with domain experts, track the nouns the experts use for
   core concepts. Map each noun to the corresponding model object. Track
   the verbs experts attach to those nouns and map them to the operations
   on those objects.

4. Watch for terms that domain experts use inconsistently across the
   session, or that experts and developers use differently. Flag each
   inconsistency for resolution.

### Phase 3 — Test terms against both sides

5. **Domain expert test:** A domain expert should object to any term or
   structure that is awkward or that fails to convey domain understanding.
   If an expert cannot recognize a term in the model, treat that as a
   signal the model requires correction — not the expert (C015).

6. **Developer test:** Developers should flag terms that are ambiguous or
   are used inconsistently across different parts of the design (C015).

### Phase 4 — Resolve and choose

7. For each contested or unclear term, try alternative expressions that
   reflect alternative model framings. Select the expression that reads
   true to the domain and that both sides accept. Document the chosen term
   and the reason alternatives were rejected.

8. Once a term is chosen, refactor the code to use it: rename classes,
   methods, and modules. Also update diagrams and written documents.
   Leaving the old term in place in any medium — even temporarily —
   reintroduces drift.

### Phase 5 — Lock language to model

9. Treat any agreed change to the Ubiquitous Language as a simultaneous
   change to the domain model, and vice versa. The two must move in
   lockstep: a language change that does not update the model, or a model
   change that does not update the shared language, is incomplete (C014).

10. Push the main domain concepts into code: verify that the central model
    concepts each have a corresponding class or method, so the code
    reproduces the language and remains readable as the model grows.

### Phase 6 — Choose communication forms deliberately

11. For diagrams, prefer several small, focused diagrams each covering a
    subset of the model over a single large all-encompassing diagram. Large
    diagrams become too cluttered to communicate clearly.

12. Supplement diagrams with explanatory text for behaviour and constraints
    that a diagram alone cannot express. Avoid long documents that are
    likely to fall out of sync with the model.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Domain model artifact | Required | Class diagram, UML model, code domain layer, or written design document that defines current domain concepts and relationships. |
| Domain expert terminology | Required | Notes from domain expert sessions, or direct access to a domain expert, providing the vocabulary experts use naturally. |
| Code identifiers | Required | Class, method, and module names from the domain layer to compare against the spoken and written language. |
| Diagram and document set | Optional | Any existing diagrams or written documents that should be consistent with the Ubiquitous Language. |

## Output

A structured language-alignment report containing:

1. **Consistency verdict** — an explicit statement of whether the
   Ubiquitous Language is currently consistent across speech, documents,
   diagrams, and code.

2. **Term inconsistency list** — for each inconsistency found:
   - The term or identifier at issue.
   - Where it appears (code, diagram, spoken discussion, document).
   - The recommended single agreed term.
   - The specific code elements (class, method, module names) and
     document/diagram elements that must be renamed or updated to align.

3. **Language-model coupling gaps** — any detected cases where a language
   change has not been reflected in the model, or a model change has not
   been reflected in the language (C014).

4. **Session notes** (if a live session was run) — terms considered and
   rejected, with reasons, to prevent the same debates recurring.

## References

- `principles/principles.yaml` — P001 (Ubiquitous Language consistency),
  C013, C014, C015.
- `references/building-block-pattern-summaries.md` — building-block
  pattern definitions that the Ubiquitous Language must name correctly.

## Provenance

Grounded in P001 (derived from C013, C014, C015) and evidence records
E008, E009, E010. Source: Avram & Marinescu, "Domain-Driven Design
Quickly" (InfoQ, 2006), sections anchored at
`domaindrivendesignqu-20260612231910-h0013` ("The Ubiquitous Language")
and `domaindrivendesignqu-20260612231910-h0014` ("The Need for a Common
Language" / "Creating the Ubiquitous Language"). Rights status:
`distillation-only` — all content paraphrased, no verbatim quotation.
