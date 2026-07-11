# Review Loop — translation-equivalence-advisor (r1)

Consolidated review pass. 3 deterministic gates + 7 reviewer lenses (agent-skills, profile,
faithfulness, ai-agent-engineering + 3 domain: descriptive-translation, translation-quality,
technical-translation). Findings deduped, most-severe first.

## Deterministic gates

| Gate | Result |
|------|--------|
| `validate_generated_package` | **FAIL** — 1 failure (adapter invariant truncation) |
| `quote_scan` | PASS |
| ellipsis truncation grep | HIT (adapter lines 32, 34 — same root cause as FAIL) |
| adapter invariant unbalanced-paren grep | clean |

---

## MUST-FIX

### M1 — Adapter invariant layer truncates rule content (P038, P058)  [DETERMINISTIC FAIL]
- **Where:** `.claude/agents/generated/translation-equivalence-advisor.md` lines 32, 34 (mirrored in `principles/principles.yaml` compiled-invariant layer); `validate_generated_package` tier-artifact FAIL.
- **Problem:** Two "Operating invariants (must hold)" lines are silently severed with a trailing `…`:
  - P038 ends `…because each language's…`
  - P058 ends `…because a collocation's meaning…`
  The compiled invariant dropped its tail — a must-hold rule is presented truncated, losing its rationale. Same class as the `compile_invariants` adapter-truncation bug found on the `technical-translation-advisor` review.
- **Fix:** Fix `compile_invariants` so must-hold invariants are emitted whole (do not hard-truncate mid-clause); re-export adapter; re-run `validate_generated_package` to green.

### M2 — quality_bar[6] over-claims dynamic equivalence as an absolute exclusion of formal closeness
- **Where:** `profile.yaml` `quality_bar[6]` (~lines 72-73). Faithfulness lens.
- **Problem:** Clause "adequacy is judged by receptor response, **not** formal closeness (P021, P034, P022, P035)" is a flat universal negation stronger than every cited principle. P022 (co-cited) explicitly endorses **formal**-equivalence/gloss when readers need close access to source form; P035 gives four adequacy criteria (sense, spirit/manner, natural expression, similar response) — not a single "receptor response" test, and never excludes formal closeness. SCOPE_BROADENED / near-CONTRADICTED. The correct, fuller phrasing already exists in this same profile at `always_on[6]`. Existing faithfulness-report verdict (WITHIN_SCOPE) is wrong on this point.
- **Fix:** Replace with the brief-conditioned wording from `always_on[6]` — adequacy judged by the brief's own criterion (sense/spirit/natural expression for receptor-response tasks; closeness to source form/terminology/structure when readers need that access). Update faithfulness-report entry.

---

## SHOULD-FIX

### S1 — Adapter routing `description` truncated mid-clause (no ellipsis)
- **Where:** `.claude/agents/generated/translation-equivalence-advisor.md` line 3 `description:`. Agent-engineering lens.
- **Problem:** Ends `…word-level, grammatical, cohesive — Not for:` — drops "or pragmatic non-equivalence and wants which strategy fits the context and purpose," and never signals the `compare` mode or register/whole-text/pragmatic scope. Router sees this first → under-routing for pragmatic/register/whole-text/compare requests that are in scope. Same adapter-gen truncation family as M1 but a distinct compiler path (description compiler, not invariant compiler).
- **Fix:** Regenerate description with a length budget that ends on a complete clause and samples across all three modes' triggers (advise/review/compare). If shared compiler bug, fix in `tools/subagent_factory/` repo-wide, not one-off.

### S2 — Profile body size 984w — 16w from the 1000w hard-FAIL line (Phase 8 WARNING)
- **Where:** `profile.yaml` `quality_bar` (277w, 9 bullets), `forbidden_behaviours` (106w), `modes` (104w). Profile lens.
- **Problem:** Phase 8 check-14 WARNING is real; any future fold-in pushes it to hard-FAIL. Several quality_bar bullets restate the same "judged by function, not form" framing across levels.
- **Fix:** Compress the shared "function-not-form" clause once; lead each bullet with only distinguishing content. Reclaims 100+ words of headroom.

### S3 — Back-translation framed only negatively; omits its mandated QA role
- **Where:** `principles.yaml` P100; `skills/dynamic-and-formal-equivalence/SKILL.md` step 7. Technical-translation lens.
- **Problem:** Framed as "theoretically unsound compromise... only to expose structure." Omits back-translation's established (if limited) QA/validation role in high-stakes domains (ISPOR/FDA linguistic validation of PROs, clinical-trial/pharma, WHO instrument protocols). Inconsistent with sibling `technical-translation-advisor` P035 ("a limited quality check"). Could steer a caller away from a QA step their industry requires.
- **Fix:** Soften P100 + skill step to acknowledge back-translation as a recognized limited checking/validation device in specific high-stakes domains, alongside its structural-illustration use.

### S4 — Nida source title is inaccurate / possibly a derived extract cited as primary
- **Where:** `profile.yaml` `sources[1]` (~lines 208-213). Technical-translation lens.
- **Problem:** Cited title "Toward a Science of Translating: dynamic and formal equivalence" is not Nida's real subtitle (actual: *…With Special Reference to Principles and Procedures Involved in Bible Translating*, 1964). Ingested markdown is ~10.4k words — far shorter than the monograph — suggesting a secondary extract/summary cited as if it carried the book's own subtitle.
- **Fix:** Correct `sources[].title`; if the ingested doc is a summary/extract, mark that honestly (authority/notes) so a reader can locate the primary source.

### S5 — Equivalent-effect / receptor-response presented as a checkable criterion
- **Where:** `principles.yaml` P034-P036; `skills/dynamic-and-formal-equivalence` (procedure step 8, Output, Anti-patterns). Descriptive-translation lens.
- **Problem:** "Similar audience response" treated as a verifiable test, but the ST audience's historical response is unmeasurable (van den Broeck 1978 and later) — it's an interpretive judgment, not an empirical outcome.
- **Fix:** Note that equivalent-effect is an informed approximation the translator argues for; instruct the reviewer to ask for the translator's *reasoning* about audience response, not treat "matches audience response" as itself verifiable.

### S6 — Adversative-passive rule overstated for contemporary Mandarin
- **Where:** `principles.yaml` P009; `skills/grammatical-equivalence` step 2; `quality_bar[2]`. Translation-quality lens.
- **Problem:** Faithful to Baker's 1992 generalization but as an unqualified rule overstates Mandarin: 被 (bèi)'s unfavorable-event bias has weakened markedly since the 1990s and is now routine in neutral/positive contexts. Reliable for Japanese (迷惑受身), register/era-sensitive for Mandarin.
- **Fix:** Qualify P009 + skill step: strongest for Japanese; a register/era-sensitive tendency for contemporary Mandarin — check text type/register before inferring adversity.

### S7 — "dynamic equivalence" terminology lacks Nida's own later revision
- **Where:** `principles.yaml` P034; `skills/dynamic-and-formal-equivalence` purpose / key-concepts reference. Descriptive-translation lens.
- **Problem:** Nida & de Waard (1986) replaced "dynamic equivalence" with "functional equivalence" precisely because "dynamic" was misread as "free/impactful." Skill inherits the 1964 term without this note.
- **Fix:** Add a short note that Nida later preferred "functional equivalence" for the same concept, to prevent conflating "dynamic" with "free/loose."

### S8 — Text-level "umbrella" skill triggers overlap all sibling skills
- **Where:** `skills/text-level-approach-and-limits-of-equivalence/SKILL.md` "When to use" (~lines 65-70). Agent-skills lens.
- **Problem:** Bullets ("A translation decision must be made or justified", "A translation is being critiqued overall") match essentially every invocation of the other 8 skills → weak lens-fit, risk of loading instead of the specific level-skill.
- **Fix:** Tighten to this skill's distinct trigger — caller asks whether a translation is "right/literal enough/faithful" overall without naming one level; or level-skill findings must be weighed against the whole-text standard.

### S9 — source_of_truth_policy.precedence converts graded weighting into a binary gate
- **Where:** `profile.yaml` `source_of_truth_policy.precedence` (~lines 104-107). Faithfulness lens.
- **Problem:** "preserve it **only where** it carries genre, emotional, or aesthetic effect (P005, P021)" — P005 is graded ("preserving form **more strongly** when…"). HEDGING_REMOVED: implies zero form-preservation absent an explicit label.
- **Fix:** Reword to graded: "weight form by its communicative function, preserving it more strongly where it carries genre, emotional, or aesthetic effect."

---

## NICE

- **N1** — Add per-skill `## Example` (before/after: diagnosed non-equivalence → strategy → finding) to higher-branching skills (word-level, collocation-idiom, dynamic-formal); 7 of 9 skills currently have zero example coverage. *(agent-skills)*
- **N2** — `when_not_to_use[2]` duplicates `forbidden_behaviours[1]` (relative-equivalence rule) in near-identical wording; collapse one to a pointer. *(profile)*
- **N3** — `forbidden_behaviours[0]` (no finished target text) carries no in-profile citation; add a parenthetical "(advisory-scope boundary, not a source claim)" so a future maintainer doesn't read it as ungrounded. *(profile)*
- **N4** — `review` mode output "highest-impact first" bounds the list implicitly; make explicit ("representative and impact-ranked, not an exhaustive segment-by-segment rewrite") to close the finished-translation loophole. *(agent-engineering)*
- **N5** — `handoff_rules[1]` cites P094 (a terminology *technique*) to ground an ownership/delegation claim it doesn't support; drop or re-scope the citation. *(faithfulness)*
- **N6** — Contrastive-rhetoric claims P033 (German digression / Arabic repetition / Japanese linkless) stated as fixed national norms; hedge as genre/text-type tendencies (essentialism critique — Kubota, Zamel). *(descriptive-translation)*
- **N7** — Gricean maxim labeled "Relevance" (Grice's is "Relation"); add "(Grice's maxim of Relation)" once to avoid conflation with Sperber & Wilson Relevance Theory. *(descriptive-translation)*
- **N8** — Gender: P015 masculine-as-unmarked framed as default; add prompt to check the brief's inclusive-language policy up front (EU/UN/corporate/legal norms). *(translation-quality, technical-translation)*
- **N9** — P009 "objectivity in scientific English" (passive) is dated; modern style guides favor active voice — reframe as "was long associated with," keep the function-not-form point. *(descriptive-translation)*
- **N10** — Nida's F-E/D-E framework originated in Bible translation; add one line so callers calibrate audience-decoding-rate/expansion advice against their actual text type. *(descriptive-translation)*
- **N11** — Scope currency: no Skopos/functionalist theory (Reiss & Vermeer, Nord), Vinay & Darbelnet procedures, or error-based TQA (MQM/DQF). Legitimate given disclosed 2-source scope; confirm sibling-family coverage, else consider future fold-in. *(translation-quality, technical-translation)*
- **N12** — Some procedure steps carry 3+ principle citations covering distinct sub-instructions; split for scannability. Identical boilerplate References block per skill — optionally point to the specific index section. *(agent-skills)*
- **N13** — `inputs.required` crams source text + draft/decision + brief into one list entry; split into discrete entries. *(profile)*

---

MUST_FIX_COUNT: 2
