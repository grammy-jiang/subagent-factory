---
name: selecting-self-hosting-installers
kind: skill
status: ready
provenance:
  principles:
  - P011
  claims:
  - CL060
  - CL042
  - CL043
  source_anchors:
  - cloud-native-devops-ed89eef5-h0139
  - cloud-native-devops-ed89eef5-h0109
  - cloud-native-devops-ed89eef5-h0110
  authored_from_digest: f84f307d0d3322f0419648deb356d3814eb90402b50437ded6b1963379785072
---

# Selecting self-hosting installers

## Purpose

When a team has determined it *must* self-host Kubernetes — because a real requirement
cannot be met by any managed provider — guide the choice of a mature installer and set
expectations that self-hosting is an ongoing operational investment, not a one-time setup
[P011]. Self-hosting from scratch is impractical outside learning exercises; the right
move is a mature, widely used installer.

## When to use

- The managed-vs-self-hosted decision has already landed on self-hosting (special
  requirement confirmed — see `evaluating-managed-kubernetes-offerings`).
- A team is choosing an installer for an on-prem, bare-metal, or multi-cloud cluster.
- A team underestimates the continuing cost of running its own cluster and needs that
  surfaced before committing.

Do not use this skill to make the build-vs-buy decision itself, or to audit an existing
cluster's readiness (use `production-readiness-checklist` / `resilience-testing-guidance`).

## Procedure

1. **Re-confirm self-hosting is warranted.** Verify there is a concrete special
   requirement that no managed provider supports. If not, return to
   `evaluating-managed-kubernetes-offerings` — managed remains the default [P011].
2. **State the ongoing cost explicitly.** Self-hosting requires production-readiness work
   across at least eight areas: control-plane HA, worker-node HA, cluster security (TLS,
   RBAC, etcd access control), service security, conformance, node configuration
   management, data backup and restore, and ongoing maintenance [P011, CL042]. Beyond
   setup, the team must monitor, alert, keep up with Kubernetes releases, periodically
   resilience-test, and reprovision for new features [CL043]. Make clear most
   point-and-click installers solve only the easy problems.
3. **Match the installer to the environment.** Recommend a mature, widely used tool:
   - **kops** — command-line provisioner, part of the Kubernetes project. Long-standing
     AWS tool now adding support for Google Cloud, DigitalOcean, Azure, and OpenStack.
     Builds HA clusters, uses declarative configuration, and can scale, resize, and
     upgrade. Default for AWS / growing multi-cloud [CL060].
   - **Kubespray** — Kubernetes-umbrella project that deploys production-ready clusters
     via Ansible playbooks. Focused on existing machines, especially on-prem and
     bare-metal, but works on any cloud. Default when the team already uses Ansible or
     runs on-prem [CL060].
   - For clusters that must span multiple clouds or platforms while keeping options open,
     note VMware Tanzu or Google Anthos as a management layer rather than an installer.
   See `self-hosting-installer-comparison` for the side-by-side.
4. **Plan the production-readiness work, not just the install.** Tie the chosen installer
   to the eight-area checklist so the team budgets for HA, security, conformance, backup,
   and maintenance from the start (`production-readiness-checklist`).
5. **Schedule recurring resilience testing.** Self-hosting means the team owns control-
   plane HA verification; route to `resilience-testing-guidance` for the cadence.

## Inputs

- Confirmed special requirement that rules out managed services.
- Target environment (AWS, other cloud, on-prem/bare-metal, multi-cloud).
- Existing configuration-management tooling (e.g. Ansible experience).
- Available ops headcount for sustained cluster operation.

## Output

A named installer recommendation (kops, Kubespray, or a multi-cloud management layer)
with the environment-based rationale, plus an explicit statement of the continuing
operational burden and a pointer to the production-readiness checklist.

## References

- `self-hosting-installer-comparison`
- `production-readiness-checklist`

## Provenance

Derived from principle P011 (claims CL060, CL042, CL043) of *Cloud Native DevOps with
Kubernetes, 2nd Edition*. Source is `distillation-only`: paraphrased, not quoted.
