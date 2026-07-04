---
name: deploying-skills-across-platforms
kind: skill
status: ready
provenance:
  principles:
  - P004
  - P009
  - P016
  - P020
  - P030
  - P036
  - P037
  - P048
  - P050
  - P053
  - P055
  - P060
  - P077
  - P095
  - P096
  - P122
  - P124
  - P133
  claims:
  - C00775
  - C00776
  - C00777
  - C00778
  - C00810
  - C00875
  - C00876
  - C01890
  - C01897
  - C01898
  - C01899
  - C01900
  evidence:
  - E00347
  - E00348
  - E00349
  - E00350
  - E00363
  - E00395
  - E00396
  - E00769
  - E00770
  - E00771
  - E00772
  - E00773
  source_anchors:
  - df66a50cc0de-c0000
  - 59f8ec5e7b03-c0000
  - c86c41e74ac0-c0000
  - d057d7be0709-c0000
  - 4f2d849c6b6d-c0000
  authored_from_digest: bad1740601bba4d31a374459b0ff173de190e371974e44d380df57fbe812f1bf
---

# Skill: deploying-skills-across-platforms

## Purpose

Get a skill installed, permitted, and running on the specific surface the caller targets —
matching each surface's install location, runtime limits, headers, permission model, and
invocation visibility — while keeping the skill portable. Grounded in P004, P016, P030, P048,
P095.

## When to use

- You have an authored skill and need to deploy it to a concrete surface or manage it there.
- A skill needs tools pre-approved, or its invocation visibility set, to run without prompts.
- You are shipping the same skill to more than one surface and must account for the differences.

## Procedure

1. **Place the skill where its audience and surface expect it.** Match the install location to the
   intended scope — a repository/project skills directory scanned from the working directory up,
   a per-user home location, or a plugin/marketplace install — so the runtime auto-discovers it
   [P004], [P030], [P077].
2. **Design for the surface's runtime limits.** Account for what the target allows: for example an
   API sandbox may have no network access and no runtime package installation (only pre-installed
   packages), so bundle what the skill needs [P016].
3. **Pre-approve the tools the skill needs.** Declare them in the `SKILL.md` allowed-tools
   frontmatter so the agent does not hit a per-use confirmation prompt; a tool omitted from all
   grants is not available [P048].
4. **Set invocation visibility deliberately.** Use the user-invocable / disable-model-invocation
   controls to choose between an auto-loaded command, a user-only command, or model-only
   invocation — omit both when a slash command should also auto-load [P037]; manage which skills
   the agent may invoke through the platform's skill-visibility settings [P122].
5. **On the API surface, send the required beta headers and select skills explicitly.** Enable the
   code-execution tool and set the required beta headers (e.g. the code-execution and skills beta
   headers, adding the files-api header when returning files), keeping the tool type and headers
   consistent [P009], [P133]. Select skills via the request's container/`skills` parameter, giving
   each entry its type, `skill_id`, and version [P020]. Retrieve a generated file through the
   Files API using the file id from the code-execution result [P036].
6. **Constrain what can run in shared or sensitive contexts.** Scope or deny skill invocation
   through the permission system (wholesale deny, or exact/prefix scoping by skill name) so only
   the intended skills run [P096].
7. **Manage each surface separately and keep it portable.** Do not assume skills sync across
   surfaces — upload and manage them per surface — and author against the open standard with
   forward-slash paths so the same skill runs unchanged elsewhere [P095], [P053], [P055].

## Pitfalls / anti-patterns

- Assuming a skill uploaded to one surface appears on the others [P095].
- Inventing an install path, header, or permission token not in the sources — recommend only
  documented mechanisms.
- Relying on network or package installation in a sandbox that forbids them [P016].
- Forgetting data-retention constraints: do not rely on Zero Data Retention for skills; keep
  sensitive data out of definitions and execution [P060].

## Grounding

Principles: P004, P009, P016, P020, P030, P036, P037, P048, P050, P053, P055, P060, P077, P095,
P096, P122, P124, P133. Distillation-only: no verbatim source quotation.
