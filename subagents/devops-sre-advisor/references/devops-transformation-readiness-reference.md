---
name: devops-transformation-readiness-reference
kind: reference
status: ready
provenance:
  principles:
  - P003
  - P075
  - P122
  - P015
  - P039
  - P045
  claims:
  - C00057
  - C00058
  - C00059
  - C00060
  - C00061
  - C00063
  - C00066
  - C00067
  - C02705
  - C02706
  - C02707
  - C01267
  evidence:
  - E00036
  - E00037
  - E00038
  - E00039
  - E00040
  - E00042
  - E00044
  - E00045
  - E00589
  - E00590
  - E00591
  - E00425
  source_anchors:
  - 9d4b1cf206e5-c0002
  - 9d4b1cf206e5-c0003
  - 861f0551c788-c0005
  - 9fe26df35c80-c0033
  authored_from_digest: 64f50556adbb50675177640fbb537b43fcb8beb23d2b86fbae01ae0af6742c1e
---

# DevOps transformation readiness reference

A readiness checklist for adopting DevOps/SRE. The governing finding: this is a
culture-and-collaboration change, not just tooling (P012) — a tooling rollout stalls when ways of
working do not change. Use the dimensions below to judge whether a transformation is set up to
stick, and to name what is missing.

## 1. Culture (P012)

- [ ] A Westrum **generative culture** — high cooperation, shared risk, learning from failure —
      which statistically predicts both delivery and organisational performance (CL024).
- [ ] A just, learning-oriented stance where failure is a learning opportunity and leaders visibly
      participate in retrospectives and reward surfacing systemic problems (CL015).

## 2. Leadership (P012)

- [ ] **Transformational leadership** — vision, inspirational communication, intellectual
      stimulation, support — a significant enabler of the practices that drive delivery performance
      (CL029).
- [ ] A clear, measurable goal and vision that technical and non-technical stakeholders understand,
      broken into a prioritised roadmap (CL066).

## 3. Team and collaboration (P012)

- [ ] A **dedicated, cross-functional team** drives the adoption, rather than part-time volunteers
      who lack the focus and mandate (CL064).
- [ ] That team practises what it preaches and repeats the vision patiently to many audiences —
      credibility and understanding take repetition (CL065).
- [ ] Collaboration is made the default by deliberately lowering the barriers to it; siloed
      behaviour reasserts itself without sustained effort (CL067).

## 4. Flow and work management (P013)

- [ ] Work is made **visible across the whole value stream** so queues and bottlenecks surface
      (CL001).
- [ ] **Work-in-process limits** are imposed so teams finish before starting; WIP is a leading
      indicator of lead time (CL002).
- [ ] Lean management — WIP limits, visual management, feeding production monitoring back into
      decisions — improves delivery performance and reduces burnout (CL028).

## 5. Architecture and simplicity (P010)

- [ ] A **loosely coupled, independently deployable** architecture — the strongest single predictor
      of continuous-delivery capability, outweighing tooling alone (CL023) — lets teams test and
      deploy without cross-team coordination (CL006).
- [ ] Simplicity is treated as a reliability property: unnecessary complexity is a primary source of
      unreliability and operational burden, removed during design review (CL059).

## 6. Change management (P011)

- [ ] Lightweight, peer-review-based change approval rather than a heavyweight external
      change-advisory board, which slows delivery without improving stability (CL025).

## Expectation-setting

- The adoption has a real **upfront cost** — a dedicated team, tooling, hosting, and process change
  — to weigh against the long-term quality and speed gains (CL072).
- Better delivery practice improves human outcomes too: adopting continuous delivery has been seen
  to sharply reduce deployment pain and improve work/life balance (CL030) — a correlational, single
  case, not a guarantee.

## Provenance

Derived from principles P012, P013, P010, P011 (claims and evidence as listed) across
`accelerate-the-scien-7241289b`, `the-devops-handbook-c4933b3c`, `comp500-15893c30`, and
`comp109-5dbbef8d` (all distillation-only — paraphrase, no verbatim quotation). The Accelerate
culture/leadership/architecture claims are correlational survey findings; P012 is held at medium
confidence in the package principles.
