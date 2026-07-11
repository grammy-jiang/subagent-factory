---
name: clusterless-container-services-reference
kind: reference
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

# Clusterless container services reference

Taxonomy of compute options above and beside full Kubernetes, used in workload-fit
analysis (`clusterless-and-faas-fit-analysis`). Not every workload needs a cluster:
stateful workloads usually belong on managed services [P006], and short event-driven jobs
fit FaaS or clusterless containers.

## Compute option taxonomy

| Option | What it is | Best fit | Examples |
|---|---|---|---|
| **Full managed Kubernetes** | You manage workloads via kubectl; provider runs the control plane | Long-running services needing orchestration, scaling, scheduling | GKE, EKS, AKS |
| **Clusterless containers** | A cluster exists under the hood but you have no kubectl access; you specify an image + CPU/memory | Self-contained, long-running compute or batch jobs where managing worker nodes isn't justified; build containers; demand bursts | AWS Fargate, Azure Container Instances (ACI), Google Cloud Run |
| **FaaS (functions as a service)** | Run code per event with no server provisioning; billed per execution time | Short, standalone, event-driven jobs that integrate with cloud services | AWS Lambda, Google Cloud Functions/Run, Azure Functions |
| **Funtainers (FaaS on Kubernetes)** | Run functions on an existing cluster | Teams already on Kubernetes wanting event-driven functions | OpenFaaS, Knative, Kubeless |
| **Managed database service** | Provider runs the stateful datastore | Databases and other stateful workloads | (cloud-managed DBs) |

## Clusterless service notes

| Service | Notes |
|---|---|
| **AWS Fargate** | "EC2 but you get a container"; define a task and launch it, no node provisioning; per-second billing on CPU/memory; suits simple long-running or batch jobs and build containers |
| **Azure ACI** | Similar to Fargate; integrates with AKS to burst extra Pods or run ad-hoc batch jobs without idle nodes |
| **Google Cloud Run** | Container-as-a-service; publish an image, runs per web request / Pub/Sub message; containers time out by default after 5 minutes (extendable to 60) |

## Placement rules

- **Stateful (databases):** prefer a managed database service. Replicas are not
  interchangeable — each has unique state requiring coordination for restarts, consistency,
  and schema changes — so enterprise-grade reliability inside Kubernetes needs a large
  engineering investment that managed services absorb [P006, CL020].
- **Short/event-driven:** prefer FaaS or clusterless; mind run-time limits (e.g. Lambda's
  15-minute cap, Cloud Run's default 5-minute timeout).
- **Microservices are a deliberate choice,** not a default. They are inherently complex
  distributed systems, hard to observe and prone to surprising failures; a containerised
  monolith can deliver real value and serve as a transitional step [P007, CL027].

## Provenance

Derived from principles P006 and P007 (claims CL020, CL027) of *Cloud Native DevOps with
Kubernetes, 2nd Edition*. Source is `distillation-only`: paraphrased, not quoted.
