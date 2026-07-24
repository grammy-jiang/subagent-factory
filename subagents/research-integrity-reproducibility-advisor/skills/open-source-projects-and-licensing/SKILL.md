---
name: open-source-projects-and-licensing
kind: skill
status: ready
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

1. Run an open source project with the essential files (P018).
2. Contribute well to another open source project (P024).
3. Understand usage-restricting licences (P020).
4. Choose a data licence deliberately (P025).
5. License the parts of an ML or AI system separately (P028).
6. Make research sufficiently open for exchange, scrutiny, and authorized follow-on use while withholding only information protected by valid secrecy, confidentiality, or intellectual-property duties (P012).

## Inputs

- The software, dataset, or model to release or contribute to, its intended licence, and the openness and rights constraints.
- The reasoning offered for the decision under review: the goal, the plan or practice in place, and any claim of reproducibility or compliance made.

## Output

Per finding: name the gap and the principle it engages, give the correction, state the residual trade-off or the referral to make, and end with a concrete next step. Order findings highest-impact first. This skill advises on research-integrity and reproducibility practice; it does not run the study, produce the output, make an institutional misconduct finding, or give legal advice.

## Anti-patterns to flag

- Overlooking P018: Run an open source project with the essential files.
- Overlooking P024: Contribute well to another open source project.
- Overlooking P020: Understand usage-restricting licences.
- Overlooking P025: Choose a data licence deliberately.
- Overlooking P028: License the parts of an ML or AI system separately.
- Overlooking P012: Make research sufficiently open for exchange, scrutiny, and authorized follow-on use while withholding only information protected by valid secrecy.

## References

See `../../references/reproducibility-integrity-principles-index.md` for the full principle catalogue grouped by skill, and `../../references/reproducibility-integrity-evidence-notes.md` for how these principles are grounded and kept faithful to the sources.

## Provenance

Derived from P018, P024, P020, P025, P028, P012, grounded in the distillation-only sources (*The Turing Way*, a handbook for reproducible, ethical, and collaborative research; *On Being a Scientist*, a guide to responsible conduct in research; and a higher-education academic-norms guide). The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`.
