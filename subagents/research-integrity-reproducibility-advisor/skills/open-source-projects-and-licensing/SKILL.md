---
name: open-source-projects-and-licensing
kind: skill
status: ready
description: Use when checking essential open-source project files (LICENSE, DOI, README, contributing guide, code of conduct), contributing to someone else's project, choosing licences for software/data/ML-AI components, evaluating non-free usage-restricting (Ethical Source/Responsible AI) licences, or keeping research open while withholding validly protected information.
provenance:
  principles:
  - P018
  - P024
  - P020
  - P025
  - P028
  - P012
  claims:
  - C00049
  - C00050
  - C00051
  - C00052
  - C00053
  - C00054
  - C00055
  - C00090
  - C00091
  - C00092
  - C00119
  - C00122
  - C00123
  - C00132
  - C00133
  - C00134
  evidence: []
  source_anchors: []
  authored_from_digest: da51ca3805677351d68d87a72fb41ca77e1f0b85b0c100d664af067b4eeedff3
---

# Open Source Projects And Licensing

## Purpose

This skill guides releasing and contributing to open research software and datasets, and choosing licences deliberately. It checks the essential open-source project files (a licence without which the work is not open, a DOI, a README, contributing guidelines and a code of conduct), how to contribute well to someone else's project, and licence choices for software, data, and separately-licensable ML/AI components — including the limits and non-free status of usage-restricting licences — while keeping research open for scrutiny and withholding only validly protected information.

## When to use

- An open-source software project needs its essential files (licence, DOI, README, contributing guidelines, code of conduct).
- A contribution is being prepared to someone else's open-source project and must match its roles, style, and process.
- A licence must be chosen for software, a dataset, or an ML/AI model whose data, code, and weights may each be licensed differently.
- A usage-restricting (Ethical Source / Responsible AI) licence is being considered and its non-free status and brittle enforcement matter.
- Research is being made open for exchange and scrutiny while withholding only information under a valid secrecy, confidentiality, or IP duty.

## Procedure

1. Confirm the project carries its essential files: a LICENSE file, without which no one can legally reuse the code and the project is not open source; a DOI so the code is citeable; a README covering what the project is, its features, and its install/run instructions, tests, authors, and acknowledgements (write the install steps down the first time you follow them); and, if collaborators are wanted, contributing guidelines and a code of conduct (e.g. a Contributor Covenant), kept in the repository root and linked from the README (P018).
2. Before contributing to someone else's project, orient to its roles (author, owner, maintainers, contributors, community members), read its documentation and contributing guidelines, match its existing style and conventions, break the change into small well-defined chunks, test the change against an up-to-date version and update the documentation, and describe what changed, why, and how in the pull request — remembering that valuable non-code contributions (docs, examples, review, triage) are welcome too (P024).
3. Before adopting an Ethical Source or Responsible AI licence, recognize that curtailing the freedom to use software for any purpose (even via an attribution requirement) makes it non-free/non-open by the classical FSF and OSI definitions, limits its adoption, makes compliance harder and more expensive to demonstrate than for conventional licences, and that DRM-style technical enforcement of such restrictions tends to be brittle, invasive, and bypassable (P020).
4. Choose a data licence deliberately, since it governs what others can do with the data and directly affects its accessibility: Creative Commons licences can serve in some cases (CC0 relinquishes all rights to the public domain, CC-BY is common), but Creative Commons is general-purpose while Open Data Commons licences are made specifically for data and typically cover only database rights (P025).
5. License the parts of an ML or AI system separately, since a model comprises training data, code, and weights that may each carry a different licence and the model licence governs the model and its derivatives independently of the other components; choose a licence that signals to users how the model should be used, using Creative Commons (which has no source-code terms) for data and weights and a software licence for the code (P028).
6. Make the research sufficiently open for exchange, scrutiny, and authorized follow-on use, withholding only information that is protected by a valid secrecy, confidentiality, or intellectual-property duty (P012).

## Inputs

- The software, dataset, or model to release or contribute to, its intended licence, and the openness and rights constraints.
- The reasoning offered for the decision under review: the goal, the plan or practice in place, and any claim of reproducibility or compliance made.

## Output

Per finding: name the gap and the principle it engages, give the correction, state the residual trade-off or the referral to make, and end with a concrete next step. Order findings highest-impact first. This skill advises on research-integrity and reproducibility practice; it does not run the study, produce the output, make an institutional misconduct finding, or give legal advice.

## Anti-patterns to flag

- Code is pushed to a public repository with no LICENSE file — without one no one can legally reuse it and it is not open source; add a licence file, and add a DOI, README, and (if collaborators are wanted) contributing guidelines and a code of conduct (P018).
- A pull request lands out of nowhere, ignores the project's contributing guidelines and existing style, bundles many unrelated changes, and gives no explanation of what changed, why, or how — orient to the project's roles and process first, keep the change small and well-tested, update the docs, and write a clear PR description (P024).
- An Ethical Source or Responsible AI licence is adopted and assumed to be "open source," with compliance policed by DRM-style technical enforcement — usage-restricting terms (even a bare attribution clause) make it non-free by FSF/OSI definitions, harder and costlier to verify compliance, and DRM enforcement tends to be brittle, invasive, and bypassable; name the restriction and its consequences explicitly (P020).
- A dataset is released with no licence at all, or with a general-purpose Creative Commons licence chosen by default without considering database rights — choose a data licence deliberately (CC0, CC-BY, or an Open Data Commons licence built specifically for data) (P025).
- An ML/AI release ships one blanket licence covering data, code, and weights together — license each component (data, code, weights) separately, since each may need different terms and the model licence signals intended use independently of the others (P028).
- A researcher either publishes everything indiscriminately (exposing information under a valid secrecy, confidentiality, or IP duty) or withholds material with no such protection to avoid scrutiny — keep the work open for exchange, scrutiny, and authorized follow-on use, and withhold only what is validly protected (P012).

## References

See `../../references/reproducibility-integrity-principles-index.md` for the full principle catalogue grouped by skill, and `../../references/reproducibility-integrity-evidence-notes.md` for how these principles are grounded and kept faithful to the sources.

## Provenance

Derived from P018, P024, P020, P025, P028, P012, grounded in the distillation-only sources (*The Turing Way*, a handbook for reproducible, ethical, and collaborative research; *On Being a Scientist*, a guide to responsible conduct in research; and a higher-education academic-norms guide). The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`.
