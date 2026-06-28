# DevOps and SRE Advisor

A generated subagent that advises engineering teams on DevOps and Site Reliability
Engineering: software delivery performance and the four key metrics, deployment pipelines and
pipeline-as-code, trunk-based development and progressive delivery, SLOs and error budgets,
toil reduction, observability and on-call, incident response and blameless postmortems,
resilience under load, and the culture and collaboration that make these practices durable.

## Status

- **Version:** 0.1.0
- **Status:** draft (skill/reference bodies are stubs; package validates and is usable for advice)
- **Tier:** 2 (multi-source)

## What it does

| Mode | Use it when |
|------|-------------|
| advise | A team asks how to improve delivery, reliability, or a DevOps/SRE practice. |
| review | A team submits a pipeline, deployment plan, alerting design, or postmortem for critique. |
| validate | A team asks whether a design or service meets production-readiness or reliability criteria. |
| compare | A team asks for a comparison of delivery or reliability options. |

It does **not** write or debug application feature code, perform single-vendor product/cloud
administration, or make regulatory, contractual, or legal sign-off decisions.

## Canonical source of truth

`subagents/devops-sre-advisor/profile.yaml`. The runnable adapter is generated from the
profile — do not hand-edit the installed adapter.

## Grounding

Distilled (no verbatim quotation; all sources are `distillation-only`) from:

1. The DevOps Handbook — Gene Kim, Jez Humble, Patrick Debois, John Willis
2. Accelerate: The Science of Lean Software and DevOps — Forsgren, Humble, Kim
3. Pipeline as Code: Continuous Delivery with Jenkins, Kubernetes, and Terraform — Labouardy
4. The Site Reliability Workbook — Beyer, Murphy, Rensin, Kawahara, Thorne (eds.)
5. Continuous Delivery and DevOps: A Quickstart Guide — Paul Swartout

See `provenance-ledger.md` for the full field-by-field distillation log and rights notes.
