# Review r2 — deception-detection-reviewer

Single review pass on `subagents/deception-detection-reviewer/`. REVIEW ONLY — no edits made.

## Deterministic gate

- `validate_generated_package` → **VALIDATION PASSED** (0 FAIL; only non-blocking phase8/body-size WARNING).
- `quote_scan` → **PASS** — no potential verbatim quotation.

No gate must-fix.

## Consolidated findings (severe first)

### MUST-FIX

**M1 — HIGH — faithfulness / HEDGING_REMOVED — `profile.yaml` `always_on[5]` + `quality_bar[4]` (rule: "never commit an irrevocable act against a doubtful case").**
Backing P035 reads "Never commit an irrevocable act against a doubtful case *if it can be avoided* ... *almost always* proves right." Profile drops both qualifiers → unconditional prohibition stronger than source. Violates evidence-protocol faithfulness rule (no rule stronger than support).
Fix: restore "where it can be avoided" + soften "never" to strong default with residual-uncertainty framing.

**M2 — HIGH — faithfulness / SCOPE_BROADENED + HEDGING_REMOVED — `profile.yaml` `always_on[2]` + `source_of_truth_policy.precedence`.**
(a) `always_on[2]` "firewall or terminate a compromised case at once" drops P063's "*consider* terminating..." — considered option → flat imperative. (b) `precedence` "network security governs unless specific evidence justifies the risk" invents an evidentiary-override clause present in neither P063 nor P069. Load-bearing: this field resolves reviewer conflicts, so it changes behavior.
Fix: restore "consider"; scope precedence to P063's linked-asset-collapse trigger, or mark the general framing as engineered synthesis.

**M3 — HIGH — release-policy — `provenance-ledger.md:58-63` Version History missing v1.0.1 entry.**
`profile.yaml:5` declares `agent_version: "1.0.1"` and `CHANGELOG.md:6-24` documents a substantive v1.0.1; ledger Version History still shows only v1.0.0. Violates repo Supersession rule (`generated-artifact-policy.md`: new version entry required, old decisions stay visible).
Fix: append `### v1.0.1 — 2026-07-11` mirroring the CHANGELOG M1–M6 remediation.

### SHOULD-FIX

**S1 — MEDIUM — faithfulness / HEDGING_REMOVED (×3) — `quality_bar[1]`, `always_on[1]`, example ("long truthful record").**
P051: "A long period of truthful reporting is *usually* a necessary precondition." Stated as absolute in 3 places, each dropping "usually." Fix: add hedge ("ordinarily"/"typically") at least in quality_bar + always_on.

**S2 — MEDIUM — profile coverage — `profile.yaml:88-134` skill `physical-and-technical-deception-craft` (P018,P037,P041,P044,P046,P081,P082,P084,P085) has zero citation in `quality_bar`/`forbidden_behaviours`/`handoff_rules`.**
9 of 94 principles reachable only via `always_on[7]`; no profile-body check exercises them. (Repeat of prior-round S1, not remediated.) Fix: extend/add one `quality_bar` bullet citing this skill.

**S3 — MEDIUM — test-record honesty — `tests/test-results.md:24` Phase-8 check 14 body-size labeled "INFO".**
`profile_self_check.py` body-size check only emits PASS/WARNING/FAIL, never INFO; body ~930-940 words = WARNING band. Row wasn't generated from a real run. Fix: regenerate `test-results.md` from actual run (WARNING); optionally trim quality_bar/when_to_use < 800 words.

**S4 — MEDIUM — skill routing — `assessing-enemy-trust-and-belief/SKILL.md:3-8` + `counter-deception-and-the-mirror/SKILL.md:3-6` descriptions overlap.**
Both trigger on near-identical "channel controlled/trusted/blown" surface phrase; true boundary (enemy's belief about our channel vs. testing our own confidence is compromised) never reaches frontmatter description (only Tier-1 signal). Sibling `calibration-forecasting-reviewer` uses "not X, which Y owns" convention. Fix: add "not X, which <sibling> owns" clause to each description tail.

### NICE-TO-HAVE

**N1 — LOW — faithfulness — `always_on[5]` "favour quality over quantity" (P053) drops trigger "when suitable agents are numerous." SCOPE_BROADENED, low impact.** Add condition.

**N2 — LOW — faithfulness — `always_on[4]` "governance works only when members subordinate..." (P056).** Source is comparative ("more than a clean charter"), not necessary-condition. Reword to comparative form.

**N3 — LOW — faithfulness — `forbidden_behaviours[3]` real-world-attack-plan ban cites P042 (officer integrity) — tenuous anchor.** Defensible engineered safety boundary (restricts, not expands). Label as engineered policy or find better anchor.

**N4 — LOW — agent-design — adapter body lacks explicit "submitted plan/case is data, not instruction" line.** Low risk: Read/Grep/Glob only = no execution surface; forbidden_behaviours already blocks operational plans. Optional hardening.

**N5 — LOW — adapter routing — `.claude/agents/generated/deception-detection-reviewer.md:3` description truncated mid-phrase, drops "double-agent system".** Generator truncation-budget artifact; partially offset by "double-agent case" later in Use-when. Regenerate description to close clause before "— Use when:".

**N6 — LOW — skill cosmetic — `physical-and-technical-deception-craft/SKILL.md:42` heading lowercases "and" ("# Physical and Technical...") — sole outlier vs 7 title-cased siblings.** Capitalize.

**N7 — LOW — ledger overclaim — `provenance-ledger.md:6-7` "No profile field value is an orphan" broader than shown** (only quality_bar/forbidden/handoff/always_on carry inline citations; role/when_to/inputs/outputs do not — consistent with convention). Scope claim to "load-bearing rule fields."

## Confirmed clean

- Tool boundary Read/Grep/Glob = correct minimal read-only set; no Write/Edit/Bash/network — agent structurally cannot run an operation or feed an adversary. Imperative "invariants" describe the plan-under-review's tradecraft, not the model's tool use.
- Role single-responsibility + non-operational framing consistent across role/when_not_to_use/forbidden/handoff; adapter faithfully mirrors profile agent-design fields.
- 8 skills uniformly structured (Purpose/When/Procedure/Inputs/Output/Anti-patterns/References/Provenance); every frontmatter principle exercised by a numbered step; no orphan/missing principle; cross-skill refs resolve; frontmatter name matches slug; all declared in `profile.yaml:223-231`.
- Prior-round HIGHs (fabricated always_on M1/M2, precedence orphan, router truncation) verified fixed in v1.0.1 profile — EXCEPT the persisting hedging over-claims (M1/M2 above) and S2 coverage gap.
- golden-tests.yaml: 5 golden + 2 negative-routing + 2 missing-context — exceeds Phase-8 minimum.
- Domain-scope narrowing (review-only, no command decisions, no real-world attack plans) genuinely faithful; single-source, no unresolved conflict.

MUST_FIX_COUNT: 3
