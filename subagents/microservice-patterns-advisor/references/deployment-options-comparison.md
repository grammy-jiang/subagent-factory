---
name: deployment-options-comparison
kind: reference
status: ready
provenance:
  principles:
  - P123
  - P124
  - P051
  - P021
  - P046
  - P097
  - P043
  claims:
  - C00017
  - C00471
  - C00447
  - C00448
  - C00451
  - C00466
  - C00467
  - C00061
  - C00074
  source_anchors: []
  authored_from_digest: b5464bd4226d0146ae9db1f351f25aa9834d5a22c895de11d10302b6e87bf898
---

# Deployment Options Comparison

Choose a deployment style by trading isolation against overhead and scaling
behaviour, preferring the most lightweight pattern that supports the service's
requirements (P123, P124). This table compares the deployment patterns of the
microservices pattern language so a recommendation can be tied to the caller's forces.

## Comparison

| Option | Isolation | Overhead / startup | Scaling | When it fits |
|---|---|---|---|---|
| Service per VM | Strong (full OS + stack per instance) | Heavyweight; slow startup | Coarse-grained, slower to scale | Strong isolation or full-stack encapsulation required |
| Service per Container | Most of a VM's isolation and stack encapsulation | Lower overhead; fast startup | Fast, fine-grained | Common default for most services |
| Serverless deployment | Platform-managed; no servers to run | No infra management; cold starts | Automatic, scales to zero | Bursty / low-idle workloads tolerant of the constrained runtime |

## Cross-cutting traffic layer

| Option | What it does | Trade-off |
|---|---|---|
| Service mesh / Sidecar | Route all traffic in/out of services through an infrastructure layer (often a sidecar process beside each instance) that implements circuit breaking, distributed tracing, service discovery, and security | Moves cross-cutting concerns out of service code and the language chassis, at the cost of operating the mesh |

## Decision notes

- Containers are the common default: most of a VM's isolation with faster startup
  and lower overhead, run under an orchestrator such as Kubernetes (C00447, C00451,
  P051, P021).
- Serverless removes infrastructure management and scales to zero but constrains
  the runtime (cold starts, limited execution model), so it fits some services and
  not others (C00466, C00467, P046).
- A service mesh / sidecar is orthogonal to the packaging choice: it handles
  cross-cutting traffic concerns regardless of VM/container/serverless (P043); back
  the whole estate with an automated deployment platform (C00061, C00074, P097).

## Provenance

Tier 2 reference. Grounded in principles P123/P124 (the deployment patterns; choose
the most lightweight that fits), P051 (containers), P021 (Kubernetes), P046
(serverless), P097 (automated deployment platform), and P043 (service mesh /
sidecar), and in claims C00017, C00471, C00447–C00448, C00451, C00466–C00467, C00061,
C00074 from `chris-richardson-mic-19016f24` (Microservices Patterns, Chris Richardson,
Manning 2018, `distillation-only`). No verbatim quotation.
