# Intelligence-Analysis Agent — design docs

Design for a composed AI agent (skills + subagents + MCP) that runs the intelligence-analysis workflow,
grounded in a distilled corpus of 11 canonical works (2,084 principles MAPped in
`../../inputs/intelligence-analysis-advisor/`). The design was dogfood-reviewed by 5 of this repo's own
advisors (agent-skills, mcp-quality, mcp-security, ai-agent-engineering, product-blueprint).

## Read in this order
1. **`BLUEPRINT-intel-analysis-agent.md`** — the *what / why*: problem, thesis, users, **non-goals**, the
   **open decisions** (deployment/classification, production scope, team use — all deferred), the
   load-bearing decisions with trade-offs, the MVP boundary + success criteria, build sequencing, and
   downstream-stage routing. Implementation-neutral.
2. **`PIPELINE-grounded.md`** — the *grounded workflow*: the 12 analysis steps, each with scope, the four
   I/O legs (upstream-in · store-read · downstream-out · store-write), the source-defined artifact formats,
   the persistent stores (per-case vs cross-case "learning" layer), and loop-back/human-gate. **Every step
   and format cites a source claim; pure build-plumbing is quarantined at the end.**
3. **`DESIGN-SPEC-intel-analysis-agent.md`** — the *how*: skill internals, MCP tool ops/schemas, security
   controls, OSINT primitives, test techniques. Engineering detail, realizes the blueprint.

## Rule this design follows
Every component (workflow step, skill, subagent, MCP, persistent store) traces to a source/claim. The only
non-groundable items — pure software form (MCP label, JSON, `case_id`, hash-chain) — are explicitly
quarantined, never presented as grounded.

## Status
Design complete + grounded. Not yet built. MVP = the `structured-analytic-techniques` skill +
`analytic-tradecraft-reviewer` subagent (split into bias / method / calibration reviewers) + human gate.
