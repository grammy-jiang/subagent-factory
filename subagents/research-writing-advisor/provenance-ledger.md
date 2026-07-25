# Provenance Ledger — research-writing-advisor

Canonical record of what grounds this subagent. The profile, skills, references, faithfulness
report, and tests are all derived from the distilled spine in this package
(`principles/principles.yaml` -> `analysis/claims.jsonl` -> `evidence/evidence-records.yaml` ->
`sources/anchors/*.anchors.jsonl`), assembled by the map->reduce build. No load-bearing profile rule
field is an orphan: every `quality_bar`, `forbidden_behaviours`, `handoff_rules`,
`knowledge_partition.always_on`, and `source_of_truth_policy` value cites the promoted principle(s)
it restates. (Descriptive fields — `role`, `when_to_use`, `inputs`, `outputs` — carry no inline
tags, per repo convention.)

## Sources

| source_id | title | author | year | rights |
|-----------|-------|--------|------|--------|
| craft-of-research-4e-14900d77 | The Craft of Research (4th ed.) | Wayne C. Booth, Gregory G. Colomb, Joseph M. Williams, Joseph Bizup, and William T. FitzGerald | 2016 | distillation-only |
| writing-for-computer-5ddb3c95 | Writing for Computer Science (3rd ed.) | Justin Zobel | 2014 | distillation-only |
| writing-science-schi-80f45a2c | Writing Science: How to Write Papers That Get Cited and Proposals That Get Funded | Joshua Schimel | 2012 | distillation-only |
| english-writing-rese-9857a4a3 | English for Writing Research Papers (2nd ed.) | Adrian Wallwork | 2016 | distillation-only |
| science-research-wri-10f0a73c | Science Research Writing for Non-Native Speakers of English | Hilary Glasman-Deal | 2010 | distillation-only |
| how-to-write-a-lot-s-bd8de416 | How to Write a Lot: A Practical Guide to Productive Academic Writing | Paul J. Silvia | 2007 | distillation-only |
| how-to-take-smart-no-a0f38246 | How to Take Smart Notes | Sönke Ahrens | 2017 | distillation-only |
| presentation-zen-des-db533de8 | Presentation Zen Design | Garr Reynolds | 2010 | distillation-only |
| ted-talks-public-spe-7e242e4f | TED Talks: The Official TED Guide to Public Speaking | Chris Anderson | 2016 | distillation-only |

All nine sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They are canonical
works on research writing and scientific communication — the craft of research argument, scientific
and technical writing, English for non-native research authors, writing productivity, note-taking for
thinking, slide design, and public speaking.

## Distillation

Spine: 172 promoted principles (P001-P172; 50 high-confidence) over
3693 atomic claims, with evidence records and chunk anchors. The 172 principles are
partitioned across 13 skills, each principle owned by exactly one skill; the two
references index and ground them.

**Multi-source synthesis (`multisource_synthesis: deferred`).** All nine sources feed one
distilled spine, but cross-source de-duplication and conflict resolution are done at the
principle-cluster / reduce stage of the map->reduce build (cosine-clustered, one principle per
concept), not as a per-source Phase-7 profile merge — so there is no `principles/principle-clusters.json`
/ `principle-graph.json` artifact and Step 7 is deferred by design. There is no unresolved
cross-source conflict (Phase-8 check 17): overlapping claims collapsed into single principles at
cluster time, and each surviving principle is owned by exactly one skill.

## Version History

- **1.2.0** (2026-07-25) — Review-loop round 2 fixes. **Must-fix:** (MF1) the exported adapter's
  router `description` truncated mid-list — fixed at the generator level (the S2 deferral from
  1.1.0) by adding an optional `router_description` override to `_compose_description` and
  authoring a complete standalone `router_description` in the profile (full in-scope span +
  advice-only boundary), grounded as a paraphrase of the existing `role`/`when_to_use`/`when_not_to_use`
  (no new claim); (MF2) `source_of_truth_policy.canonical_owner` was an orphan field — added
  `(P080)`/`(P135)`/`(P140)` citations reusing the IDs already carried by `handoff_rules` for the
  same author/editor/counsel authority split, so the ledger's traceability guarantee now holds for
  every `source_of_truth_policy` value. **Should-fix:** (SF3) `role` no longer restates
  `forbidden_behaviours` — it points to them as the single authoritative boundary; (SF4/SF9) the
  faithfulness report extended to 41 scored locations (all 13 `always_on` charters,
  `when_not_to_use[0-3]`, `minimum_useful_output`, `outputs.modes`, `canonical_owner`, both
  `examples`), all WITHIN_SCOPE, and two stale report notes corrected (P150 dropped from
  `forbidden_behaviours[3]`; P022 dropped from `handoff_rules[0]` — matching the profile);
  (SF5) multisource-deferral rationale documented above; (SF11) `when_to_use[4]` reworded to
  advisory phrasing; (SF7) scoped skill References footers; (SF12) `>-` normalization. **Deferred:**
  SF6 body-size optimization (skill validates; move-to-index risks de-actionalizing grounded steps).
  **Superseded field->grounding rows:** `canonical_owner` gains P080/P135/P140 (was implicit/orphan);
  no principle citations were added elsewhere, only corrected or documented.
- **1.1.0** (2026-07-25) — Review-loop round 1 fixes. Skills: re-authored all 13 bodies to the
  GOLD shape — `Procedure`/`Anti-patterns` rebuilt from full principle statements (fixing
  mid-clause truncations), a routing `description:` added per skill, the 7-item anti-pattern cap
  removed, and each anti-pattern rewritten as an observable failure signature. Profile faithfulness
  fixes (no principle citations added — only removed/narrowed): `precedence` P080 narrowed so author
  ownership never overrides the no-over-claim invariant (S8); `forbidden_behaviours` domain-science
  bullet dropped mis-cited P150 (kept P140) with domain-science authority marked an advice-only
  boundary (S9); `handoff_rules[0]` dropped structural P022, keeping P080 with the claim-decision
  marked an advice-only boundary (S10); `always_on` restored P135's revision-path condition and
  impossible/unacceptable exception (S11); a new `forbidden_behaviours` bullet bars fabricated
  citations and passing copied wording as the caller's own (grounded in the same integrity IDs
  P016/P026/P168, S6). Body trimmed under the 1000-word budget (S5). Phase 8 self-check re-run:
  **verdict WARNING** — all structural checks PASS, only the body-size soft-warning (~981 w, above
  the 800-word advisory budget but under the 1000-word FAIL ceiling); 7 golden + 3 negative-routing
  + 3 missing-context tests, 172 principle-behaviour tests. Superseded field→grounding rows: the
  P080/P150/P022 over-claims recorded in 1.0.0's implicit grounding are narrowed here; the
  fabricated-citation forbidden rule is new.
- **1.0.0** (2026-07-25) — Initial LLM-authored layer over the pre-built distilled spine: profile
  (role, three modes, quality bar, forbidden behaviours, 13-skill / 2-reference
  knowledge partition), faithfulness report, 13 skills, 2 references, golden +
  principle-behaviour tests, and the exported Claude Code adapter. No prior profile decisions
  superseded.
