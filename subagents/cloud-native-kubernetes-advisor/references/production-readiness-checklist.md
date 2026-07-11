---
name: production-readiness-checklist
kind: reference
status: ready
provenance:
  principles:
  - P011
  - P002
  - P003
  - P005
  claims:
  - CL042
  - CL043
  - CL038
  - CL040
  - CL025
  source_anchors:
  - cloud-native-devops-ed89eef5-h0109
  - cloud-native-devops-ed89eef5-h0110
  - cloud-native-devops-ed89eef5-h0106
  - cloud-native-devops-ed89eef5-h0107
  - cloud-native-devops-ed89eef5-h0034
  authored_from_digest: 60228720fe111eecb8a724aba9554e5392e850ef65d7a3410b1f83b843746548
---

# Production-readiness checklist

A working cluster is a long way from a production-ready one. A self-hosted cluster must
address at least eight areas beyond basic setup [P011, CL042], and readiness is an ongoing
obligation, not a one-time setup [CL043]. Use this checklist to assess a cluster design or
to scope self-hosting work.

## Eight readiness areas

| # | Area | Pass criteria |
|---|---|---|
| 1 | **Control-plane HA** | Minimum 3 control-plane nodes for etcd quorum; cluster still serves deployments/updates if one node is lost [P002] |
| 2 | **Worker-node HA** | Workers distributed across ≥2 (ideally 3) availability zones; cluster auto-provisions/heals on multi-node or zone loss [P003] |
| 3 | **Cluster security** | Internal components use TLS with trusted certs; least-privilege RBAC; container security defaults set; etcd access controlled and authenticated |
| 4 | **Service security** | Internet-facing services authenticated/authorised; cluster API access strictly limited |
| 5 | **Conformance** | Cluster meets CNCF Kubernetes conformance standards |
| 6 | **Node config management** | Nodes config-managed (not imperative scripts left alone); OS/kernel patched and updated |
| 7 | **Backup & restore** | Cluster data and persistent storage backed up; a tested restore process exists |
| 8 | **Ongoing maintenance** | Defined process to provision nodes, roll out config and Kubernetes updates, scale to demand, and enforce policy |

## Ongoing obligations (not just initial setup)

- Apply all eight areas to **every** cluster, for its whole life — re-check HA, security,
  etc. on every change or upgrade [CL043].
- Monitoring on all nodes/components, plus alerting that can page staff day or night.
- Keep up with Kubernetes releases; reprovision to gain new functionality where needed.
- Regularly resilience-test (see `resilience-testing-guidance`) — e.g. chaos tooling, or
  rely on real-world provider failures where frequent enough.

## Observability (first-class for production workloads and microservices)

Observability — structured logging, metrics, distributed tracing, and alerting — is a key
requirement of cloud-native distributed systems, which are inherently harder to inspect
and debug than monoliths. Treat it as built-in from the start, not bolted on [P005, CL025].

| Pillar | Purpose |
|---|---|
| Logging | Structured records of what each service did |
| Metrics | Quantitative signals on health and load |
| Tracing | Follow a request across distributed services |
| Alerting | Page staff on failure conditions |

## Provenance

Derived from principles P011, P002, P003, and P005 (claims CL042, CL043, CL038, CL040,
CL025) of *Cloud Native DevOps with Kubernetes, 2nd Edition*. Source is
`distillation-only`: paraphrased, not quoted.
