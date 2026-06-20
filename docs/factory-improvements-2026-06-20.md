# Factory improvements — 2026-06-20

Serialized improvement pass after Round 1 of the dual-engine topic-subagent campaign
(`software-architecture` on Claude Code, `software-design` on GitHub Copilot). Each finding is
grounded in something the run actually exposed. `make verify` green (617 passed) after all changes.

## P0 — correctness / silent recurrence

### 1. Adapter frontmatter was never YAML-validated
- **Evidence:** the tdd regression earlier this session — an unescaped `"` in the `description`
  broke the adapter's YAML frontmatter, so Claude Code silently never registered the agent, yet
  every existing `adapter-quality` check passed.
- **Fix:** `validate_adapter_quality.py` now parses the `---`-delimited frontmatter and FAILs on
  a missing block, invalid YAML, or missing `name`/`description`. Regression-tested
  (`_parse_frontmatter`: good→ok, unescaped-quote→invalid).
- **Also:** the exporter is now structurally safe — `export_claude_agent._yaml_scalar` JSON-encodes
  the description into a valid single-line YAML scalar (escapes quotes; no HTML-escaping, unlike
  Jinja `tojson`). The template emits it raw (`description: {{ description }}`), so **any** renderer
  produces valid frontmatter without a custom Jinja filter.

## P1 — quality / high ROI

### 2. The factory's own PDF converter produced flat text
- **Evidence:** chain is Docling→MarkItDown→PyMuPDF, but Docling is slow/uninstalled and MarkItDown
  isn't installed here, so it fell to `_try_pymupdf` which used raw `fitz.get_text()` → `headings=0`
  → weak provenance anchoring. We only got good Round-1 sources by *bypassing* it with pymupdf4llm.
- **Fix:** `_try_pymupdf` now prefers `pymupdf4llm.to_markdown()` (recovers heading structure, no
  ML/OCR wait) and falls back to raw `fitz`. Added `pymupdf4llm` to the mypy missing-imports
  allowlist.

### 3. No review automation
- **Fix:** new `campaign/review-run.py` — engine-agnostic. Parses `===GENERATE/FINISH_SUMMARY===`
  blocks, runs the authoritative `cli validate`, reads real faithfulness findings, flags known
  failure signatures → `campaign/logs/review-<slug>.md`.

### 4. Concurrent-launch startup collision
- **Evidence:** launching two `claude -p` + the Copilot smoke test at the same instant produced a
  transient empty-log `rc=1` (cost the first architecture run). Isolated retry streamed fine.
- **Fix:** `generate-review-pair.sh` now staggers the second engine by `PAIR_STAGGER` (default 75s).

## P2 — process / robustness (documented, not code)

### 5. GitHub Copilot `-p` caps at ~27 premium requests/session
- **Evidence:** smoke (1-liner), generate (26 min), finish (20 min) all reported exactly
  "27 Premium". Copilot built `software-design` to a validated **draft** + 7/8 skill bodies, then
  stopped mid-authoring; it never reached `ready`. Not raisable by flag (only
  `--max-autopilot-continues` exists).
- **Implication:** Copilot can complete **generate (2a)** for a ~5-source package but **cannot
  complete finish-skills (2b)**. Dual-engine strategy: use Copilot for 2a, Claude for 2b; keep a
  Claude backstop for promotion. `software-design` was promoted to `ready` via that backstop.

### 6. `/author-subagent` stops at `draft`
- Reaching `ready` requires a separate `author-skills` drive (Phase 2b). Candidate future work:
  fold author-skills→ready into the main pipeline so one drive lands `ready`.

### 7. Double-background footgun
- `nohup … &` inside a harness-tracked background Bash call reports the *wrapper* as "completed"
  while the real work runs detached → misleading. Launch long work as a single tracked command.

## Files touched
- `tools/subagent_factory/validate_adapter_quality.py` (frontmatter parse check)
- `tools/subagent_factory/export_claude_agent.py` (`_yaml_scalar`, filter-free template path)
- `templates/claude-agent-adapter.md.j2` (`description: {{ description }}`)
- `tools/subagent_factory/convert_pdf.py` (`_try_pymupdf` → pymupdf4llm)
- `pyproject.toml` (mypy allowlist: `pymupdf4llm`)
- `campaign/review-run.py` (new), `campaign/generate-review-pair.sh` (stagger)
- tests: `test_validate_adapter_quality.py`, `test_validate_generated_package.py` (realistic
  frontmatter fixtures)

---

## Round-2 process review (same day)

Both Round-2 packages (`python-code-reviewer`, `devops-sre-advisor`) reached `ready`, validated,
0 stubs, 0 faithfulness over-claims. The Copilot-2a → Claude-2b split worked (Copilot built a
`validate: PASS` draft within its ~27-req cap; Claude finished to ready). Process fixes:

- **`review-run.py` mislabelled over-claims** — it counted *total* faithfulness findings as
  over-claims. Now counts only `verdict ∈ {CONTRADICTED, HEDGING_REMOVED, SCOPE_BROADENED}`.
- **multisource-synthesis WARN was permanent noise** (fired on all 4 Tier-2 packages; Step 7 is
  opt-in and never run). `validate_generated_package` now honours `multisource_synthesis: deferred`
  in profile.yaml → acknowledged OK instead of a per-validate WARN. Flag set on all 4 ready
  packages (not in the adapter → no re-export/version bump).
- **Phase gate (2a→2b)** — `finish-skills.sh` now runs `cli validate` first and ABORTs 2b if the
  2a draft fails (was: authored skills unconditionally, relying on luck that 2a completed).
- **Auto-review** — `prep-round.py`'s generated orchestrator runs `review-run.py` for every
  package after both chains finish.

### Open (not yet done)
- **Output-quality eval** has been run on **none** of the 6 ready packages — we prove validates +
  faithful + no-stubs, not that the advice is *good* (`docs/output-quality-eval.md`). Highest
  remaining quality gap.
- Retire superseded launchers (`stage-sources.py`, `round2-pair.sh`, `generate-review-pair.sh`)
  once `prep-round.py --launch` is proven on a real round (Round 3).

---

## Output-quality eval + grounding-check hardening (same day)

Ran the eval (reliable grounding half) on the 4 new packages, dogfooding the factory's own code as
in-domain inputs. **Finding: advice quality is high** (python review on `convert_pdf.py` caught real
bugs — the swallowed exception, the `if t:` empty-string-vs-None trap, duplicated table branch — and
withdrew a false positive). **Grounding coverage ranks by source richness** (software-design 25% ≫
python 3%), confirming python's 2-source thinness; advice unaffected (base model carries it). No
re-author triggered — no clean missing-source signal.

The eval exposed two **grounding-check** defects, both fixed in `grounding_check.py`:
- **Generic-bigram noise** → false cross-source borrows (e.g. "correctness performance" attributed
  to `xv6-kernel-internals-reviewer` for a Python reviewer). Fix: a bigram grounded in ≥ `_GENERIC_DF`
  (3) packages, or whose **both tokens are universal qualifiers**, is dropped from coverage / leaks /
  attribution. Coverage now measures **distinctive** concept grounding (`n_generic_dropped` reported).
- **Single-phrase source suggestions** → noisy "add source X". Fix: a source is suggested only when
  **≥2 distinct distinctive borrows** point to it; single collisions ("architecture review") are
  listed as candidates but not suggested.

Method caveat still open: no absolute-coverage **calibration baseline** — the *rank* across packages
is the usable signal, not the absolute %.
