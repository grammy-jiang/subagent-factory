# Blueprint — Intelligence-Analysis AI Agent

> Implementation-neutral product blueprint. Re-elevated after a `product-blueprint-reviewer` pass found
> the prior v2 had absorbed design-spec detail from four domain reviews. The *how* (tool ops, schemas,
> protocol conventions, security-control mechanics, file layout, test techniques) now lives in the
> companion **DESIGN-SPEC-intel-analysis-agent.md**. This document holds only decisions, trade-offs,
> open decisions, and sequencing. **Decision-vs-detail rule:** if getting it wrong breaks the tradecraft
> method or the trust thesis, it belongs here (as a decision + rationale + trade-off); if it's *which*
> mechanism/schema/protocol realizes a decision, it belongs in the design-spec.

## Problem & thesis
Help an analyst work an intelligence question — hypothesize, weigh evidence, judge under uncertainty —
applying analytic tradecraft correctly and catching their own biases. Grounded in a distilled corpus of
11 canonical works (Heuer, Kahneman, Tetlock ×2, Jervis, Kent, CIA SAT Primer, Bazzell, Bellingcat,
Masterman, FM 2-22.3; 2,084 principles MAPped). **Thesis: augment, not replace, the human analyst** —
the agent structures and challenges reasoning; the human owns the judgment.

## Users & roles
- **Primary (MVP): a single analyst**, one case at a time.
- Secondary roles (reviewer, approver) exist conceptually but collapse to the same person at MVP.
- Team / multi-analyst use is an **open decision** (below), not assumed.

## Non-goals
- **Not** an autonomous analyst that self-commits or self-publishes — every judgment is human-gated.
- **Production** (drafting/formatting/disseminating the finished assessment) is **deferred** (open decision).
- No assumption of a classified/compartmented deployment (deployment-agnostic; open decision).

## Open decisions (surfaced, not resolved — decide before the phase noted)
1. **Deployment / classification context** — unclassified/OSINT-only vs classified/compartmented.
   Deferred, kept **deployment-agnostic**; must be resolved **before Phase 4 (OSINT/live connectors)**,
   because it changes whether live external collection is permissible at all.
2. **"Production" scope** — does the agent draft the finished assessment, or does the analyst?
   Deferred; revisit after the MVP proves the analysis core.
3. **Team / multi-analyst use** — solo for MVP; if adopted, per-case RBAC + identity binding +
   cross-case isolation become load-bearing (see design-spec). Decide before any shared-state MCP ships.
4. **Escalation target** — when the reviewer raises the same finding twice, escalate *to whom*?
   (Trivially "the analyst" at solo-MVP; re-open if team use is adopted.)

## Architecture intent — three responsibility layers
A composition, not one deliverable; one principle base feeds all three:
- **SKILLS** — the *method* the main agent runs in-flight (how to reason).
- **SUBAGENTS** — independent read-only *critics* it delegates to (outside check).
- **MCP servers** — *state + computation* the agent calls (what prose can't do).
(The invocation/orchestration mechanism between layers is deliberately left open — start with the
simplest that is actually exercised.)

## Load-bearing decisions (each breaks the method or trust thesis if wrong)
1. **Human-in-the-loop before any commit.** No probability, grade, or assessment is treated as final
   without analyst approval. *Alternative considered:* full autonomy + post-hoc audit. *Trade-off
   accepted:* latency / analyst-availability cost, in exchange for the trust the "augment not replace"
   thesis depends on. Failed review loops back to revise (bounded retry; repeated same finding →
   escalate, not retry).
2. **Independent critique reads raw case state, not the agent's narrative.** The reviewer subagent must
   see the actual evidence/hypotheses/grades. *Rationale:* Heuer — self-review from inside one's own
   reasoning trace fails; a critic fed only the story critiques the story. *Trade-off:* more plumbing
   than a narrative hand-off.
3. **The analyst/skill supplies judgment; tools only validate, compute, persist.** Grades, ACH cell
   ratings, probabilities are human/model judgments *fed into* tools as required input — never invented
   by a tool. *Trade-off:* reintroduces judgment variance the tool can't smooth, in exchange for keeping
   reasoning auditable and human-owned.
4. **History is immutable.** Corrections are superseding entries, never in-place edits. *Rationale:*
   an audit trail that can be quietly rewritten isn't one. *Trade-off:* downstream must resolve
   current-vs-historical state.
5. **Forecasts lock at commit; only the outcome is appended later.** *Rationale:* Tetlock — editing a
   past forecast reintroduces hindsight bias and defeats calibration scoring. *Trade-off:* no "fixing"
   a mis-stated forecast, only superseding it.
6. **ACH ranks by least-total-inconsistency (disconfirmation), not most-confirmation.** *Rationale:*
   Heuer — reversing this inverts the method it exists to enforce. (A method-fidelity invariant.)
7. **A shared case identity correlates state across tools.** Forecast ↔ matrix ↔ evidence must be
   linkable or the audit trail can't be reconstructed. *Trade-off:* a foundational data-modeling
   commitment made early.
8. **OSINT collection is separated from grading; ingested content is inert data, never instruction.**
   The collector fetches/stores raw; grading is a separate analyst-confirmed step. *Rationale:* in intel,
   the subject controls the very footprint being collected → a self-grading collector launders injected
   directives into "vetted" record. *Trade-off:* per-item review load.
9. **OSINT tooling holds the sole external-egress surface; other tools have none.** *Rationale:* confine
   the untrusted-content + private-data + outbound "trifecta" to one isolated, gated surface. *Trade-off:*
   legitimate cross-tool network needs must route through the one surface.
10. **OSINT outputs are candidate-only** (geolocation, matches) — proposals for human confirmation, not
    facts. *Rationale:* verification is a human/model judgment; a tool asserting it is overreach.

## MVP-0 (build + validate FIRST; zero MCP is load-bearing)
`structured-analytic-techniques` **skill** (prose; ACH as an in-context matrix) + `analytic-tradecraft-
reviewer` **subagent** + the human-approval gate + the loop-back edge. Delivers the core loop: frame →
hypothesize → weigh → adversarial-check → human-approve.
**Success criteria (the gate that lets Phase 2 start):** on a set of real practice questions (e.g.
Heuer's ACH worked examples / classic intelligence-failure cases), the agent-assisted pass must (a)
surface a *broader, better-disconfirmed* hypothesis set than an unaided baseline, and (b) have the
reviewer catch injected bias/assumption/overconfidence flaws a control run misses. Define the exact
question set + pass bar before building.

## Deferred / dropped
- `deception-detection-reviewer` — **deferred** to Phase 3/4 (needs a real evidentiary chain to interrogate).
- standalone `bias-mitigation` skill — **dropped** (trigger collision, encyclopedic drift, duplicates the
  reviewer); distributed into the SAT and forecasting skills.

## Build sequencing
1. **MVP-0** — SAT skill + tradecraft-reviewer + human-gate + loop-back; validate on real questions.
2. **Skills** — `calibrated-forecasting` + `source-evaluation`; success measure = Brier baseline on
   Tetlock's resolved questions.
3. **MCP** — persistent state/compute (calibration → evidence → ACH), only after the prose core proves out.
4. **OSINT** — collection tooling + investigation skill + deception reviewer; gated on the security
   review and the deployment-context decision *before* any live connector.

## Downstream-stage routing
- **security-review — RUN, mandatory, BLOCKING before Phase 4.** Reason: data egress + untrusted external
  content + a potential exfil path (the trifecta). Owner: security. Do not ship a live connector without it.
- **UX-design — RUN.** Signals: human review loop, failure-recovery, in-flight state correction, and
  life-safety stakes imply a non-trivial interaction surface beyond chat. Classify the primary surface.
- **architecture-design — DEFER** to the design-spec (the layer taxonomy is settled here; the wiring is not).
- **test-design — RUN at each phase gate** (the whole-agent evaluation, not just per-component).
