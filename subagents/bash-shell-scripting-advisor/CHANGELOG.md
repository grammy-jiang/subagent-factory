# Changelog — bash-shell-scripting-advisor

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml` (semver).

## [1.0.2] — 2026-07-25

### Added
- `router_description` in `profile.yaml`: the adapter frontmatter `description` is the string the
  runtime routes on, and without this field the exporter composes it from the role plus only the
  first two `when_to_use` triggers and the first `when_not_to_use` exclusion — silently dropping the
  remaining domains. The authored description names the full remit and boundary. Adapter
  re-exported; no principle, rule, or skill changed.

## [1.0.1] — 2026-07-10

### Fixed
- Completed the LLM-authored layer so the package validates (0 failures). The 1.0.0 layer was
  incomplete: the ten skill bodies were stubs missing their `## Procedure` section, and
  `reports/faithfulness-report.yaml` and the exported adapter were absent.
  - Added a grounded `## Procedure` (the repeatable review/advise steps, each citing the skill's own
    principle IDs) to every skill in `skills/`.
  - Added `reports/faithfulness-report.yaml` — 21 per-rule claim-strength findings over the profile's
    role, `when_to_use`/`when_not_to_use`, `quality_bar`, `forbidden_behaviours`, and output modes;
    all verdicts EXACT_SUPPORT/WITHIN_SCOPE (the profile narrows the sources to review/advice), no
    rule stronger than its evidence, provenance carried in each note via principle + claim IDs.
  - Exported `adapters/claude-code/bash-shell-scripting-advisor.md` and installed the runtime adapter.
- No change to the deterministic map→reduce spine (claims, principles, evidence, anchors, sources).

## [1.0.0] — 2026-07-10

### Added
- Initial release. LLM-authored layer built over the deterministic map→reduce spine:
  - `profile.yaml` (portable-profile-v1) — role, scope, modes, quality bar, forbidden behaviours,
    source-of-truth policy, and a ten-skill knowledge partition, every rule grounded in promoted
    principle IDs.
  - `reports/faithfulness-report.yaml` — per-rule claim-strength check; no rule stronger than its
    evidence.
  - `skills/` — ten skill bodies grounding the 150 promoted principles by theme.
  - `references/` — principles index and evidence notes.
  - `tests/golden-tests.yaml` + `tests/principle-behaviour-tests.yaml` — routing goldens plus one
    behaviour test per principle (every high-confidence principle covered).
  - `adapters/claude-code/bash-shell-scripting-advisor.md` — exported Claude Code adapter.

### Distilled spine (unchanged, deterministically built)
- 150 principles, 3,614 claims, 1,789 evidence records, 142 chunk anchors across 11 sources
  (GNU Bash manual, POSIX shell, BashGuide, Bash Pitfalls, Google Shell Style Guide, pure-bash-bible,
  OWASP command-injection attack + defence, Effective Shell, Linux Pocket Guide, The Linux Command
  Line).
