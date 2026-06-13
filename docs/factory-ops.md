# Factory operations guide

Practical commands for running and maintaining the factory. Generated packages under
`subagents/<slug>/` and adapters under `.claude/agents/generated/` are **gitignored regenerable
output**; the factory *code* is tracked.

## Corpus health — start here

```bash
python -m tools.subagent_factory.cli corpus-health          # table
python -m tools.subagent_factory.cli corpus-health --json    # machine-readable
```

Per package: converter, anchor count + dominant type, tier/status, claims, dangling refs, and a
health flag. Flags:

- `empty-anchors` — conversion produced no anchors (old MarkItDown flatten / never re-authored).
- `no-headings` — paragraph-only anchors (MarkItDown fallback); a Docling re-author upgrades these.
- `junk-anchors` — paragraph anchors dominated by PDF noise.
- `dead-refs` — claims cite anchors not in the index (inconsistent package).
- `ok` — heading anchors, no dead refs.

## PDF conversion (Docling)

Docling is the preferred converter (semantic headings); MarkItDown is the fallback (flattens).
Install CPU-only (see `enhancement-steps/step-20-document-ai-pdf-parsing.md`):

```bash
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
python -m pip install docling
```

The markdown cache is **converter-keyed** (`inputs/markdown-cache/<sha>.<converter>.md`), so
installing Docling over a MarkItDown-cached corpus auto-invalidates the old entries — a re-author
re-converts with Docling automatically, **no manual cache purge needed**.

## Re-author a package on clean anchors

```bash
# /author-subagent <pdf...> --update <slug>   (run via a Claude Code session / headless `claude -p`)
python -m tools.subagent_factory.cli validate <slug>
```

- `source_id` is content-addressed (`<stem>-<sha8>`): re-authoring the same source reuses the id
  and overwrites artifacts in place — no orphaned references, even if a run is interrupted.
- Multi-source packages: pass every source PDF; clear/let the converter-keyed cache invalidate each.
- After a re-author, confirm with `cli validate <slug>` and `cli corpus-health`.

## Faithfulness report flaky? Repair it

The faithfulness step occasionally emits free-text `source_anchors` instead of ids, failing
validation. Repair deterministically (quarantines the bad entries, keeps verdicts):

```bash
python -m tools.subagent_factory.cli repair-faithfulness <slug>   # writes reports/faithfulness-repair.yaml
python -m tools.subagent_factory.cli validate <slug>
```

## Evaluate extraction (claim recall)

Compare two claim sets on content (no ML) — e.g. structure-mapped units vs flat claims:

```bash
python -m tools.subagent_factory.claim_recall <reference> <candidate> [threshold]
#   each path: analysis/claims.jsonl OR sources/maps/<id>.source-map.yaml
```

Reports recall / precision / f1 and the unmatched reference statements (the recall gaps). Lexical
lower bound — use for relative arm comparison, not as absolute truth.

## Evaluate output quality (does the expert give good advice?)

Structural `validate` proves the package is consistent; it does not prove the generated expert gives
good advice on a real task. To measure that — and the **eval-driven multi-source grounding** recipe
that turns a grounding leak into a stronger, more faithful subagent — see
[`output-quality-eval.md`](output-quality-eval.md). Harness: `examples/review-with-subagents.sh`
(read-only, headless).

## Validate before release

```bash
python -m tools.subagent_factory.cli validate <slug>     # per package
make verify                                               # factory code: lint + type + tests + secrets
```
