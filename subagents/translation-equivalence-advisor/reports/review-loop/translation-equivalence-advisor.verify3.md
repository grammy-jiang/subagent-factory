# Adversarial verify gate — translation-equivalence-advisor (verify3)

Independent re-check after the review loop reached must-fix=0. Five reviewers spawned in
parallel; findings re-derived, not trusted. This gate adjudicates convergence and downgrades
citation/should-fix noise. **One genuine must-fix survives**, and it was *introduced by the
review loop's own r4 P094 narrowing* — exactly the class an adversarial verify exists to catch.

Reviewer raw verdicts: faithfulness **8**, descriptive **1**, quality **1**, technical **0**,
adapter-safety **0**. Adjudicated real must-fix: **1** (three reviewers converge on the same
P094 root; the faithfulness 8 downgrade to should-fix; see below).

---

## MUST-FIX 1 — P094 over-correction CONTRADICTS its source claim C00360 (introduced by r4 SF1)

**Where:** `principles/principles.yaml` P094 statement; propagated to
`skills/dynamic-and-formal-equivalence/SKILL.md` step 6, `profile.yaml` handoff_rules, and the
exported adapter. Converged on by **descriptive (must-fix)**, **quality (must-fix)**, and
**technical (should-fix — same gap, output walled off downstream)**.

**Current P094 (post-r4):**
> "Use concordant terminology only where it helps readers track important source terms for study
> or interpretation, and relax it for stylistic or literary concordance when consistency produces
> unnatural or meaningless receptor text; **this is stylistic concordance, not subject-matter
> terminology consistency.**"

**Source claims it is derived from (verified in `analysis/claims.jsonl`):**
- **C00360:** "Concordant rendering of source terms is useful in some formal-equivalence
  settings, **especially for key terms in technical or philosophical texts**."
- **C00361:** "Concordant rendering becomes counterproductive when pushed so far that the target
  text becomes relatively meaningless."

**Defect:** The trailing clause "this is stylistic concordance, **not** subject-matter
terminology consistency" **directly contradicts C00360**, which names technical/philosophical
key-term concordance as the *paradigm* useful case. The r4 SF1 fix (meant to narrow P094 to
source scope) over-shot: it re-labelled Nida's terminological/formal-equivalence concordance as
a *stylistic-only* phenomenon the source never characterises that way — a CONTRADICTED-grade
faithfulness fault, worse than the SCOPE_BROADENED it replaced. The skill-step-6 propagation
compounds it: it drops C00361's own naturalness-relax valve ("relax when the target becomes
meaningless") and folds P094 together with the distinct P056 (authorial voice/tone) under one
"stylistic or literary concordance" umbrella — conflating terminological accuracy with style.

**Failure scenario:** A reviewer using this advisor on a technical/scientific/legal/philosophical
draft reads P094 and concludes inconsistent rendering of a recurring key term is "merely
stylistic" and out of scope — precisely the domain C00360 flags as where term-tracking
concordance matters *most*.

**Fix (grounded, no new claim):** Restate P094 as a formal-equivalence device — keep concordance
where readers must track a recurring key term (incl. technical/philosophical texts) for study or
interpretation; relax it where rigid consistency makes the receptor text unnatural or meaningless
(C00361). Encode the "subject-matter glossary governance routes to technical-translation-advisor"
routing as a *scope/ownership* decision, NOT as a redefinition of what concordance is. Re-sync
skill step 6, profile handoff_rules, and re-export the adapter.

---

## Downgraded — should-fix, NOT must-fix

**Faithfulness reviewer's 8 quality_bar SCOPE_BROADENED (quality_bar[0,1,2,3,5,6,7,8]).**
Each terse `quality_bar` bullet cites only 1–2 principle IDs while folding in content the
reviewer maps to *other real corpus principles* (P103/P001, P058/P043, P015/P064/P046/P085,
P002, P007/P020, P022, P076/P077, P010/P062). The parallel fully-cited `always_on` bullets carry
the complete provenance, and the faithfulness-report already grades that cluster a "faithful
digest." So the folded content is **grounded in the corpus, merely under-cited in the digest tag**
— a citation-completeness gap, not a rule stronger than its source support. The flagged
"most-severe" quality_bar[2] (P009 voice stretched to gender/number/tense/modality) is core
Baker obligatory-category material, grounded. No genuine over-claim → should-fix (tighten the
digest citation tags), not a release blocker.

**P100 (quality reviewer should-fix).** Added clause "not by itself a general test of translation
quality" exceeds the single cited C00016 (which is Baker's pedagogical-illustration point, silent
on QA). Content is defensible and the skill hedges it correctly; grounding-provenance gap only →
should-fix (add a QA-scoped anchor or narrow to C00016's scope).

**P094 wording awkwardness (descriptive #2, technical #2).** Self-referential phrasing subsumed
into MUST-FIX 1's reword.

---

## Clean (independently confirmed)

- **Adapter safety (0):** 5 Operating-invariants (P009, P024, P037, P038, P058) complete —
  byte-compared to source statements, no truncation, no "…"/"(e.g"/dangling-clause. Advice-only
  boundary intact (Role + forbidden_behaviours bar producing finished target text; all modes hand
  wording back). Tools = Read/Grep/Glob only, no widening. DO-NOT-EDIT header present.
- **Technical (0):** P094's routing does NOT wrongly tell technical translators to relax genuine
  subject-matter terminology consistency — profile + skill wall it off to the sibling. Grammar,
  collocation, word-level, register skills give no wrong terminology/register/grammar advice.
  P100 correctly hedged.
- Word-level (Baker's 8 strategies), collocation-typicality, two idiom traps, FSP vs Hallidayan
  theme, 5 cohesion types (incl. continuative), Grice-as-culture-relative, dynamic/formal
  equivalence, back-translation critique — all accurately represented; no sibling-package concept
  bleed (Toury/Venuti/skopos); no "reads smoothly = correct" fallacy. Worked examples never hand
  back a finished rendering.

---

MUST_FIX_COUNT: 1
