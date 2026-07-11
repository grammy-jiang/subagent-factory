# Changelog — deception-detection-reviewer

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [1.0.3] — 2026-07-11

### Fixed
- Residual-fix phase (`reports/intel-review-loop/RESIDUAL-TRIAGE.md`) + independent post-fix faithfulness verification.
- **H1/H2/H3** — restored the reviewer-only authority boundary; restored P004's `applies_when` condition on `knowledge_partition.always_on[3]`; aligned the governance-approval skill's declared scope.
- **`quality_bar[5]` faithfulness (SCOPE_BROADENED)** — the staged-sabotage clause is P018's content (leaves surviving evidence), not P037 (uncontrollable-exfiltration-channel); citation corrected P037→P018 (matches sibling `always_on[6]`).
- **`handoff_rules[1]` faithfulness (SCOPE_BROADENED)** — P042 (personal integrity) is a topic mismatch for delegation-by-specialism; corrected to P006 (staff distinct roles by specialism), and the handed-off list now explicitly includes the review's own process/approval-routing quality.
- Regenerated `reports/faithfulness-report.yaml` (authoritative, independently re-derived).

## [1.0.2] — 2026-07-11

### Fixed
- Review R2 remediation (`reports/intel-review-loop/subagent-deception-detection-reviewer.r2.review.md`).
- **M1 faithfulness (HEDGING_REMOVED)** — restored P035's qualifiers on the irrevocable-act rule in
  `always_on[5]` ("where it can be avoided") and `quality_bar[4]` ("where they can be"); no longer an
  unconditional prohibition stronger than the source.
- **M2 faithfulness (SCOPE_BROADENED + HEDGING_REMOVED)** — `always_on[2]` restores P063's "consider
  terminating" (was flat "firewall or terminate ... at once"); `source_of_truth_policy.precedence`
  drops the invented evidentiary-override clause and is scoped to P063's linked-asset-collapse trigger.
- **M3 release-policy** — added the missing `provenance-ledger.md` Version History entry for v1.0.1.
- **S1 faithfulness** — restored P051's "usually/ordinarily" hedge on the long-truthful-record rule in
  `quality_bar[1]`, `always_on[1]`, and the worked example.
- **S2 coverage** — added a `quality_bar` bullet exercising the `physical-and-technical-deception-craft`
  skill (P037, P041, P044, P046, P081), previously reachable only via `always_on[7]`.
- **S4 skill routing** — added sibling-boundary clauses ("not X, which <sibling> owns") to the
  `assessing-enemy-trust-and-belief` and `counter-deception-and-the-mirror` descriptions.
- **N1/N2 faithfulness** — restored P053's "when suitable agents are numerous" trigger; reworded
  P056's governance rule to its comparative source form ("more because ... than because its charter").
- **N6/N7** — capitalized the `physical-and-technical-deception-craft` H1 to match siblings; scoped the
  ledger's no-orphan claim to load-bearing rule fields.

## [1.0.1] — 2026-07-11

### Fixed
- Review R1 remediation (`reports/intel-review-loop/subagent-deception-detection-reviewer.r1.review.md`).
- **M1/M2 faithfulness** — removed two fabricated `knowledge_partition.always_on` clauses that wore
  citation lists but had no source: the "champion slow to see undermining evidence" governance clause
  (replaced with P056's grounded "members subordinate their department's interest to the common goal")
  and the "cap certainty short of the endpoints" mirror clause (removed; P070/P045 already carry the
  intent). Restored P059's "in part" hedge on prevention-by-absence (L1).
- **M4 router export** — reworded `role` to drop the "J. C." middle initials ("Masterman's history")
  so the adapter exporter no longer truncates the router description mid-word.
- **M5 orphan field** — `source_of_truth_policy.precedence` now cites its grounding principles
  (P013, P045, P063, P069, P089).
- **M3 faithfulness coverage** — `reports/faithfulness-report.yaml` gains findings for all eight
  `always_on` bullets, `source_of_truth_policy` (owner + precedence), and the three mode triggers —
  the previously unreviewed block where M1/M2/M5 hid.
- **M6 skills** — re-authored all eight `SKILL.md` bodies to gold shape: the flaw taxonomy is now
  enumerated once (in `## Anti-patterns to flag`); `## Output` is a short generic contract plus one
  worked example; `description` frontmatter moved to 3rd-person with a skill-specific trigger (S4/S5).

## [1.0.0] — 2026-07-11

### Added
- Initial release of the **deception-detection-reviewer** subagent (Tier 1).
- `profile.yaml` derived from the 94 promoted principles (P001–P094): role, when/when-not-to-use,
  three modes (review / advise / compare), quality bar, forbidden behaviours, handoff rules, and an
  eight-skill / two-reference `knowledge_partition` covering all principles exactly once.
- Eight authored skills: turning-and-running-a-controlled-agent, building-and-feeding-the-deception,
  network-security-and-compartmentation, assessing-enemy-trust-and-belief,
  governance-approval-and-organization, strategic-stewardship-and-timing,
  physical-and-technical-deception-craft, counter-deception-and-the-mirror.
- Two references: deception-detection-principles-index, deception-detection-evidence-notes.
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded EXACT_SUPPORT or
  WITHIN_SCOPE against its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` (5 golden, 2 negative-routing, 2 missing-context) and
  `tests/principle-behaviour-tests.yaml` (one behaviour test per principle, 94 total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- One distillation-only source: J. C. Masterman, *The Double-Cross System* (1972) — the official
  history of Britain's WWII double-agent operations run by the Twenty (XX) Committee. Spine: 303
  atomic claims, 303 evidence records, 21 chunk anchors.
