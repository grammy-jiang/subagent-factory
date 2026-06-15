# Step 6 — Patch Safety Contract

> Master: `docs/subagent_enhancement_build_plan.md` §8 Step 6. Depth: **full**
> (promoted from medium). The last active step; Step 7 stays deferred.

## Goal
A review/advise subagent never silently becomes a code-modifying agent: patch authority is
explicit, bounded, and validated. When a profile grants a patch/produce mode, it must carry a
patch-safety policy.

## New files
| Path | Kind | Responsibility |
|------|------|----------------|
| `subagents/<slug>/policy/patch-policy.yaml` | artifact | The patch contract. |
| `schemas/patch-policy-v1.schema.json` | schema | Policy shape + enums. |
| `tools/subagent_factory/validate_patch_policy.py` | tool (validator) | Schema + self-consistency. |
| `tests/subagent_factory/test_validate_patch_policy.py` | fixtures | Validator + gate tests. |
| `subagents/<slug>/tests/patch-safety-tests.yaml` | artifact | Patch-safety tests (schema-exempt; coverage via Step 5). |

## `patch-policy-v1` schema
```yaml
schema_version: patch-policy-v1
default_mode: patch_suggest_only        # patch_suggest_only | direct_patch | read_only
direct_patch_allowed_when:
  - user_explicitly_requests_patch
  - target_files_are_supplied
  - validation_command_exists
  - patch_scope_is_bounded
must_not:
  - silently_edit_canonical_artifacts
  - rewrite_architecture_without_approval
  - patch_without_risk_explanation
  - patch_on_weak_evidence
```

## Reuse
- `export_claude_agent._determine_tools` — already gates tools by mode (read-only default;
  `produce`/`patch-suggest` → `Edit`,`Write`). The policy must be consistent with this.
- `profile_self_check` **#10** — `may_edit_canonical` already enforced false for specialists.
- `forbidden_behaviours` (profile) — patch refusals live there too.

## Gate wiring — a direct, **mode-conditional** block (not the tier registry)
In `validate_generated_package` (after the adapter-policy scan):
```text
has_patch_mode = any mode in {produce, patch-suggest}
if policy/patch-policy.yaml present:     validate it (any tier)
elif has_patch_mode:                     FAIL — patch mode but no policy
else:                                    OK (read-only role; no policy needed)
```
Requiredness is keyed on *profile modes*, not tier — hence a direct block rather than the
tier-gated registry.

## `validate_patch_policy.py` (schema + self-consistency)
- schema-valid; `default_mode` ∈ enum; `direct_patch_allowed_when` and `must_not` non-empty.
- when `default_mode: direct_patch`, `direct_patch_allowed_when` must include
  `user_explicitly_requests_patch` (no unconditional direct patching).

## LLM ↔ deterministic split
- Deterministic: `validate_patch_policy.py` + the mode-conditional gate block.
- LLM: `profile-deriver` authors `patch-policy.yaml` when it assigns a patch mode (no new skill).

## Fixtures
- valid `patch_suggest_only` policy → `[]`.
- bad `default_mode` enum → schema error.
- `default_mode: direct_patch` without `user_explicitly_requests_patch` → error.
- profile with a `produce` mode + missing `patch-policy.yaml` → gate FAIL (tested via the gate).
- read-only profile + no policy → no FAIL.

## Exit criteria + verify
1. `validate_patch_policy` passes a good policy; fails enum/consistency violations.
2. Gate FAILs a patch-mode profile lacking a policy; passes read-only profiles unchanged.
3. `make verify` green; **0/15 packages regressed** (all 15 are read-only review roles).

## Caveats
- The policy is a contract, not an enforcement runtime; the adapter-policy scan (Step 1) +
  `_determine_tools` are what actually bound tool authority. This step makes the contract
  explicit and required wherever patch authority is granted.

## Patch generation + validation (automated-program-repair research, I-track — SPEC)

> Folds `docs/Research/automated-program-repair/` (§20 #13, **41 papers, 3 rounds, validation PASS
> 1.0, reviewer-accepted**). (The Copilot run hit the hourly rate limit *after* completing + validating
> — an earlier "provisional/unvalidated" note was based on a stale `round_state.json`; the SUMMARY
> confirms it validated.) Step 6 enforces patch *safety* (mode-gated policy); this adds the
> *generation + validation* method for the produce/patch-suggest modes + the patch-capable subagents
> (incl. the new `legacy-code-change-advisor`).

**Spec (design only — what a patch-capable subagent should do; no code yet):**
1. **Deterministic validation ladder, in order:** compile/parse → scope/locality → reproduction
   (fail→pass) → full regression (pass→pass) → CI. [2605.27238], [2604.27148]
2. **Reference-free oracle rungs after tests pass:** intent oracle from the issue/PR text, behavioral
   fingerprint diff, and (for small in-scope changes) a *sound* symbolic-equivalence / patch-impact
   check. [2602.05270], [2604.16933], [2605.13885]
3. **Never let an LLM/learned judge override a deterministic verdict** — LLM only *ranks*
   deterministically-passing candidates + raises an abstain / "needs human" flag; judge scoped diffs.
   [2603.11262], [2604.18309]
4. **Generate + protect a RED (bug-reproduction) test** — anchor localization on it, forbid deletion,
   apply a reachability filter, flag fix↔test mutual overfitting for review. [2601.19066], [2604.19224]
5. **Bound the diff by construction** — minimal-edit generation, function/element scope, cheap locality
   rejection of over-edits even when tests pass. [2604.03113]
6. **Ground generation in execution evidence**; filter LLM artifacts deterministically. [2512.24635]
7. **Scale validation depth to risk (mode-gated)** — human review for high-blast-radius / security /
   weak-oracle changes; for vulnerabilities verify root-cause, not symptom. [2604.25363], [2605.04251]
8. **Discount benchmark numbers** (memorization, weak oracles); add mutation-guided adequacy checks.
   [2604.21579], [2602.10471]

The load-bearing principle matches the factory's: **deterministic gate decides, LLM only proposes +
ranks.** ENGINEERING-HIGH = a `validate_patch` ladder for the produce/patch-suggest modes. Open
academic gaps carried from the report (re-confirm on re-validation).
