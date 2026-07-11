---
name: managed-kubernetes-service-comparison
kind: reference
status: ready
provenance:
  principles:
  - P001
  - P010
  claims:
  - CL046
  - CL059
  source_anchors:
  - cloud-native-devops-ed89eef5-h0115
  - cloud-native-devops-ed89eef5-h0138
  authored_from_digest: 299db77cd33c3ebb7c50d83cb12a506e814a1dde6a818e4bff86d5687e5a15f4
---

# Managed Kubernetes service comparison

Use this table to match a team to a managed offering. The dominant selection factor is the
cloud the team already runs on, because operational integration (IAM, networking,
registries, IaC modules) is the largest cost. All listed services manage the control plane
and bill on worker nodes unless noted. Default to managed over self-hosting [P001]; for
small/mid teams, start with one offering [P010].

| Service | Best fit | Control plane | Notable features | Billing |
|---|---|---|---|---|
| **GKE** (Google) | Teams on GCP; wanting the originating vendor | Managed | Multi-zone clusters, node auto-repair, auto security patching, cluster autoscaling; **Autopilot** tier also manages worker nodes | Worker nodes (autoscaling helps control cost) |
| **EKS** (AWS) | Teams already on AWS (most common production home for Kubernetes) | Managed | Integrates with existing AWS infrastructure; supersedes the older proprietary ECS for Kubernetes workloads | Worker nodes |
| **AKS** (Azure) | Teams on Azure | Managed | Often first to support newer Kubernetes versions; cluster autoscaling | Worker nodes |
| **DigitalOcean Kubernetes** | Smaller teams wanting simplicity and strong docs | Managed | Simple offering, excellent documentation/tutorials | Worker nodes only (no charge for managed control plane) |
| **IBM Cloud Kubernetes Service** | Teams on IBM Cloud | Managed | Established vendor option | Worker nodes |

## Multi-cloud management layers (not single-cluster services)

For workloads that must span clouds or platforms while keeping options open:

| Tool | Role |
|---|---|
| **VMware Tanzu** (Mission Control) | Centrally manage multiple clusters wherever they run |
| **Google Anthos** | Centrally manage clusters across GKE, AWS, and on-prem; hooks on-prem into Google Cloud services |
| **OpenShift** | Full PaaS spanning bare-metal, VMs, private and public clouds |

**Scale guidance:** most small and mid-sized teams should *not* start multi-cloud — the
added complexity and cost are not justified at that scale. Start with containers on one
managed offering and build up; move to multi-cloud only when a specific availability,
regulatory, or cost requirement makes it necessary [P010, CL059].

## Caveat

The managed-services marketplace is highly competitive and features, pricing, and HA
support change rapidly. Treat every entry above as a starting point and verify current
provider documentation before deciding.

## Provenance

Derived from principles P001 and P010 (claims CL046, CL059) of *Cloud Native DevOps with
Kubernetes, 2nd Edition*. Source is `distillation-only`: paraphrased, not quoted.
