---
name: extension-and-failure-checklist
kind: reference
status: ready
provenance:
  principles:
  - P003
  - P008
  - P026
  - P028
  - P029
  - P033
  claims: []
  evidence: []
  source_anchors: []
---

# Extension and Failure Checklist

A checklist for finding and writing the extension conditions and failure handling of a
use case — where the most interesting requirements live (P003). Use alongside
`write-use-case-scenarios`.

---

## Find the conditions

Brainstorm all failures and alternative successes for each step (P003):

- [ ] For every step, ask: what else could happen here?
- [ ] Use a failure checklist that includes **internal** failures (the system's own
      validation, resource, or timing failures), not just actor errors.
- [ ] Reduce the brainstormed list by explicit criteria (relevance, likelihood,
      stakeholder impact).
- [ ] **When in doubt, include the condition** — an extra extension is cheaper than a
      missed requirement.

## End conditions drive the failures

- [ ] A success End Condition and a Failed End Protection exist for all stakeholders,
      written **before** the main scenario (P008).
- [ ] Each failure-handling fragment protects the relevant stakeholders' interests.
- [ ] Writing the failure protection has been used to reveal the logging/recording the
      main scenario needs.

## Write the extension condition

- [ ] Each condition is a short **"what is different"** phrase, in a grammar distinct
      from action steps (P033).
- [ ] Numbering conventions applied: letter-and-colon (e.g. `3a:`), step ranges,
      asterisk (`*`) for any-time conditions.
- [ ] Loops are flattened into named conditions rather than nested.

## Write the handling fragment

- [ ] Each fragment is written in the **same style** as the main scenario, starting at
      the named step (P028).
- [ ] The fragment ends one of three ways (resumes the main flow, ends in success, or
      ends in failure) and usually needs no explicit "go to step".
- [ ] Any new validation a fragment reveals is moved **back into** the main success
      scenario.

## Control depth and breakout

- [ ] A failure-within-a-failure is handled by **indentation**, not by a new use case
      (P029).
- [ ] A fragment is broken out into its own sub-use case only once inline handling
      exceeds about **three pages or four indent levels**.
- [ ] The failure of every called sub-use case is handled.
- [ ] Failure roll-up is used to avoid a scenario explosion.

## Preconditions vs conditions

- [ ] Preconditions hold only what the system can guarantee and will never re-check
      (P026); they are not used to hide conditions that should be handled as
      extensions.
- [ ] Merely-usual context is recorded in a Context-of-use note, not as a precondition.

---

## Provenance

Grounded in principles P003, P008, P026, P028, P029, P033 of this package, derived
from Alistair Cockburn, "Writing Effective Use Cases" (2001). Source is
`distillation-only` — all content is paraphrased; no verbatim quotation.
