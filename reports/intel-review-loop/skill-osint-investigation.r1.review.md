# Review — `osint-investigation` SKILL.md (round 1)

**Target:** `/home/grammy-jiang/projects/intelligence-analysis-agent/.claude/skills/osint-investigation/SKILL.md`
**Grounding:** `docs/intelligence-analysis/PIPELINE-grounded.md` (Step 3, collect + grade) + `docs/design/phase4-osint-design.md`
**Nature:** This is a **METHOD** skill — the procedure the intel-analysis agent *runs* to collect OSINT evidence. Not a reviewer skill.
**Reviewers:** `agent-skills-advisor` (authoring quality) + `ai-agent-engineering-reviewer` (method design). Findings deduped and verified against the file.

---

## MUST-FIX

### M1. Human-approval gate is stated, not operationalized (method) — lines 29-30, 33-34, 37-40, 58-59
"gated," "explicit confirmed invocation," "human-confirmed," "proposals for human confirmation" recur 4×, but **no step tells the agent to stop, present candidate + confidence, and block the next tool call until an explicit reply**. An LLM running this cannot distinguish "user already implied approval by asking for the investigation" from "must re-ask now, before this specific egress/upload." This is the core trust-model control the whole skill exists to enforce — and it is the one control left descriptive. Contrast: `ach-engine refuses to score until graded` (line 14) is a *real* gate; the human checks should hold to the same enforced-not-stated bar.
**Fix:** Add a reusable gate template — "output a structured candidate summary (what / why / confidence); do NOT proceed to the next tool call until the user replies confirm/reject" — and apply it at each of the 4 confirmation points (private-individual scoping, near-miss fetch, reverse-image upload, pre-analysis verification acceptance).

### M2. Verify (Step 5) runs before archive (Step 6) and grade (Step 7), inverting provenance (method) — lines 37-47
As written, a "verified conclusion (with its confidence)" is produced on content **not yet in the ledger and not yet graded**, so an ungraded/unlogged item's derived confidence can already reach the main analysis; a crash between Step 5 and 6 loses provenance. Contradicts the Purpose claim (lines 10-14) that collection is separated from grading via an ingested-then-graded record.
**Fix:** Reorder to fetch → hash/EXIF → **archive as ingested/ungraded (durable hash-anchored record first)** → verification workflow (operates against the ledger item id, writes output as an annotation on that record) → grade.

### M3. `reverse_image_search` + `get_map_tile` absent from the Procedure (method + authoring) — line 58-59 vs 37-40
Step 5 ("verify as a workflow") is exactly where geolocation (`osint-toolkit:get_map_tile`) and image corroboration (`osint-toolkit:reverse_image_search`) belong per the phase-4 design. But `get_map_tile` appears **nowhere** in the file, and `reverse_image_search` — a tool that **uploads a real subject's likeness to a third party** — appears only as a Security footnote (line 58), with no step number, trigger, or numbered confirmation checkpoint. An agent following the numbered Procedure literally has no instruction to run either.
**Fix:** Name both in Step 5: `get_map_tile` for a candidate tile to compare; `reverse_image_search` treated as fetch-equivalent with its OWN explicit-confirmation gate that discloses the likeness will leave the environment.

### M4. `allowed-tools` frontmatter missing (authoring) — lines 1-4
Frontmatter has only `name` + `description`. Both siblings (`structured-analysis`, `source-evaluation`) declare `allowed-tools:` for every MCP tool + `Task`/`Skill` they call, so calls are pre-approved and don't stall on per-use prompts. This skill calls `osint-toolkit:*`, `Task`, and `Skill` with none declared.
**Fix:** `allowed-tools: Task, Skill, osint-toolkit:search, osint-toolkit:fetch, osint-toolkit:compute_hash, osint-toolkit:extract_exif, osint-toolkit:reverse_image_search, osint-toolkit:get_map_tile, osint-toolkit:propose_to_ledger` (+ any ledger read-backs used).

### M5. MCP tool references non-fully-qualified and inconsistent (authoring) — lines 31, 33, 35, 41
Lines 31/33/41 use dot notation (`osint-toolkit.search`, `.fetch`, `.propose_to_ledger`); line 35 drops the server prefix entirely (`compute_hash`, `extract_exif`). Repo convention is colon + full prefix (`evidence-ledger:add_evidence`). Risks tool-not-found resolution.
**Fix:** Standardize to `osint-toolkit:search|fetch|compute_hash|extract_exif|reverse_image_search|get_map_tile|propose_to_ledger` throughout.

---

## SHOULD-FIX

- **S1. "verified" vs "unverified" contradiction (method) — lines 39 vs 42.** Step 5 calls its output "the verified conclusion"; Step 6 calls the ledger note "an unverified annotation." Two distinct axes are being conflated. Fix: name them separately — a per-claim `verification` status (Step 5) vs a per-item `grade` (A–F/1–6, Step 7) — and use each term consistently.
- **S2. Current-phase / deferred-capability disclosure absent (authoring) — Steps 3, 7.** Sibling `structured-analysis` states the live-collection gate (`OSINT_LIVE=0`, read-only) and the `deception-detection-reviewer` security-review gate; this skill instructs live fetch (line 33) and unconditional deception delegation (lines 43-47). Fix: add a "Current phase" note with the degraded behavior (proceed search-only + flag; skip Step-7 deception delegation + note omission) when either gate is off. *(Reviewer rated this MUST; downgraded to SHOULD here pending confirmation that the `OSINT_LIVE` gate is actually wired for this deployment — verify before dismissing.)*
- **S3. Step-5 delegation target unnamed, no I/O contract (method) — lines 38-39.** "forked context / subagent" names no roster member (none of bias/method/deception/calibration reviewers is a geo/chrono verifier) and specifies no input/output. Fix: state it's a `Task` call to a general-purpose subagent (no dedicated verifier exists); pass only the one item + question; require return shape {verification, confidence, rationale} as the sole payload re-entering the main thread.
- **S4. No concrete trigger for `deception-detection-reviewer` escalation (method) — lines 44-46.** "serious D&D risk" is undefined → inconsistent escalation across runs. Fix: name a trigger, e.g. corroboration fails across independent channels, or `source-trust-registry` shows prior manipulated-media/feedback-controlled history.
- **S5. Private-individual gate covers only initial scoping (method) — lines 29-30.** Fires when collection is aimed at a named person from the start; silent on a private individual surfaced mid-investigation. Fix: re-trigger the gate whenever the target shifts to a newly identified named private individual.
- **S6. Skill-boundary not reciprocal with `source-evaluation` (authoring) — lines 22-25.** `source-evaluation` excludes collection ("that's `osint-investigation`"); this "When not to use" doesn't return the favor. Fix: add "Grading a collected item's reliability/credibility — that's `source-evaluation`; this skill only files an ungraded proposal (Step 6)."

---

## NICE-TO-HAVE

- **N1.** No per-step source citations (siblings cite claim IDs per step, e.g. `(FM 2-22.3, C428)`); sourcing is bulk-gestured only in Grounding (lines 62-67). Attach the relevant citation to each step to keep the grounded-not-invented signal per-step.
- **N2.** No "Load-bearing invariants" block; collect-then-grade, candidate-only, private-individual gate, sole-egress are scattered across prose. `structured-analysis` promotes its non-negotiables to one numbered list — do the same for the one skill that touches the network.
- **N3.** No explicit "return to `structured-analysis` Step 4 with EvidenceItem[]" step; hand-back is only implicit in the calling convention. One sentence.
- **N4.** No in-Procedure refusal check for classified-adjacent taskings (only in "When not to use"); add a check-and-decline in Step 1.
- **N5.** No `references/` or worked example (search → fetch → hash/EXIF → propose → grade); body is short (68 lines), so a one-pass trace wouldn't overload context and would aid execution fidelity.
- **N6.** Grounding doesn't state `source-trust-registry` is read by `source-evaluation`, not by this skill — risks a maintainer duplicating or dropping the read.

---

## Note worth preserving
The collect/grade separation IS mechanically enforced in one place — "ach-engine refuses to score it until graded" (line 14) is a real gate, not a stated intention. That is the standard M1 asks the human-confirmation language to meet everywhere else.

MUST_FIX_COUNT: 5
