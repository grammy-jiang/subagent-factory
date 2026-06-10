# Step 6 — Patch Safety Contract

> Master: `docs/subagent_enhancement_build_plan.md` §8 Step 6. Depth: **medium** (outline).
> **Promote to full when:** Step 5 merged, **or** earlier if a subagent that needs patch modes is requested
> (it is fairly independent — reuses `_determine_tools` + self-check #10).

## Goal
A review/advise subagent never silently becomes a code-modifying agent: patch authority is
explicit, bounded, and validated.

## New files (sketch)
- `subagents/<slug>/policy/patch-policy.yaml` — artifact.
- `schemas/patch-policy-v1.schema.json` — schema.
- `tools/subagent_factory/validate_patch_policy.py` — validator.
- `subagents/<slug>/tests/patch-safety-tests.yaml` — tests.

## `patch-policy-v1` (draft)
```yaml
schema_version: patch-policy-v1
default_mode: patch_suggest_only
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
- `export_claude_agent.py` `_determine_tools` — already gates tools by mode (read-only default;
  `produce`/`patch-suggest` → `Edit`,`Write`). Patch policy must be **consistent** with this.
- `profile_self_check.py` **#10** — `may_edit_canonical` already enforced false for specialists.
- `forbidden_behaviours` (profile) — patch refusals live here.

## Validator (at full)
- `default_mode` ∈ {patch_suggest_only, …}; if any mode grants `Edit/Write`, a `patch-policy.yaml` must exist.
- Consistency: tools granted by `_determine_tools` ⊆ what the policy authorizes.
- `may_edit_canonical` respected; canonical-artifact edit paths never in allowed set.

## Research input (light)
Prompt-injection effect-side enforcement / least-privilege (PI F2/F9): authority to cause
effects must be explicit and gated — the same principle applied to patch authority.

## Gate wiring
All tiers **with patch modes** (present-gated on patch-policy when a patch mode exists).
