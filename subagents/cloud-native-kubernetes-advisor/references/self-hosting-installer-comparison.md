---
name: self-hosting-installer-comparison
kind: reference
status: ready
provenance:
  principles:
  - P011
  claims:
  - CL060
  source_anchors:
  - cloud-native-devops-ed89eef5-h0139
  authored_from_digest: a9658020e668a073fe073a0ece52e01a80b0acd73366cba26a42fbc9eeed0232
---

# Self-hosting installer comparison

Use this table only after the managed-vs-self-hosted decision has landed on self-hosting
(a special requirement no managed provider supports). Self-hosting from scratch is
impractical outside learning; choose a mature, widely used installer [P011]. Recommend
kops or Kubespray depending on environment [CL060].

| Installer | Primary environment | Provisioning model | HA support | Notes |
|---|---|---|---|---|
| **kops** | AWS (default); growing alpha/beta support for Google Cloud, DigitalOcean, Azure, OpenStack | Command-line, declarative configuration | Yes — builds HA clusters suitable for production | Part of the Kubernetes project; also scales, resizes nodes, and performs upgrades |
| **Kubespray** | On-prem / bare-metal (default); any cloud, including private cloud | Ansible playbooks | Yes — production-ready clusters with HA options | Kubernetes-umbrella project; best fit when the team already uses Ansible for config management |
| **kubeadm** | Any; lower-level building block | Bootstraps a cluster on already-provisioned machines | Manual | Underlies higher-level tools; more hands-on |

## Multi-cloud / multi-platform spanning

If the cluster must span multiple clouds or platforms (including bare-metal) and the team
wants to keep options open, consider **VMware Tanzu** or **Google Anthos** as a management
layer rather than an installer. Because most of the administration overhead is in the
control plane, this can be a reasonable compromise.

## Decision notes

- Pick **kops** for AWS or a growing multi-cloud footprint with declarative tooling.
- Pick **Kubespray** for on-prem / bare-metal, or when Ansible is already in use.
- Many point-and-click installers solve only the easy problems and ignore the hard ones;
  prefer mature, widely used tools.
- Whichever is chosen, budget for the eight-area production-readiness work
  (`production-readiness-checklist`) — the installer handles setup, not ongoing operation.

## Provenance

Derived from principle P011 (claim CL060) of *Cloud Native DevOps with Kubernetes, 2nd
Edition*. Source is `distillation-only`: paraphrased, not quoted.
