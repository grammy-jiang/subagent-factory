---
name: version-control-and-collaboration
kind: skill
status: ready
provenance:
  principles:
  - P019
  - P029
  - P031
  claims:
  - C00011
  - C00015
  - C00033
  - C00034
  - C00086
  - C00087
  - C00088
  - C00089
  - C00547
  - C00548
  - C00549
  - C00550
  - C00551
  - C00552
  - C00553
  - C00554
  evidence: []
  source_anchors: []
  authored_from_digest: 9a483f1ca4e25a2ddbafda1535bb706d157a3c76b01b1f963d2ee3766444229a
---

# Version Control And Collaboration

## Purpose

This skill guides use of version control as the backbone of reproducible, collaborative research. It checks that changes are tracked in version control rather than manual v01/v02 files, that commits are atomic, name their files, exclude generated artefacts, and carry a meaningful message, and that the main branch is kept stable with merge conflicts fully understood before resolution.

## When to use

- Files are being versioned by hand (v01, v02) instead of with version control.
- Commit hygiene is at issue — atomic single-change commits, staging specific files, meaningful messages, and not committing generated files.
- Several people work on a shared codebase and need branch discipline and a stable main branch.
- A merge conflict must be resolved and both versions understood first.

## Procedure

1. Use version control, the systematic recording of changes to files over time (P019).
2. Commit well: make each commit an atomic single change, commit no generated files, stage the specific files by name rather than adding everything, and write a meaningful message with a roughly 50-character present-tense imperative (P029).
3. Keep the main branch always stable and only merge finished, tested work into it; when a merge conflict occurs (P031).

## Inputs

- The repository or file-management practice, the commit and branch conventions in use, and the collaboration setup.
- The reasoning offered for the decision under review: the goal, the plan or practice in place, and any claim of reproducibility or compliance made.

## Output

Per finding: name the gap and the principle it engages, give the correction, state the residual trade-off or the referral to make, and end with a concrete next step. Order findings highest-impact first. This skill advises on research-integrity and reproducibility practice; it does not run the study, produce the output, make an institutional misconduct finding, or give legal advice.

## Anti-patterns to flag

- Overlooking P019: Use version control, the systematic recording of changes to files over time.
- Overlooking P029: Commit well: make each commit an atomic single change, commit no generated files, stage the specific files by name rather than adding everything.
- Overlooking P031: Keep the main branch always stable and only merge finished, tested work into it; when a merge conflict occurs.

## References

See `../../references/reproducibility-integrity-principles-index.md` for the full principle catalogue grouped by skill, and `../../references/reproducibility-integrity-evidence-notes.md` for how these principles are grounded and kept faithful to the sources.

## Provenance

Derived from P019, P029, P031, grounded in the distillation-only sources (*The Turing Way*, a handbook for reproducible, ethical, and collaborative research; *On Being a Scientist*, a guide to responsible conduct in research; and a higher-education academic-norms guide). The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`.
