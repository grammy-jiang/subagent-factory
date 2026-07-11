---
name: kubernetes-control-plane-components
kind: reference
status: ready
provenance:
  principles:
  - P002
  claims:
  - CL037
  - CL038
  source_anchors:
  - cloud-native-devops-ed89eef5-h0106
  authored_from_digest: 653402dfaf0cd4599ffbbbc98015b35cd0de126f4fd849e84562cfc325496112
---

# Kubernetes control-plane components

Reference for the components of a Kubernetes cluster, used when explaining architecture or
auditing HA. The control plane runs the cluster's brain; worker nodes run user workloads.
In a production cluster the control-plane components run across multiple servers for high
availability [P002].

## Control-plane components

| Component | Responsibility |
|---|---|
| **kube-apiserver** | Frontend server for the control plane; handles all API requests |
| **etcd** | The database storing all cluster state — what nodes and resources exist |
| **kube-scheduler** | Decides which node runs each newly created Pod |
| **kube-controller-manager** | Runs resource controllers (e.g. Deployments) |
| **cloud-controller-manager** | Interacts with the cloud provider, managing resources such as load balancers and disk volumes |

## Worker-node components

| Component | Responsibility |
|---|---|
| **kubelet** | Drives the container runtime to start scheduled workloads and monitors their status |
| **kube-proxy** | Routes network traffic between Pods on different nodes and between Pods and the internet |
| **Container runtime** | Starts/stops containers and handles their communication (Docker, containerd, CRI-O) |

There is no intrinsic difference between a node running control-plane components and a
worker node; both run containerised components.

## etcd quorum and control-plane HA

- etcd is replicated across nodes and survives individual node failures **only while a
  quorum — more than half of the original replicas — remains available** [CL037].
- Therefore a production control plane needs a **minimum of three nodes**: with two, any
  single failure loses quorum. Control-plane failure stops new deployments and breaks
  controllers, even though already-running Pods keep running [CL038, P002].

## Provenance

Component descriptions derive from the profile's always-on cluster-architecture knowledge;
the etcd-quorum and control-plane-HA guidance derives from principle P002 (claims CL037,
CL038) of *Cloud Native DevOps with Kubernetes, 2nd Edition*. Source is
`distillation-only`: paraphrased, not quoted.
