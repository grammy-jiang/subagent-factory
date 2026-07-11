# cloud-native-kubernetes-advisor

**Version:** 0.1.0  
**Tier:** 1  
**Status:** draft  

## Purpose

Advises engineering teams on building, deploying, scaling, and operating modern
applications using containers and Kubernetes. Covers managed-vs-self-hosted
cluster decisions, control-plane and worker-node architecture, high-availability
design, container image best practice, workload fit analysis, deployment
strategies, observability requirements, microservices trade-offs, and DevOps
organisational practice.

## Source

Single source: *Cloud Native DevOps with Kubernetes, 2nd Edition* by John Arundel
and Justin Domingus (O'Reilly, 2022). Rights status: distillation-only — no
verbatim quotation is permitted in any generated output.

Source ID: `cloud-native-devops-ed89eef5`

## Modes

| Mode | Trigger |
|------|---------|
| advise | Build-vs-buy questions, hosting strategy, DevOps org decisions |
| compare | Managed services, self-hosting installers, clusterless services, FaaS platforms |
| validate | Production-readiness assessment of cluster design or deployment architecture |
| produce | Starter Dockerfiles, multi-stage build examples, kubectl command sequences |

## Key files

| File | Purpose |
|------|---------|
| `profile.yaml` | Canonical subagent profile (source of truth) |
| `provenance-ledger.md` | Full field-level distillation log |
| `principles/principles.yaml` | 11 evidence-grounded principles (Tier 1) |
| `evidence/evidence-records.yaml` | 20 evidence records (EV001–EV020) |
| `policy/patch-policy.yaml` | Patch safety policy (required for produce mode) |
| `tests/golden-tests.yaml` | 4 golden tests including 1 negative routing |

## Validation

```bash
python -m tools.subagent_factory.cli selfcheck cloud-native-kubernetes-advisor
```

## Review cadence

Annual — managed Kubernetes service features and pricing change rapidly.
Verify current capabilities against provider documentation before acting on
comparisons.

## Limitations

- Managed service feature comparisons reflect the 2022 state of the market;
  verify against current provider documentation before using in production decisions.
- Deep cluster-operations troubleshooting (node repair, networking internals,
  etcd repair) is out of scope; consult a cluster-operations specialist resource.
- Application source code authoring is out of scope.
