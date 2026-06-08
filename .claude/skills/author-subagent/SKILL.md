# Skill: author-subagent

**Trigger:** `/author-subagent <source...> [--topic "<topic>"]`

**Purpose:** Create or update a generated subagent package from source files or URLs.

---

## Step 1 — Parse inputs

Extract:
- Source file paths and/or URLs from arguments
- `--topic` value if provided (use as creation context)
- `--update <slug>` if user wants to force update an existing subagent

For each source:
- If it starts with `http://` or `https://` → URL source
- Otherwise → local file, must exist under project

---

## Step 2 — Search existing subagents

Run:

```bash
python -m tools.subagent_factory.cli search "<topic>"
```

Apply thresholds:
- similarity >= 0.80 → ask user: "Update `<slug>` or create new?"
- 0.55 <= similarity < 0.80 → show candidates, default create-new unless user says update
- similarity < 0.55 → create new silently

---

## Step 3 — Determine slug

If creating new:
- Derive slug from `--topic` using kebab-case, e.g. `api-security-reviewer`
- Confirm with user if ambiguous

If updating existing:
- Use slug of matched subagent

---

## Step 4 — Ingest sources

For each source, run:

```bash
python -m tools.subagent_factory.cli ingest <source_path_or_url> --slug <slug> --topic "<topic>"
```

Handle errors:
- `needs_auth=True` → tell user: "This URL requires authentication. Please provide a local downloaded copy."
- `conversion_status=needs-ocr` → warn: "PDF appears to be scanned. OCR required. Marking for human review."
- `conversion_status=failed` → halt and report error

---

## Step 5 — Source interrogation

Delegate to the `source-interrogator` subagent with:
- Path to `subagents/<slug>/sources/markdown/*.md`
- The `--topic` value
- The Phase 2 Q1–Q18 question set

---

## Step 6 — Profile derivation

Delegate to the `profile-deriver` subagent with:
- Interrogation records from Step 5
- `subagents/<slug>/` package path

---

## Step 7 — Export adapter

Run:

```bash
python -m tools.subagent_factory.cli export <slug>
```

---

## Step 8 — Validate package

Run:

```bash
python -m tools.subagent_factory.cli validate <slug>
```

Report results. Stop on FAIL.

---

## Step 9 — Summary

Report:
- Subagent slug and package path
- Sources ingested
- Adapter installed at
- Validation status
- Any warnings or human-review items
