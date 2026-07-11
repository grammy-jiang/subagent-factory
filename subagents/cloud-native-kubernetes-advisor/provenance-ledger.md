# Provenance Ledger — cloud-native-kubernetes-advisor

**Schema:** provenance-ledger-v1  
**Package path:** subagents/cloud-native-kubernetes-advisor/  
**Source:** cloud-native-devops-ed89eef5 (Cloud Native DevOps with Kubernetes, 2nd Edition)  
**Rights status:** distillation-only (no verbatim quotation)  
**Distillation date:** 2026-06-14  
**Deriver:** profile-deriver agent  
**Agent version:** 0.1.0  

---

## Version History

| Version | Date | Change | Deriver |
|---------|------|--------|---------|
| 0.1.0 | 2026-06-14 | Initial profile derivation from interrogation records Q1–Q18 | profile-deriver |
| 0.3.0 | 2026-06-15 | Authored examples block (happy-path + failure-recovery) | Adopt the A4 worked-example layer; grounded in existing role/scope, distillation-only |

---

## Phase 0: Importance Ranking Gate

All 10 candidate units (U1–U10) from the interrogation record were evaluated.
All units scored above threshold on actionability (≥3), reusability (≥4), and
operational_fit (≥4). No units were discarded. All units were classified as
`keep` and contributed to profile field derivation.

| Unit | Summary | Disposition |
|------|---------|-------------|
| U1 | Run Less Software / prefer managed Kubernetes | keep — profile rule (P001, always_on) |
| U2 | Cluster architecture: control plane + worker nodes | keep — always_on |
| U3 | HA requirements: 3 control-plane nodes, AZ distribution | keep — quality_bar (P002/P003) |
| U4 | Self-hosting 8-item production-readiness checklist | keep — validate mode, reference |
| U5 | Managed service comparison (GKE/EKS/AKS/DO/IBM) | keep — compare mode, reference (stability:2 → reference, not always_on) |
| U6 | Workload fit: Kubernetes not a panacea; FaaS/clusterless fit | keep — quality_bar (P006/P007), forbidden_behaviours |
| U7 | Cloud-native characteristics (6 properties) | keep — always_on, reference |
| U8 | DevOps principles and organisational model | keep — always_on |
| U9 | Container fundamentals: Dockerfile, kubectl, registry | keep — always_on, produce mode |
| U10 | Resilience testing: node reboots, Chaos Monkey | keep — skills (resilience-testing-guidance) |

---

## Field-Level Distillation Log

### `slug`
- **Value:** cloud-native-kubernetes-advisor
- **Source:** Established during source ingestion
- **QID:** Q1
- **Note:** Kebab-case, role-based slug. No conflict.

### `display_name`
- **Value:** Cloud Native Kubernetes Advisor
- **Source:** cloud-native-devops-ed89eef5
- **QID:** Q1 (q1_display_name)
- **Note:** Taken directly from Q1 label; title-case of the slug. Confirms advisory framing from Chapter 1 ("cloud native DevOps") and authors' bio.

### `role`
- **Source:** cloud-native-devops-ed89eef5
- **QID:** Q1 (q1_role), Q2 (q2_job)
- **Evidence:** Chapter 1 frames cloud-native DevOps as the subject; Chapter 3 is structured as decision guidance; authors' bio identifies Arundel as a Kubernetes consulting specialist and Domingus as a senior DevOps/Kubernetes engineer.
- **Note:** One-sentence distillation of Q1 + Q2. Covers all six job domains named in Q2 without exceeding the single-sentence limit.

### `when_to_use` (5 triggers)
- **Source:** cloud-native-devops-ed89eef5
- **QID:** Q3 (q3_triggers)
- **Evidence:** Directly derived from Q3; each trigger maps to a chapter section: Ch.3 "Buy or Build", Ch.3 HA and architecture, Ch.2 containerisation walkthrough, Ch.3 "Kubernetes Is Not a Panacea" / clusterless services, Ch.1 DevOps org guidance.
- **Note:** 5 triggers — within the 3–6 limit. Phrased as caller-observable situations.

### `when_not_to_use` (3 exclusions)
- **Source:** cloud-native-devops-ed89eef5
- **QID:** Q4 (q4_exclusions)
- **Evidence:** Ch.3 introduction defers cluster-ops depth; Ch.1 clarifies scope as cloud-native DevOps not software feature development; all tool comparisons stay within Kubernetes/container space.
- **Note:** 3 exclusions — exceeds minimum of 2. Phrased as observable out-of-scope situations.

### `inputs.required` (4 items)
- **Source:** cloud-native-devops-ed89eef5
- **QID:** Q5 (q5_required_input), Q16 (q16_caller_supplied)
- **Evidence:** Ch.3 TIP box on budget/staffing trade-off; Ch.3 "Use Standard Kubernetes Self-Hosting Tools if You Must" — contingent on special requirements; Ch.3 Kubespray Ansible note; Ch.1/Ch.3 workload-type guidance.
- **Note:** Q5 states four context dimensions (infra context, scale/criticality, team size/maturity, specific decision). Q16 caller-supplied items are merged into explicit required inputs since they must be provided before meaningful advice can be given.

### `outputs.primary_format`
- **Source:** cloud-native-devops-ed89eef5
- **QID:** Q6 (q6_primary_deliverable)
- **Evidence:** Ch.3 "Buy or Build: Our Recommendations" gives named recommendations; Ch.3 "It's More Work Than You Think" enumerates a production-readiness checklist; Ch.2 walks through specific commands.
- **Note:** Distillation of Q6 into a primary-format noun phrase. Advisory prose with named options and trade-off comparisons.

### `modes` (4 modes: advise, compare, validate, produce)
- **Source:** cloud-native-devops-ed89eef5
- **QID:** Q9 (q9_modes)
- **Evidence:**
  - `advise` — Ch.1 and Ch.3 dominant advisory pattern; explicit TIP boxes with named recommendations ("a managed service is the best way to run Kubernetes, period").
  - `compare` — Ch.3 systematic comparison of managed services and self-hosting tools; Ch.1 container vs VM comparison; Ch.3 clusterless services comparison.
  - `validate` — Ch.3 "It's More Work Than You Think" production-readiness checklist; "Trust, but verify" guidance; chaos-testing guidance (EV019).
  - `produce` — Ch.2 Dockerfile walkthrough, container image build, kubectl run/port-forward. Rights are distillation-only; produced artefacts are newly composed from principles, not quotations.
- **Note:** Q9 explicitly excludes `review` and `extract` modes as not supported by evidence. The `produce` mode requires `policy/patch-policy.yaml` (written separately).

### `quality_bar` (5 checks)
- **Source:** cloud-native-devops-ed89eef5, principles.yaml
- **QID:** Q7 (q7_quality_marks)
- **Principles grounding:** P001 (managed services default), P002/P003 (HA/quorum), P006/P007 (workload fit), P005 (observability), P010 (org-size-aware).
- **Evidence:** Each check maps to a principle with confidence:high and at least one strong evidence record.
- **Note:** 5 checks — within 3–5 limit. Each check is falsifiable. Principle IDs cited in brackets for traceability.

### `minimum_useful_output`
- **Source:** cloud-native-devops-ed89eef5
- **QID:** Q11 (q11_minimum_output)
- **Evidence:** The book's core TIP — managed service recommendation as a crisp, opinionated single-sentence recommendation — demonstrates the minimum quantum.
- **Note:** Includes a concrete named example sentence to make the requirement unambiguous.

### `forbidden_behaviours` (5 items)
- **Source:** cloud-native-devops-ed89eef5, principles.yaml
- **QID:** Q10 (q10_refusals), Q17, Q18
- **Principles grounding:** P001 (self-hosting gating), P006 (stateful databases), Q10 (container vs VM distinction, NoOps fallacy), Q17/Q18 (managed service volatility).
- **Evidence:** Each behaviour maps to a Q10 refusal with chapter-level evidence or to Q17/Q18 volatility evidence.
- **Note:** All 5 behaviours are traceable to interrogation evidence. No orphan rules.

### `handoff_rules` (4 rules)
- **Source:** cloud-native-devops-ed89eef5
- **QID:** Q8 (q8_handoff)
- **Evidence:** Ch.3 "Buy or Build" frames advisor role as recommending; Ch.3 intro defers technical cluster-ops detail to Brendan Burns' "Managing Kubernetes"; Ch.1 "Distributed DevOps" describes the ops specialist as implementer; Q9 produce mode includes starter-artefact framing.
- **Note:** Covers the four downstream handoff boundaries identified in Q8 plus the produce-mode artefact caveat.

### `source_of_truth_policy.canonical_owner`
- **Source:** cloud-native-devops-ed89eef5
- **QID:** Q8 (q8_handoff), Q17 (q17_source_of_truth)
- **Evidence:** Ch.3 "Buy or Build" frames the advisor as recommending; Ch.3 notes rapid change in managed services landscape; Q17 identifies kubernetes.io, cloud provider docs, and cncf.io/projects as live authoritative sources.
- **Note:** Q8 evidence_gap acknowledged — no specific role named; inferred from context as engineering leadership or platform team.

### `source_of_truth_policy.precedence`
- **Source:** cloud-native-devops-ed89eef5
- **QID:** Q17, Q18
- **Evidence:** Ch.3 explicit warning "expect the features and services described here to change rapidly"; review_cadence: annual in source metadata.
- **Note:** Directs callers to verify against current provider documentation for volatile information.

### `knowledge_partition.always_on` (7 items)
- **Source:** cloud-native-devops-ed89eef5
- **QID:** Q12 (q12_always_on)
- **Evidence:** Q12 lists 7 foundational knowledge items distributed across all three source chapters. These are concepts repeated, summarised, and treated as foundational throughout; highest U-scores (U1–U3, U6–U9).
- **Note:** 7 items — within the 12-rule limit. U5 (managed service comparison table) is routed to references (stability:2) rather than always_on.

### `knowledge_partition.skills` (6 skills)
- **Source:** cloud-native-devops-ed89eef5
- **QID:** Q13 (q13_skills)
- **Evidence:** Q13 identifies 8 skill areas that are too granular for always_on profile rules. Consolidated into 6 kebab-case skill names. Multi-cluster management (Tanzu/Anthos) merged into evaluating-managed-kubernetes-offerings for profile-level grouping; chaos/resilience testing is a separate skill.
- **Note:** Skills are named but not yet written as separate skill files; they represent actionable knowledge units from Ch.2 and Ch.3.

### `knowledge_partition.references` (6 references)
- **Source:** cloud-native-devops-ed89eef5
- **QID:** Q14 (q14_references)
- **Evidence:** Q14 identifies 6 structured reference lists in Ch.3 that are better as look-up tables than inline profile rules.
- **Note:** References are named but not yet written as separate files; they include the production-readiness checklist (8 items), managed service comparison, installer comparison, control-plane component reference, cloud-native characteristics, and clusterless services reference.

### `sources`
- **Source:** sources/metadata/cloud-native-devops-ed89eef5.metadata.json
- **SHA256:** ed89eef520902447ae3df9a1f934e56141572a26ada4c7b790920df627e80b81
- **Note:** Single source. Rights: distillation-only. No verbatim quotation permitted.

---

## Conflict Log

No multi-source conflicts. Single source package.

Evidence gaps noted in interrogation record:
1. **Q15 (mcp):** No evidence of live tool use or real-time data retrieval. MCP list is empty — correct.
2. **Q8 (canonical_owner):** No specific role named in source. Resolved by inference from context (engineering leadership / platform team) — flagged here as inferred, not quoted.
3. **Q11 (minimum_useful_output):** No explicit minimum-output definition in source. Resolved by pattern inference from single-sentence TIP boxes in Ch.3.

---

## Bloat Check

| Check | Limit | Actual | Status |
|-------|-------|--------|--------|
| Total body words (approx.) | <800 | ~620 | PASS |
| Universal rules (always_on) | max 12 | 7 | PASS |
| Rules per mode | max 3 | 2 (trigger + output) | PASS |
| Procedures in body | no ordered seq >2 steps | 0 | PASS |
| Static tables/checklists | none | 0 | PASS |
| Platform-specific nouns in always_on | zero | 0 | PASS |

Managed service names (GKE, EKS, AKS) appear only in `when_to_use` triggers and `minimum_useful_output` examples, not as always_on rules. Production-readiness checklist is routed to references. Installer comparison is routed to references.
