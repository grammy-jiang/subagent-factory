# Review — translation-equivalence-advisor (round 5)

Consolidated review across deterministic gates + 7 reviewer lenses (agent-skills, profile,
faithfulness, ai-agent-engineering, plus domain: descriptive / quality / technical translation).
Dedup applied; most-severe first. REVIEW ONLY — nothing fixed.

## Deterministic gates (STEP 1)

| Gate | Result |
|------|--------|
| `validate_generated_package` | **PASS** (0 FAIL; phase8 WARNING only) |
| `quote_scan` | PASS — no verbatim quotation |
| truncation `…` scan (skills + adapter) | clean |
| adapter invariant-severed-parenthetical scan | clean |

No deterministic FAILs.

---

## MUST-FIX

### MF1 — Reference index drifted from the corrected spine; P094/P100 still carry pre-round-4 (over-broad) wording
- **where:** `references/translation-equivalence-principles-index.md:248` (P094), `:251` (P100)
- **severity:** must-fix
- **problem:** Round 4 narrowed two genuine domain over-generalizations in `principles.yaml`, but the principle-index reference — which every skill points to as "the full principle catalogue" — was not regenerated, so at the point of use an agent retrieves the un-patched statement, undoing the fix.
  - P094 index reads "...relax it when consistency produces unnatural or meaningless receptor text." — **missing** the corrected clause "this is stylistic concordance, not subject-matter terminology consistency" (`principles.yaml:1776-1777`). Without it, a reader can license relaxed terminology consistency in technical/legal/scientific translation, where consistency is near-mandatory.
  - P100 index reads "Use back-translation only to expose ... structure, remembering it is a theoretically unsound compromise that never reproduces the original's meaning." — **missing** both the "As a pedagogical illustration of structural differences" scoping and "so it is not by itself a general test of translation quality" qualifier now in `principles.yaml:1864-1867`. Reads as a blanket dismissal of back-translation as a QA check.
  - Confirmed by diff of index vs `principles.yaml` P094/P100.
- **fix:** Regenerate `translation-equivalence-principles-index.md` from current `principles.yaml` so every principle whose statement was edited in v1.2.0–v1.2.5 (P094, P100, and re-verify P066 at index `:197`) carries the current wording verbatim. Add the index to the re-export/verify step that runs after any `principles.yaml` edit — this is the second index (after the r4 adapter-description truncation) to silently drift from the spine.

### MF2 — Phase-8 test-hygiene artifacts stale relative to shipped v1.2.5
- **where:** `tests/test-results.md:3` (`Generated: 2026-07-11T19:46:38`, body `~974 words` at line 24) and `tests/golden-tests.yaml:4` (`profile_version: 1.2.4`) vs `profile.yaml:4` (`agent_version: 1.2.5`)
- **severity:** must-fix
- **problem:** v1.2.5 (round-4 fix) changed `export_claude_agent.py` `_compose_description` and trimmed the body to ~968w — exactly what Phase-8/10 testing re-verifies — but round 4 dropped the "test hygiene" regen step that rounds r1–r3 each ran. `test-results.md` still reports the v1.2.3/1.2.4-era 974-word number and a pre-v1.2.5 timestamp; `golden-tests.yaml` still declares `profile_version: 1.2.4`. `validate_generated_package.py` only checks these files *exist*, not that they match `agent_version` — so `validate PASS` does not certify freshness. Confirmed by version diff.
- **fix:** Re-run `profile_self_check` (or `cli selfcheck`) and regenerate `tests/test-results.md` against v1.2.5; bump `golden-tests.yaml` `profile_version` to `1.2.5`; add the standard v1.2.5 "test hygiene" changelog/ledger line matching v1.2.0/1.2.2/1.2.3/1.2.4.

---

## SHOULD-FIX

### SF1 — No worked `compare`-mode example anywhere in the package
- **where:** `profile.yaml:176-214` (`examples:`, mirrored in adapter `:133-151`); every `skills/*/SKILL.md` Output section references compare mode
- **severity:** should-fix (raised independently by agent-skills #2, profile #2, ai-agent #1 — deduped)
- **problem:** Three modes declared (`advise`/`review`/`compare`) but the three examples cover advise, review, and a review-adjacent decline; `compare`'s distinct contract (side-by-side of two strategies → purpose-weighted recommendation) is asserted but never demonstrated. Golden GT-004 exercises it, but the profile's own example gallery — what teaches response shape concretely — does not. r4 SF8 partially closed this (added review example) but left compare.
- **fix:** Add a fourth `examples` entry (`kind: happy-path`) showing a compare-mode `ideal_response` — e.g. weighing formal vs dynamic equivalence for one segment under a stated brief — so the least-demonstrated mode has the concreteness of the other two.

### SF2 — `knowledge_partition.always_on[6]` reproduces a HEDGING_REMOVED over-claim already fixed elsewhere
- **where:** `profile.yaml:143-149`
- **severity:** should-fix (faithfulness #1)
- **problem:** The always-on digest presents the four receptor-response adequacy criteria (P008/P021/P022/P023/P035) as a flat universal test — omitting P022's alternate closeness-to-source-form adequacy path (for formal-access briefs) and P035's explicit "accepting multiple valid solutions" hedge. This is the identical over-claim class fixed in v1.1.0 for `quality_bar[6]` and propagated to the skill/glossary/GT-004, but not propagated to this always-on line. P022/P035 are cited numerically but their content isn't reflected in the prose.
- **fix:** Reword to mirror the corrected `quality_bar[6]`, e.g. "...evaluating adequacy by sense, source spirit and manner, natural receptor expression, and similar audience response for a receptor-response task, or by closeness to source form when readers need that access (P022) — accepting multiple valid solutions (P035)."

### SF3 — Dynamic-equivalence content never names the standard "receptor response is not measurable" critique
- **where:** `skills/dynamic-and-formal-equivalence/SKILL.md` (P034–P036); `references/translation-equivalence-key-concepts.md` "Dynamic equivalence"/"Adequacy" entries; `profile.yaml` quality_bar formal-vs-dynamic clause
- **severity:** should-fix (descriptive #1 + quality + technical concur — deduped)
- **problem:** "Similar audience response"/"equivalent effect" is operationalized as an adequacy criterion (P035/P036) without flagging the well-known TS objection (van den Broeck, House, Gutt) that receptor response is not empirically observable, so "equivalent effect" is an intuitive judgment dressed as a testable standard. The sibling `descriptive-translation-reviewer` already encodes this ("equivalent effect can be illusory"). Anti-pattern lists hedge it in behaviour ("directional target, not pass/fail") but the specific epistemic limit is never named. Dynamic equivalence is one of only two source pillars, so its best-known limitation should be explicit.
- **fix:** Add one caveat sentence to the skill + the "Dynamic equivalence"/"Adequacy" glossary entries: a claim of achieved dynamic equivalence is a defensible interpretation, not a measured outcome. Keeps the package's own P078/P051 relative stance consistent at its most operationalization-prone criterion.

### SF4 — `NR-002` (`do_not_invoke`) reads as contradicting the profile's own failure-recovery example
- **where:** `tests/golden-tests.yaml:103-107` (NR-002) vs `profile.yaml:203-214` (`examples[2]`, failure-recovery)
- **severity:** should-fix (profile #3)
- **problem:** NR-002's prompt ("Translate the whole thing... send me the final file") is the same request class as `examples[2]` ("just translate this"), but the two assert opposite outcomes: NR-002 says do-not-invoke; `examples[2]` is a worked example of this subagent being invoked and gracefully declining+redirecting. An implementer can't tell whether the failure-recovery path is ever meant to fire via autorouting. (Same pattern exists in sibling `translation-quality-reviewer` — likely an undocumented family convention.)
- **fix:** Add a one-line note (golden-tests or ledger): `do_not_invoke` = autorouter should not select this subagent as primary for a bare deliver-the-translation request; if invoked directly/misrouted it must decline per `forbidden_behaviours[0]`/`examples[2]`. Apply family-wide.

### SF5 — `field`/`tenor`/`mode` is load-bearing vocabulary but defined nowhere reachable
- **where:** `skills/register-style-and-literary-form/SKILL.md` (Procedure step 2); `profile.yaml:73` (quality_bar cites the trio as a pass/fail criterion); `references/translation-equivalence-key-concepts.md` glossary (no entry)
- **severity:** should-fix (agent-skills #1)
- **problem:** Unlike other level-specific jargon (implicature, markedness, T/V) which each get an inline gloss, field/tenor/mode is named but never explained anywhere reachable — yet it's the operative test in both the skill procedure and the quality_bar. An agent self-grading against the quality_bar can't apply the term without outside knowledge.
- **fix:** Add a glossary entry to `translation-equivalence-key-concepts.md` (Register: field = subject matter; tenor = participant relationship/formality; mode = channel) and reference it from the skill's References section.

### SF6 — Invariants worded as imperative production directives, resting entirely on one disclaimer to keep the advisor from acting on them
- **where:** `profile.yaml:9-14` (Role) vs invariants rendered at adapter `:21-34` (P009 "Translate...", P038 "Do not transfer... rework...")
- **severity:** should-fix (ai-agent #2)
- **problem:** The five must-hold invariants read as first-person action directives to a translator producing text, not as review checks. The only guard against a weaker model reading them as its own task is a single Role sentence ("The invariants below are review criteria, not instructions to produce the target text"). One disclaimer carrying the entire anti-overreach load against five imperative bullets is fragile for the highest-priority safety layer. (Enforcement note: the adapter always carries `forbidden_behaviours`, so this is a robustness concern, not a live failure today.)
- **fix:** Reframe each invariant's surface form as self-evidently advisory ("Flag a draft that renders passive-by-passive mechanically instead of by function...") so the posture is legible from the bullet, not solely from the override.

---

## NICE

- **N1 — P015 masculine-as-unmarked stated too broadly.** `principles/principles.yaml` P015 ("the masculine is usually the unmarked term") compresses Baker's "in most languages with a gender category" into an apparent typological universal; doesn't apply to noun-class (Bantu) or genderless (Chinese/Japanese/Turkish) systems. Skill text partially corrects. Add scope qualifier ("in languages with a masculine/feminine gender category"). (descriptive + quality concur)
- **N2 — P009 Chinese adversative passive is dated.** `principles.yaml` P009 ("signalling adversity in Japanese and Chinese"): Japanese *meiwaku-ukemi* holds, but Mandarin 被-passive has broadened well beyond adversative in contemporary registers. Soften ("historically/in formal registers") or keep only the Japanese case. (descriptive)
- **N3 — P033 Gricean gloss loose.** `principles.yaml` P033 ("sincerity, brevity, relevance") is a loose paraphrase not 1:1 with the maxim names (Quantity/Quality/Manner/Relevance) in P032; "brevity" maps to Manner not Quantity. Name each mapping or drop the three-term gloss. (quality)
- **N4 — P033 cross-cultural rhetoric patterns could use an anti-essentializing caveat.** German "digression" / Arabic "repetition-by-assertion" / Japanese "linkless anecdote" are already hedged as culture-relative; add one clause that these are genre/period tendencies, not fixed per-language rules. (technical N1)
- **N5 — Advisor-vs-deliverer boundary present in only 2/9 skill Purpose paragraphs, 0/9 anti-pattern lists.** Enforced package-wide via always-on `forbidden_behaviours`, so not a live risk; for portability to single-SKILL.md consumers, add the one-clause reminder to the other 7 Purpose paragraphs. (agent-skills #4)
- **N6 — Dense multi-instruction Procedure steps.** ~6–8 steps (e.g. `dynamic-and-formal-equivalence` step 6, `grammatical-equivalence` step 7, `pragmatic-equivalence` step 7) pack 2–4 instructions into one 60–90-word sentence; split action vs exception into sub-bullets for scannability. (agent-skills #3)
- **N7 — Profile readability nits.** Role field (`profile.yaml:9-14`) double-negative dense; `inputs.required` (`:36-38`) one run-on bullet; Role names only 2 of 3 modes (omits `compare`); body-size WARNING near-zero headroom (~968/1000w) before a future add-source flips it to FAIL. (profile #4-6, ai-agent #3-4)

---

MUST_FIX_COUNT: 2
