---
name: cloud-native-characteristics-reference
kind: reference
status: ready
provenance:
  principles:
  - P008
  claims:
  - CL024
  source_anchors:
  - cloud-native-devops-ed89eef5-h0032
  authored_from_digest: 52f93515f76c2eb4884ebd2ca7afd7acb15a8e8a6764b5a02dcde4331b5d0501
---

# Cloud-native characteristics reference

Taxonomy of the characteristics that define a cloud-native application, used when assessing
whether a design is genuinely cloud-native. The defining property is that availability
comes from inherent distribution, redundancy, and graceful degradation rather than the
reliability of any single node [P008].

## Characteristics

| Characteristic | What it means |
|---|---|
| **Automatable** | Apps follow common standards, formats, and interfaces so machines (not humans) deploy and manage them; Kubernetes supplies these standard interfaces |
| **Ubiquitous / flexible** | Decoupled from physical resources, containerised microservices move easily between nodes or clusters |
| **Resilient / scalable** | Inherently distributed, so made highly available through redundancy and graceful degradation — instead of single points of failure at process, hardware, or network level |
| **Dynamic** | An orchestrator schedules containers for maximum resource use, runs many copies for HA, and performs rolling updates without dropping traffic |
| **Observable** | Distributed apps are harder to inspect/debug, so monitoring, logging, tracing, and metrics are key requirements (see `production-readiness-checklist`) |
| **Distributed** | Built as multiple cooperating microservices rather than a single monolith — about *how* the app works, not *where* it runs |

## Availability contrast

| | Traditional applications | Cloud-native applications |
|---|---|---|
| Failure model | Single points of failure (process crash, hardware fault, network congestion) | Inherently distributed |
| How availability is achieved | Reliability of individual components | Redundancy and graceful degradation across failure domains [CL024] |

Note: monoliths can still run in containers in the cloud and deliver real value — running
a monolith may be a step toward gradually extracting microservices (see
`clusterless-and-faas-fit-analysis`).

## Provenance

Derived from principle P008 (claim CL024) and the profile's always-on cloud-native
characteristics knowledge, from *Cloud Native DevOps with Kubernetes, 2nd Edition*. Source
is `distillation-only`: paraphrased, not quoted.
