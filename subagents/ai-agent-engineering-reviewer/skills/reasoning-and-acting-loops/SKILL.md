---
name: reasoning-and-acting-loops
kind: skill
status: ready
provenance:
  principles: [P003, P005, P007, P008, P010, P011, P016, P017, P026, P028, P032, P041, P042, P057]
---

# Reasoning and Acting Loops

## Purpose

Review or advise on an agent's reasoning-and-acting loop — the interleaving of internal
"thought" steps with environment-facing actions and the observations those actions return — so
that reasoning stays grounded in the environment instead of drifting into unchecked internal
association, and acting stays informed by reasoning instead of degrading into blind action
selection. Use it to check whether thoughts do real operational work, whether their frequency
fits the task, whether the loop grounds knowledge-intensive answers in retrieval or action
observations, whether it stays transparent and correctable, and whether it detects and recovers
from stalls — then to size the demonstration and fine-tuning approach against what prompting
alone can carry.

## When this applies

- The subject under review can emit both an internal reasoning trace and environment-facing
  actions, and the caller wants the interleaving pattern checked (P008).
- A prompt, trajectory, or trace contains intermediate thoughts and the caller wants their
  quality — not just their presence — assessed (P010).
- The task is reasoning-heavy (inference is the bottleneck at every step) or long-horizon with
  many possible actions (decision points are sparse but consequential), and thought frequency
  needs to be matched to that shape (P041).
- The answer depends on external, current, or fine-grained facts, and retrieval or environment
  actions are available to ground it (P011).
- The task is a recognizable shape covered by a playbook below: product/option selection,
  household-object manipulation, tool selection among distinct APIs, multi-hop question
  answering, or fact verification (P003, P005, P007, P016, P017).
- Few-shot demonstrations are being authored, or a trajectory is repeating or producing
  no-effect steps and needs a replanning check (P026, P028).
- The caller is deciding whether prompting is enough or whether to fine-tune on trajectory data
  (P032), or wants the trace exposed for human inspection and correction (P057).

## Procedure

1. **Classify the loop shape.** Confirm the subject actually interleaves thoughts and actions —
   thoughts as language steps that update the working context, actions as environment-facing
   steps that return observations for later reasoning (P008). If either channel is absent, stop
   here and name the anti-pattern (see Anti-patterns) before continuing.
2. **Check thought frequency against task shape.** Reasoning-heavy tasks call for dense
   thought-action-observation cycles; long-horizon tasks with many possible actions call for
   sparser thoughts placed at genuine decision points rather than before every action (P041).
   Flag a mismatch either way: dense thoughts padding a long action horizon spend budget without
   adding decision value, and sparse thoughts on a reasoning-heavy task starve the trace of the
   inference it needs.
3. **Audit thought content, not just thought presence.** Each thought should do operational
   work — decomposing a goal, extracting a salient detail from the last observation, tracking
   progress, applying commonsense, reformulating a failed search, transitioning between plan
   stages, or handling an exception (P010). A thought that only restates the goal or the last
   observation does not count as doing this work.
4. **For decision/manipulation tasks, check thoughts stay capable, not reduced to reminders.**
   Where the environment requires multi-step object, location, or subgoal reasoning, thoughts
   must still decompose goals, apply commonsense search, detect subgoal completion, and choose
   the next subgoal — not collapse into a dense stream of bare environment-state reminders after
   every action (P042). This is a distinct, narrower failure than merely-sparse thoughts: it is
   frequent but empty of the reasoning work step 3 checks for.
5. **Check grounding for knowledge-intensive answers.** When the answer depends on external,
   current, or fine-grained facts, the trace should use retrieval or environment actions to fetch
   evidence, with each observation shaping the next information target, rather than answering
   from unchecked internal association (P011). An answer with no supporting action or observation
   behind it is ungrounded regardless of how confident the prose reads.
6. **Match the task shape to its playbook, if one applies.** See Task playbooks below for
   shopping/product selection, household-object tasks, tool selection, multi-hop question
   answering, and fact verification (P003, P005, P007, P016, P017). Apply the playbook's specific
   checks in addition to steps 1-5, not instead of them.
7. **Check transparency and correctability.** Confirm reasoning, observations, and actions are
   surfaced as separate, inspectable channels rather than merged into one opaque stream, and —
   where the interface supports it — that intermediate thoughts can be corrected by a human
   reviewer or operator (P057). This is what makes steps 1-6 checkable on a live or logged trace
   in the first place.
8. **If reviewing demonstrations, check quality over quantity.** Few-shot examples should read as
   natural, concise thought-action-observation trajectories. Prioritize demonstration quality and
   the target model's capability over adding more examples: more examples did not reliably help
   in the evidence behind this practice, and a sufficiently complex action space can in any case
   exceed what in-context examples can cover (P026).
9. **Check for stall detection and replanning.** Scan the trace, or the design's stated recovery
   logic, for repeated thoughts, repeated actions with no effect, or observations that carry no
   new information. Any of these is a failure signal; the loop must detect it and replan from the
   last state that was actually useful rather than continuing to repeat it (P028).
10. **Decide whether prompting is enough.** If the task is well within a capable model's reach
    with good demonstrations (steps 3 and 8 pass), prompting can stand. If prompting is not
    robust enough despite that — the model still cannot reliably obtain and use information — and
    trajectory data plus the needed tools or actions are available, recommend fine-tuning on
    high-quality successful trajectories rather than continuing to patch the prompt (P032).
11. **Write up findings.** For each gap found in steps 1-10, name the failure mode, the principle
    it bears on, the trade-off any fix implies (denser thoughts cost more tokens and latency;
    fine-tuning costs data and training effort prompting does not), and a concrete next step. End
    with the single most important fix if several are found.

## Task playbooks

### Shopping and product selection (P003)

Reason explicitly over the stated constraints (attribute, size, quantity, price, and similar).
Reject candidates whose visible attributes conflict with those constraints before opening a
page. Once on a product page, verify the page-level selectable options against every critical
constraint. Buy only after all critical attributes have been checked and matched — never on a
plausible-looking title alone.

### Household-object tasks (P005)

Decompose the goal into acquisition (find and take the object), required transformation (clean,
heat, cool, or similar — only where the goal demands a changed state), and placement (move it to
the target location or receptacle). Use commonsense knowledge of likely locations to search
systematically rather than exhaustively, and after each subgoal completes, have the next thought
name the completed subgoal and choose the next one explicitly — the same "capable, not a
reminder" check as Procedure step 4, applied to its most common failure shape.

### Tool selection among distinct APIs (P007)

Match the tool to the failure mode it is meant to cover, rather than defaulting to one tool for
everything: a direct question-answering call for bounded factual completion, a calculator for
arithmetic, a calendar lookup for reasoning that depends on the current date, a translation call
when the answer must be produced in a different language than the source material, and a
broader retrieval call when the question needs evidence a direct-answer tool cannot supply. Note
that retrieval trades away directness — it returns text the model must still read and interpret —
and that a non-interactive, single-shot retrieval call limits performance when it returns a poor
match and the trace cannot reformulate the query or examine another result.

### Multi-hop question answering (P016)

Decompose the question into an explicit sequence of retrieval targets instead of searching once
and answering from whatever comes back. When a search returns partial or ambiguous results,
reformulate rather than guessing from what is available. For comparison or yes/no-over-entities
questions, retrieve the relevant fact or attribute for each candidate and compare them explicitly
in a thought before finishing. Reserve the finish/answer action until the gathered evidence is
actually sufficient to support it.

### Fact verification (P017)

Search for the claim's subject first, then compare the retrieved evidence against the claim's
predicate and any qualifiers (date, location, or similar) it depends on. Return a refutation only
when evidence directly conflicts with the claim's key attribute. Return insufficient information
— not a guessed support or refute — when the evidence covers part of the claim but is missing a
qualifier its truth depends on, or when no decisive evidence turns up at all.

## Anti-patterns

- **Action-only loop.** Actions with no thought steps between them. The loop loses goal
  decomposition and state tracking, which is exactly what a household-manipulation or
  long-horizon task needs to stay on track (P008, P005, P042).
- **Reason-only loop.** Thoughts with no grounding actions — reasoning proceeds entirely from
  the model's internal associations. On knowledge-intensive tasks this is where unsupported or
  fabricated connections creep in, because nothing in the loop checks a thought against an
  external observation (P011, P008).
- **Thoughts reduced to reminders.** A thought fires after every action but only restates the
  current environment state, without decomposing goals, applying commonsense, or choosing the
  next subgoal. This looks dense and is not sparse, but it is empty of the operational work
  Procedure steps 3-4 check for, and it under-performs a genuinely capable sparse-thought loop on
  multi-step tasks (P042, P010).
- **Loops that never detect repetition.** The trace repeats a thought or an action that had no
  effect, or keeps acting on an uninformative observation, with nothing that notices and replans.
  Left alone this stalls the task or drifts further from a recoverable state (P028).
- **Thought frequency mismatched to task shape.** Dense thoughts on every step of a long action
  horizon, or sparse thoughts on a reasoning-heavy task, either spend budget without adding
  decision value or starve the reasoning the task actually needs (P041).
- **More examples instead of better examples.** Padding a demonstration set with additional
  few-shot trajectories when the existing ones are already natural and concise does not reliably
  help, and can crowd out context better spent elsewhere; the fix is demonstration quality and
  model capability, not volume (P026).
- **Opaque or unreviewable trajectories.** Reasoning, observations, and actions collapsed into
  one undifferentiated stream, or a trace with no way for an operator to inspect or correct an
  intermediate thought. This blocks Procedure steps 7-9 and removes the operator's cheapest lever
  for correcting a trajectory in flight (P057).
- **Staying prompt-only past its limit.** Continuing to patch a prompt when the model still
  cannot reliably obtain and use information, despite good demonstrations and available
  trajectory data, instead of fine-tuning on successful trajectories (P032).

## Principles covered

- **P003** — For shopping/product-selection tasks: reason over constraints, reject mismatches,
  verify page-level options, buy only once everything critical matches.
- **P005** — For household-object tasks: decompose into acquisition, transformation, and
  placement; use likely locations and subgoal updates to drive each next action.
- **P007** — Choose the tool by the task's failure mode: direct question answering, calculator,
  calendar, translation, or retrieval.
- **P008** — Build the loop as interleaved trajectories: thoughts update context, actions gather
  observations for later reasoning.
- **P010** — Make every thought operational: decompose, extract salient detail, track progress,
  apply commonsense, reformulate, transition plans, or handle exceptions.
- **P011** — Ground knowledge-intensive answers with retrieval or environment actions, letting
  each observation guide the next information target.
- **P016** — For multi-hop question answering: decompose into retrieval targets, reformulate
  incomplete searches, compare facts explicitly, finish only when evidence suffices.
- **P017** — For fact verification: search the subject, compare evidence to predicates and
  qualifiers, refute on direct conflict, return insufficient information when evidence is
  missing.
- **P026** — Author few-shot demonstrations as natural, concise trajectories; prioritize quality
  and model capability over example count.
- **P028** — Detect repeated thoughts, repeated ineffective actions, or uninformative
  observations as failure signals, and replan from the last useful state.
- **P032** — When prompting is insufficient, fine-tune on high-quality successful trajectories so
  the model learns how to obtain and use information.
- **P041** — Choose thought frequency by task shape: dense for reasoning bottlenecks, sparse at
  decision points for long action horizons.
- **P042** — Keep decision-task thoughts capable of goal decomposition, commonsense search,
  subgoal-completion detection, and next-subgoal choice; do not reduce them to reminders.
- **P057** — Expose reasoning, observations, and actions separately so a reviewer or operator can
  inspect, diagnose, and, where supported, edit intermediate thoughts.
