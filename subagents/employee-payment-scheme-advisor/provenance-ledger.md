# Provenance Ledger — Employee Payment Scheme Participation Advisor

**Subagent slug:** `employee-payment-scheme-advisor`
**Profile version:** 0.3.0
**Updated:** 2026-06-12T12:00:00+00:00

## Source Registry

| ID | Title | Author | Year | Authority | Rights | Volatility | Review cadence |
|----|-------|--------|------|-----------|--------|------------|----------------|
| payment-systems-and-20260612115310 | Payment Systems and Performance Improvement: Participation in Payment System Design | Bowey, Angela; Thorpe, Richard | 1989 | secondary | distillation-only | low | annual |

Source is a four-page article in *Employee Relations*, Vol. 11 Iss. 1, pp. 17–20
(Emerald, DOI 10.1108/EUM0000000001014). Rights status `distillation-only`: copyrighted
journal content accessed under subscription; no verbatim quotation in any generated
artifact.

**Conversion note (0.3.0):** Re-converted with Docling (CPU-only) on 2026-06-12. The
Docling conversion produced 19 real heading anchors (h0000–h0018) compared with 0 from
the prior MarkItDown conversion. All provenance in this version points to the new
source_id `payment-systems-and-20260612115310`. The old source_id
`payment-systems-and-20260608231654` is retired; it referred to the same PDF with an
empty anchor index and is no longer cited anywhere in generated artifacts.

## Domain note (role-inference record)

The source file sits under a `System Design/` folder, but its content is a management /
employee-relations article about the **participative design of employee incentive payment
(reward) schemes for performance improvement**, not software or financial system design.
Role was inferred from the article text (extract-sample + full ingested markdown), not from
the folder or filename. Slug deliberately uses `employee-payment-scheme` to disambiguate
from financial/software payment-processing systems.

## Distillation Log (0.3.0)

All fields re-derived from the interrogation record grounded to
`payment-systems-and-20260612115310` (Docling, 19 anchors). No substantive content
change from 0.2.0; anchors are the correction.

| Field | Source IDs | QIDs | Anchors | Notes |
|-------|-----------|------|---------|-------|
| `slug` | payment-systems-and-20260612115310 | Q1 | h0005 | Unchanged from 0.1.0 |
| `display_name` | payment-systems-and-20260612115310 | Q1 | h0005 | From q1_display_name |
| `role` | payment-systems-and-20260612115310 | Q1, Q2 | h0005, h0008 | Synthesised from q1_role and q2_job; carries the participation-over-structure thesis |
| `when_to_use` | payment-systems-and-20260612115310 | Q3 | h0005, h0006, h0007, h0008, h0010, h0011 | Five triggers from q3_triggers |
| `when_not_to_use` | payment-systems-and-20260612115310 | Q4 | h0005, h0010, h0016 | Three exclusions from q4_exclusions |
| `inputs.required` | payment-systems-and-20260612115310 | Q5, Q16 | h0006, h0010 | Scheme description and organisation context |
| `outputs.primary_format` | payment-systems-and-20260612115310 | Q6 | h0008, h0009 | Canonical deliverable from q6_primary_deliverable |
| `outputs.modes[advise]` | payment-systems-and-20260612115310 | Q9 | h0005, h0008 | Evidence: article is framed as prescriptive guidance |
| `outputs.modes[review]` | payment-systems-and-20260612115310 | Q9 | h0005, h0007 | Evidence: diagnosing scheme modification and subversion |
| `outputs.modes[validate]` | payment-systems-and-20260612115310 | Q9 | h0006, h0007 | Evidence: explicit success criteria in source |
| `quality_bar` | payment-systems-and-20260612115310 | Q7 | h0006, h0007, h0010, h0016 | Five quality marks; each anchor now points to Docling heading |
| `minimum_useful_output` | payment-systems-and-20260612115310 | Q11 | h0008, h0009 | From q11_minimum_output |
| `forbidden_behaviours` | payment-systems-and-20260612115310 | Q10 | h0005, h0006, h0007, h0009, h0010, h0016 | Five do-not rules |
| `handoff_rules` | payment-systems-and-20260612115310 | Q8 | h0010 | Downstream owner: responsible managers |
| `source_of_truth_policy.canonical_owner` | payment-systems-and-20260612115310 | Q8, Q17 | h0017 | Responsible managers advised by the Bowey/Thorpe research base |
| `source_of_truth_policy.precedence` | payment-systems-and-20260612115310 | Q17 | h0017 | Advisor informs but does not take the decision |
| `knowledge_partition.always_on[0]` | payment-systems-and-20260612115310 | Q12 | h0006 | Central thesis: participation-over-structure |
| `knowledge_partition.always_on[1]` | payment-systems-and-20260612115310 | Q12 | h0007 | Two failure modes: subversion; policy decay |
| `knowledge_partition.always_on[2]` | payment-systems-and-20260612115310 | Q12 | h0009, h0016 | Participation-productivity-pay relationship |
| `knowledge_partition.always_on[3]` | payment-systems-and-20260612115310 | Q12 | h0010 | Boundary rule: participative vs. negotiation channel issues |
| `knowledge_partition.skills` | payment-systems-and-20260612115310 | Q13 | h0009, h0010, h0011, h0012, h0013, h0014, h0015 | Four skill areas; procedural detail routed out of profile body |
| `knowledge_partition.references` | payment-systems-and-20260612115310 | Q14 | h0006, h0018 | Research base and cited literature |

## Phase 2.5 importance ranking

Applied in-thread (no-spawner branch). `keep` units: the participation-over-structure thesis;
the two scheme failure modes (subversion; policy decay); the participation→productivity→reward
relationship; the participative cross-level group method; the negotiation-boundary rule. These
score highest on authority, actionability, reusability, risk_impact, and transferability and
form the profile core, skills, and always-on knowledge. `discard`/route-to-ledger units: the
specific 1989 organisational case examples and the period-bound trade-union and negotiation
context — low on stability and transferability, recorded here and in the volatility note rather
than the core.

## Generated Artifacts

| Artifact | Path |
|----------|------|
| Profile | `profile.yaml` |
| Provenance ledger | `provenance-ledger.md` |
| Changelog | `CHANGELOG.md` |
| Readme | `README.md` |
| Golden tests | `tests/golden-tests.yaml` |
| Source-pack manifest | `source-pack.manifest.yaml` |

## Version History

| Version | Date | Changes | Sources involved |
|---------|------|---------|-----------------|
| 0.1.0 | 2026-06-08 | Initial generation | payment-systems-and-20260608231654 (MarkItDown, 0 anchors) |
| 0.2.0 | 2026-06-11 | Authored skill and reference bodies (Step 8); promoted to status: ready | payment-systems-and-20260608231654 (MarkItDown, 0 anchors) |
| 0.3.0 | 2026-06-12 | Re-grounding: source re-converted with Docling; all provenance re-pointed to payment-systems-and-20260612115310 (19 real heading anchors h0005–h0018); old source_id payment-systems-and-20260608231654 retired; status reset to draft pending skill re-authoring | payment-systems-and-20260612115310 (Docling, 19 anchors) |
| 0.4.0 | 2026-06-15 | Authored examples block (happy-path + failure-recovery) | Adopt the A4 worked-example layer; grounded in existing role/scope, distillation-only |

**Supersession note (0.3.0):** Versions 0.1.0 and 0.2.0 cited `payment-systems-and-20260608231654`,
which was a MarkItDown conversion of the same PDF that produced zero heading anchors. All anchor
references in those versions were therefore structural placeholders rather than real document
locations. Version 0.3.0 re-derives every provenance citation against the Docling conversion
(`payment-systems-and-20260612115310`), whose 19 heading anchors are verified against the article
structure: article header (h0000–h0004), article body (h0005–h0017), references (h0018). No
substantive content of the profile changed; the anchor pointers are the correction.

## Open Questions

- The two referenced figures (consultation→success correlation at h0006; policy weakening
  lower down the organisation at h0007) appear as image placeholders even in the Docling
  conversion. Their captions are represented in prose from the surrounding text only.
- The article is a condensed account of a larger research programme (Bowey, Thorpe & Hellier,
  *Payment Systems and Productivity*, Macmillan); deeper procedural detail would require those
  underpinning sources, which are out of scope for this package.

## Conflict Log

_No conflicts recorded; single source. Old/new source_id difference is a conversion artefact,
not a content conflict._
