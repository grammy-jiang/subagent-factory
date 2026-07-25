---
name: research-data-management-and-sharing
kind: skill
status: ready
description: Data Management Plan, per-dataset README, data dictionary, persistent-identifier (PID) metadata, discipline metadata standards, or sharing sensitive/human-participant data that cannot be fully opened.
provenance:
  principles:
  - P001
  - P017
  - P027
  - P033
  claims:
  - C00018
  - C00240
  - C00241
  - C00242
  - C00243
  - C00244
  - C00245
  - C00246
  - C00320
  - C00323
  - C00324
  - C00328
  - C00329
  - C00330
  - C00331
  - C00332
  evidence: []
  source_anchors: []
  authored_from_digest: 6be58ebf3f30de5ac7bc7eabb815ba4540b75fd70fc2e3194e72124397b068e3
---

# Research Data Management And Sharing

## Purpose

This skill guides how research data is planned, documented, licensed, deposited, and shared so that others can find, understand, and reuse it. It checks for a Data Management Plan, adequate documentation and metadata (a per-dataset README, a human- and machine-readable data dictionary, discipline standards), rich persistent-identifier metadata that raises discoverability, and a deliberate, consent-and-rights-aware stance on data that legitimately cannot be fully opened.

## When to use

- A project is starting and needs a Data Management Plan covering roles, storage and backup, post-project preservation, reuse and licensing, and costs.
- Data is being prepared for deposit and needs documentation, a data dictionary, and a repository that mints a persistent identifier and states a preservation policy.
- Human-participant or otherwise sensitive data cannot be openly shared and a partial, obscured, or controlled-access sharing route must be designed.
- A dataset's discoverability and reuse depend on richer PID and community metadata than the required minimum.

## Procedure

1. Address the real barriers to data sharing — organising data presentably, resolving licensing uncertainty, and choosing a repository; for anonymised human-participant data, ensure the consent forms cover sharing with other researchers and the participant sheets state how the data is stored, preserved, used, and kept confidential; and accept that some data legitimately cannot be fully opened for legal, ethical, privacy, security, or commercial reasons, in which case share a partial or obscured dataset instead of withholding it entirely (P001).
2. Manage outputs with a Data Management Plan — a living document covering roles and responsibilities, data types and sizes and metadata, storage and backup, post-project preservation, reuse and licensing, and costs — ensure at least one other person has access to the data (restricting sensitive data to those who need it), apply a licence when depositing so others know how they may reuse it, and choose a repository that mints a persistent identifier and states its preservation policy (P017).
3. Describe data so it can be understood and reused, since data without metadata is useless: write plain-language documentation covering source, strengths, weaknesses, and limitations; share a README per dataset describing methods and data-specific details; provide a data dictionary or codebook, human- and machine-readable, sufficient to interpret the data alone; store data in a logical folder structure with a README; and use recognised discipline-specific community metadata standards so the data can be combined across sources (P027).
4. Provide rich persistent-identifier metadata — description, keywords, related identifiers, funding references, contributors with ORCID iDs, and affiliations with ROR IDs — rather than only the required minimum, because this machine-readable, publicly accessible metadata complements domain-specific metadata and substantially increases discoverability and reusability (P033).

## Inputs

- The dataset(s), the data-management or data-sharing plan (or its absence), the consent and rights constraints, and the intended repository or audience.
- The reasoning offered for the decision under review: the goal, the plan or practice in place, and any claim of reproducibility or compliance made.

## Output

Per finding: name the gap and the principle it engages, give the correction, state the residual trade-off or the referral to make, and end with a concrete next step. Order findings highest-impact first. This skill advises on research-integrity and reproducibility practice; it does not run the study, produce the output, make an institutional misconduct finding, or give legal advice.

## Anti-patterns to flag

- A dataset is withheld entirely with only a vague "it's sensitive" or "licensing is complicated" — name the actual barrier (organising, licensing, choosing a repository), and share what legitimately can be shared: a partial or obscured dataset, backed by consent forms and participant sheets that state how the data is stored, used, and kept confidential (P001).
- No Data Management Plan exists, or the working data lives on one person's laptop with no one else able to open it — write a DMP covering roles, storage and backup, post-project preservation, reuse and licensing, and costs; give at least one other person access; and deposit to a repository that mints a persistent identifier and states its preservation policy (P017).
- A dataset is deposited as bare files with no README, no codebook, and column headers like "var3" or "x1" — add a per-dataset README, a data dictionary or codebook usable without contacting the author, a logical folder structure, and a discipline-standard metadata schema (P027).
- A repository record carries only the mandatory title/author/date fields and nothing else — add the optional PID metadata (keywords, related identifiers, funding references, ORCID iDs for contributors, ROR IDs for affiliations), since this is what actually drives discoverability and reuse (P033).

## References

See `../../references/reproducibility-integrity-principles-index.md` for the full principle catalogue grouped by skill, and `../../references/reproducibility-integrity-evidence-notes.md` for how these principles are grounded and kept faithful to the sources.

## Provenance

Derived from P001, P017, P027, P033, grounded in the distillation-only sources (*The Turing Way*, a handbook for reproducible, ethical, and collaborative research; *On Being a Scientist*, a guide to responsible conduct in research; and a higher-education academic-norms guide). The frontmatter `provenance` block lists the exact principle and claim ids, which resolve into `principles/principles.yaml` and `analysis/claims.jsonl`.
