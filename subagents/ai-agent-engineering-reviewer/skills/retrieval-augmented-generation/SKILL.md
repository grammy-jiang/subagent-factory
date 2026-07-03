---
name: retrieval-augmented-generation
kind: skill
status: ready
provenance:
  principles: [P040, P055, P056]
---

# Retrieval-Augmented Generation

## Purpose

Review or advise on retrieval-augmented generation (RAG) designs for knowledge-intensive
tasks — generation or question-answering work whose correct output depends on facts a model
cannot reliably keep in its own parameters. This skill covers three tightly linked
decisions: whether the baseline architecture has the right shape (a pretrained
sequence-to-sequence generator conditioned on a neural retriever over a dense external text
index), whether the serving and infrastructure plan accounts for the index's search and
memory cost as something distinct from model-training compute, and whether the training data
handed to the generator has been normalized into targets it can actually learn to produce.
Use it to catch designs that reach for a bigger model instead of grounding, that plan
capacity only around the trainable model, or that train on noisy or malformed answer labels.

## When this applies

- The caller is designing or reviewing a system for a knowledge-intensive task — open-domain
  question answering, fact verification, or any generation task whose answers should reflect
  facts outside the model's own parameters — and is deciding whether, and how, to add
  retrieval grounding.
- The caller is planning deployment, capacity, or cost for a large-scale dense-index RAG
  system and has not yet separated the index's search latency and memory footprint from the
  trainable model's compute budget.
- The caller has question-answering training data with multiple valid answers per question,
  noisy or unsuitable answer variants, or answers expressed as regular expressions, and needs
  those turned into clean generation-training supervision.

## Procedure

1. **Confirm the task is knowledge-intensive.** Ask whether a correct answer depends on facts
   the model cannot be expected to hold in its parameters, or whose provenance and freshness
   matter. If not, retrieval augmentation may be unnecessary complexity — say so and stop
   here.
2. **Check the baseline architecture shape.** For a general-purpose knowledge-intensive
   generation design, the reviewed or proposed system should connect a pretrained
   sequence-to-sequence generator to a neural retriever that searches a dense vector index of
   external text passages, with the retrieved passages conditioning generation (P040). Flag a
   design that instead tries to solve a knowledge-intensive task by scaling the generator
   alone, with no retrieval or grounding mechanism at all.
3. **Check how the retriever is built and indexed.** Prefer a retriever initialized from an
   existing pretrained encoder pair (a query encoder and a passage encoder) over training
   retrieval ability from scratch, since it starts from a working knowledge-access mechanism
   (P040). Confirm the external corpus is split into passages, each passage encoded once and
   stored in a searchable vector index, with retrieval treated as an approximate
   nearest-neighbor search over that index at inference time (P040).
4. **For a large-scale dense-index system, separate the serving/capacity plan from the
   training-compute plan.** Ask, independently of how many accelerators the trainable
   generator needs, how the retrieval index will be searched and where its vectors will live:
   search over a large external index can be fast enough on ordinary processors, so the index
   need not compete with the generator for accelerator memory (P055). Check whether index
   compression has been considered to shrink the memory footprint, and confirm the design
   treats the non-parametric index — large but not itself trained — as separate from the
   trainable model, whose size is what drives accelerator cost (P055).
5. **Review how QA-style supervision was normalized into generation targets.** For a dataset
   where a question has several valid answers, confirm each valid annotation is used as its
   own training pair rather than collapsed into one, since using them separately tends to
   help accuracy a little (P056). For a dataset with noisy or unsuitable answer strings,
   confirm unsupported variants are filtered out — for example by checking whether a
   candidate answer appears in the passages the retriever actually surfaces — before they
   become training targets (P056). For a dataset whose answers are given as regular
   expressions rather than literal text, confirm those patterns have been resolved into
   concrete generation targets (for example, by retrieving supporting passages and picking
   the most frequent string that matches the pattern, with a documented fallback for when no
   match is found) rather than trained on directly (P056).
6. **State the residual trade-offs and hand back.** Name any anti-pattern found
   (Anti-patterns, below), the principle each finding rests on, and the trade-off it
   implies — for example, accepting a small added indexing/serving cost in exchange for
   grounded, updatable knowledge. The design owner decides the final architecture,
   infrastructure, and data pipeline; this skill informs that decision, it does not implement
   it.

## Anti-patterns

- **Scaling the model instead of grounding it.** Growing the generator's parameter count to
  cover a knowledge-intensive task instead of adding retrieval over an external index (P040).
- **Ignoring index-search and memory-footprint serving cost.** At scale, planning capacity
  only around the trainable model's accelerator needs and treating the retrieval index as
  free, instead of planning its search cost and memory footprint separately (P055).
- **Training on unsupported QA targets.** Feeding the generator raw answer strings —
  duplicate-collapsed multi-answer annotations, unfiltered noisy variants, or literal regex
  patterns — instead of normalized, filtered, resolved generation targets (P056).

## Principles covered

- **P040** — Build the RAG baseline as a pretrained seq2seq generator conditioned on a neural
  retriever over a dense external text index.
- **P055** — Plan index-search and memory footprint separately from GPU model-training
  compute when training and serving a large-scale RAG system.
- **P056** — Normalize QA supervision into supported generation targets: use each valid
  annotation, filter out unsupported variants, and resolve regex-form labels before training.

## Inputs

- The knowledge-intensive task and why the answer needs external grounding, the proposed or
  existing retriever/generator architecture, the external corpus and its scale, the planned
  serving/infrastructure setup, and the training data's answer format (single, multi-answer,
  noisy-variant, or regex).

## Output

A finding list naming any architecture, serving-cost, or supervision-normalization gap, the
principle each finding applies, the trade-off it implies, and a concrete next step — handed
back to the design owner for implementation.

## References

- `references/agent-engineering-principles-index.md` — the full principle index, including
  P040, P055, and P056 in context with the package's other agent-engineering principles.

## Provenance

Tier 2. Grounded in P040 (baseline architecture), P055 (serving/training-compute planning),
and P056 (QA supervision normalization), distilled from the retrieval-augmented-generation
research source in this package (Lewis et al., "Retrieval-Augmented Generation for
Knowledge-Intensive NLP Tasks," 2020; `distillation-only`). Paraphrased throughout — no
verbatim quotation.
