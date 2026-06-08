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

## Step 5 — Ingest sources

For each source:

```bash
python -m tools.subagent_factory.cli ingest <source> --slug <slug> \
  [--title "<title>"] [--author "<author>"] [--year <year>]
```

Pass `--title`, `--author`, `--year` when known from the content sample (Step 2a).
The `[Source title hint: ...]` line in the extract-sample output is the title.

Handle errors:
- `needs_auth=True` → stop: "This URL requires authentication. Provide a local downloaded copy."
- `conversion_status=needs-ocr` → warn: "PDF appears scanned. OCR needed. Marked for human review. Continuing."
- `conversion_status=failed` → halt and report.

---

## Step 6 — Source interrogation

Invoke the `source-interrogator` subagent via `Agent(subagent_type="source-interrogator")`.
Include in the prompt:
- Paths to `subagents/<slug>/sources/markdown/*.md`
- Inferred topic as context
- Package path `subagents/<slug>/`
- Instruction to write the record to `subagents/<slug>/interrogation-records.yaml`

**Do NOT** use `Skill("source-interrogation")` — that loads instructions into main context
instead of delegating. The subagent handles Q1–Q18 internally.

---

## Step 7 — Profile derivation

Invoke the `profile-deriver` subagent via `Agent(subagent_type="profile-deriver")`.
Include in the prompt:
- Path to `subagents/<slug>/interrogation-records.yaml`
- Package path `subagents/<slug>/`
- For updates: path to existing `profile.yaml` for merge context

**Do NOT** use `Skill("profile-deriver")` or `Skill("profile-generation")` — those load
instructions into main context instead of delegating.

---

## Step 8 — Export adapter

```bash
python -m tools.subagent_factory.cli export <slug>
```

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
- Sources ingested
- Adapter installed at `.claude/agents/generated/<slug>.md`
- Validation status
- Any warnings or human-review items
