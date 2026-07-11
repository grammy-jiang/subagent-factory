---
name: clusterless-and-faas-fit-analysis
kind: skill
status: ready
provenance:
  principles:
  - P006
  - P007
  claims:
  - CL020
  - CL027
  source_anchors:
  - cloud-native-devops-ed89eef5-h0027
  - cloud-native-devops-ed89eef5-h0036
  authored_from_digest: 0e9e6659f5dc3e9fd3e2d177d4333841495eeb8310d33dc3599fb515f9623ad8
---

# Clusterless and FaaS fit analysis

## Purpose

Assess whether a workload actually belongs on Kubernetes before placing it there. Not
every workload should run on a full cluster: stateful databases are usually better on a
managed database service [P006], and short, event-driven jobs often fit functions-as-a-
service (FaaS) or clusterless container services instead. Microservices are a deliberate
architectural choice with real distributed-systems cost, not a default [P007].

## When to use

- A team is deciding where to host a database or other stateful workload.
- An engineer is assessing whether a job fits FaaS (Lambda, Cloud Functions, Azure
  Functions) or clusterless containers (Fargate, ACI, Cloud Run) instead of Kubernetes.
- A team is weighing a monolith-to-microservices migration or the decomposition level of
  a new system.

Do not use this skill to design deployment strategy for a workload already placed on
Kubernetes (use `deployment-strategy-selection`).

## Procedure

1. **Classify the workload first.** Determine stateful vs stateless, long-running vs
   short/event-driven, and its coordination needs. This classification drives placement —
   do not default everything to Kubernetes.
2. **Route stateful workloads to managed services.** For databases and similar stateful
   workloads, prefer a managed database service. Database replicas are not interchangeable
   — each carries unique state requiring coordination for restarts, consistency, and
   schema changes — so enterprise-grade reliability inside Kubernetes demands a large
   engineering investment that managed services absorb. Flag that investment whenever a
   team proposes running a database in Kubernetes [P006, CL020]. Exception: a dedicated
   team with deep stateful-Kubernetes expertise and a specific need (cost, data
   sovereignty) managed services cannot meet.
3. **Route short, event-driven jobs to FaaS.** Standalone tasks that run only when
   triggered, integrate with existing cloud services, and finish quickly are good FaaS
   candidates — billed per execution rather than for an always-on server. Note FaaS run-
   time limits (e.g. Lambda's 15-minute cap). For Kubernetes-resident functions, mention
   OpenFaaS, Knative, or Kubeless ("funtainers").
4. **Consider clusterless container services.** For self-contained, long-running compute
   or batch jobs that do not justify managing worker nodes, weigh Fargate, Azure Container
   Instances, or Google Cloud Run, where you specify an image and resources and the
   provider runs it. See `clusterless-container-services-reference`.
5. **Treat microservices as a deliberate decision.** Microservice architectures are
   distributed systems — hard to observe and prone to surprising failures; monoliths are
   easier to understand and trace but harder to scale. A containerised monolith can
   deliver real cloud value and serve as a transitional step before gradually extracting
   services. Do not push a team to microservices by default; recommend the decomposition
   their complexity and team scale actually justify [P007, CL027].
6. **State the placement recommendation with its rationale**, naming the alternative
   (managed DB / FaaS / clusterless) and why the workload's characteristics point there.

## Inputs

- Workload characteristics: stateful vs stateless, long-running vs event-driven,
  coordination/consistency needs, run duration.
- SLA, traffic profile, and team's stateful-operations expertise.
- For architecture questions: current monolith-vs-microservices state and team scale.

## Output

A placement recommendation — Kubernetes, managed database service, FaaS, or clusterless
containers — with the workload-classification rationale; and for architecture questions,
a deliberate microservices-vs-monolith recommendation rather than a default.

## References

- `clusterless-container-services-reference`

## Provenance

Derived from principles P006 and P007 (claims CL020, CL027) of *Cloud Native DevOps with
Kubernetes, 2nd Edition*. Source is `distillation-only`: paraphrased, not quoted.
