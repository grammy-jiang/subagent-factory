# Skill: author-subagent

**Trigger:** `/author-subagent <source...> [--topic "<topic>"]`

**Purpose:** Create or update a generated subagent package from source files or URLs.

---

## Step 1 — Parse inputs

Extract from the user's prompt:
- Source file paths and/or URLs
- `--topic "<topic>"` if provided
- `--update <slug>` if user explicitly names an existing subagent to update
- `--slug <slug>` if user wants to set the slug manually

For each source:
- Starts with `http://` or `https://` → URL source
- Otherwise → local file; must exist; check it is readable

---

## Step 2 — Understand the content

### 2a. Extract content sample

Run on the first source (and any additional sources):

```bash
python -m tools.subagent_factory.cli extract-sample <source_path>
```

Read the output carefully: headings, table of contents, opening prose.

From the opening content, identify the rights status:
- "All rights reserved" or similar copyright with no open license → `distillation-only`
- Open license (MIT, Apache, CC-BY, public domain, Creative Commons open) → `open`
- Internal/confidential/proprietary notice → `proprietary/restricted`
- No copyright notice found → `unknown`

Record this as `<detected_rights>` for use in Step 5.

### 2b. Infer expert role from content

If `--topic` was NOT supplied, answer this question from the content sample:

> "What expert reviewer, auditor, or advisor role would a subagent
> built entirely from this material perform?
> What problems does the material teach you to solve?
> What would you be qualified to review, critique, design, or guide
> after internalising this content?"

Express as `<domain> <function>`, 2–4 words, e.g.:
- `"software design reviewer"`
- `"API security auditor"`
- `"distributed systems architect"`
- `"technical writing reviewer"`
- `"agile delivery coach"`

Do NOT just echo the title or filename.

If `--topic` was supplied by the user, use that as-is.

### 2c. Extract domain keywords

From the content sample (headings + body), identify the 15–25 most
significant domain terms — the vocabulary this field uses. These are
used to improve similarity matching against existing subagents.

Example for a software design book:
`complexity, abstraction, modules, interfaces, encapsulation, cohesion,
coupling, decomposition, dependencies, layering, information, hiding`

---

## Step 3 — Search existing subagents

Run with BOTH inferred topic AND domain keywords:

```bash
python -m tools.subagent_factory.cli search "<inferred_topic>" \
  --keywords "<kw1>,<kw2>,<kw3>,..."
```

### Interpret results and decide

| Similarity | Default action | What to do |
|------------|---------------|-----------|
| >= 0.80 | **Update existing** | Inform user: "Found close match `<slug>` (similarity X). Updating it with new source." Proceed to update unless user says "no, create new". |
| 0.55–0.79 | **Ask user** | Show the candidate(s). Ask: "Found similar subagent `<slug>`. Update it or create new `<inferred-slug>`?" Wait for answer. |
| < 0.55 | **Create new** | Inform user: "No close match found. Creating new subagent `<inferred-slug>`." Proceed. |

**If `--update <slug>` was explicitly given:** skip search, go straight to update that slug.

**If no subagents exist yet:** skip search, create new.

---

## Step 4 — Determine slug

If creating new:
- Derive from inferred topic: kebab-case, function-last
- Examples: `software-design-reviewer`, `api-security-auditor`
- If user supplied `--slug`, use that

If updating:
- Use the matched existing slug

Confirm slug with user only if it looks ambiguous or too generic (e.g. "reviewer").

---

## Step 4.5 — Guard: check for existing complete package

Before ingesting, check if a complete valid package already exists:

```bash
python -m tools.subagent_factory.cli validate <slug> 2>/dev/null && echo "VALID" || echo "INVALID"
```

- If **VALID**: inform user — "Package `<slug>` already exists and passes validation.
  Continuing will re-ingest sources and rebuild the profile. Confirm to proceed (y/n)?"
  Wait for user response. If user says no, stop here.
- If **INVALID** or package does not exist: continue to Step 5.

---

## Step 5 — Ingest sources

For each source:

```bash
python -m tools.subagent_factory.cli ingest <source> --slug <slug> \
  --rights <detected_rights> \
  [--title "<title>"] [--author "<author>"] [--year <year>]
```

Pass `--title`, `--author`, `--year` when known from the content sample (Step 2a).
The `[Source title hint: ...]` line in the extract-sample output is the title.
Pass `--rights <detected_rights>` from Step 2a (default: `distillation-only`).

Handle outputs:
- `SKIP: source already ingested as source_id=<id> (sha256 match)` → source unchanged;
  note the existing `<id>` for Step 7 check.
- `needs_auth=True` → stop: "This URL requires authentication. Provide a local downloaded copy."
- `conversion_status=needs-ocr` → warn: "PDF appears scanned. OCR needed. Marked for human review. Continuing."
- `conversion_status=failed` → halt and report.

Track whether any source was newly ingested (not skipped). If ALL sources were skipped
(all sha256 matches), no new content was added — note this for Step 7.

---

## Step 6 — Source interrogation

Invoke the `source-interrogator` subagent via `Agent(subagent_type="source-interrogator")`.
Include in the prompt:
- Paths to `subagents/<slug>/sources/markdown/*.md`
- Inferred topic as context
- Package path `subagents/<slug>/`
- Instruction to write the record to `subagents/<slug>/interrogation-records.yaml`

**The interrogator has the Write tool and must write the file to disk.**
Do NOT use `Skill("source-interrogation")` — that loads instructions into main context
instead of delegating.

After the agent returns, verify the file was written:

```bash
test -f subagents/<slug>/interrogation-records.yaml && echo "WRITTEN" || echo "MISSING"
```

If **MISSING**: the interrogator returned its YAML as text without writing it (may include
an agent ID in its output). If an agent ID was reported, use `SendMessage` to that agent
to request the YAML content. Then write `subagents/<slug>/interrogation-records.yaml`
in the main thread using the Write tool.

---

## Step 7 — Profile derivation

Check if profile.yaml already exists and whether new sources were added:

- If `subagents/<slug>/profile.yaml` **does not exist** → invoke profile-deriver (new package).
- If profile.yaml **exists** AND all Step 5 ingests were skipped (sha256 match, no new content)
  → skip profile-deriver; log "Profile unchanged — no new sources added."
- If profile.yaml **exists** AND new sources were ingested → invoke profile-deriver with
  merge context (pass existing profile.yaml path).

When invoking, use `Agent(subagent_type="profile-deriver")`. Include in the prompt:
- Path to `subagents/<slug>/interrogation-records.yaml`
- Package path `subagents/<slug>/`
- For updates: path to existing `profile.yaml` for merge context
- Explicit instruction to write ALL required outputs before returning:
  `profile.yaml`, `provenance-ledger.md`, `CHANGELOG.md`, `README.md`,
  and `tests/golden-tests.yaml` (minimum 3 tests, 1 negative routing)

After the agent returns, verify the required files were written:

```bash
for f in profile.yaml provenance-ledger.md CHANGELOG.md README.md tests/golden-tests.yaml; do
  test -f subagents/<slug>/$f && echo "OK: $f" || echo "MISSING: $f"
done
```

For any MISSING file: the agent omitted it. Write or request the content before proceeding.

**Do NOT** use `Skill("profile-deriver")` or `Skill("profile-generation")` — those load
instructions into main context instead of delegating.

---

## Step 7.5 — Phase 8 self-check gate

Run the deterministic Phase 8 gate before generating any adapter. The process
cycle is explicit: **do not generate adapters until the gate passes.**

```bash
python -m tools.subagent_factory.cli selfcheck <slug>
```

This runs the 18-check profile self-check and writes `subagents/<slug>/tests/test-results.md`.

- **Verdict FAIL** (exit 1): STOP. Report the failing checks. Delegate fixes back to
  `profile-deriver` (re-run Step 7), then re-run this gate. Do NOT proceed to export.
- **Verdict WARNING/PASS** (exit 0): continue to Step 8.

For judgement-heavy review (mode evidence, conflict resolution), optionally delegate to
the `profile-reviewer` agent via `Agent(subagent_type="profile-reviewer")`.

---

## Step 8 — Export adapter

```bash
python -m tools.subagent_factory.cli export <slug>
```

---

## Step 8.5 — Scaffold skill/reference stubs

Create the stub files for every entry in the profile's
`knowledge_partition.skills` and `knowledge_partition.references` so the package
matches the expected layout. Idempotent — existing files are left untouched.

```bash
python -m tools.subagent_factory.cli stubs <slug>
```

This writes `subagents/<slug>/skills/<name>/SKILL.md` and
`subagents/<slug>/references/<name>.md`, each marked `STATUS: STUB` until authored.

---

## Step 9 — Validate

```bash
python -m tools.subagent_factory.cli validate <slug>
```

Stop on FAIL. Report all findings.

---

## Step 10 — Summary

Report:
- Action taken: created `<slug>` / updated `<slug>`
- Inferred topic (and whether user confirmed or overrode)
- Detected rights status
- Sources ingested (or skipped as duplicates)
- Adapter installed at `.claude/agents/generated/<slug>.md`
- Phase 8 self-check verdict and `tests/test-results.md` path
- Validation status
- Any warnings or human-review items
- **Skills not yet authored** (from `profile.yaml knowledge_partition.skills`):
  list each as a stub path `subagents/<slug>/skills/<skill-name>/SKILL.md`
- **References not yet authored** (from `profile.yaml knowledge_partition.references`):
  list each as a stub path `subagents/<slug>/references/<ref-name>.md`
- Note: package remains `status: draft` until all skills and references are authored
