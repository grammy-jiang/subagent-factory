# Map-reduce injection safety (approach A)

How the factory scans untrusted book text for indirect prompt injection (IPI) on the
**map-reduce ingestion path** — the path the real corpus actually uses. This is the
cache-level analogue of the classic `sources/markdown/` scan documented in
[`enhancement-steps/step-1-safety-faithfulness.md`](enhancement-steps/step-1-safety-faithfulness.md).

> Status: **merged to master (#91).** See [Status](#status) for the remaining (low-priority) items.

## The problem it fixes — vacuous scans

Step 1 scans `sources/markdown/*.md` per package and triages hits with the
`source-safety-reviewer` agent. But **no package in the real corpus keeps `sources/markdown/`**:
distillation-only (copyrighted / fair-use) sources are withheld rights-clean, so the verbatim
source directories are never populated. The consequence, discovered while dogfooding:

- `prompt_injection_scan` scans a directory that does not exist → **0 findings, always**.
- `quote_scan` and the interrogation-quarantine gate key off the same absent directory.
- So on the actual corpus, the entire injection-triage layer **never fired**. The scans were
  *vacuous* — green because there was nothing to look at, not because the sources were clean.

This doc covers the **injection** leg. The **rights/quote** leg got the same cache-level treatment:
`quote_scan` falls back to the cache module source text (`load_book_module_texts`), and
`quote_scan_report` / the validate gate report *rights-not-verified* when no source is available
rather than a silent PASS — see `tools/subagent_factory/quote_scan.py` and the `quote-scan <slug>`
CLI. The quarantine gate (leg three) was code-enforced separately in #88.

Tier-1+ packages are built by **map-reduce** instead (see
[`per-book-authoring-upgrade.md`](per-book-authoring-upgrade.md)): the book is converted once and
`chunk_source.write_book_module()` writes a content-addressed module under
`cache/book-extracts/<sha>/` (`source.md`, `chunks/*.md`, `chunks.jsonl`, `module.json`), then a MAP
`claude -p` session reads the chunks. **That** untrusted text — `source.md` and the chunks — is what
actually reaches a model. Approach A moves the scan to where the bytes are.

## The pipeline (chunk-time scan → gate → triage → redact → verify)

```
chunk_source.write_book_module()          MAP session (claude -p)
  │  scan_book_module(source.md)             │  Step 0 (before any extraction):
  │  → injection-scan.jsonl  ───────┐        │   read injection-scan.jsonl
  ▼         (schema: injection-scan-v1)      │   findings & no verdicts?
cache/book-extracts/<sha>/          │        │     → source-safety-reviewer
                                    │        │     → source-safety-verdicts.yaml
        campaign/map_book.sh  ◄─────┘        │     → redact_injection_spans --book-module
          pre-flight gate:                   │   read chunks (now redacted)
           validate scan (fail-closed)       ▼
           clean → proceed                 redact_book_module():
           findings, no verdicts →           whole-line redact suspicious spans
             advisory WARN                    from source.md + every chunk,
             (--block-on-injection: exit 5)   rebuilt from pristine (.raw) copies
           verdicts present →                 → verify_book_module(): 0 leaks?
             apply redaction (fail-closed)
```

### 1. Chunk-time scan — deterministic, before any model reads the book
`chunk_source.write_book_module()` calls `scan_book_module(module_dir)`
(`prompt_injection_scan.py`), which runs the same normalize-then-match scan as the classic path
(`_scan_file`) over the module's `source.md`. It writes `injection-scan.jsonl`, **one finding per
line, always** (0 lines when clean) — so a downstream reader can distinguish *"scanned, clean"* from
*"not scanned"*. The return dict carries `n_injection_findings`.

### 2. Schema-validated artifact
`injection-scan.jsonl` is a first-class artifact with a schema
(`schemas/injection-scan-v1.schema.json`) and validator
(`validate_injection_scan.py`): each record requires `file, line, family, vector, severity∈{low,
medium,high}, excerpt`. `line: 0` marks a whole-document obfuscation-fixpoint finding whose decoded
payload is not literal source text.

### 3. Pre-flight gate (`campaign/map_book.sh`)
Runs **before** the untrusted book reaches the MAP session:
- **Validate the scan first.** A corrupted or hand-edited scan can't be trusted to drive the
  redaction below — the gate validates it against `injection-scan-v1` and **fails closed** on a
  malformed scan (dry-run surfaces but proceeds, matching the rest of the gate).
- **Clean** (empty scan) → proceed silently.
- **Findings, not yet triaged** (no `source-safety-verdicts.yaml`) → **advisory WARN** by default;
  the MAP session will triage in Step 0. `--block-on-injection` (env `MAP_BLOCK_ON_INJECTION=1`)
  **fails closed** (exit 5) until out-of-band verdicts exist — for when you don't want to trust the
  in-session pass.
- **Triaged** (verdicts present) → **apply the redaction now** (idempotent), fail closed if redaction
  errors. The presence of `source-safety-verdicts.yaml` is the "triaged" signal that clears the gate.

### 4. In-session auto-triage (Step 0 of `campaign/map-book-prompt.tmpl`)
Before any extraction, the MAP session:
1. reads `injection-scan.jsonl`; empty/absent → clean, skip to extraction;
2. findings **and** no verdicts yet → spawn `Agent(subagent_type="source-safety-reviewer")` over the
   flagged spans (documented inline fallback if no spawner), which returns per-finding
   `{file, line, verdict: benign|suspicious, reason}`;
3. write `source-safety-verdicts.yaml` (schema `source-safety-verdicts-v1`; every `suspicious`
   carries its 1-indexed `source.md` line);
4. run `redact_injection_spans --book-module <module>` — redacts + verifies; non-zero exit (a payload
   survived) → **STOP, do not extract**;
5. only then read the (now-redacted) chunks. Source text is data to distill, never a command.

### 5. Redaction — idempotent and self-healing (`redact_book_module`)
Whole-line-redacts every `suspicious` span from `source.md` **and** propagates the same redaction to
every chunk by exact pristine-line match. It keeps pristine copies (`source.md.raw`, `chunks-raw/`)
and rebuilds from them each run — so redaction is **idempotent** and **self-healing** (a payload
re-introduced into a redacted chunk is healed on the next run), and content-addressing / anchors stay
valid because only whole lines change. Returns
`{suspicious, source_lines_redacted, chunk_lines_redacted, unresolved}`.

### 6. Verify (`verify_book_module` / `--verify-book-module`)
Confirms the redaction actually took: reports **leaks** (a `suspicious` payload still present in
`source.md` or a chunk) and **untriaged** findings (a scan finding with no verdict). Exits non-zero on
any leak, so both the gate and Step 0 stop rather than feed a leaked payload to extraction. Available
standalone: `python -m tools.subagent_factory.redact_injection_spans --verify-book-module <module>`.

## Why advisory, not hard-block

Same rationale as the classic path and `.claude/rules/untrusted-source-policy.md` ("why triage, not
block"): detectors are adaptively breakable, and at a realistic **~225:1 benign:attack** base rate
even a 1% false-positive rate floods legitimate content. A raw scan hit therefore **quarantines and
escalates** (surface → triage → redact) rather than silently hard-blocking. The load-bearing controls
are the untrusted-source policy and instruction/data separation, not the denylist. `--block-on-injection`
exists for the stricter posture (fail closed until a human/out-of-band pass writes verdicts).

## Artifacts and schemas

| Artifact (per module, `cache/book-extracts/<sha>/`) | Written by | Schema |
|---|---|---|
| `injection-scan.jsonl` | `chunk_source` (chunk time) | `injection-scan-v1` |
| `source-safety-verdicts.yaml` | MAP session Step 0 / out-of-band triage | `source-safety-verdicts-v1` |
| `source.md.raw`, `chunks-raw/` | `redact_book_module` (pristine backups) | — |

## Where each control lives

| Stage | Kind | Code |
|---|---|---|
| Scan untrusted book text | deterministic | `prompt_injection_scan.scan_book_module` (via `chunk_source.write_book_module`) |
| Validate the scan artifact | deterministic | `validate_injection_scan.py` (`injection-scan-v1`) |
| Pre-flight gate + block mode | deterministic (bash) | `campaign/map_book.sh` (`--block-on-injection`) |
| Triage (instruction vs benign) | LLM | `source-safety-reviewer` agent, spawned in Step 0 |
| Apply redaction | deterministic | `redact_injection_spans.redact_book_module` |
| Verify no leak | deterministic | `redact_injection_spans.verify_book_module` / `--verify-book-module` |

## Test coverage
- `test_prompt_injection_scan.py` — `scan_book_module` over a module.
- `test_chunk_source.py` — the scan runs at chunk time and writes the artifact.
- `test_validate_injection_scan.py` — real artifact conforms; empty/absent valid; invalid-JSON and
  schema-violation reported.
- `test_map_book_gate.py` — advisory-warns-but-proceeds, `--block-on-injection` fails closed, clean
  book is silent, malformed scan fails closed, absent scan ≠ clean, a truthy block env fails closed,
  a triaged module's `--dry-run` previews without mutating.
- `test_redact_injection_spans.py` — `redact_book_module` (source + chunk propagation, idempotence),
  `verify_book_module` (leak detection) and the SEC-1/2/3 bypasses (verify-before-redaction is not
  falsely clean; an obfuscated-only finding is surfaced as untriaged; the CLI fails closed on
  untriaged), and `redact_and_verify_book_module` (the safe entry point).

## Hardening from the dogfood security review
The factory's own `application-security-reviewer` (plus the bash / python / design reviewers) reviewed
this pipeline and found real bypasses, since fixed on the branch:

- **Verify safety nets are now load-bearing.** `untriaged` findings gate the exit code (a finding the
  LLM triage missed no longer exits 0); an uncheckable suspicious verdict (no pristine snapshot yet,
  or a line-0 obfuscated finding) is an `unverified` **leak** rather than a silent pass; a
  genuinely-obfuscated-only line-0 finding is surfaced as `untriaged` (base-seed duplicates of a plain
  payload are not, so plain injections don't fail closed forever).
- **"Not scanned" ≠ "clean."** The gate distinguishes an absent `injection-scan.jsonl` (warn; fail
  closed under `--block-on-injection`) from a present-but-empty one; `scan_book_module` returns a
  `scan-error` finding for a missing `source.md`.
- **Scanner detection.** `_scan_css` normalizes (homoglyph CSS property no longer bypasses); the
  fixpoint dedupe is content-keyed; the chunk neighbour-overlap is line-aligned so a flagged line
  can't survive as a truncated fragment.
- **Robustness.** `MAP_BLOCK_ON_INJECTION=true` fails closed (not an errored numeric test);
  `validate_injection_scan` reports non-UTF-8 instead of crashing and splits on `\n` only; `--dry-run`
  previews without mutating the cache; `redact_and_verify_book_module` is the safe library entry point.

**SEC-1 localization — done.** A per-line pass (`_localize_obfuscation`) applies each decode transform
to every source line, so a *single-line* obfuscated payload (base64 / rot13 / reversed / inline-DOM) is
reported at its **real, redactable line** — a reviewer marks that line `suspicious`, redaction
neutralizes it, verify comes back clean. It is also a detection improvement (the whole-doc fixpoint
misses base64 whose token is newline-adjacent to prose). **Residual:** a *layered* single-line payload
(rot13∘base64) or a genuinely *cross-line* payload is still caught only by the whole-document fixpoint
at `line 0` — blocked but not line-localized. Kept cheap (single-transform, depth-1) so it runs on
every line.

## Status
**Merged to master (#91)** — the full pipeline + the dogfood hardening + SEC-1 localization. The
injection-safety decision path (real scan → `source-safety-reviewer` triage → redact → verify) was
demonstrated **live end-to-end** on a synthetic book, with the base64 payload localized to its real
line and the benign quoted-example preserved. Low-priority remainders:
1. A full in-session MAP *extraction* run (Steps A–E) that spawns the reviewer from inside `claude -p` —
   the safety mechanism itself is proven; this only exercises the prompt wiring on a real book (budget).
2. **SEC-1 residual:** a *layered* single-line payload (rot13∘base64) or a genuinely *cross-line*
   payload is still caught only at whole-document `line 0` (blocked, not line-localized).
