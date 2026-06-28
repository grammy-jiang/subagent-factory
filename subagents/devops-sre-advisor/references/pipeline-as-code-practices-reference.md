---
name: pipeline-as-code-practices-reference
kind: reference
status: ready
provenance:
  principles:
  - P012
  - P058
  - P125
  - P002
  - P007
  - P013
  claims:
  - C01311
  - C01312
  - C01313
  - C02516
  - C00070
  - C00071
  - C00072
  - C00073
  - C00074
  - C00075
  - C01028
  - C01029
  evidence:
  - E00433
  - E00434
  - E00435
  - E00578
  - E00046
  - E00047
  - E00048
  - E00049
  - E00050
  - E00051
  - E00401
  - E00402
  source_anchors:
  - 9fe26df35c80-c0035
  - 0bea4daa68ab-c0040
  - 9d4b1cf206e5-c0003
  - 9fe26df35c80-c0023
  authored_from_digest: 115bfb146187e05839176cc6cb903c5592bebc20269a47b1210cf2c0018f2d8b
---

# Pipeline-as-code practices reference

A practice checklist for a continuous-delivery pipeline, grouped by the four foundations. Use it to
design a pipeline or to review one gap by gap. It governs *practices*; specific tools and commands
change quickly, so confirm them against current official documentation.

## 1. Version control and flow (P006)

- [ ] Application code, system configuration, and build/deploy scripts are all in version control
      — the foundational CD capability (CL019).
- [ ] Trunk-based development with very short-lived branches merged at least daily (CL020).
- [ ] Change ships in small, frequent increments, not large bundled releases (CL061); smaller
      batches shrink lead time and lower per-deployment risk (CL003).

## 2. Continuous integration and automated testing (P004)

- [ ] CI builds and tests every change frequently against the live codebase — the base CD rests on
      (CL063).
- [ ] The build-and-test path is automated for consistent, repeatable, trustworthy results (CL062).
- [ ] Automated unit, integration, and acceptance test stages fail fast on regressions so untested
      changes cannot proceed (CL039, CL007).
- [ ] Test suites are reliable and developers own the acceptance tests (CL021).
- [ ] Every manual deployment step — packaging, configuration, environment setup, testing — is
      automated so releases are safe, repeatable, frequent (CL008).

## 3. Pipeline and infrastructure as code (P007)

- [ ] The pipeline is defined as code in version control alongside the application, replacing
      hand-clicked job configuration with reproducible, auditable definitions (CL031).
- [ ] Infrastructure is provisioned with infrastructure-as-code so environments are versioned,
      reviewable, and reproducible (CL035).
- [ ] Immutable, baked images are used so failed nodes are replaced by identical instances and
      scaling avoids runtime configuration drift (CL034).
- [ ] Pipeline stages run in containers for clean, reproducible, ephemeral build environments
      (CL038).

## 4. Lightweight change management and security (P011)

- [ ] Peer review (code review, pairing) is the change-approval mechanism, not a heavyweight
      external change-approval board, which slows delivery without improving stability (CL025).
- [ ] The automated pipeline is used to satisfy segregation-of-duties and compliance needs without
      a separate approval board (CL026).
- [ ] Security testing is integrated into the pipeline and daily work, not gated at the end (CL014).
- [ ] Automated security scanning (e.g. dependency vulnerability checks) blocks risky artifacts from
      progressing (CL040).
- [ ] Code-quality gates stop changes that fail the bar before deployment (CL041).

## 5. Pipeline observability (supporting)

- [ ] Logs from controller and agents are aggregated centrally so pipeline activity is searchable
      and auditable (CL043).
- [ ] Build and CI metrics (queue depth, executor use, agent availability) are exported to a
      monitoring system so CI health is observable and can drive scaling (CL044).

## Provenance

Derived from principles P004, P006, P007, P011 (claims and evidence as listed above) across
`accelerate-the-scien-7241289b`, `the-devops-handbook-c4933b3c`, `comp109-5dbbef8d`, and
`pipeline-as-code-con-2e091c45` (all distillation-only — paraphrase, no verbatim quotation).
Accelerate claims are correlational survey findings; the pipeline-as-code claims are tool-specific
practitioner guidance generalised here to the practice, not the product.
