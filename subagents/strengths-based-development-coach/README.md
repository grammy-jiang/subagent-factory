# strengths-based-development-coach

**Display name:** Strengths-Based Development Coach
**Version:** 0.2.0
**Tier:** 2
**Status:** draft

## Purpose

Expert advisor grounded in Gallup's 40-year strengths research who helps
individuals and managers discover, interpret, and deliberately develop natural
talents into productive strengths using the 34-theme Clifton StrengthsFinder
taxonomy.

## When to invoke

- Interpreting a person's top-five StrengthsFinder 2.0 theme results
- Manager engagement and assignment advice based on a direct report's themes
- Career direction alignment with natural talents
- Team strengths-grid mapping and complementary pairing
- Strengths-zone diagnostic for disengaged or underperforming individuals

## When NOT to invoke

- Clinical psychology or mental health diagnosis
- Formal HR competency assessment or performance-management evaluation
- Ranking individuals against one another on a fixed scale

## Required inputs

1. The individual's top-five StrengthsFinder 2.0 theme names (from the online
   assessment — cannot be supplied by this agent)
2. Current role, goals, or presenting challenge for contextualisation
3. Purpose of the guidance: self-development, manager coaching, or team mapping

## Sources

1. StrengthsFinder 2.0, Tom Rath, Gallup Press, 2007.
   Rights status: distillation-only (c) 2007 The Gallup Organization.

2. Clifton StrengthsFinder, Gallup Press, July 2015 ed. (ISBN 978-1-59562-024-8).
   Rights status: distillation-only (c) The Gallup Organization.

No verbatim quotation permitted from either source. The 34 Clifton StrengthsFinder
theme names are Gallup trademarks referenced here as a taxonomy. The Gallup Q12
engagement items are proprietary and legally protected; only engagement statistics
derived from Q12 research may be cited.

## Package contents

```text
profile.yaml                    Canonical subagent profile
provenance-ledger.md            Full distillation log with field-level traceability
CHANGELOG.md                    Version history
README.md                       This file
tests/golden-tests.yaml         Routing and output tests
```

## Validation

```bash
python -m tools.subagent_factory.validate_generated_package subagents/strengths-based-development-coach
```
