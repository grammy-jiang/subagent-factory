---
name: ousterhout-red-flags-catalogue
kind: reference
status: ready
provenance:
  principles:
  - P028
  - P027
  - P019
  - P030
  - P011
  claims:
  - C00116
  - C00280
  - C00303
  - C00304
  - C00305
  - C00306
  - C00307
  - C00308
  - C00327
  - C00328
  - C00329
  - C00346
  - C00347
  - C00350
  - C00351
  - C00381
  source_anchors:
  - 5e67c59e0e18-c0001
  - aca1f3444508-c0000
  - aca1f3444508-c0001
  authored_from_digest: 09027404bdd41f0a5f35cd85cf0260a1addc6bcbee77f3861f0cfedc4523b851
---

# Ousterhout Red-Flags Catalogue

A recognition checklist of design red flags drawn from Ousterhout's complexity and
deep-module model. A red flag is a visible symptom that, when present, signals that
complexity is being added or hidden information is leaking. Red flags are heuristics for
*where* to look, not automatic failures (clm-025; PRC-013). Use this catalogue with
`skills/assess-module-complexity-and-depth/` and `skills/detect-code-smells/`.

## How to read this catalogue

Complexity is anything about a system's structure that makes it harder to understand or
modify (clm-001; PRC-001). It has two underlying **causes** — *dependency* (an element cannot
be understood or changed in isolation) and *obscurity* (important information is not visible
from the structure) — and shows up through three **symptoms** — *change amplification*, *high
cognitive load*, and *unknown unknowns*, the last being the most dangerous because the
affected developer cannot see it (clm-002; clm-003). Every red flag below maps to at least one
cause and one symptom, and is answered by the governing remedy: **information hiding** —
encapsulate the design decisions most likely to change so callers never depend on them
(clm-010; PRC-006).

## Primary red flags

The six flags an interface-depth review tests first. The IDs (RF-1…RF-6) match the scan table
in `assess-module-complexity-and-depth`.

| # | Red flag | Signal to look for | Cause | Dominant symptom | Grounding |
|---|---|---|---|---|---|
| RF-1 | **Shallow module** | The interface is about as complex as the implementation it wraps; the module hides little, so callers gain little abstraction | Obscurity / poor information hiding | High cognitive load | clm-008; PRC-005 |
| RF-2 | **Information leakage** | One design decision (file format, wire protocol, internal data structure) is reflected in two or more modules, forcing them to change together | Dependency | Change amplification | clm-011; PRC-006 |
| RF-3 | **Temporal decomposition** | Module boundaries mirror the *order operations execute* (read → parse → validate → write) instead of the information each part owns and hides | Dependency | Change amplification | clm-012; PRC-006 |
| RF-4 | **Pass-through method** | A method does nothing but forward its arguments to another method with the same or near-identical signature, adding no behaviour and hiding nothing | Obscurity | High cognitive load | clm-014; PRC-021 |
| RF-5 | **Classitis** | Many small classes each contribute minimal functionality; the belief that classes must be tiny multiplies interface and boilerplate overhead | Obscurity | High cognitive load | clm-009; PRC-021 |
| RF-6 | **Exposed volatile decision** | A decision likely to change — algorithm, storage format, external protocol detail — is visible in the public interface rather than hidden behind it | Obscurity / dependency | Unknown unknowns | clm-010; PRC-006 |

## Extended recognition checklist

The broader Ousterhout red-flag set (clm-025). Several overlap with the primary flags and with
Fowler smells; when a finding matches more than one entry, cite each — convergence strengthens
the finding.

| Red flag | Signal to look for | Grounding |
|---|---|---|
| **Shallow module** | Interface complexity ≈ implementation complexity (see RF-1) | clm-008 |
| **Information leakage** | A shared design decision reflected across module boundaries (see RF-2) | clm-011 |
| **Temporal decomposition** | Structure follows execution order, not information ownership (see RF-3) | clm-012 |
| **Overexposure** | The interface forces callers to learn details they should not need — commonly configuration or internal modes pushed onto the caller | clm-008; clm-015 |
| **Pass-through method** | A method forwards a call without adding behaviour (see RF-4) | clm-014 |
| **Repetition** | The same snippet of logic appears at several call sites with no shared extraction | clm-016 |
| **Special-general mixture** | Special-purpose code is interleaved with the general-purpose mechanism it specialises, so neither can be understood alone | clm-016 |
| **Conjoined methods** | Two methods can only be understood by reading them together; they are coupled but presented as separate | clm-003 |
| **Vague name** | A name so broad it conveys no precise image of the entity | clm-021 |
| **Hard-to-pick name** | No precise name can be found — usually because the underlying entity is not cleanly defined | clm-021 |
| **Hard-to-describe** | The module's behaviour cannot be summarised without enumerating exceptions and special cases | clm-008 |
| **Nonobvious code** | A reader must work hard to infer what code does; its side effects or assumptions are not visible locally | clm-023 |

## Remedies

Each remedy is a structural move, not replacement code. Apply the smallest one that removes the
flag's root cause; bound every change to present known requirements (PRC-007).

| Remedy | What it does | Answers | Grounding |
|---|---|---|---|
| **Information hiding** | Encapsulate the design decisions most likely to change inside one module so callers never depend on them | RF-2, RF-3, RF-6, overexposure | clm-010; PRC-006 |
| **Pull complexity downward** | Let the implementer absorb unavoidable complexity rather than expose it; a simple interface matters more than a simple implementation | RF-1, overexposure | clm-015; PRC-005 |
| **Deepen by combining** | Bring code together when pieces share information, when it simplifies the interface, or when it removes duplication; merge shallow classes that share an information domain | RF-4, RF-5, repetition | clm-016; PRC-021 |
| **Separate special from general** | Split special-purpose code out from the general mechanism it specialises | special-general mixture | clm-016 |
| **Bounded general-purpose interface** | Shape the interface to the present *family* of known needs rather than one narrow case — often simpler and deeper — but never to a speculative future need | RF-1, overly narrow interface | clm-013; PRC-026 |
| **Rename to a precise image** | Replace a vague or hard-to-pick name; if no precise name exists, treat it as evidence the entity itself needs redefining | vague / hard-to-pick name | clm-021; PRC-016 |
| **Make code obvious** | Restructure or rename until behaviour is clear from a local read; nonobvious code raises cognitive load and unknown unknowns | nonobvious code | clm-023 |

## Provenance

Derived from *A Philosophy of Software Design* (Ousterhout, source
`a-philosophy-of-soft-5e67c59e`, `distillation-only`) via principles PRC-001, PRC-005, PRC-006,
PRC-021, and PRC-026 and their supporting claims (clm-001–clm-003, clm-008–clm-016, clm-021,
clm-023, clm-025), grounded in source anchors `a-philosophy-of-soft-5e67c59e-h0020` through
`-h0623` as recorded in `principles/principles.yaml` and `analysis/claims.jsonl`. All content is
paraphrased; no verbatim source wording appears in this file.
