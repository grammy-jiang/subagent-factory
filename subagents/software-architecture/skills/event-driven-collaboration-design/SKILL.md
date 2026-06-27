---
name: event-driven-collaboration-design
kind: skill
status: ready
provenance:
  principles:
  - P007
  - P024
  - P049
  - P047
  claims:
  - C00204
  - C00207
  - C01295
  - C01297
  - C01336
  - C01346
  - C01254
  - C01255
  evidence:
  - E00055
  - E00056
  - E00200
  - E00201
  - E00207
  - E00208
  - E00198
  - E00199
  source_anchors:
  - 508117177502-c0008
  - 508117177502-c0009
  - d95ad6b6daba-c0012
  - d95ad6b6daba-c0014
  - d95ad6b6daba-c0015
  - d95ad6b6daba-c0009
  authored_from_digest: 4d735c274671f70169dc590a117b74514102bc83291365207abc38dbedadffca
---

# Event-driven collaboration design

## Purpose

Use events as a basis for collaboration to decouple services from direct request/response calls —
but treat loose coupling as a deliberate trade-off, not an absolute good. Letting services react
to facts that have happened, rather than command each other directly, reduces the coupling created
by point-to-point calls. Yet some essential data coupling between services is unavoidable, and
over-decoupling can hide necessary dependencies, so the choice between event notification and state
transfer must be made consciously. This skill designs that collaboration.

## When to use

- The caller is designing how services collaborate and is weighing events vs. direct calls.
- A design pursues decoupling without acknowledging the data dependencies that remain.
- Point-to-point request/response chains have made services brittle and tightly bound.

Do not invoke when the interaction is wholly in-process within a single component.

## Procedure

1. **Map the current collaboration.** Identify where services command each other directly
   (request/response) and the coupling that creates.
2. **Identify event opportunities.** Find interactions that are really "react to a fact that
   happened." Those can become events, letting consumers act without the producer calling them
   and reducing point-to-point coupling.
3. **Surface the essential data coupling.** Determine what data a consumer genuinely needs from
   the producer. This coupling is unavoidable; name it rather than pretending events remove it.
4. **Choose notification vs. state transfer — consciously.**
   - *Event notification* — tell consumers something happened, minimal payload; lowest coupling,
     but consumers may need to call back for data (reintroducing coupling).
   - *Event-carried state transfer* — carry the needed data in the event; consumers stay
     autonomous, at the cost of duplicated/derived state to keep consistent.
   Pick per interaction based on the essential data coupling found in step 3.
5. **Resist over-decoupling.** Flag designs that chase maximal decoupling to the point of hiding
   real dependencies; recommend making the dependency explicit instead.
6. **State the trade-off.** For the chosen design, name what coupling it removes and what it costs
   (e.g. eventual consistency, duplicated state, harder end-to-end tracing).

## Inputs

- The services involved, how they currently collaborate, and the data each needs from the others.

## Output

A collaboration design that converts suitable direct calls to events, names the essential data
coupling that remains, chooses notification vs. state transfer per interaction deliberately, and
states the trade-off each choice carries. Decoupling is treated as a conscious decision, not a goal
to maximize.

## References

- [Laws of software architecture](../../references/laws-of-software-architecture.md) — coupling
  decisions as deliberate trade-offs.

## Provenance

Distilled from principle(s) **P005/P019/P042/P040**, claims **C00267/C00270/C01804/C01806/C01845/C01855**, evidence **E00057/E00058/E00261/E00262/E00267/E00268**, anchored in the cited architecture sources (`sources/anchors/`). Source is `distillation-only`: content is paraphrased, never quoted verbatim.
