# Subagent Authoring Process Cycle

End-to-end process for creating and maintaining reusable experienced subagents
from technical books, articles, papers, and domain handbooks.

## Inputs and outputs of the full cycle

```
SOURCE MATERIAL
    │
    ▼
[Phase 1] Source Selection & Rights
    │  output: approved source list + rights status
    ▼
[Phase 2] Source Interrogation (Q1–Q18)
    │  output: interrogation record per source
    ▼
[Phase 2.5] Importance Ranking
    │  output: importance-scored unit shortlist
    ▼
[Phase 3] Artifact Decision Gate
    │  output: subagent / skill / reference / discard decision
    ▼
[Phase 4] Content Triage
    │  output: tagged unit worksheet
    ▼
[Phase 5] Profile Field Derivation
    │  output: draft portable profile + provenance ledger
    ▼
[Phase 6] Skill & Reference Extraction
    │  output: skill stubs + reference file stubs
    ▼
[Phase 7] Multi-Source Merge   ← only when 2+ sources
    │  output: conflict log + merged profile view
    ▼
[Phase 8] Profile Self-Check Gate
    │  output: PASS / WARNING / FAIL verdict
    ▼
[Phase 9] Platform Adapter Generation
    │  output: Claude / Copilot / Codex adapters
    ▼
[Phase 10] Testing
    │  output: golden test results + negative routing results
    ▼
[Phase 11] Release
    │  output: versioned artifacts + changelog entry
    ▼
[Phase 12] Maintenance Trigger
    │  output: stale flag → re-enter at Phase 2 or Phase 7
    └──────────────────────────────────────────────────────┐
                                                           │
                         source drifts / platform changes ┘
```

---

## Phase 1 — Source Selection & Rights

**Goal:** Confirm each source is authoritative enough and legally usable before
any distillation work begins.

**Inputs:** candidate sources (books, articles, papers, official docs, experience notes)

**Steps:**

1. Record source metadata: title, author, year, type, URL/ISBN
2. Classify authority: `primary` (official/original), `secondary` (survey/summary), `experiential` (internal lessons)
3. Record rights status using SPDX identifier or one of: `open`, `distillation-only`, `proprietary/restricted`
4. Classify volatility: `low` (stable principles), `medium` (evolving guidance), `high` (preview/changelog-driven)
5. Assign a review cadence based on volatility (see Phase 12)

**Hard rule:** No source enters distillation without rights status recorded.
Distillation-only sources may not be quoted verbatim anywhere downstream.

**Output:**

```
| ID | Title | Author | Year | Type | Authority | Rights | Volatility | Review cadence |
|----|-------|--------|------|------|-----------|--------|------------|----------------|
| S1 | ...   | ...    | ...  | ...  | primary   | open   | low        | annual         |
```

**Human decision required when:** rights are unclear; source is the only evidence for
a critical rule; source authority is weak (secondary only).

---

## Phase 2 — Source Interrogation (Q1–Q18)

**Goal:** Extract all information needed to author a profile before writing any YAML.

**Inputs:** approved source list from Phase 1

**Run these 18 questions against each source:**

| QID | Question | Maps to profile field |
|-----|----------|-----------------------|
| Q1  | Expert title or function? | `display_name`, `role` |
| Q2  | Job repeatedly performed? | `role`, `supported_modes` |
| Q3  | 3–5 situations that trigger this expert? | `when_to_use[]` |
| Q4  | 2–3 situations expert should NOT be involved? | `when_not_to_use[]` |
| Q5  | First thing expert asks for before engaging? | `inputs.required[]` |
| Q6  | Primary deliverable? | `outputs.primary_format`, mode contracts |
| Q7  | What distinguishes good work from bad? | `quality_bar[]` |
| Q8  | Who receives the work next / owns final decision? | `handoff_rules`, `canonical_owner` |
| Q9  | Which modes does source actually justify? | `supported_modes[]` |
| Q10 | What would expert refuse even if asked? | `forbidden_behaviours[]` |
| Q11 | Smallest useful output? | `minimum_useful_output` |
| Q12 | Knowledge that must be always-on? | `knowledge_partition.always_on[]` |
| Q13 | Actionable but too detailed for profile? | `knowledge_partition.skills[]` |
| Q14 | Better as reference file? | `knowledge_partition.references[]` |
| Q15 | Must be retrieved through MCP or tools? | `knowledge_partition.mcp[]` |
| Q16 | Project-specific, must be caller-supplied? | `knowledge_partition.caller_supplied[]` |
| Q17 | Source of truth for this domain? | `source_of_truth_policy` |
| Q18 | What is volatile or likely to drift? | provenance ledger review schedule |

**Mode evidence rule:** Assign a mode only when source provides both a credible
action verb AND a credible deliverable. No phantom modes.

| Source evidence | Allowed mode |
|----------------|-------------|
| Draft / create from scratch | `produce` |
| Review / critique existing artifact | `review` |
| Verify / gate against criteria | `validate` |
| Extract / classify / structure | `extract` |
| Suggest minimal bounded change | `patch-suggest` |
| Compare alternatives | `compare` |
| Recommend / consult / guide | `advise` |

**Purpose-review pattern:** When a source justifies critiquing goals, intent, or
project framing — not only code or documents — record it as a `purpose-review`
advisory pattern layered over `advise` / `validate` / `compare`. See the
**Purpose Review Pattern** section for the full contract.

**Output:** completed interrogation record per source (YAML answer template from
*Portable Source-to-Profile Method*)

**Human decision required when:** two plausible roles emerge from one source;
Q3 yields fewer than 3 concrete triggers; Q6 yields no clear deliverable.

---

## Phase 2.5 — Importance Ranking

**Goal:** Rank extracted candidate knowledge so that only the most authoritative,
actionable, reusable, and risk-reducing material becomes part of the generated
subagent package. Phase 2 interrogation finds *what* a source says; this phase
decides *what is worth keeping*. Without it a profile can be structurally correct
but intellectually weak.

**Inputs:** interrogation record from Phase 2; source segmented into candidate units

**Scoring dimensions (score each 1–5):**

| Dimension | Description |
|-----------|-------------|
| Authority | Primary, official, classic, peer-reviewed, or domain-authoritative source? |
| Actionability | Can it directly change the subagent's behaviour or output quality? |
| Reusability | Will it be useful across many future review or advisory tasks? |
| Risk impact | Does it prevent severe mistakes, unsafe advice, bad architecture, or invalid conclusions? |
| Evidence strength | Supported by data, examples, experiments, case studies, or clear reasoning? |
| Uniqueness | A distinctive insight from the source rather than generic background knowledge? |
| Transferability | Can it be applied outside the narrow example used in the source? |
| Stability | A durable principle rather than a version-specific detail likely to drift? |
| Operational fit | Does it map cleanly into a profile rule, skill workflow, reference checklist, or test case? |

**Score record (per candidate unit):**

```yaml
importance_score:
  authority: 1-5
  actionability: 1-5
  reusability: 1-5
  risk_impact: 1-5
  evidence_strength: 1-5
  uniqueness: 1-5
  transferability: 1-5
  stability: 1-5
  operational_fit: 1-5
```

**Decision rule:**

```text
High-value extraction candidate:
- total score >= 32 out of 45
- or risk_impact >= 5 and actionability >= 4
- or authority >= 5 and operational_fit >= 4

Discard or provenance-only candidate:
- total score < 20
- and no strong actionability, risk, or uniqueness
```

This rubric does not replace the Phase 4 triage tree; it runs before triage and
feeds it. Low-value units route to the provenance ledger only (or are dropped);
high-value units proceed to Phase 4 for destination assignment.

**Human decision required when:** a high-authority source scores low on operational
fit (keep for reference vs discard); a unique insight has weak evidence strength.

**Output:** importance-scored unit shortlist feeding Phase 3 and Phase 4

---

## Phase 3 — Artifact Decision Gate

**Goal:** Decide what to build before building anything.

**Inputs:** interrogation record from Phase 2

| Build this | When |
|-----------|------|
| Full subagent | Q1, Q3, Q4, Q5, Q6, Q7, Q9, Q11 all credibly answered; stable role identity; 3+ triggers; 2+ exclusions; 1+ modes with real outputs |
| Mode inside existing subagent | Same owner/inputs/artifacts as existing role; different output flavor only |
| Skill only | Source mainly teaches a repeatable workflow or procedure; no stable role identity |
| Reference file only | Source mainly contains tables, taxonomies, rubrics, checklists; no identity value |
| Discard / provenance note only | Background, history, motivation; no operational content |

**Stop here if:** the source only justifies a skill or reference — do not force a subagent.

---

## Phase 4 — Content Triage

**Goal:** Assign every content unit exactly one destination before writing profile prose.

**Inputs:** source text (segmented into units), interrogation record

**Triage decision tree (apply in order):**

```
0. Importance check
   Score the unit with the Phase 2.5 importance-ranking rubric.
   Low-score background material → provenance ledger only, unless needed
   for traceability. High-value units continue through the tree below.

1. Rights check
   Verbatim third-party text → paraphrase or exclude + log rights

2. Routing/identity check
   Defines role, trigger, exclusion, ownership, refusal, minimum output,
   universal quality rule → portable profile

3. Atomic heuristic check
   Single short rule or "if X then Y", fits one sentence, no branching → profile mode rule

4. Procedure check
   Ordered workflow 3+ steps OR any branching → skill

5. Static knowledge check
   Checklist 5+ items, taxonomy, rubric, matrix, glossary, long example → reference file

6. External-dependency check
   Needs scripts, repo search, runtime data, external API → MCP or tool-backed skill

7. Cross-mode reuse check
   Used by 2+ modes → shared skill or reference, not duplicated per-mode text

8. Volatility check
   Version-specific, preview behavior → adapter note or MCP-backed retrieval, not core

9. Background check
   History, rationale, anecdote → provenance ledger only
```

**Extraction thresholds (hard rules):**

| Threshold | Decision |
|-----------|---------|
| Procedure with 3+ steps | Extract to skill |
| Any branching logic | Extract to skill |
| Requires scripts or external tool calls | Extract to skill |
| Reused across 2+ modes | Extract to skill |
| Checklist with 5+ items | Extract to reference file |
| Table with 8+ rows | Extract to reference file |
| Taxonomy / scoring rubric / matrix | Extract to reference file |
| Live / volatile / tool-dependent | MCP or tool-backed skill |
| Single-sentence, always-on, platform-neutral rule | Keep in profile |

**Output:** source analysis worksheet

```
| Unit ID | Source ID | Location | Paraphrased unit | Tags | Mode | Destination | Confidence | Trace IDs |
|---------|-----------|----------|-----------------|------|------|-------------|------------|-----------|
```

---

## Phase 5 — Profile Field Derivation

**Goal:** Convert interrogation answers into portable profile fields with traceability.

**Inputs:** interrogation record, triage worksheet

**Derivation rules:**

| Field | Derivation rule |
|-------|----------------|
| `display_name` | Explicit role label or synthesized `<domain> <function>` |
| `role` | One sentence: what the role does, to what, for what reason |
| `when_to_use[]` | Convert Q3 triggers into caller-observable situations (3–6 items) |
| `when_not_to_use[]` | Convert Q4 exclusions into explicit non-routing rules (2+ items) |
| `inputs.required[]` | Q5: first required artifact/scope/context |
| `outputs.primary_format` | Q6: canonical deliverable noun |
| `quality_bar[]` | Q7: rewrite into falsifiable checks (3–5 items) |
| `supported_modes[]` | Q9: only modes with both action and deliverable evidence |
| `handoff_rules[]` | Q8: downstream owner or artifact handoff |
| `canonical_owner` | Q8+Q17: prefer human/artifact with final authority |
| `forbidden_behaviours[]` | Q10: translate anti-patterns into do-not rules |
| `minimum_useful_output` | Q11: smallest acceptable result |
| `source_of_truth_policy` | Q8+Q17: owner + edit authority + precedence |
| `knowledge_partition.*` | Q12–Q16: always_on / skills / references / mcp / caller_supplied |

**Traceability rule:** every major field must link to interrogation QIDs + distillation
row IDs + source IDs. No orphan field values.

**Profile bloat limits:**

| Check | Limit |
|-------|-------|
| Total body | Under 800 words |
| Universal rules | Max 12 |
| Rules per mode | Max 3 short rules |
| Procedures in body | No ordered sequence > 2 steps |
| Static tables/checklists | None |
| Platform-specific nouns | Zero |

**Simultaneously update provenance ledger** — distillation log row for every field.

**Output:** draft portable profile YAML + provenance ledger (draft)

---

## Phase 6 — Skill & Reference Extraction

**Goal:** Move all non-profile content into correct artifacts before self-check.

**Inputs:** triage worksheet (procedure/table/reference rows), draft profile

**For each skill candidate:**

1. Create `skills/<skill-name>/SKILL.md` — keep under 500 lines / 5,000 tokens
2. Move supporting detail to `skills/<skill-name>/references/` or `assets/`
3. Add skill name to profile `knowledge_partition.skills[]`
4. Log in provenance ledger under Generated Artifacts

**For each reference file candidate:**

1. Create `references/<topic>.md`
2. Add reference name to profile `knowledge_partition.references[]`
3. Log in provenance ledger

**Verify:** no multi-step procedure remains in profile body.

**Output:** skill stubs + reference file stubs + updated profile (no bloat)

---

## Phase 7 — Multi-Source Merge (skip if single source)

**Goal:** Resolve conflicts between sources explicitly before profile is considered complete.

**Inputs:** interrogation records from all sources, draft profile per source

**Conflict classes:**

| Class | Default resolution |
|-------|--------------------|
| Scope conflict | Apply narrower scope; log disagreement |
| Mode conflict | Keep both as mode variants; select primary by source authority |
| Quality standard conflict | Use stricter standard or split into mode variants |
| Terminology conflict | Pick one canonical term; map aliases in reference file |
| Anti-pattern conflict | Log as open question; do not silently resolve |
| Platform conflict | Keep core neutral; map in adapters only |
| Lifecycle conflict | Prefer current source in fast-moving domains |
| Ownership conflict | Prefer advisory mode unless ownership is explicit |
| Evidence conflict | Prefer concrete operational content over abstract principle |
| Rights conflict | Distill only what rights permit; record restriction |

**Source priority rules (apply in order):**

1. Concrete operational content over abstract principle
2. Official platform documentation for platform behavior
3. Primary sources over summaries
4. Later publication date in fast-moving domains
5. Source aligned with target domain and mode
6. If unresolved: preserve variants or split roles

**When to split vs preserve vs open question:**

| Outcome | Use when |
|---------|---------|
| Preserve variants | Same role identity, same inputs, different operational context or output style |
| Split into two subagents | 3+ of these differ: role identity, triggers, outputs, owner, forbidden behaviours |
| Open question | No authoritative tie-breaker; conflict affects scope or quality bar |

**Required merge record:**

```
| Conflict | Sources | Decision | Rationale |
|----------|---------|----------|-----------|
```

**Human decision required when:** conflict affects forbidden behaviour; ownership
conflict cannot be resolved to advisory; scope conflict removes role's main value.

**Output:** conflict log + merged portable profile

---

## Phase 8 — Profile Self-Check Gate

**Goal:** Verify profile is ready for adapter generation. Stop on any FAIL.

**Inputs:** draft portable profile + provenance ledger

| # | Check | Severity if failed |
|---|-------|--------------------|
| 1 | Role slug is kebab-case and role-based | FAIL |
| 2 | `when_to_use` has 3–6 concrete triggers | FAIL |
| 3 | `when_not_to_use` has 2+ explicit exclusions | FAIL |
| 4 | Every assigned mode has source evidence | FAIL |
| 5 | `inputs.required` explicit enough to avoid blind work | FAIL |
| 6 | `outputs.primary_format` explicit | FAIL |
| 7 | Every mode states its output format | FAIL |
| 8 | `minimum_useful_output` defined | FAIL |
| 9 | `canonical_owner` named in `source_of_truth_policy` | FAIL |
| 10 | `may_edit_canonical: false` for specialist roles | FAIL |
| 11 | `quality_bar` requires evidence citation | FAIL |
| 12 | All `forbidden_behaviours` traceable to source or policy | FAIL |
| 13 | Every multi-step workflow is in a skill, not profile body | FAIL |
| 14 | Profile body under 800 words | WARNING → FAIL if >1000 |
| 15 | No platform-specific file paths or tool names in core | FAIL |
| 16 | Provenance ledger exists and is complete | FAIL |
| 17 | No unresolved conflict in scope, ownership, or quality bar | FAIL |
| 18 | At least 3 golden tests exist including 1 negative routing test | FAIL |

**Fail-fast conditions (stop immediately):**

- No provenance ledger
- No explicit exclusions
- Unevidenced modes
- Missing canonical owner
- Platform-specific contamination in core
- Unresolved hard conflict
- Multi-step workflow still in body

**Do not generate adapters until gate passes.**

**Output:** PASS / WARNING / FAIL verdict with finding list

---

## Phase 9 — Platform Adapter Generation

**Goal:** Compile platform-native files from the portable core.

**Inputs:** passing portable profile, adapter config (platform-specific tool names, paths, MCP config)

**Adapter mapping summary:**

| Platform | Direct field mappings | Into body instructions | Known caveats |
|----------|-----------------------|----------------------|---------------|
| Claude Code | `name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `skills`, `mcpServers` | modes, exclusions, inputs, outputs, quality bar, handoffs, owner, forbidden behaviours | Plugin agents cannot carry `mcpServers`, `hooks`, `permissionMode` |
| GitHub Copilot | `name`, `description`, `tools`, `target`, `model` (where supported), `mcp-servers` (cloud only) | all role semantics beyond description | Cloud agent: MCP tools only, no resources/prompts; VS Code: no `mcp-servers` in per-agent profile |
| Codex | `name`, `description`, `developer_instructions`, `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config` | modes, exclusions, quality bar, ownership | Subagents only spawn when explicitly asked; no autonomous routing like Claude |

**Adapter-generator rules:**

- Description: compress to `role + top 2–3 triggers + top 1 exclusion`
- Body rendering order: role → use when → do not use when → required inputs → outputs by mode → quality bar → handoff → forbidden behaviours → source of truth
- Tool mapping: map from abstract adapter config only; never from literals in core
- MCP mapping: resolve concrete server names/transport/secrets in adapter only
- Read-only default: review/validate/extract/advise roles default to read-only unless patch mode selected
- Unsupported-field fallback: render in body instructions; log downgrade in adapter changelog

**Output:** Claude `.claude/agents/<slug>.md`, Copilot `.github/agents/<slug>.agent.md`,
Codex `.codex/agents/<slug>.toml`

---

## Phase 10 — Testing

**Goal:** Verify routing, output contract, permission boundaries, and regression stability.

**Inputs:** generated adapters, golden test cases

**Required test classes:**

| Class | What it checks |
|-------|---------------|
| Golden tests | Stable structured output for known tasks |
| Negative routing tests | Agent does NOT invoke when `when_not_to_use` applies |
| Missing-context tests | Agent warns/requests rather than hallucinates |
| Schema validation | Output matches `specialist-result-v1` |
| Permission tests | Read-only roles cannot write, spawn forbidden tools, or touch disallowed MCP |
| Cross-platform export validation | Adapters parse and load correctly on each platform |
| Canonical ownership tests | `patch-suggest` does not silently become direct artifact overwrite |

**Golden test template:**

```
| Test ID | Prompt | Expected route | Expected mode | Must ask for | Minimum output | Must not do |
|---------|--------|---------------|--------------|--------------|----------------|-------------|
| GT-001  | ...    | invoke        | review        | missing artifact if absent | 1 finding + evidence | mutate canonical artifact |
| GT-002  | ...    | do not invoke | n/a           | n/a          | non-route reason | invent scope |
```

**Minimum coverage:** positive routing, negative routing, missing-input handling,
one output schema check, one permission boundary check.

### Claude Code Runtime Smoke Tests

Structural validation (schemas, adapters, fixtures) proves the package is
well-formed. It does not prove Claude Code behaves correctly with the generated
agent: a syntactically valid adapter can still route badly or ignore its
read-only contract. Run these runtime checks against the installed adapter:

```text
1. Claude Code can discover the generated adapter.
2. The generated agent name does not collide with another agent.
3. The generated description is specific enough to support routing.
4. A positive prompt routes to the generated agent.
5. A negative prompt does not route to the generated agent.
6. The agent reads or references the canonical package when deeper context is needed.
7. The agent respects read-only behaviour for review/validate/advise modes.
8. The agent does not silently edit canonical artifacts unless patch mode is explicitly requested.
9. The agent returns the expected minimum useful output.
10. The agent cites or names evidence/provenance when making major claims.
```

**Output:** test results; PASS required before release

---

## Phase 11 — Release

**Goal:** Publish versioned artifacts with traceable history.

**Inputs:** passing tests, adapters, updated ledger

**Steps:**

1. Bump version in portable profile (`agent_version` semver)
2. Add changelog entry: what changed, which sources, which conflicts resolved
3. Commit all generated adapter files alongside portable core (both generated AND committed)
4. Add provenance comment or sidecar metadata to each adapter: portable profile version, export tool version, source hash
5. Tag release

**Hard rule:** Never silently overwrite a prior version. Supersede old decisions in ledger
Version History rather than rewriting them.

**Output:** versioned release with portable core + adapters + ledger + changelog

---

## Phase 12 — Maintenance Cycle

**Goal:** Keep profiles accurate as sources drift and platforms change.

**Inputs:** stale-source review schedule from provenance ledger, platform changelogs

**Review cadence by source type:**

| Source type | Cadence |
|-------------|---------|
| Official platform docs, preview features, MCP/CLI behavior | Quarterly or on changelog event |
| Cloud architecture/security/reliability guidance | Semiannual |
| Books and stable architectural principles | Annual |
| Internal engineering experience notes | On major platform/repo/process change |
| Conflict-heavy merged profiles | At every version bump |

**Maintenance trigger types:**

| Trigger | Re-enter at phase |
|---------|------------------|
| Source content changed materially | Phase 2 (re-interrogate) |
| New source adds a mode or changes quality bar | Phase 2 → Phase 7 |
| Platform adapter format changed | Phase 9 (adapter only, no re-interrogation) |
| Test failure after platform update | Phase 9 → Phase 10 |
| Conflict re-opened by new evidence | Phase 7 |
| Profile body became bloated after updates | Phase 5 → Phase 8 |
| Rights status changed | Phase 1 (stop distillation if rights withdrawn) |

**Stale flag rule:** if a source is flagged stale, adapters generated from it must be
marked `status: stale` and human-reviewed before next release.

---

## Purpose Review Pattern

Use when the user asks a generated subagent to critique a goal, intention, project
purpose, proposed direction, or strategic rationale. "Review my purpose" is more
abstract than code or document review: it is intent validation, scope critique,
and feasibility analysis. Model it explicitly so review/advisory subagents can
challenge project framing instead of merely encouraging the user.

A subagent in this pattern may assess whether a goal is clear; whether scope is
realistic; whether assumptions are hidden or weak; whether the stated purpose
matches the proposed implementation; whether the outcome is measurable; whether
the effort is justified; and whether the user should proceed, narrow scope,
gather evidence, or stop.

**Mode contract:**

```yaml
purpose_review:
  mode_family: advise / validate / compare
  primary_output: purpose critique report
  required_inputs:
    - stated purpose or goal
    - target user or stakeholder
    - intended output or deliverable
    - constraints
    - success criteria, if available
  checks:
    - goal clarity
    - scope realism
    - hidden assumptions
    - stakeholder fit
    - evidence required before commitment
    - risk/reward balance
    - implementation feasibility
    - alignment between purpose and proposed solution
  minimum_useful_output:
    - one-sentence verdict
    - top 3 risks or weaknesses
    - top 3 improvement suggestions
    - one recommended next action
  forbidden_behaviours:
    - do not merely encourage the user
    - do not accept vague goals without flagging ambiguity
    - do not rewrite the purpose without explaining the reasoning
    - do not invent stakeholder requirements
```

Realise this pattern in one of three ways: as the mode contract above embedded in
a generated profile; as a reference file template (`references/purpose-review-pattern.md`);
or as a built-in skill used by review/advisory subagents.

---

## Reference documents

| Document | Role in this cycle |
|----------|--------------------|
| `Designing Reusable Experienced Subagents…` | Canonical profile schema; platform comparison; mode contracts |
| `Designing Reliable Complex Skills…` | Skill structure; advisory vs deterministic; workflow control |
| `Neutral Reusable Subagent System…` | Rule pack concept; repository layout; starter agent set; test categories |
| `Portable Source-to-Profile Method…` | Interrogation question set; triage decision tree; conflict classes; ledger template; adapter matrix |
| `subagent-guide-gap-analysis.md` | Original gap identification |
| `subagent-guide-remaining-gaps.md` | Gap detail before Portable Method doc |
