---
name: duplication-taxonomy-table
kind: reference
status: ready
provenance:
  principles:
  - P040
  - P002
  - P070
  - P071
  - P053
  claims:
  - C00040
  - C00041
  - C00042
  - C00043
  - C00046
  - C00049
  - C00050
  source_anchors: []
  authored_from_digest: 292ad883e604717037bf04724c712d9ede1be69e453bdfcce6008ef1f537087b
---

# Duplication Taxonomy

DRY requires that every piece of knowledge have a single, unambiguous, authoritative
representation within a system (C00040). Duplicated knowledge guarantees eventual
inconsistency: when the same thing lives in two or more places, one copy will eventually
be updated while the other is forgotten (C00041). Duplication arises from four distinct
sources; naming the source points to the appropriate countermeasure (C00042).

| Category | Origin | Typical signal | First-line remedy | Grounding |
|---|---|---|---|---|
| **Imposed** | The environment or tooling appears to force the duplication (e.g. the same structure required in two languages, or code that must be mirrored in documentation). | "We have to keep these in sync because the platform requires both." | Generate every derived copy from one authoritative source using an active code generator wired into the build — not a one-time conversion. Normalize data; use calculated fields. | C00043, C00046 (P002) |
| **Inadvertent** | The developer did not realize the knowledge was already represented elsewhere; often discovered only when one copy changes independently. | The same business rule independently re-encoded in two modules. | Surface the existing representation; consolidate to one and reference it. Eliminate derivable or mutually dependent fields by computing them from the authoritative source. | C00042, C00046 (P040, P002) |
| **Impatient** | A developer took a shortcut, copying rather than abstracting, because it was faster in the moment. | Copy-paste blocks with small edits; "I'll refactor it later." Deadline pressure is the trigger. | Resist the shortcut; the time saved now costs more later (C00049). Use the duplication as a refactoring trigger. | C00049 (P071) |
| **Interdeveloper** | Two or more team members independently duplicate the same knowledge without knowing of each other's work. | Parallel implementations of the same concept in different modules or teams. | Frequent communication, clear design with divided responsibilities, a project librarian, a shared utility location, and routine code reading (C00050). Make reuse easier than rewriting (P053). | C00050 (P053) |

## Permitted exception: deliberate performance duplication

You may intentionally break DRY when a measured performance need such as caching
justifies it. The violation must be localized — kept hidden behind the owning module's
interface so callers never see the inconsistency (P070, C00048). This exception does
not apply to design-time knowledge; it applies only to derived runtime values.

## Related distinctions

- **Code vs comments:** Low-level knowledge belongs in the code, not duplicated in
  adjacent comments. Comments should carry high-level explanation only. When code and
  comments re-state the same thing, they will drift and the comments become
  untrustworthy (P012, C00044 — see also the documentation-as-code principle).
- **Imposed duplication is often avoidable:** When the environment seems to force it,
  generating every representation from one metadata source keeps the knowledge in one
  place and eliminates the entire category (C00043).
- **Accessor functions as a seam:** Routing attribute access through accessor functions
  (Uniform Access) lets caching or other behavior be introduced later without exposing
  the violation to callers (C00047, P002).

## Provenance

Derived from P040 (DRY), P002 (single-source generation), P070 (deliberate perf
exception), P071 (impatient duplication), and P053 (interdeveloper reuse) using claims
C00040, C00041, C00042 (core DRY taxonomy), C00043, C00046 (imposed/inadvertent
remedies), C00049 (impatient), and C00050 (interdeveloper). Source is
distillation-only; all wording is paraphrased.
