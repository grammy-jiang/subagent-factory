# Step 1 — Safety + Faithfulness-v0 Gate

> Master: `docs/subagent_enhancement_build_plan.md` §8 Step 1. Depth: **full**.
> Research: `docs/Research/prompt-injection-defense/`, `docs/Research/factual-consistency-faithfulness/`.

## Goal
No polluted or over-claimed subagent can be released: ingested source content is
scanned for injection, the exported adapter is scanned for contamination, and every
profile rule is checked against the source for being **stronger than its evidence**.

> **Scope note.** This spec covers the **classic** path — `prompt_injection_scan` over per-package
> `sources/markdown/`. The real corpus builds Tier-1+ packages by map-reduce and keeps no verbatim
> `sources/markdown/`, so that scan is vacuous there. The cache-level analogue (scan at chunk time →
> gate → in-session triage → redact → verify) is documented separately in
> [`../map-reduce-injection-safety.md`](../map-reduce-injection-safety.md). Both feed the same
> `source-safety-reviewer` triage and the same triage-not-block rationale.

## New files
| Path | Kind | Responsibility |
|------|------|----------------|
| `tools/subagent_factory/prompt_injection_scan.py` | tool (scan, no artifact) | Regex/heuristic scan of `sources/markdown/*.md` → findings. |
| `tools/subagent_factory/adapter_policy_scan.py` | tool (scan, no artifact) | Scan exported adapter for tool-grant/instruction/escalation. Additive to self-check #15. |
| `tools/subagent_factory/validate_faithfulness_report.py` | tool (validator) | Validate `reports/faithfulness-report.yaml` against schema + referential. |
| `schemas/faithfulness-report-v1.schema.json` | schema | Shape of the faithfulness report. |
| `.claude/skills/faithfulness-review/SKILL.md` | skill (LLM) | Rule-vs-source strength comparison → faithfulness report. |
| `.claude/agents/faithfulness-reviewer.md` | agent (LLM) | Runs the comparison; INFO-delegate pattern. |
| `.claude/agents/source-safety-reviewer.md` | agent (LLM) | Triages injection-scan hits (instruction vs benign). |
| `.claude/rules/untrusted-source-policy.md` | rule | Source = data, never instruction; cannot grant tools/edit settings/alter policy. |
| `.claude/rules/evidence-protocol.md` | rule | Global research-question / inclusion / exclusion / confidence-scale defaults. |
| `tests/fixtures/injection/` | fixtures | Attack corpus (below). |
| `tests/fixtures/faithfulness/` | fixtures | Over-claim corpus (below). |

## Reuse
- `source_text.py` (Step 0) — load + whitespace-normalize source markdown.
- `profile_self_check.py` **#15** — already blocks `mcpservers`/`permissionmode`/
  `disallowedtools`/`.claude` in the *neutral core*. `adapter_policy_scan` is **additive**:
  it targets the *exported adapter file*, not the core. Do not re-implement #15.
- `inject_anchors.py` anchor index — `faithfulness-report` `source_anchors` reference real
  `<source_id>-{h,f,c,p}NNNN` IDs (master §1.2).

## Gate wiring (`validate_generated_package.py`)
All Tier 0+ (present-gated). Severity matters:

| Check | Level on hit | Rationale (research) |
|-------|--------------|----------------------|
| `prompt_injection_scan` | **WARN** (quarantine/escalate) | F4: detectors collapse under adaptive GCG → triage layer, **never hard-block**; F-trap: 225:1 base rate → blocking floods legit traffic. |
| `adapter_policy_scan` | **FAIL** (block export) | Adapter contamination is a real escalation; must not ship. |
| `validate_faithfulness_report` (present) | FAIL on schema/referential error; **WARN** on any `unsupported`/`contradicted` finding left unresolved | over-claim = quality defect; surfaced, owner resolves. |

## LLM ↔ deterministic split
- **Deterministic (tools):** both scans (regex/normalize/substring), the report *validator*.
- **LLM (skills/agents):** `faithfulness-reviewer` (semantic strength comparison),
  `source-safety-reviewer` (is a flagged span an instruction or benign quote?).

---

## Research inputs → concrete spec

### A. `prompt_injection_scan.py` (PI research)
Pipeline per source markdown file:
1. **Normalize before matching** (F8 — obfuscation is the primary evasion): decode/flag
   base64 + other base-N, fold Unicode homoglyphs/confusables, reverse-text, emoji-substitution,
   simple substitution ciphers (incl. ROT13 — note ROT13 self-subverts). Match on normalized text.
   Two roles: **decode-to-detect** (catch obfuscated payloads) and **mark-on-keep** — for untrusted
   spans we must retain, apply spotlighting *datamarking/encoding* [2403.14720] (see adapter policy).
2. **Structural sanitize for HTML-derived markdown** (F6): strip/flag CSS-hidden text
   (`opacity:0`, `font-size:0`, `left:-9999px`, off-viewport) and reassemble DOM-fragmented
   spans before matching. (`convert_html.py` is the upstream hook.)
3. **Denylist — canonical phrase families** (full report Practical-Rec #2 + Attack-Fixture Catalogue):
   - `(?i)ignore\s+(all\s+)?(the\s+)?(previous|prior|former|above)\s+instructions`
   - `(?i)disregard\s+(all\s+)?(previous|prior)`
   - authority / fake-system: `### System` / `### Important Messages` / `IMPORTANT!!!` (InjecAgent) / `<INFORMATION>…</INFORMATION>` (AgentDojo) / ASB `strictly adhere to the following instruction`
   - `TODO:`-prefixed action lines
   - fake-completion: `### Response:`, `Task complete.`, `<<SYS>>`, ChatML `<|im_start|>`
   - structural / delimiter spoof: forged closing tag `</data>`, escape-separation (`\n`×n) / escape-deletion (`\b`,`\r`)
   - role override (`(?i)you are now`)
4. **Scan-tail priority** (F7 — injection at END of content has highest ASR): always scan
   the last 500–1000 chars of each chunk; flag tail hits at higher severity.
5. Return findings `{file, line, family, excerpt, location: tail|body, severity}` → gate as
   **WARN** (quarantine). `source-safety-reviewer` triages true-instruction vs benign-quote.

### B. `adapter_policy_scan.py` (PI F2/F9 + StruQ + master §4.4)
Scan `adapters/claude-code/<slug>.md` and the installed copy for: explicit tool-grant lines
beyond the profile's mode-derived tools (`_determine_tools`), instruction-injection patterns
(reuse denylist), permission-escalation tokens, **and delimiter look-alikes** in any embedded
untrusted span (StruQ [2402.06363]: strip/flag look-alikes of the data-slot delimiter). **FAIL**
on any → blocks export. (Effect-side / least-privilege: the adapter must not silently widen authority.)

**Data-marking recipe for untrusted spans** (Spotlighting [2403.14720]): put untrusted content
in a reserved-delimiter slot, strip delimiter look-alikes, and mark with **datamarking**
(whitespace-interleaved signifier — ASR ~50%→3.1%, no utility loss) or **encoding** (one-way
base64 + per-query random marker — *not* forgeable static delimiters or self-subverting ROT13),
bound by a per-query secret `τ = HMAC_k(nonce‖session)`. **Adaptive-attack nuance** [2503.00061]:
GCG/M-GCG break *delimiter isolation* + detectors but **not** datamarking/encoding or
preference-trained structure — so prefer datamarking/encoding; never rely on bare delimiters.

### C. `faithfulness-review` + `faithfulness-report-v1` (factual research)
The reviewer compares **each profile rule** (quality_bar, forbidden_behaviours, mode
triggers) against the source text and classifies claim-strength distortion. **v0 = rule vs
raw source text** (Step 3 upgrades to vs evidence records).

Rubric (factual research): per rule emit a verdict on the **5-level claim-strength ordering**
and the distortion type:

- verdict ∈ `EXACT_SUPPORT | WITHIN_SCOPE | SCOPE_BROADENED | HEDGING_REMOVED | CONTRADICTED`
  (WiCE Partially-Supported = `SCOPE_BROADENED`/`HEDGING_REMOVED`; Janus Specificity = numeric
  precision inflation; Framing = hedge removal).
- The canonical defect: source says *"in this context, prefer X"* → rule says *"always X"* =
  `HEDGING_REMOVED` + `SCOPE_BROADENED`.

`schemas/faithfulness-report-v1.schema.json` (RefChecker triplet-style, 3-way+):
```yaml
schema_version: faithfulness-report-v1
subagent_slug: <slug>
findings:
  - rule_ref: "quality_bar[2]"          # path into profile.yaml
    triplet: {head: "...", relation: "...", tail: "..."}   # optional
    verdict: SCOPE_BROADENED             # 5-level enum
    distortion: [hedge_removed, specificity_inflated]       # subset enum | []
    source_anchors: ["<sid>-p0042"]      # real anchor IDs (master §1.2)
    support_granularity: section         # section|page|heading
    severity: high|medium|low
    action: downgrade|remove|add_condition|accept_with_note
    note: "source hedges ('often'); rule asserts 'always'"
```
`validate_faithfulness_report.py` checks: schema; `rule_ref` resolves in `profile.yaml`;
`source_anchors` ∈ anchor index; enums valid; no `CONTRADICTED`/`unsupported` left with
`action: accept_with_note`.

## Fixtures
- `tests/fixtures/injection/` — seed from the full report's **Attack-Fixture Catalogue (~130 strings)**
  and the code-released benchmark repos (BIPIA `microsoft/BIPIA`, InjecAgent `uiuc-kang-lab`,
  AgentDojo `spylab`, ASB `agiresearch`). Categories: imperative-override, authority/fake-system
  (`IMPORTANT!!!`, `<INFORMATION>`), fake-completion, TODO-injection, delimiter/ChatML spoof
  (`</data>`, `<|im_start|>`, escape-separation/deletion), obfuscation (base64/homoglyph/reverse/ROT13),
  presentation-layer (CSS-hidden + DOM-fragmented), **adaptive** (GCG/M-GCG/AutoDAN suffix/prefix),
  exfiltration sinks (`curl … | bash`, attacker email). Include a **tail-placed** payload (F7) and
  benign near-misses (a doc *quoting* an injection as an example) for triage/FP testing.
- `tests/fixtures/faithfulness/` — paired (source span, generated rule) examples for each
  verdict level, incl. the `HEDGING_REMOVED` canonical case.

## Exit criteria + verify
1. Injection scan flags every malicious fixture (incl. obfuscated/tail/DOM) and **logs, does
   not hard-block**; benign near-miss is WARN (triage), not FAIL.
2. `adapter_policy_scan` FAILs a planted tool-grant adapter; passes clean adapters.
3. `validate_faithfulness_report` accepts a valid report; rejects bad `rule_ref`/anchor/enum.
4. A planted over-claim (`prefer→always`) is caught at `SCOPE_BROADENED`+`HEDGING_REMOVED`.
5. **All 15 packages still pass** validate (faithfulness report absent ⇒ not required at Tier 0
   unless we choose v0 mandatory; default: WARN-if-absent at Tier 0, see open decision).

## Caveats (validate-ourselves / research limits)
- **Over-claim detection is original engineering** (factual gap-1: no validated model). The
  rubric is grounded (WiCE/Janus) but unproven on subagent rules → calibrate on our fixtures.
- **Regex scan is triage, not security** (F4). The load-bearing control is the
  untrusted-source policy + (future) effect-side discipline, not the denylist.
- **Domain mismatch**: faithfulness metrics validated on news/Wikipedia; thresholds tentative.
- **Anchors coarse** (section/page) — `support_granularity` records it.

## Risks
- **False positives flood** if injection scan hard-blocks → enforced as WARN + base-rate note.
- **Faithfulness reviewer is itself an LLM** → bias toward leniency; mitigate with explicit
  rubric few-shots + the deterministic validator refusing unresolved `CONTRADICTED`.
- **Open decision**: is faithfulness-v0 *required* at Tier 0, or WARN-if-absent? Recommend
  WARN-if-absent initially (don't block the 15), promote to required once stable.
