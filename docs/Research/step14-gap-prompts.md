# Step-14 gap research prompts (3 open academic gaps)

Three self-contained research prompts — one per HIGH/ACADEMIC gap blocking Step 14 (runtime
retrieval for generated expert agents). Each carries the full background, the precise gap, and a
literature-search instruction. Paste any one into a research agent / literature tool.

Shared context (prepend if the tool has no memory of the project):

> We build *expert subagents* by distilling books/papers into a structured layer: atomic **claims**
> (source-anchored statements) → **principles** (operational rules, each `derived_from` specific
> claims, typed, with applies_when/does_not_apply_when, confidence). A package may hold 300–600
> principles. At runtime today we **bake** a top-N importance-ranked slice into a static system
> prompt ("distill"); the rest sit in files. We measured that dumping *all* principles into the
> prompt does NOT improve review quality vs a lean top-25% slice — grounding (faithfulness to the
> source-under-review) is equal-or-worse with more principles, because a large always-on instruction
> set dilutes attention. We want to move to **runtime retrieval**: keep the full principle store and
> retrieve only the principles relevant to the current task, so more principles help instead of
> diluting. The three questions below are what the literature does NOT yet answer for this case.

---

## Prompt 1 — G1: distilled-in-prompt vs runtime-retrieval for an agent's OWN knowledge

Background: An LLM agent can hold its specialized knowledge two ways — (a) **distilled** into the
system prompt / parameters as always-on rules, or (b) kept in an external store and **retrieved at
answer time** (RAG). For general world knowledge, RAG vs parametric is well studied. But for an
agent's **own curated, distilled principle set** (a few hundred operational rules it authored from
sources, not an open web corpus), there is no empirical comparison: when does baking them in beat
retrieving them, as a function of store size, task diversity, and instruction-following capacity?
The "Expert Mind" line proposes a self-distilled store but reports no head-to-head results.

The gap: **No study empirically compares an agent's own distilled-in-prompt principle store against
runtime retrieval of those same principles, measuring task quality / grounding vs store size.**

Search task: Find papers (2023–) that empirically compare in-context/parametric distilled knowledge
vs runtime retrieval *for a model's own curated knowledge set* (not open-domain QA). Keywords:
self-RAG, parametric vs retrieved knowledge, in-context vs retrieval tradeoff, instruction
dilution / instruction-following degradation with prompt length, memory-augmented agents, agent
self-distillation, "when does RAG help vs hurt", long-context vs RAG. For each: does it measure the
crossover point (store size where retrieval starts to win), and on what task? Report whether the
exact comparison exists, the closest analogues, and any measured dilution thresholds.

---

## Prompt 2 — G2: retrieval over a typed argument / principle graph

Background: Our principle store is naturally a **graph of typed claims**: nodes are
principles/claims; edges are argumentative/operational relations — `supports`, `contradicts`,
`refines`, `specializes`, `decision-criterion`, `applies-when`. We want graph-aware retrieval: given
a task (e.g. "review this code"), traverse this argument graph to pull the relevant, mutually
consistent principle set (e.g. follow `applies-when` edges, surface `contradicts` pairs so the agent
sees the tension). GraphRAG and knowledge-graph retrieval exist — but every method we found operates
over **entity knowledge graphs** (people, places, organizations, factual relations), not over
**argument/claim graphs** with stance/defeasible edges.

The gap: **Retrieval over a typed argument/principle graph (claims with supports / contradicts /
refines / decision-criterion edges) is unstudied; all graph-RAG evidence uses entity KGs.**

Search task: Find work (2022–) on retrieval or traversal over **argument graphs, claim graphs, or
debate/stance graphs** for answer generation — as opposed to entity KGs. Keywords: argument graph
retrieval, claim graph, argumentation mining + retrieval, GraphRAG over non-entity graphs, stance/
defeasible-edge traversal, structured-knowledge retrieval with typed edges, Personalized PageRank
over claim graphs, retrieval over discourse/rhetorical structure. For each: what graph type, what
edge semantics, does it retrieve mutually-consistent subsets, and could the method transfer to a
supports/contradicts/refines principle graph? Report whether argument-graph retrieval exists or only
entity-KG analogues do.

---

## Prompt 3 — G3: graph-native per-claim citation / provenance at answer time

Background: Faithfulness is core to us — every principle is `derived_from` specific source claims,
each anchored to a real source passage. When the agent answers using a retrieved principle, we want
it to **cite the exact source passage that grounds that principle** (per-claim provenance), so the
advice is verifiable back to the book/paper. Flat-passage RAG citation (cite the retrieved chunk) is
studied (e.g. generate-then-cite, attributed QA). HippoRAG-style methods keep passages alongside a
graph. But **graph-native per-claim citation** — where the retrieval unit is a graph node
(principle) yet the citation must resolve to the underlying source passage with provenance preserved
through the graph — is open.

The gap: **Graph-native per-claim citation/provenance is open — how to keep verifiable
source-passage citations when the retrieval/reasoning unit is a graph node, not a passage.**

Search task: Find work (2022–) on **attribution / citation / provenance in graph-based or
structured retrieval** — where answers cite back to source passages through a knowledge/claim graph,
not just the retrieved text chunk. Keywords: attributed generation, citation generation, grounded
QA with provenance, knowledge-graph provenance, per-claim attribution, HippoRAG passages, FRONT /
fine-grained citation, faithfulness with structured retrieval, provenance-preserving graph
retrieval. For each: is the citation unit a passage or a node, and how is passage-level provenance
preserved through graph traversal? Report whether graph-native per-claim citation exists, or whether
the state of the art is "keep passages and cite those" (HippoRAG-2 / FRONT style) adapted to graphs.

---

## How to use the results

For each gap the answer is one of:
1. **Closed** — a paper directly addresses our case → adopt its method, cite it.
2. **Approximated** — only adjacent methods exist (entity-KG retrieval, flat-passage citation) →
   adapt them; note the residual novelty.
3. **Still open** — confirms we'd be charting new ground → build behind a per-package *measurement*
   (answer G1 empirically on our own packages instead of citing a paper).

Expected (per the prior internal assessment): all three are likely 2 or 3, not 1 — these are
"no-study-exists" gaps. The value of the search is the **adjacent methods** to adapt and confirmation
the gap is still open, not a silver-bullet paper.
