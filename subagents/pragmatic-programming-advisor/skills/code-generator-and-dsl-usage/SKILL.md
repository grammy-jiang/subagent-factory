---
name: code-generator-and-dsl-usage
kind: skill
status: ready
provenance:
  principles:
  - P002
  - P005
  - P065
  - P016
  claims:
  - C00043
  - C00045
  - C00093
  - C00094
  - C00153
  - C00154
  - C00155
  - C00157
  - C00210
  - C00211
  source_anchors: []
  authored_from_digest: f3158299ea6e8b409b7e43adc4275d65d5430e1a77242e4be2b1ae8c10d7d33f
---

## Purpose

Decide when to generate code or express a problem in a small domain-specific language
instead of hand-maintaining duplicated representations, and which kind of generator to
use. The goal is a single authoritative source (DRY) that drives every derived form, with
details kept in metadata outside the compiled code base so the design stays decoupled and
flexible (P002, P016).

## When to use

- The same knowledge appears in several places or languages — a schema reflected in SQL,
  application objects, and documentation — and is being kept in sync by hand.
- A requirement is naturally expressed in the vocabulary of the problem domain and the
  code that implements it is drifting from that vocabulary.
- Deeply ingrained choices (algorithms, middleware, UI style) or volatile business rules
  are wired into compiled code instead of being driven from metadata.
- Repetitive boilerplate is typed by hand across new files or repeated in multiple target
  representations.

## Procedure

### Step 1 — Identify imposed duplication and its source

Determine whether the duplication is _imposed_ (the environment or platform forces multiple
representations) or _inadvertent_ (a design choice). Only imposed duplication calls for an
active generator; inadvertent duplication is resolved first by normalization and accessor
functions (C00043, C00046).

Ask: "What is the one authoritative representation from which every other form could be
derived?"

### Step 2 — Choose generator type

Use C00155 (passive vs active) as the decision frame:

**Passive generator**
- Run once; output becomes a normal, edited, source-controlled file.
- Use when: scaffolding boilerplate that diverges from the input after initial generation,
  one-off language conversions, or prototyping a new file layout.
- Cost note: a passive generator need not be perfectly accurate — finish its output by hand
  (C00156). Invest proportionally in generator quality vs. hand-editing effort.

**Active generator**
- Run every build from the single metadata source; output is disposable and always
  regenerated.
- Use when: multiple representations must stay in lock-step (e.g., database schema + its
  access code) so that a change to the source automatically updates every derived form and
  errors surface at compile time (C00157).
- Wire the generator into the build so it runs automatically; a source change that breaks
  the generated form should fail the build, not be discovered later.

**Test generation**
- Generate tests programmatically from the specification so they stay in sync automatically
  when the specification changes (C00045). This is a specialised active-generator case.

**Non-code output**
- Generators need not produce program source; they can generate HTML, XML, plain text, SQL,
  or any artifact that feeds another part of the project (C00159). Apply the same passive/
  active choice to non-code artifacts.

### Step 3 — Keep the generator's input format simple

A complex input format makes the generator complex. Use the simplest format that captures
the authoritative information — often a line-oriented plain text or a minimal structured
format (C00158, P016: metadata in plain text).

### Step 4 — Consider a mini-language (DSL) when domain vocabulary shapes the problem

When requirements are naturally expressed in the bounded vocabulary of a domain, consider a
mini-language that lets you work at the domain's level of abstraction and ignore petty
implementation details (C00093). Write code using the vocabulary of the application domain,
backed by a project glossary (C00092).

A mini-language can begin as a non-executable specification that captures user requirements
and later be promoted to executable code — the two endpoints of the same continuum (C00094).

Choose implementation weight to match complexity:

- **Line-oriented format** parsed with switch statements or regular expressions — the right
  choice for simple, well-bounded cases (C00097).
- **Formal grammar** (define syntax in BNF, use a parser generator such as yacc/bison/
  javaCC) only when the language is genuinely complex. Specify the grammar first, build the
  parser second (C00097).
- **Extend an existing language** (embed a scripting engine such as Lua, Python, or Tcl)
  when parsing overhead is not justified and behavior must change without recompiling
  (C00100). Prefer the more readable form up front; most applications outlive their expected
  lifetimes (C00101).

Provide a mini-language or mini-environment for each distinct class of user: end users,
operations, configuration and test managers, and future developers each have their own
problem domain (C00096).

Embedding a language or DSL also enables domain-specific validation and error messages
reported in the user's vocabulary rather than generic compiler messages (C00095).

### Step 5 — Push specifics into metadata

Where behavior varies, program for the general case and move the specifics outside compiled
code into metadata (C00211). This is the "configure, don't integrate" principle: implement
deeply ingrained choices — algorithms, database products, middleware, UI style — as
configuration options driven by metadata rather than wiring them in (C00210).

Represent configuration metadata in plain text so it remains readable, portable, and
modifiable without special tools (C00214).

Benefits of a metadata-driven design: more decoupled and abstract code, the ability to
work around bugs without recompiling, behavior expressed closer to the problem domain, and
reuse of one engine across projects via different metadata (C00212).

### Step 6 — Learn a text-manipulation language to build the generator quickly

A text-manipulation language (Python, awk, sed, Tcl, or Perl) lets you hack utilities and
prototype ideas five to ten times faster than with conventional languages (C00153). The
generator, once built, is reused throughout the project at virtually no additional cost,
eliminating repetitive typing and mistakes (C00154). The one-time investment in building it
multiplies productivity for the rest of the project (P065).

### Step 7 — Verify the generator earns its cost and keeps the design decoupled

Before recommending an active generator, confirm:

1. The single-source benefit outweighs building and maintaining the generator.
2. The generated output is never edited by hand — only the authoritative source changes.
3. The design remains decoupled from a specific vendor or implementation detail; the
   generator does not bake in choices that belong in metadata.

If the generator would tightly couple the code base to a specific tool or format, reconsider
whether metadata-driven configuration (P016) is the better fit.

## Inputs

- The duplicated representations or the domain requirement under review.
- The authoritative metadata or specification, if one already exists.
- The build pipeline (to host an active generator).
- The set of user classes whose vocabulary shapes the domain.

## Output

- A recommendation: passive generator, active generator, mini-language/DSL, metadata
  configuration, or none — with the single source of truth named.
- The decoupling or metadata change that removes the duplication.
- A note on generator cost vs. benefit and input format simplicity.
- Generator type (code, HTML, XML, plain text) as appropriate.

## References

- `references/duplication-taxonomy-table.md` — the imposed-duplication cases a generator
  addresses.
- `references/pragmatic-tips-70-cheatsheet.md` — Write Code That Writes Code (Tip 52);
  Put Abstractions in Code, Details in Metadata (Tip 38); Program Close to the Problem
  Domain (Tip 11).

## Provenance

Derived from principles P002 (single authoritative source / active generator), P005
(program close to the domain / mini-languages), P065 (text-manipulation language and code
that writes code), and P016 (configure, don't integrate / metadata-driven design).

Key grounding claims: C00043 (active generator for imposed duplication), C00045 (generate
tests from spec), C00093 (mini-language at domain abstraction level), C00094 (non-executable
spec growing into executable code), C00153 (text-manipulation language for 5-10x utility
speed), C00154 (code generator reused at virtually no cost), C00155 (passive vs active
generator distinction), C00157 (active generators honor DRY across disparate environments),
C00210 (configure not integrate, deeply ingrained choices as metadata), C00211 (abstractions
in code, details in metadata). Source is distillation-only; all wording is paraphrased.
