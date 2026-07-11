---
name: evaluating-managed-kubernetes-offerings
kind: skill
status: ready
provenance:
  principles:
  - P001
  - P010
  claims:
  - CL046
  - CL054
  - CL053
  - CL059
  source_anchors:
  - cloud-native-devops-ed89eef5-h0115
  - cloud-native-devops-ed89eef5-h0133
  - cloud-native-devops-ed89eef5-h0130
  - cloud-native-devops-ed89eef5-h0131
  - cloud-native-devops-ed89eef5-h0132
  - cloud-native-devops-ed89eef5-h0138
  authored_from_digest: cc04d8d890889409cc76efb72e305f51abf539fe6f9c35df27fc34535c0f03fe
---

# Evaluating managed Kubernetes offerings

## Purpose

Decide whether a team should run Kubernetes on a managed service and, if so, which
offering fits. The default recommendation is to outsource cluster operations:
installing, configuring, securing, upgrading, and keeping a cluster reliable is
undifferentiated heavy lifting that does not differentiate the business, so a managed
service is the more cost-effective choice for almost all organisations [P001]. Small and
mid-sized teams in particular should begin with a single managed offering and grow from
there rather than reaching for multi-cloud complexity [P010].

## When to use

- A team is choosing between self-hosting the control plane and a managed service.
- An organisation wants a build-vs-buy cost/operational analysis for Kubernetes.
- A small or mid-sized team asks how to start with Kubernetes infrastructure.
- A team wants the trade-offs between named managed offerings (GKE, EKS, AKS,
  DigitalOcean) for their cloud and skills.

Do not use this skill to design control-plane HA internals (use
`resilience-testing-guidance`) or to pick a self-hosting installer once managed is ruled
out (use `selecting-self-hosting-installers`).

## Procedure

1. **Apply the Run Less Software test first.** Confirm that running the cluster is
   undifferentiated heavy lifting for this organisation — installation, configuration,
   security, upgrades, and reliability work that costs money rather than making it. If
   so, the default is to outsource it [P001, CL054, CL053].
2. **Check for a disqualifying special requirement.** Self-hosting is justified *only*
   when a concrete requirement cannot be met by any managed provider — e.g. regulatory,
   compliance, air-gap, or specific hardware (bare-metal GPU) constraints. Absent such a
   requirement, recommend managed [P001]. If one exists, hand off to
   `selecting-self-hosting-installers`.
3. **Anchor on the team's existing cloud and skills.** Default to the managed service
   native to where the team already runs infrastructure, because operational integration
   (IAM, networking, registries, Terraform modules) is the dominant cost:
   - **GKE (Google):** the originating vendor's service; multi-zone clusters, node
     auto-repair, auto security patching, optional cluster autoscaling, and an Autopilot
     tier that also manages worker nodes.
   - **EKS (AWS):** sensible when infrastructure already lives in AWS; the most common
     place Kubernetes runs in production.
   - **AKS (Azure):** often the first to support newer Kubernetes versions; control plane
     managed, billed on worker nodes, supports cluster autoscaling.
   - **DigitalOcean Kubernetes:** simple, well-documented; no charge for the managed
     control plane, billed on worker nodes — fits smaller teams.
   See `managed-kubernetes-service-comparison` for the dimension-by-dimension table.
4. **Right-size the architecture for team scale.** For small and mid-sized teams,
   recommend one managed offering, not multi-cluster or multi-cloud. Multi-cloud adds
   complexity and cost that early scale does not justify; progress to it only when a
   specific availability, regulatory, or cost requirement makes it necessary [P010,
   CL059].
5. **Frame vendor lock-in correctly.** Because Kubernetes is a standard platform,
   workloads built for one certified provider port to another with minor manifest
   tweaks. Note that managed services let a team trial a production-grade cluster cheaply
   before committing.
6. **Qualify all provider specifics.** Managed-service features, pricing, and HA support
   change rapidly; direct the team to verify current provider documentation before
   acting on any named feature.

## Inputs

- Cloud provider and existing tooling ecosystem (AWS / GCP / Azure / on-prem / hybrid).
- Team size and dedicated ops headcount.
- Any regulatory, compliance, air-gap, or special-hardware requirement.
- Production vs dev/test, and SLA expectations.

## Output

A named recommendation — managed vs self-hosted, and which managed offering — with its
primary rationale (operational cost, existing cloud fit, team scale), the disqualifying
requirements checked, and a directive to confirm current provider docs. For small/mid
teams, an explicit "start with one managed offering" steer.

## References

- `managed-kubernetes-service-comparison`
- `production-readiness-checklist`

## Provenance

Derived from principles P001 and P010 (claims CL046, CL054, CL053, CL059) of *Cloud
Native DevOps with Kubernetes, 2nd Edition*. Source is `distillation-only`: paraphrased,
not quoted.
