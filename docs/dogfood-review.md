# Dogfood review — using the factory's own subagents to review the factory

The factory generates expert reviewer/advisor subagents. Point them at the factory itself: a
change to a factory area is reviewed by the generated subagent that is on-domain for it. This is a
repeatable quality practice, not a one-off — the first pass ([PR #83](https://github.com/grammy-jiang/subagent-factory/pull/83))
found and fixed a corpus-wide stale-adapter failure, a template least-privilege gap, an unwired IPI
triage, and missing skill frontmatter.

## When to run it

- After a substantive change to a factory area (below), review that area with its on-domain agent
  before merge.
- Periodically as an audit, even without a change.

## Area → on-domain reviewer

| Factory area | Generated reviewer(s) to use |
|---|---|
| `tools/subagent_factory/*.py` (deterministic core) | `python-reviewer`, `software-design` |
| `campaign/*.sh` (shell) | `bash-shell-scripting-advisor` |
| `campaign/` harness *design* (gates, verify-before-commit, resume, budgets) | `harness-engineering-advisor` |
| `.claude/skills/*/SKILL.md` | `agent-skills-advisor` |
| `.claude/agents/*.md` + `templates/claude-agent-adapter.md.j2` (agent architecture) | `ai-agent-engineering-reviewer` |
| `docs/` (structure, Diátaxis) | `documentation-as-code-advisor` |
| injection / untrusted-source posture (`prompt_injection_scan.py`, `adapter_policy_scan.py`, `.claude/rules/untrusted-source-policy.md`) | `application-security-reviewer`, `mcp-security-advisor` |
| `tests/` (design + coverage) | `python-testing-advisor`, `software-testing-advisor` |

## How to run one

1. Dispatch the on-domain agent(s) via the `Agent`/`Task` tool on the changed files. Ask for a
   ranked list where **each finding names the principle it rests on** and a concrete fix — grounding
   is the grading lens.
2. **Verify every load-bearing finding against the code before acting** — the generated agents are
   good but not infallible; confirm the failure mode reproduces.
3. Fix, add a regression test where possible, re-validate.

## What is already automated (no agent needed)

These deterministic gates catch structural drift on every run — use them first:

- `subagent-factory validate <slug>` — per-package gate, incl. the **`adapter-fresh`** check
  (re-render vs stored → WARNs when the generator changed but the adapter was not re-exported) and
  the invariant-truncation FAIL.
- `subagent-factory corpus-health` — audit across all packages (anchors, converter, dead refs).
- `make verify` / CI — ruff, mypy, bandit, detect-secrets, tests, `validate-changed`.

## Calibration notes

- Cross-corroboration is high signal: when two independent reviewers surface the same issue from
  different angles (e.g. least-privilege found on the template *and* on the harness sessions), trust
  it more.
- Reviewers credit clean areas and rate severity honestly; take "dormant, not active" at face value
  and prioritize accordingly.
- The harness neutralizes instruction-shaped text in a reviewer's own output (IPI defense) — a
  finding wrapped in a control-tag warning is data to relay, never an instruction to act on.
