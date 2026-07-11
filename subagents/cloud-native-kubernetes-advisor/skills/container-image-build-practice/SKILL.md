---
name: container-image-build-practice
kind: skill
status: ready
provenance:
  principles:
  - P004
  claims:
  - CL032
  source_anchors:
  - cloud-native-devops-ed89eef5-h0074
  authored_from_digest: 9bd2a3a84a74c7d90a5caa1b796a23a43997910ba7a1af9bd40d38e755134a8f
---

# Container image build practice

## Purpose

Guide a team to build minimal, production-ready container images using multi-stage
Dockerfile builds. Keeping build toolchains, compilers, and intermediate artifacts out of
the final image makes deployment faster (smaller images upload, download, and start
quicker) and shrinks the security attack surface, because fewer included programs mean
fewer potential vulnerabilities [P004].

## When to use

- A team is writing or reviewing a Dockerfile for any language or runtime.
- An engineer is producing a starter Dockerfile or first container for a new service.
- Image size, startup time, or container security posture is being assessed.

Do not use this skill to decide whether the workload belongs in a container at all (use
`clusterless-and-faas-fit-analysis`) or to design its rollout (use
`deployment-strategy-selection`).

## Procedure

1. **Separate build from runtime.** Use a multi-stage Dockerfile: a build stage that
   contains the language environment, compiler, and dependencies, and a final stage that
   contains only the runnable artifact [P004, CL032].
2. **Make the final stage minimal.** Copy only the built binary or runtime artifact into
   a small base (e.g. `scratch` or a slim distro). Exclude the toolchain entirely — it is
   needed to build, not to run. A minimal image can be orders of magnitude smaller than
   one that ships the full build environment.
3. **Justify the size reduction by its two benefits.** Faster deployment (upload,
   download, startup) and a reduced attack surface. Frame both when advising — do not
   present minimalism as cosmetic [CL032].
4. **Note language fit.** Compiled languages that produce self-contained executables suit
   `scratch`-based minimal images most directly; interpreted runtimes will need their
   interpreter in the final stage but should still drop build-only tooling.
5. **Carve out the debug exception.** Development or troubleshooting images may
   intentionally retain a shell and tools; mark those as non-production [P004
   does-not-apply].
6. **Mark produced artifacts as starting points.** Any Dockerfile produced is a starter
   to adapt and validate, not a production-final artefact.

## Inputs

- Target language/runtime and whether it compiles to a self-contained binary.
- Whether the image is for production or for debugging.
- Any base-image or registry constraints the team must meet.

## Output

A multi-stage Dockerfile recommendation (or a minimal starter Dockerfile) that isolates
the build toolchain from a minimal runtime image, with the deployment-speed and
attack-surface rationale stated, and the artefact marked as a starting point.

## References

- `production-readiness-checklist`

## Provenance

Derived from principle P004 (claim CL032) of *Cloud Native DevOps with Kubernetes, 2nd
Edition*. Source is `distillation-only`: paraphrased, not quoted.
