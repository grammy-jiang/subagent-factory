---
name: agent-memory-and-reflection
kind: skill
status: ready
provenance:
  principles: [P001, P002, P012, P018, P031, P048, P049, P058]
---

# Agent Memory and Reflection

## Purpose

This skill reviews and advises on how an LLM-based agent engineers memory: what it stores, how
it retrieves a working subset of that store for each decision, how it synthesizes raw experience
into higher-level understanding, and how it plans so behaviour stays coherent over time. It
treats memory as a retrieval-and-reflection system, not a growing transcript that gets replayed
wholesale or reduced to one running summary, and it checks the practical cost — token spend and
latency — of running that system at the scale the caller intends. Every finding names the
failure mode at stake, the principle that addresses it, and the trade-off the caller must weigh
(P001, P002, P012, P018, P031, P048, P049, P058).

## When this applies

- The caller is designing or reviewing an agent that must stay consistent with its own history
  across many turns, sessions, or units of simulated time, and is deciding how to store that
  history.
- The agent already keeps a growing log of experience and the caller needs a way to decide what
  to condition each response or action on, instead of replaying the whole log every time.
- The caller wants the agent to draw higher-level conclusions from its own experience — a
  preference, a relationship, a pattern — rather than only reacting to the latest single event.
- The caller is designing a multi-agent or social simulation and wants to know whether
  group-level outcomes need to be scripted or can be left to emerge from individual agents.
- The caller is running or reviewing a comparative study of agent believability or behaviour
  quality and needs the scoring method checked.
- The caller is scaling a memory-driven agent from a single demonstration instance toward many
  concurrent agents or real-time response, and needs the cost implications reviewed.

## Procedure

1. **Confirm memory is actually warranted (P018 applies_when).** Ask whether the agent must stay
   consistent with its own history across turns, sessions, or simulated time. A stateless,
   single-turn tool call does not need a persistent memory stream; if the agent genuinely has no
   such requirement, note that and move to reviewing its other subsystems instead of forcing a
   memory design onto it.
2. **Check the memory representation (P018).** The store should be a persistent, natural-language
   stream of memory objects, not a database of opaque structured state and not a single mutable
   field that gets overwritten. Each object should carry a natural-language description of what
   happened, a creation timestamp, and a most-recent-access timestamp, and its most basic unit
   should be an observation — something the agent directly perceived, whether its own action or
   another agent's or object's behaviour. Flag a design that stores only structured state, or
   that discards history rather than appending to it.
3. **Verify retrieval replaces replay (P048).** The design must not place the entire memory
   stream into the prompt on every turn, and must not substitute a single running summary for
   retrieval. The whole-stream approach eventually exceeds the context window and, even while it
   still fits, dilutes the model's attention across mostly irrelevant material; a blanket summary
   loses the specific detail a good answer needs and produces generic output instead. The
   corrective is a retrieval function that takes the agent's current situation and returns only a
   compact, relevant subset.
4. **Check the retrieval scoring function (P001).** That subset should be chosen by scoring each
   candidate memory on three factors — how recently it was accessed, how important it is on its
   own terms, and how relevant it is to the present query — combined into one normalized score so
   no single factor dominates by scale alone, with the weighting tuned to the task rather than
   fixed, and the highest-scoring memories taken up to what the context window allows. Recency is
   commonly implemented as decay from time since last access, importance as a rating the model
   assigns once when the memory is created (independent of any particular later query), and
   relevance as similarity between the memory's own content and the current query. Flag a design
   that uses only one of the three factors, or that never revisits the weighting for the task at
   hand.
5. **Check for a reflection step (P012).** Raw observations alone are not enough: an agent
   limited to them struggles to generalize or answer questions that require synthesizing many
   experiences. The design should periodically generate higher-level reflections from recent
   memory — triggered by an accumulating signal (such as a running sum of importance scores
   crossing a threshold) rather than a fixed clock, drawing a small set of salient questions from
   a recent window of memories, retrieving evidence for each question, and having the model state
   the resulting insight while citing the specific memories that support it. Because a reflection
   is itself a memory, it should re-enter the stream and be retrievable like any observation, and
   a later reflection may synthesize earlier reflections as well as raw observations.
6. **Check the planning horizon and structure (P031).** An agent optimized only to pick whatever
   action looks most believable moment to moment tends to drift into behaviour that is locally
   plausible but globally incoherent — repeating an already-completed activity, or oscillating
   without overall progress, are the classic symptoms. Long-horizon coherence needs an explicit
   plan built top-down: a broad agenda derived from the agent's own standing self-description and
   its immediately preceding history, then recursively broken into progressively shorter,
   time-boxed chunks down to whatever granularity execution needs. Confirm plans are themselves
   stored in and retrievable from the memory stream, and that the design allows a plan to be
   revised mid-course rather than treated as fixed once generated.
7. **If the design is multi-agent or social, check whether group behaviour is being
   over-scripted (P049).** Coordinated group outcomes — information spreading from one agent to
   others, previously unacquainted agents becoming acquainted, several agents independently
   converging on the same activity — can emerge from giving a single agent a minimal seeded
   intent and letting ordinary memory-driven interaction carry it through the group; this need
   not be authored as an explicit multi-agent protocol. Flag a design that hand-scripts the group
   outcome directly, since that adds authoring cost the architecture should absorb and
   misrepresents what the architecture itself is contributing.
8. **If a comparative believability or behaviour study is planned or under review, check the
   scoring method (P058).** Raw human rankings across conditions are not directly comparable as
   collected. The design should convert ranked comparisons into interval ratings using a
   pairwise, skill-rating-style scoring model, test differences with a significance method suited
   to ranked data plus a correction for running many pairwise comparisons, and include a
   human-authored condition as a baseline so scores are grounded against real behaviour and not
   only against each other. Flag a report built on a raw mean rank or a single aggregate score
   with no baseline condition and no correction for multiple comparisons.
9. **Check the token-cost and latency budget (P002).** A memory-driven agent issues multiple
   model calls per action — reading memory, reflecting, planning, and acting can each be their
   own call — and this compounds quickly once the design moves from a single demonstration agent
   to many, or toward real-time response. The design should show it has budgeted for this:
   caching a reusable self-description or summary instead of regenerating it every prompt,
   decomposing plans only as far as needed to act now rather than fully up front, batching
   generation where several outputs can be produced together, and parallelizing independent
   agents rather than running them strictly one after another. Flag a design validated only at
   small, non-real-time scale that is being scaled up without re-checking these costs.
10. **Synthesize findings.** For each gap found in steps 2 through 9, state the failure mode it
    risks, the principle that addresses it, and the trade-off the fix costs — for example, tuned
    retrieval weighting needs task-specific tuning effort, reflection adds model calls, and
    long-horizon planning adds authoring and replanning logic. Hand the actual weighting,
    thresholds, and implementation back to the caller's team; this skill informs the design, it
    does not build it.

## Anti-patterns

- **Whole-stream prompt dump.** Feeding the agent's entire accumulated history into every
  prompt. It eventually exceeds the context window, and well before that it dilutes the model's
  attention across mostly irrelevant material (P048).
- **Summarize-everything.** Replacing retrieval with a single rolling summary of all experience.
  It reads smoothly but lacks the specific detail a query-relevant answer needs, so responses
  turn generic (P048).
- **Single-factor or untuned retrieval.** Scoring memories on relevance alone, or recency alone,
  or holding one fixed weighting across every task instead of combining recency, relevance, and
  importance and tuning the balance to what the task needs (P001).
- **Observation-only memory with no reflection.** Storing every event but never synthesizing
  across them, so the agent can recite what happened but cannot answer a question that requires
  connecting several experiences into an inference (P012).
- **Next-action-only planning.** Choosing whatever action looks most believable in the moment
  with no longer-horizon plan behind it, which reliably produces locally sensible but globally
  incoherent behaviour (P031).
- **Hand-scripted group behaviour.** Authoring a multi-agent outcome directly as a scripted
  sequence instead of seeding one agent's intent and letting memory-driven interaction carry it
  through the group (P049).
- **Unweighted believability reporting.** Reporting a raw mean rank or "won more comparisons"
  from a ranking study with no interval-rating conversion, no significance test suited to ranked
  data, no multiple-comparison correction, and no human-authored baseline to ground the scale
  (P058).
- **Unbudgeted scale-up.** Moving a memory-driven design from one demonstration agent to many
  concurrent agents, or to real-time response, without re-checking token cost and latency, and
  without caching, just-in-time planning, batching, or parallelization to keep it tractable
  (P002).

## Principles covered

- **P001** — Score candidate memories by recency, relevance, and importance together, tune the
  weighting to the task, and retrieve only the top-scoring subset that fits the context window.
- **P002** — Budget for the token cost and latency of memory-driven agents at scale, using
  caching, just-in-time plan decomposition, batched generation, and parallelization to keep it
  tractable.
- **P012** — Periodically synthesize raw observations into higher-level reflections, triggered by
  an accumulating-importance signal, so the agent can generalize and answer questions that need
  synthesis.
- **P018** — Store agent experience as a persistent natural-language memory stream of timestamped
  observation records, not opaque or overwritten state.
- **P031** — Plan over a long horizon, top-down and recursively decomposed, so behaviour stays
  coherent rather than only locally believable.
- **P048** — Never place the whole memory stream in the prompt or replace retrieval with a
  summary of everything; retrieve only the relevant subset.
- **P049** — Expect coordinated group behaviour to emerge from a single agent's seeded intent
  plus ordinary memory-driven interaction, rather than needing to be scripted.
- **P058** — Convert ranked believability comparisons into interval ratings with a significance
  test suited to ranked data and a human-authored baseline, not a raw ranking or aggregate alone.

## Inputs

- A description of the agent's memory representation, retrieval function, reflection logic,
  and/or planning approach under review, or the specific decision the caller wants advice on.
- The agent's task and environment: whether it must remain consistent across turns, sessions, or
  simulated time; whether it is single- or multi-agent; and whether real-time or many-agent scale
  is a target.
- What is already decided versus still open, so the review targets what can still change.

## Output

A findings or recommendation list scoped to the agent's memory-and-reflection subsystem, each
entry naming the failure mode at stake (see Anti-patterns), the principle applied (see
Principles covered), and the trade-off it implies, ending with a next step handed back to the
caller's team.

## References

- `references/agent-engineering-principles-index.md` — index of this package's agent-engineering
  principles, including the full statements for the principles cited above.

## Provenance

Distilled primarily from "Generative Agents: Interactive Simulacra of Human Behavior" (2023) for
the memory-stream representation, retrieval scoring, reflection, planning, emergent social
behaviour, and believability-evaluation methodology this skill reviews against; corroborated by
"A Survey on Large Language Model based Autonomous Agents" (2024) for the recency/relevance/
importance memory-reading formulation and the multi-call inference-cost driver. Grounded in
P001, P002, P012, P018, P031, P048, P049, P058. Distillation-only sources — paraphrased
throughout, no verbatim quotation.
