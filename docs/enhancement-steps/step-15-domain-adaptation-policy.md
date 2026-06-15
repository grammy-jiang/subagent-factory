# Step 15 — Domain-Adaptation Policy (regulated / non-technical domains)

> Folds `docs/Research/domain-adaptation-regulated-advice/` (25 papers, validated PASS 1.0, 2 rounds).
> This is the **J-track** of `research-integration-plan.md`, and the concrete answer to the **Q1**
> question (can the factory author finance/stock — and legal/medical — books?). See memory
> `financial-domain-readiness`. **Design capture; the *method* answer is HIGH-confidence.**

**Goal** — Let the factory author safe, well-scoped packages in regulated / high-stakes domains
(finance, legal, medical): a **graded** no-advice boundary, a server-side **defer-to-professional**
gate, and **authority-grounded** evidence norms — produced by a **hybrid** method (deterministic
per-domain template + LLM interrogation for evidence norms only).

## Why (the gap)

The pipeline is domain-agnostic and already builds non-CS packages (advertising, negotiation,
startup-CEO). But for finance/legal/medical it must not give personalized advice, must defer to a
licensed professional, and must ground claims in authority — and the factory does **not** add these
automatically. The research settles *how*.

## Core method answer (the Q1 resolution)

**Deterministic structural scaffolding beats prompt-only scope control** (which is unstable +
model-inconsistent). So:
- author `forbidden_behaviours` + disclaimers + handoff defaults from a **deterministic per-domain
  template**;
- use **LLM source-interrogation only to populate `source_of_truth_policy` evidence norms** (not to
  enforce scope).

## Built (2026-06-15) — `domain_policy` template + opt-in gate

`tools/subagent_factory/domain_policy.py` — the deterministic per-domain scaffolding (the buildable
half; evidence norms stay LLM). Pure data + pure functions, no schema change, no export change.

- `domain_policy(domain)` for `finance` / `legal` / `medical` → `{domain_risk_category, professional,
  forbidden_behaviours (GRADED no-advice lines), handoff_rules (defer-to-professional / τ default),
  standing_disclaimer, source_precedence_hint}`. Each no-advice line is **safe-completion** — "explain
  the general framework … then refer to a licensed professional" — not a binary refusal (J1, J2). The
  handoff rule **triggers on an external uncertainty signal, not the model's own confidence** (J3, J4).
  The disclaimer is the human-in-the-loop "decision support, not a replacement" posture (J7).
- `merge_domain_policy(profile, domain)` folds the template into a profile dict (idempotent): extends
  `forbidden_behaviours` + `handoff_rules` (the fields the adapter **already renders**, so the boundary
  surfaces with no export change) and adds the disclaimer as a handoff rule.
- `check_domain_policy(profile)` — **opt-in deterministic gate**, wired into
  `validate_generated_package` (block #14). Inert for any profile with no `domain_risk_category` (every
  technical/non-regulated package → Tier-0 untouched). For a regulated package it lenient-checks
  (keyword-based, so rephrasing still passes) for a no-advice boundary, a defer-to-professional handoff,
  and a non-empty disclaimer — and **FAILs** a regulated package that ships without them.
- CLI: `python -m tools.subagent_factory.domain_policy <domain> [--merge profile.yaml]` (emit / preview;
  never writes). 18 tests.

**Authoring integration:** when the source-interrogator/profile-deriver classifies a source as a
regulated domain, it sets `domain_risk_category` and merges `domain_policy(domain)`; the gate enforces
the boundary at validation time regardless, so a forgotten boundary is caught deterministically (gate
decides, not the LLM). **Carried (LLM/academic):** J5 evidence norms (LLM interrogation, ties Step-14);
J6's LLM half; the open regulatory gaps below.

## Spec (findings → factory design; no code yet)

| field / mechanism | design | finding |
|---|---|---|
| `forbidden_behaviours` | **GRADED** no-advice boundary (safe-completion: answer the safe/general part → flag the regulated part → refer to a licensed professional), **not** a binary refusal; **per-domain-risk-category, reconfigurable without retraining** | F1, F8 |
| (frontier) | target the safety↔over-refusal frontier — a maximize-refusal boundary blocks the legitimate questions the expert should answer | F2 |
| `handoff_rules` | **defer-to-professional = a server-side, retraining-free uncertainty-threshold (τ) abstention gate** — the *same selective-prediction shape as the Step-13 ask-gate* | F3 |
| (gate input) | **do NOT use the model's own confidence** as the gate — LLMs are worst-calibrated exactly on professional law/medicine; τ needs external grounding | F4 |
| `source_of_truth_policy` | **retrieval-from-authority with mandatory citations** — answer from a curated, authority-weighted repository, generate only on retrieval miss; ties to **Step-14** runtime retrieval | F5 |
| role / standing disclaimer | **human-in-the-loop, "decision support, not a replacement for a licensed professional"** as the default posture | F7 |
| judge gating | **validate any LLM-as-judge before it gates scope** (multi-judge consensus) — ties to B-track | F9 |
| security | the deferral/refusal signal is an **attack surface** — keep it server-side + isolated from untrusted input (aligns with `untrusted-source-policy`) | F10 |

## LLM ↔ deterministic split

- **Deterministic:** the per-domain policy template (forbidden_behaviours / disclaimers / handoff
  defaults), the τ deferral gate, retrieval-from-authority.
- **LLM:** source-interrogation to populate evidence norms only. **Not** scope control (prompt-only is
  unstable).

## Reuse / ties

- **Step 13 ask-gate** — the τ abstention gate is the same mechanism (defer-to-professional ≈ abstain).
- **Step 14 runtime-retrieval** — retrieval-from-authority + citations is the evidence-norm half.
- **`evidence-protocol.yaml`** — per-domain override is the existing seam for domain evidence norms.
- **`untrusted-source-policy`** — finding F10 (deferral-as-attack-surface) aligns with it.

## Research inputs (paper IDs)

GRADED boundary [2505.08054, 2601.17642, 2405.20947, 2603.10068]; over-refusal frontier [2405.20947,
2510.08158, 2407.18418]; τ deferral gate [2601.01008, 2511.16625, 2412.06748]; calibration distrust
[2306.13063, 2401.01301, 2407.08662]; retrieval-from-authority [2511.01668, 2505.02164, 2311.10723];
method (det scaffolding > prompt-only) [2402.15062, 2507.16642]; liability/human-in-loop [2510.07243,
2505.02164]; judge validation [2603.10068, 2508.11222]; deferral attack surface [2502.05206, 2512.11933].

## Exit criteria (when built)

- A per-domain policy template emits the graded-boundary `forbidden_behaviours` + disclaimer + handoff
  defaults; a finance/legal/medical package authored with it ships the no-advice boundary by default.
- The τ deferral gate (Step-13 mechanism) wired into `handoff_rules`, externally grounded (not
  self-confidence).
- `make verify` green; Tier-0 packages untouched (opt-in per domain).

## Caveats — open gaps (not in arXiv → manual regulatory review, not a research round)

- **personalized-vs-general advice detection** (the boundary's classifier) — no benchmark.
- **disclaimer legal efficacy / liability allocation** — a legal question, not an ML one.
- a **finance/legal graded-scope benchmark** does not exist.

Generalizes beyond finance to **legal and medical** — the same graded-boundary + τ-deferral +
authority-grounding shape.
