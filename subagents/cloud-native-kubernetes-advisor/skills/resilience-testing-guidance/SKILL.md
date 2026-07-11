---
name: resilience-testing-guidance
kind: skill
status: ready
provenance:
  principles:
  - P002
  - P003
  - P008
  - P011
  claims:
  - CL037
  - CL038
  - CL040
  - CL024
  - CL043
  source_anchors:
  - cloud-native-devops-ed89eef5-h0106
  - cloud-native-devops-ed89eef5-h0107
  - cloud-native-devops-ed89eef5-h0110
  authored_from_digest: 1eb6b311d985a61ed2ec0073a7c8e4de43f8a4028e70be6363ff227a8f826522
---

# Resilience testing guidance

## Purpose

Verify that a cluster's high-availability design actually survives failure, rather than
assuming it does. HA must be tested, not declared: control-plane quorum, worker-node loss,
and availability-zone loss should each be exercised. For self-hosted clusters this is an
ongoing obligation, not a one-time check [P011].

## When to use

- Auditing a cluster's HA readiness before or during production.
- Reviewing control-plane node count, worker topology, or replica configuration.
- Establishing a recurring resilience-testing cadence for a self-managed cluster.

Do not use this skill to choose a managed offering or installer (use
`evaluating-managed-kubernetes-offerings` / `selecting-self-hosting-installers`).

## Procedure

1. **Check control-plane quorum sizing.** Production control planes need a minimum of
   three nodes. etcd uses a quorum that requires more than half of its replicas to stay
   available; with two nodes, any single failure loses quorum entirely. Control-plane
   failure stops new deployments and breaks controllers even while existing Pods keep
   running [P002, CL037, CL038]. (Non-production or single-node local clusters are
   exempt.)
2. **Check worker-node distribution.** Worker nodes should span at least two, preferably
   three, availability zones. Zone-level outages are rare but real; concentrating all
   nodes in one zone means a zone failure takes down every workload [P003, CL040].
3. **Confirm replica redundancy.** A single worker-node failure is tolerated only when
   applications run with more than one replica, so Kubernetes can reschedule the node's
   Pods onto survivors. Verify replicas are configured before relying on this [P008,
   CL024].
4. **Test, don't assume.** During a maintenance window or off-peak:
   - Reboot a worker node and confirm no user-visible impact.
   - Reboot a control-plane node and confirm `kubectl` and the cluster keep working.
   A production-grade cluster should survive both. (Managed services such as EKS, AKS, and
   GKE do not expose control-plane nodes for this test — that work is the provider's.)
5. **Make it recurring for self-hosted clusters.** Self-hosting means continuous
   monitoring, alerting, keeping up with releases, and regular resilience testing — e.g.
   automated chaos tools that randomly kill nodes, Pods, or network connections. Where a
   cloud provider's real-world failures already exercise the cluster, a dedicated chaos
   tool may be unnecessary [P011, CL043].
6. **Report gaps against the readiness checklist** and name the remediation (add a third
   control-plane node, redistribute workers across zones, raise replica counts, schedule
   chaos tests). See `production-readiness-checklist`.

## Inputs

- Current control-plane node count.
- Worker-node topology across availability zones.
- Replica counts / pod disruption budgets for production workloads.
- Whether the cluster is self-hosted or managed (determines who owns control-plane tests).

## Output

A production-readiness assessment of HA — control-plane quorum, zone distribution, replica
redundancy — naming gaps, the failure tests to run, and a resilience-testing cadence for
self-hosted clusters.

## References

- `production-readiness-checklist`
- `kubernetes-control-plane-components`

## Provenance

Derived from principles P002, P003, P008, and P011 (claims CL037, CL038, CL040, CL024,
CL043) of *Cloud Native DevOps with Kubernetes, 2nd Edition*. Source is
`distillation-only`: paraphrased, not quoted.
