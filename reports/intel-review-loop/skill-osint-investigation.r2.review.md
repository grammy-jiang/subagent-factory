# Review — `osint-investigation` SKILL.md (r2)

**Target:** `/home/grammy-jiang/projects/intelligence-analysis-agent/.claude/skills/osint-investigation/SKILL.md`
**Grounding:** `docs/intelligence-analysis/PIPELINE-grounded.md` (Step 3 collect+grade)
**Nature:** METHOD skill — the OSINT collection procedure the intel-analysis agent *runs*. Review only.
**Reviewers:** `agent-skills-advisor` (authoring quality) + `ai-agent-engineering-reviewer` (method design). Consolidated below; duplicate findings merged.

---

## MUST-FIX

### M1. Verification fan-out delegates to an unbounded general-purpose subagent — can bypass invariant 4 (sole egress surface)
*(eng-reviewer #1)*
Step 6: *"delegate to a **general-purpose subagent via the `Task` tool** … Pass **only** the one ledger item id + the verification question … keep raw, untrusted material out of the main context."*

Payload-isolation shape is right, but the subagent's **tool grant is never bounded**. A Task-spawned general-purpose subagent inherits the standard palette (WebFetch, Bash, …), not this skill's `allowed-tools`. Failure: told "verify this geolocation," it web-fetches corroborating pages directly — bypassing the SSRF guard, pre-egress gate, audit, and `confirmed=True` gate. That violates invariant 4 via a path the skill itself created. Also unspecified: how the subagent even *reads* the ledger item (no ledger-read tool granted).

**Fix:** define a dedicated `geo-chrono-verifier` subagent with an explicit `tools:` allowlist mirroring only this skill's `osint-toolkit:*` grant (no WebFetch/Bash); or, if using ad-hoc Task, state its permitted tools + how it reads the ledger item, and that its output stays subject to the same confirmation-gate rules for any egress it triggers.

### M2. Two of four human-confirmation gates are prompt-only, not tool-enforced
*(eng-reviewer #2)*
The skill claims the tool layer backstops the gate, but only for two of them: *"`fetch(..., confirmed=False)` and `reverse_image_search(..., confirmed=False)` refuse … until you pass `confirmed=True`."* The **named-private-individual** gate (step 1) and **classified-decline** (step 1 / invariant 5) have **no** tool-layer enforcement — `osint-toolkit:search` takes no `confirmed`/`gate_ack`, and its pre-egress gate only screens identifier *leakage outward*, not a private-individual/classified query. Failure: under context pressure (or an injected instruction from a prior fetched page — which invariant 4 already distrusts) the agent skips step-1 reasoning and calls `search("Jane Roe home address")` — nothing stops it. Invariant 3 is labelled "must hold," but half its enforcement is aspirational.

**Fix:** add a toolkit-side precondition on `search` (and other pre-fetch calls) — a policy classifier or required `gate_ack` param set only after the step-1 human exchange — so private-individual/classified targeting is blocked at the tool boundary.

### M3. Undeclared, colliding, and mis-indexed "grading step N" numbering space
*(BOTH: skills-advisor #1, eng-reviewer #3)*
The up-front numbering note promises exactly three spaces ("collection steps," "pipeline Step N," "structured-analysis Step N") that "never share a bare 'Step N'." But the body uses a **fourth, undeclared** label `"grading step N"` (lines 22, 34, 37, 54). This collides with the sibling `source-evaluation/SKILL.md`, whose own note declares *its* procedure as "grading steps 1–7" — so a reader cannot tell which skill `"grading step 6"` points into. Worse, it's **mis-indexed against this file's own steps**: filing the ungraded proposal (`propose_to_ledger`) is **step 5**, not "grading step 6" (line 37). And "decline in grading step 1" (line 34) may imply the classified-decline lives in the *other* skill and fires *after* collection — contradicting invariant 5 ("declined, not collected") and step-1's own inline decline.

**Fix:** drop "grading" from all self-references; use the bare `"step N"` the note already declares (as done correctly at lines 91, 94); correct line-37 index to **step 5**. If any mention genuinely points into `source-evaluation`, rename it distinctly (e.g. `"eval-step N"`) and extend the numbering note. Audit every cross-ref for correctness.

### M4. Description implies this skill grades — contradicts its own "When not to use" scope
*(skills-advisor #2)*
Description (line 3): *"… verify … **and grade before the item is trusted**."* Body "When not to use" (lines 36–37): *"**Grading** … is the sibling `source-evaluation` skill's job. This skill only files an ungraded proposal."* The description is the *sole* signal at trigger time (body not yet loaded), so this risks the skill being selected for grading-only work, or a caller believing the output is graded rather than an ungraded proposal.

**Fix:** rewrite the description tail so it no longer implies grading — e.g. "… and hand off to grading, never grading it here," or drop the grade clause and let "When not to use" own the boundary.

### M5. Output "awaiting grading" contradicts Hand-back "so the grades feed the ACH matrix"
*(eng-reviewer #4)*
Adjacent bullets disagree on whether items are graded at hand-back. Output: *"awaiting grading by `source-evaluation`."* Hand-back: *"return the `EvidenceItem[]` to structured-analysis Step 3/4 so **the grades** feed the ACH matrix build."* If step 7's `source-evaluation` invocation is synchronous, "awaiting grading" is stale; if fire-and-forget (as "do not grade here" suggests), "the grades feed…" is premature — grades don't exist yet at return. This is exactly the collect/grade boundary the skill otherwise polices (invariant 1).

**Fix:** state which it is — e.g. "step 7 invokes `source-evaluation` synchronously and waits; returned items include a grade," OR keep "awaiting grading" as operative, drop "so the grades feed the ACH matrix build," and make `structured-analysis` responsible for triggering/awaiting grading before ACH assembly.

### M6. REQUIRED `pii` flag has no specified derivation
*(eng-reviewer #5)*
Step 5 marks `pii` REQUIRED but never says how the agent sets it: true whenever step-1's named-private gate fired? whenever step-4 EXIF reveals a private individual? whenever a fetched page carries incidental PII? Unspecified → agents default it to `false` (least resistance) or set it inconsistently, quietly defeating the downstream privacy handling a REQUIRED flag implies.

**Fix:** tie the value to an observable signal, e.g. "set `pii=true` if step-1's named-private-individual gate fired for this item, or if step-4 EXIF/content identifies a private individual not already covered by step 1; otherwise `false`."

### M7. `osint-toolkit:verify_chain` is granted but never scheduled in the Procedure
*(BOTH: skills-advisor #3, eng-reviewer #6)*
It's in `allowed-tools` and mentioned once in Security (*"Call `osint-toolkit:verify_chain` to confirm … hash chain is intact"*), but appears in **none** of the seven numbered steps. An agent following the Procedure step-by-step never calls it — yet the headline output claim is "each hash-anchored," so the chain can go unverified indefinitely.

**Fix:** wire it into the Procedure — e.g. end of step 5 (`verify_chain(item_id)` before returning the id) or as a step-7 hand-off precondition, with an instruction to flag/abort on failure. If it's meant to be on-demand only, say so explicitly.

---

## NICE-TO-HAVE

- **N1. No outer-loop / stopping criterion for multi-item collection** *(eng #7).* Procedure narrates one item; Output promises `EvidenceItem[]`. No rule for how many URLs to pursue or when corroboration is "enough." Add: "repeat steps 2–6 per candidate; stop when [N independent corroborating sources / evidentiary need met / budget hit], then proceed once to step 7."
- **N2. Degraded-mode (`OSINT_LIVE=0`) truncation point unclear** *(eng #8).* "Search-planning-only" vs "search/fetch return no live bytes" leaves it ambiguous whether steps 3–7 are attempted against empty content or skipped. State: "execute step 1, issue step 2's search (returns no live bytes), do not proceed to steps 3–7, return empty `EvidenceItem[]` with `live_collection=false`." (Fail-closed spirit is sound.)
- **N3. "Current phase" buried in Purpose** *(skills #NTH).* `OSINT_LIVE` + deception-reviewer readiness are transient deployment state, not purpose. Give them a `## Status` header for scannability and to keep transient state out of the stable procedural file.
- **N4. Inconsistent tool-call specificity** *(skills #NTH).* Steps 3/6 show full signatures; step 5 prose-only args; step 4 bare names. Standardise on signature style across the Procedure.
- **N5. Security section restates invariants 2 & 4 verbatim** *(skills #NTH).* Only the `verify_chain` line is new. Trim to the delta, or fold `verify_chain` into invariant 4 and drop the section.
- **N6. No worked example** *(skills #NTH).* Sibling `source-evaluation` has one. Given three numbering spaces, five invariants, and a security-relevant confirm/reject gate, one short end-to-end example (incl. the `confirmed=False → confirmed=True` sequence) would cut misuse risk.
- **N7. Grounding inlined vs offloaded** *(skills #NTH).* Sibling offloads per-step traceability to `references/grounding.md`; this file inlines it, costing the always-loaded budget. Offload for consistency if it grows.
- **N8. Description voice imperative not third-person** *(skills #NTH).* "Run an…" → "Runs an…". Low severity; normalise package-wide.

---

MUST_FIX_COUNT: 7
