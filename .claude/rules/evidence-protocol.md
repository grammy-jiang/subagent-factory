# Evidence Protocol

Default policy for what evidence a source must carry before it drives subagent behaviour.
This is the **global default**; a package may override it with a per-package
`evidence-protocol.yaml` only when its domain genuinely differs.

## Research question

> What expert behaviour should this subagent learn, and is each learned rule grounded in the
> source rather than invented or exaggerated?

## Inclusion criteria

- Authoritative source for the domain.
- Actionable, reusable principle (not motivational background).
- Evidence or strong reasoning available in the source.

## Exclusion criteria

- Motivational/historical background with no operational value.
- Unsupported opinion or weak secondary claim.
- Source with unclear or missing `rights_status` (blocks distillation until resolved — see
  `.claude/rules/rights-and-quotation-policy.md`).

## Confidence scale

| Level | Meaning |
|-------|---------|
| high | official, peer-reviewed, replicated, or classic domain source |
| medium | expert book, well-argued technical essay, strong case study |
| low | anecdotal, unsupported claim, weak secondary source |

## Faithfulness rule

No generated rule may be **stronger than its source support**. "In this context, prefer X"
must not become "always X". The `faithfulness-review` skill checks every profile rule against
the source on a five-level claim-strength scale
(`EXACT_SUPPORT → WITHIN_SCOPE → SCOPE_BROADENED → HEDGING_REMOVED → CONTRADICTED`) and writes
`reports/faithfulness-report.yaml`.
