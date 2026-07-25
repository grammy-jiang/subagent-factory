# Review-loop r2 — research-integrity-reproducibility-advisor

Single review pass. 4 reviewer lenses (agent-skills, profile, faithfulness, ai-agent-engineering)
over the package + deterministic gates. Findings deduped, most-severe first.

## Deterministic gates — ALL PASS (0 FAIL)

- `validate_generated_package` → **VALIDATION PASSED** (39 OK checks; `phase8` = self-check
  WARNING, not FAIL; `adapter-sync`/`adapter-fresh` OK; `stale-maintenance` all unchanged).
- `quote_scan` → PASS (no verbatim quotation).
- Truncation grep (`…` in skills/adapter; severed invariant `(e.g`) → **no hits**.

No deterministic must-fix.

## LLM findings

### Verified NOT must-fix (profile-reviewer's two "must-fix" downgraded)

Both rest on gate state the deterministic run resolves this pass:

- **modes have no recorded faithfulness grounding** (`profile.yaml` `outputs.modes` 47–61) — profile-reviewer
  called this a Phase-8 fail-fast ("unevidenced modes"). But `validate` ran and PASSED with `phase8` =
  WARNING, so the self-check does not treat this as a blocking FAIL. Real but non-blocking → **should-fix**
  (see #4).
- **profile body-size near 800/1000 boundary** (`profile.yaml`) — flagged "unverifiable, one edit from FAIL".
  `validate` ran this pass and PASSED (body-size FAIL is a hard gate at 1000w; it did not trip). Premise
  disproven → downgraded to **should-fix** documentation gap (see #5).

### should-fix

1. **`quality_bar[0]` universalizes context-tied principles; the anti-absolutism hedge doesn't cover them.**
   where: `profile.yaml` `quality_bar[0]` (63–64) + `source_of_truth_policy.precedence` / `forbidden_behaviours[2]`.
   problem: `quality_bar[0]` states "data prep is scripted, environment/versions captured, project is a
   version-controlled dependency build" citing P022/P023/P032 — but each of those principles is `applies_when`-scoped
   (spreadsheet storage / shared codebase / Make-based analysis), not universal (SCOPE_BROADENED). The document's
   own "adaptable guide, not absolute" guard cites only P002/P005/P030 — the three broadened principles are absent
   from it. The bar item most needing the qualifier is the one not covered. (faithfulness lens; consistent with
   agent-skills #3 boilerplate observation.)
   fix: either add P022/P023/P032 to the `precedence` + `forbidden_behaviours[2]` citation lists, OR reword
   `quality_bar[0]` so each clause carries its trigger ("scripted when it would be manual spreadsheet work;
   environment captured when results depend on specific versions; dependency build when a build tool is in use").

2. **References cited as inline code spans, not Markdown links** (all 7 skills).
   where: `skills/*/SKILL.md` `## References` (e.g. `research-data-management-and-sharing/SKILL.md:70-72`).
   problem: `` See `../../references/...md` `` is a code span, not a relative link. Non-link references are less
   reliably discovered/loaded by a skill-consuming agent (P014).
   fix: convert both citations in every skill to real relative Markdown links.

3. **Charter-wide forbidden restatement pasted verbatim into every skill's `## Output`, blurring lanes.**
   where: `skills/*/SKILL.md` `## Output` 2nd sentence (e.g. `version-control-and-collaboration/SKILL.md:59`).
   problem: every skill repeats "does not run the study, produce the output, make an institutional misconduct
   finding, or give legal advice" regardless of lane — "misconduct finding" is charter boilerplate inside
   version-control / pipelines / RSE / licensing skills, so a reader can't tell this skill's own boundary from
   the advisor-wide one.
   fix: scope each skill's boundary clause to its lane; leave the full forbidden list at profile/adapter level.

4. **Modes not graded in faithfulness report** (downgraded from must-fix).
   where: `reports/faithfulness-report.yaml`; `profile.yaml` `outputs.modes` 47–61; `provenance-ledger.md` faithfulness section.
   problem: ledger's 27 graded findings never cover the 3 mode trigger/output pairs; only shared `primary_format`
   was graded. Not gate-blocking (validate PASSED) but a traceability gap.
   fix: grade each mode's trigger+output against its principle(s), OR record in the ledger that modes are pure
   output-shape derivations of `primary_format` and exempt by convention; re-issue faithfulness PASS to cover modes.

5. **No Phase-8 self-check subsection in the ledger; body-size / test-count / synthesis-deferral undocumented.**
   where: `provenance-ledger.md`.
   problem: ledger records Phase-7 faithfulness + version history but not the Phase-8 run (word count + verdict),
   the golden-test count / negative-routing confirmation, or the `multisource_synthesis: deferred` rationale.
   Release-readiness shouldn't depend on facts the ledger omits (all currently pass, but silently).
   fix: add a "Phase 8 Self-Check" subsection recording word count + verdict, golden-test count (≥3) + ≥1
   negative-routing test, and a one-line deferral rationale for `multisource_synthesis`.

6. **Adapter frontmatter `description` truncated mid-clause both halves.**
   where: `.claude/agents/generated/research-integrity-reproducibility-advisor.md` line 3.
   problem: "...wants a reproducibility" and "...the study run, the data analysed" both cut before a complete
   phrase. This field drives parent-agent routing; a broken summary risks under-triggering. (Cosmetic vs. body,
   which is correct — not a safety/scope issue.)
   fix: regenerate with clause-aware truncation ending on a complete phrase, or hand-tune one full "use when" +
   one full "not for" example.

7. **`when_to_use` at hard ceiling (6 of 3–6).**
   where: `profile.yaml` `when_to_use` 18–29.
   problem: any future source fold-in that adds a trigger breaches the Phase-8 check-2 ceiling → FAIL.
   fix: consolidate two related triggers now for headroom, or flag "at capacity" in the ledger.

### nice

8. **`precedence` P008 citation is a weak match.** where: `profile.yaml` `source_of_truth_policy.precedence`.
   P006 grounds "infer misconduct intent from a disputed act alone"; P008 (data claims not exceeding observations)
   grounds neither clause of the meta-rule it's attached to. fix: drop P008, or split the sentence so each clause
   carries only its grounding principle.

9. **3 of 7 skill descriptions lead with a bare noun list, not "Use when …"** (inconsistent trigger phrasing).
   where: `research-data-management-and-sharing`, `research-software-engineering-and-testing`,
   `authorship-publication-and-attribution` frontmatter. fix: rewrite the 3 outliers to lead with "Use when …".

10. **Complementary skills lack cross-references** (misconduct↔authorship on plagiarism; data-mgmt↔licensing on
    data licences). fix: add a one-clause "see companion skill" pointer in each. — nice.

11. **`when_not_to_use` "pure domain-science / generic SWE" has no handoff target.** where: `profile.yaml`
    `handoff_rules`. fix: add a third handoff line redirecting no-integrity/no-reproducibility requests to a
    general/domain assistant. — nice.

12. **Two-domain persona (RCR ethics + reproducibility/SWE) is a scalability watch-item.** Coherent today
    (single source spans both, skills separate cleanly); note for future re-authoring if either half is deepened
    — no action now. — nice.

13. **Cosmetic:** title-case "And" in skill headings; `gaoxiao-xueshu-guifa` `year: null` (already documented,
    no action). — nice.

MUST_FIX_COUNT: 0
