---
name: deployment-strategy-selection
kind: skill
status: ready
provenance:
  principles:
  - P009
  - P008
  claims:
  - CL015
  - CL024
  source_anchors:
  - cloud-native-devops-ed89eef5-h0025
  - cloud-native-devops-ed89eef5-h0032
  authored_from_digest: 97747ed96f66d64990559d05aa09fe2127e74299a65ee17fa6134d9302360732
---

# Deployment strategy selection

## Purpose

Choose a release strategy for a production workload. Kubernetes rolling updates are the
default path to zero-downtime deployments; higher-risk releases warrant canary or
blue-green strategies [P009]. Underpinning all of them is configured redundancy: cloud-
native availability comes from running multiple replicas across failure domains so
Kubernetes can reschedule on failure — but only when that redundancy is set up in advance
[P008].

## When to use

- A team is planning a production deployment or release.
- An engineer is advising on risk mitigation for shipping a new version.
- Replica counts, pod disruption budgets, or rollout safety are under review.

Do not use this skill to decide whether the workload belongs on Kubernetes (use
`clusterless-and-faas-fit-analysis`) or to verify cluster HA (use
`resilience-testing-guidance`).

## Procedure

1. **Confirm redundancy is configured first.** A safe rollout assumes the workload runs
   with more than one replica spread across failure domains, so Kubernetes can detect a
   failure and reschedule Pods. Availability comes from this distribution and redundancy,
   not from any single node's reliability — and it must be configured before the
   deployment, not after [P008, CL024]. (Batch or single-run jobs where replica
   redundancy is not meaningful are out of scope.)
2. **Default to rolling updates.** For most releases, recommend Kubernetes rolling
   updates: start containers on the new version, wait until they pass health checks, then
   shut down the old ones — achieving zero downtime by default [P009, CL015]. Ensure
   readiness/health checks are defined, since the strategy depends on them.
3. **Escalate to canary for higher-risk releases.** When a change carries more risk,
   graduate the rollout — release to one server / a small slice at a time and monitor for
   errors before proceeding. This catches problems early [P009].
4. **Use blue-green when you need a clean cutover.** Spin the new version up fully in
   parallel, then switch traffic once it is healthy. Useful when partial exposure is
   undesirable [P009].
5. **Flag the mixed-version exception.** Breaking schema changes or migrations that cannot
   tolerate mixed-version traffic need a coordinated cutover, not a plain rolling update
   [P009 does-not-apply]. Surface this before recommending a rolling release.
6. **State the recommended strategy with its rationale** (risk level, downtime
   tolerance, schema compatibility) and the redundancy prerequisites it assumes.

## Inputs

- Release risk level and blast radius.
- Downtime tolerance / SLA for the workload.
- Whether the change includes breaking schema or data migrations.
- Current replica count and failure-domain distribution.

## Output

A named deployment-strategy recommendation (rolling / canary / blue-green) with its
rationale, the redundancy prerequisites it assumes, and any mixed-version-traffic caveat.

## References

- `production-readiness-checklist`

## Provenance

Derived from principles P009 and P008 (claims CL015, CL024) of *Cloud Native DevOps with
Kubernetes, 2nd Edition*. Source is `distillation-only`: paraphrased, not quoted.
