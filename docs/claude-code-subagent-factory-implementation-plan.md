# Claude Code Subagent Factory — Comprehensive Implementation Plan

**Date:** 2026-06-08  
**Target process:** `subagent-authoring-process-v1.0`  
**Status:** implementation plan  
**Primary objective:** Implement a repository-local Claude Code utility that creates or updates reusable neutral subagents from PDFs, ePUBs, Markdown files, DOCX files, and public URLs.

---

# 1. Executive Summary

This plan converts the `Subagent Authoring Process Cycle v1.0` into a practical Claude Code project-local utility.

The utility will let you run a command such as:

```text
/author-subagent ./inputs/book.pdf --topic "software architecture reviewer"
```

or:

```text
/author-subagent ./inputs/book.pdf ./inputs/paper.epub https://example.com/article
```

It will then:

1. Ingest the provided sources.
2. Convert them to canonical Markdown.
3. Generate metadata, anchors, reports, and a source-pack manifest.
4. Search existing generated subagents.
5. Ask whether to update an existing close match.
6. Create a new subagent by default when no close match exists.
7. Run source interrogation and profile derivation.
8. Generate a complete subagent package under `subagents/<slug>/`.
9. Export a Claude Code runtime adapter into `.claude/agents/generated/<slug>.md`.
10. Run validation and tests.

Core principle:

```text
.claude/ = the factory runtime
subagents/<slug>/ = canonical generated subagent package
.claude/agents/generated/<slug>.md = Claude Code runnable adapter
```

---

# 2. Confirmed Design Decisions

## 2.1 Repository-local only

The utility works only in this repository.

Use:

```text
.claude/
```

Do not use:

```text
~/.claude/
```

## 2.2 Generated subagent package path

Use:

```text
subagents/<slug>/
```

Example:

```text
subagents/api-security-reviewer/
subagents/site-reliability-reviewer/
subagents/hvac-design-reviewer/
```

## 2.3 Claude Code runnable adapter path

Export the runnable Claude Code subagent adapter to:

```text
.claude/agents/generated/<slug>.md
```

The adapter is a generated runtime artifact. It should not be manually edited.

## 2.4 Adapter behavior

The adapter should preserve the same intended behavior as the generated source package, but it is not the canonical source of truth.

Canonical source:

```text
subagents/<slug>/profile.yaml
```

Runtime adapter:

```text
.claude/agents/generated/<slug>.md
```

Policy:

```text
- Generate adapter from the canonical package.
- Add DO NOT EDIT header.
- Inline core behavior in the adapter.
- Reference the canonical package path for deeper context.
- Re-export adapter after profile, skills, or references change.
```

## 2.5 v0 source support

v0 must support:

```text
- local PDF
- local ePUB
- local Markdown
- local DOCX
- public URL returning HTML
- public URL returning PDF
- public URL returning ePUB
```

PDF is first-class from v0.

ePUB is also included in v0.

## 2.6 Authentication rule for v0

v0 supports:

```text
- local files
- public URLs
```

If a URL requires login:

```text
- mark it as needs-auth
- ask the user to provide a local downloaded copy
```

Do not implement browser credential reuse in v0.

---

# 3. Target Repository Layout

```text
.
├── CLAUDE.md
├── .claude/
│   ├── settings.json
│   ├── agents/
│   │   ├── subagent-authoring-manager.md
│   │   ├── source-interrogator.md
│   │   ├── profile-deriver.md
│   │   ├── profile-reviewer.md
│   │   └── generated/
│   │       └── README.md
│   ├── skills/
│   │   ├── author-subagent/
│   │   │   └── SKILL.md
│   │   ├── source-ingestion/
│   │   │   └── SKILL.md
│   │   ├── source-interrogation/
│   │   │   └── SKILL.md
│   │   ├── profile-generation/
│   │   │   └── SKILL.md
│   │   ├── adapter-export/
│   │   │   └── SKILL.md
│   │   └── subagent-maintenance/
│   │       └── SKILL.md
│   └── rules/
│       ├── repository-boundaries.md
│       ├── generated-artifact-policy.md
│       └── rights-and-quotation-policy.md
├── tools/
│   └── subagent_factory/
│       ├── __init__.py
│       ├── cli.py
│       ├── ingest_source.py
│       ├── fetch_url.py
│       ├── detect_file_type.py
│       ├── convert_document.py
│       ├── convert_pdf.py
│       ├── convert_epub.py
│       ├── convert_docx.py
│       ├── convert_html.py
│       ├── normalize_markdown.py
│       ├── inject_anchors.py
│       ├── extract_assets.py
│       ├── generate_metadata.py
│       ├── generate_manifest.py
│       ├── generate_conversion_report.py
│       ├── validate_metadata.py
│       ├── validate_manifest.py
│       ├── validate_anchor_index.py
│       ├── validate_generated_package.py
│       ├── find_related_subagents.py
│       ├── export_claude_agent.py
│       ├── quote_scan.py
│       └── run_tests.py
├── schemas/
│   ├── source-metadata-v1.schema.json
│   ├── source-pack-manifest-v1.schema.json
│   ├── source-anchor-index-v1.schema.json
│   ├── conversion-report-v1.schema.json
│   ├── provenance-ledger-v1.schema.json
│   └── specialist-result-v1.schema.json
├── templates/
│   ├── profile.yaml.j2
│   ├── provenance-ledger.md.j2
│   ├── source-pack.manifest.yaml.j2
│   ├── conversion-report.md.j2
│   ├── claude-agent-adapter.md.j2
│   ├── golden-tests.yaml.j2
│   └── changelog.md.j2
├── subagents/
│   └── README.md
├── tests/
│   └── subagent_factory/
└── pyproject.toml
```

---

# 4. Generated Subagent Package Layout

Each generated subagent package should look like this:

```text
subagents/<slug>/
├── README.md
├── profile.yaml
├── provenance-ledger.md
├── source-pack.manifest.yaml
├── CHANGELOG.md
├── sources/
│   ├── original/
│   │   └── <source_id>/
│   │       └── original.<ext>
│   ├── markdown/
│   │   └── <source_id>.md
│   ├── assets/
│   │   └── <source_id>/
│   ├── anchors/
│   │   └── <source_id>.anchors.jsonl
│   ├── metadata/
│   │   └── <source_id>.metadata.json
│   └── reports/
│       ├── <source_id>.conversion-report.md
│       └── human-review-queue.md
├── skills/                       # optional — present only when the source yields procedures
│   └── <generated-skill>/
│       └── SKILL.md
├── references/                   # optional — authored when the source warrants it
│   └── *.md                      #   (rubrics, glossaries, examples, taxonomies); names vary
├── adapters/
│   └── claude-code/
│       └── <slug>.md
└── tests/
    ├── golden-tests.yaml         # required — holds golden_tests: and negative_routing_tests:
    │                             #   keyed sections (Phase 8 counts keys, not files)
    └── test-results.md           # required — self-check / test-run record
```

**Test-file and references contract.** The package validator and the Phase 8 self-check
operate on *keyed sections*, not filenames: `golden-tests.yaml` carries both `golden_tests:`
and `negative_routing_tests:`, and schema validation is performed directly by the validator
against the metadata / manifest / anchor schemas. Separate `negative-routing-tests.yaml`
and `schema-tests.yaml` files are therefore not emitted. `references/` is situational —
authored only when a source yields rubrics, glossaries, examples, or taxonomies — so its
file names vary by domain and the directory may be absent.

---

# 5. Claude Code Runtime Assets

## 5.1 `CLAUDE.md`

Recommended content:

```markdown
# Claude Code Instructions

This repository is a local Claude Code subagent-authoring factory.

Use `/author-subagent` to create or update generated subagent packages under `./subagents/`.

Generated subagent source packages must not be placed directly in `.claude/`.

Only exported Claude Code runtime adapters may be installed into:

```text
.claude/agents/generated/
```

Canonical source of truth for each generated subagent:

```text
subagents/<slug>/profile.yaml
```

Do not manually edit files under `.claude/agents/generated/`.

Run validation after generation:

```bash
python -m tools.subagent_factory.validate_generated_package subagents/<slug>
```
```

## 5.2 `.claude/settings.json`

Initial settings can be minimal.

Example:

```json
{
  "permissions": {
    "allow": [
      "Bash(python -m tools.subagent_factory.*)",
      "Bash(pandoc:*)",
      "Bash(docling:*)",
      "Bash(markitdown:*)"
    ],
    "deny": [
      "Bash(rm -rf /:*)",
      "Bash(curl * --cookie*)",
      "Bash(curl * --cookie-jar*)"
    ]
  }
}
```

The exact permission syntax should be verified against the Claude Code version used in the repository.

---

# 6. Claude Code Skills

## 6.1 `author-subagent`

Path:

```text
.claude/skills/author-subagent/SKILL.md
```

Purpose:

```text
User-facing entry point to create or update generated subagent packages.
```

Responsibilities:

1. Parse user inputs.
2. Identify local files and URLs.
3. Invoke source ingestion.
4. Search existing subagents for related topics.
5. Decide create vs update according to policy.
6. Coordinate interrogation, profile derivation, extraction, adapter export, and tests.
7. Produce final summary.

## 6.2 `source-ingestion`

Path:

```text
.claude/skills/source-ingestion/SKILL.md
```

Purpose:

```text
Execute Phase 1.5: convert approved source files into canonical Markdown with assets, anchors, metadata, reports, and manifest updates.
```

Responsibilities:

1. Preserve immutable original.
2. Compute SHA-256 hash.
3. Detect file type.
4. Choose converter.
5. Convert to canonical Markdown.
6. Extract assets.
7. Inject source anchors.
8. Generate metadata JSON.
9. Generate anchor JSONL.
10. Generate conversion report.
11. Assign conversion status.
12. Update source-pack manifest.
13. Create human-review queue entries when needed.

## 6.3 `source-interrogation`

Path:

```text
.claude/skills/source-interrogation/SKILL.md
```

Purpose:

```text
Run Q1–Q18 against approved canonical Markdown sources.
```

## 6.4 `profile-generation`

Path:

```text
.claude/skills/profile-generation/SKILL.md
```

Purpose:

```text
Generate or update portable profile, provenance ledger, and artifact decisions from interrogation records.
```

## 6.5 `adapter-export`

Path:

```text
.claude/skills/adapter-export/SKILL.md
```

Purpose:

```text
Export generated subagent package into a Claude Code runtime adapter.
```

## 6.6 `subagent-maintenance`

Path:

```text
.claude/skills/subagent-maintenance/SKILL.md
```

Purpose:

```text
Maintain existing generated subagents when sources, converters, platform behavior, or requirements change.
```

---

# 7. Claude Code Subagents

## 7.1 `subagent-authoring-manager`

Path:

```text
.claude/agents/subagent-authoring-manager.md
```

Purpose:

```text
Main orchestration subagent for creating and updating generated subagents.
```

Responsibilities:

1. Own the workflow.
2. Decide create vs update.
3. Delegate deterministic tasks to scripts.
4. Use helper subagents where useful.
5. Enforce repository boundaries.
6. Ensure validation before final output.

## 7.2 `source-interrogator`

Path:

```text
.claude/agents/source-interrogator.md
```

Purpose:

```text
Focused subagent for Q1–Q18 source interrogation.
```

## 7.3 `profile-deriver`

Path:

```text
.claude/agents/profile-deriver.md
```

Purpose:

```text
Focused subagent for profile derivation and artifact decisions.
```

## 7.4 `profile-reviewer`

Path:

```text
.claude/agents/profile-reviewer.md
```

Purpose:

```text
Focused reviewer for Phase 8 self-check and release-readiness review.
```

---

# 8. Deterministic Scripts

## 8.1 Core scripts

```text
tools/subagent_factory/ingest_source.py
tools/subagent_factory/fetch_url.py
tools/subagent_factory/detect_file_type.py
tools/subagent_factory/convert_document.py
tools/subagent_factory/convert_pdf.py
tools/subagent_factory/convert_epub.py
tools/subagent_factory/convert_docx.py
tools/subagent_factory/convert_html.py
tools/subagent_factory/normalize_markdown.py
tools/subagent_factory/inject_anchors.py
tools/subagent_factory/extract_assets.py
tools/subagent_factory/generate_metadata.py
tools/subagent_factory/generate_manifest.py
tools/subagent_factory/generate_conversion_report.py
```

## 8.2 Validation and export scripts

```text
tools/subagent_factory/validate_metadata.py
tools/subagent_factory/validate_manifest.py
tools/subagent_factory/validate_anchor_index.py
tools/subagent_factory/validate_generated_package.py
tools/subagent_factory/find_related_subagents.py
tools/subagent_factory/export_claude_agent.py
tools/subagent_factory/quote_scan.py
tools/subagent_factory/run_tests.py
```

## 8.3 Script responsibility split

| Script | Responsibility |
|---|---|
| `ingest_source.py` | Main source-ingestion entry point |
| `fetch_url.py` | Fetch public URLs and preserve snapshots |
| `convert_pdf.py` | Convert PDFs, detect scanned PDFs, generate warnings |
| `convert_epub.py` | Convert ePUB, preserve chapters/images/metadata |
| `convert_docx.py` | Convert DOCX |
| `convert_html.py` | Convert HTML snapshots |
| `inject_anchors.py` | Generate `source_anchor_v1` anchors |
| `find_related_subagents.py` | Search existing subagents |
| `export_claude_agent.py` | Generate Claude Code runtime adapter |
| `quote_scan.py` | Detect prohibited quotation from restricted sources |

---

# 9. Converter Strategy

## 9.1 PDF

v0 policy:

```text
primary: Docling
fallback: MarkItDown or PyMuPDF plain extraction
```

v0 behavior:

```text
- support born-digital PDFs
- support academic PDFs with warnings
- detect scanned/image-only PDFs
- mark scanned PDFs as needs-ocr or needs-human-review
- preserve page anchors
- extract tables/figures where converter supports it
```

## 9.2 ePUB

v0 policy:

```text
primary: Pandoc
fallback: MarkItDown
```

Checks:

```text
- chapter order
- table of contents
- embedded images
- footnotes/endnotes
- heading hierarchy
- metadata: title, author, year
- rights status
```

## 9.3 DOCX

v0 policy:

```text
primary: Pandoc
fallback: MarkItDown
```

## 9.4 HTML

v0 policy:

```text
primary: readability/html-to-markdown pipeline
fallback: Pandoc or MarkItDown
```

## 9.5 Markdown

No converter required.

Steps:

```text
- normalize front matter
- assign source ID
- inject anchors
- generate metadata
```

---

# 10. Create vs Update Logic

When `/author-subagent` is invoked, the utility should search existing subagents.

Script:

```text
tools/subagent_factory/find_related_subagents.py
```

Search targets:

```text
subagents/*/profile.yaml
subagents/*/README.md
subagents/*/source-pack.manifest.yaml
```

Compare:

```text
- requested topic
- display_name
- role
- when_to_use
- source titles
- tags if available
```

Thresholds:

```text
similarity >= 0.80:
  ask user whether to update existing subagent

0.55 <= similarity < 0.80:
  show candidates, default create new unless user says update

similarity < 0.55:
  create new by default
```

---

# 11. Claude Code Adapter Export

## 11.1 Adapter generation

Canonical adapter:

```text
subagents/<slug>/adapters/claude-code/<slug>.md
```

Installed adapter:

```text
.claude/agents/generated/<slug>.md
```

## 11.2 Adapter header

```markdown
---
name: <slug>
description: <role + top triggers + top exclusion>
tools: Read, Grep, Glob
model: sonnet
---

<!-- GENERATED FILE. DO NOT EDIT DIRECTLY.
Source package: subagents/<slug>/
Source profile: subagents/<slug>/profile.yaml
Regenerate with: /author-subagent --update <slug>
-->
```

## 11.3 Adapter body

Must include:

1. Role.
2. When to use.
3. When not to use.
4. Required inputs.
5. Supported modes.
6. Output contract.
7. Quality bar.
8. Forbidden behaviors.
9. Handoff rules.
10. Source-of-truth policy.
11. Canonical package path.
12. Instruction to read package files for deeper context.

---

# 12. End-to-End Workflows

## 12.1 Create from PDF

```text
/author-subagent ./inputs/api-security-paper.pdf --topic "API security reviewer"
```

Flow:

```text
1. Parse request.
2. Search related subagents.
3. No close match → create new.
4. Create subagents/api-security-reviewer/.
5. Ingest PDF.
6. Convert PDF to canonical Markdown.
7. Generate metadata, anchors, report, manifest.
8. Run Q1–Q18 interrogation.
9. Generate profile.yaml.
10. Generate provenance-ledger.md.
11. Extract skills/references.
12. Export Claude Code adapter.
13. Install adapter.
14. Run validation/tests.
15. Report summary.
```

## 12.2 Update from ePUB

```text
/author-subagent ./inputs/security-book.epub --topic "API security reviewer"
```

Flow:

```text
1. Related subagent found.
2. Ask update or create.
3. If update:
   - ingest new source
   - update manifest
   - interrogate new source
   - run multi-source merge
   - update profile
   - re-export adapter
   - run tests
   - update changelog
```

## 12.3 Public URL

```text
/author-subagent https://example.com/article --topic "architecture decision reviewer"
```

Flow:

```text
1. Fetch public URL.
2. Preserve snapshot.
3. Convert snapshot to Markdown.
4. Continue normal workflow.
```

If authentication is required:

```text
Source requires authentication.
v0 does not reuse browser credentials.
Please provide a local downloaded copy.
```

---

# 13. Validation and Testing

## 13.1 Package validation command

```bash
python -m tools.subagent_factory.validate_generated_package subagents/<slug>
```

Checks:

```text
- required files exist
- metadata validates
- manifest validates
- anchor index validates
- conversion reports exist
- profile exists
- provenance ledger exists
- adapter exists
- installed adapter matches generated adapter
- tests exist
- restricted quote scan passes
```

## 13.2 Test fixtures

```text
tests/subagent_factory/fixtures/
├── simple.pdf
├── academic-two-column.pdf
├── sample.epub
├── sample.docx
├── article.html
└── clean.md
```

## 13.3 Test classes

```text
- PDF conversion
- ePUB conversion
- DOCX conversion
- HTML snapshot conversion
- Markdown normalization
- anchor generation
- metadata generation
- manifest update
- needs-auth detection
- scanned-PDF detection
- adapter export
- duplicate agent name handling
```

---

# 14. Implementation Milestones

## Milestone 0 — Repository Skeleton

Deliverables:

```text
- repository directories
- CLAUDE.md
- .claude/settings.json
- empty skill files
- empty agent files
- schemas directory
- tools package skeleton
- tests skeleton
```

Acceptance criteria:

```text
- Python package imports
- placeholder CLI runs
- repository layout matches plan
```

## Milestone 1 — Source Ingestion v0

Deliverables:

```text
- local PDF ingestion
- local ePUB ingestion
- local DOCX ingestion
- local Markdown normalization
- public HTML URL snapshot
- metadata generation
- manifest generation
```

Acceptance criteria:

```text
- one PDF can be ingested
- one ePUB can be ingested
- one DOCX can be ingested
- one Markdown file can be normalized
- metadata and manifest validate
```

## Milestone 2 — Anchors and Reports

Deliverables:

```text
- anchor injection
- anchor JSONL
- conversion report
- human-review queue
```

Acceptance criteria:

```text
- headings/tables/figures receive anchors where possible
- anchor index validates
- scanned PDF is detected and marked needs-human-review
```

## Milestone 3 — Package Generation

Deliverables:

```text
- generated subagent folder
- profile.yaml template
- provenance-ledger template
- changelog template
```

Acceptance criteria:

```text
- subagents/<slug>/ package is created
- required package files exist
```

## Milestone 4 — Adapter Export

Deliverables:

```text
- export_claude_agent.py
- adapter template
- install to .claude/agents/generated/
```

Acceptance criteria:

```text
- adapter generated
- adapter installed
- adapter includes DO NOT EDIT header
- adapter references canonical package
```

## Milestone 5 — Create vs Update Search

Deliverables:

```text
- find_related_subagents.py
- threshold logic
- update/create prompt protocol
```

Acceptance criteria:

```text
- high similarity triggers update question
- low similarity creates new by default
```

## Milestone 6 — Authoring Workflow

Deliverables:

```text
- author-subagent skill
- manager subagent
- source-interrogation skill
- profile-generation skill
```

Acceptance criteria:

```text
/author-subagent ./inputs/example.pdf --topic "example reviewer"
```

creates a package and adapter.

## Milestone 7 — Validation and Test Harness

Deliverables:

```text
- validate_generated_package.py
- quote_scan.py
- run_tests.py
- test fixtures
```

Acceptance criteria:

```text
- validation passes for a generated package
- adapter validation passes
- restricted quote scan runs
```

---

# 15. Dependencies

## 15.1 Python dependencies

Recommended:

```text
pydantic
pyyaml
jsonschema
python-slugify
beautifulsoup4
readability-lxml
markdownify
requests
rich
```

## 15.2 External tools

Recommended v0:

```text
pandoc
docling
markitdown
```

Optional:

```text
pymupdf
python-magic
```

Later:

```text
tesseract
ocrmypdf
mineru
playwright
```

## 15.3 Dependency policy

The utility should detect available converters and report missing optional tools.

Missing advanced converters should not break v0 if a supported converter is available.

---

# 16. Risk Register

| Risk | Impact | Mitigation |
|---|---|---|
| PDF conversion quality is poor | Bad source interrogation | quality gate + needs-human-review |
| Scanned PDF cannot be converted | Source blocked | detect and defer OCR |
| Adapter drifts from profile | Runtime behavior inconsistent | generated-file header + re-export policy |
| Duplicate agent names | Claude Code conflict | detect before install |
| Rights leakage | Legal/license issue | quote scan + restricted-source rules |
| Over-architecture | Slow implementation | v0 uses few agents and deterministic scripts |
| Login URL handling unsafe | Credential risk | v0 requires local file |
| Converter changes output | Regression risk | deterministic build + regression tests |

---

# 17. v0 Completion Definition

v0 is complete when this works:

```text
/author-subagent ./inputs/example.pdf --topic "example reviewer"
```

And produces:

```text
subagents/example-reviewer/
├── profile.yaml
├── provenance-ledger.md
├── source-pack.manifest.yaml
├── sources/
├── adapters/
│   └── claude-code/
│       └── example-reviewer.md
└── tests/
    └── test-results.md
```

And installs:

```text
.claude/agents/generated/example-reviewer.md
```

And validation passes:

```bash
python -m tools.subagent_factory.validate_generated_package subagents/example-reviewer
```

---

# 18. Final Recommendation

Build the first version around this path:

```text
PDF/ePUB → canonical Markdown → generated package → Claude Code adapter
```

Do not begin with a large multi-agent system.

v0 should use:

```text
1 manager subagent
2–3 helper subagents
4–6 skills
deterministic scripts for mechanics
subagents/<slug>/ for generated packages
.claude/agents/generated/ for runnable adapters
```

The first valuable deliverable is a reliable source-ingestion and adapter-export pipeline.

Everything else can improve iteratively after that path works.
