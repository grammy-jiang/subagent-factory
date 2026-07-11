# Residual MUST-FIX Triage — intel-review-loop (r3 final round)

Consolidates residual findings from the 10 artifacts that still carried MUST-FIX after the 3-round review→fix cap.
Source: `reports/intel-review-loop/*.r3.review.md`. **Nothing fixed here — triage only.**

## Legend

- **class**: `real-blocker` (genuine invariant / correctness / faithfulness / security break) · `real-polish` (true but non-blocking cleanup) · `drift-nitpick` (reviewer over-reaching past the artifact's altitude, or a by-design item flagged as a defect).
- **action**: `fix-now` · `defer` · `owner-decide`.
- **grounded?**: `mechanical` = safe pure edit, applyable blind (version bump, stray-tag/word delete, ledger row, add a `Field` cap, step-number fix, one-line truthiness gate). `needs-source` = change to a rule/claim/skill body that must cite a source/principle — **do not apply ungrounded**. `needs-source(code)` = substantive MCP code correctness/security fix needing engineering design + re-test — same "do not blind-apply" flag, engineering not source-citation.
- All 4 MCP servers: **test gate PASS** (88 / 99 / 110 / 122 passed). Their must-fixes are design/security/correctness invariant breaks, not failing tests.

---

## Group A — Reviewer subagents (profile / faithfulness / adapter)

### calibration-forecasting-reviewer (profile v1.0.2)
| target | finding (≤12w, file:line) | severity | class | action | grounded? |
|---|---|---|---|---|---|
| cal-fore-reviewer | M1 `forbidden_behaviours[2]` flat-bans "almost right" credit; P025/P086 want proportional (HEDGING_REMOVED) | MUST | real-blocker | fix-now | needs-source |
| cal-fore-reviewer | M2 `faithfulness-report.yaml` citations templated, mis-attributed, graded on 3-of-N IDs | MUST | real-blocker | fix-now | needs-source |
| cal-fore-reviewer | H1 routing overlap w/ `analytic-method-reviewer`; neither package disambiguates | HIGH | real-blocker | owner-decide | needs-source |
| cal-fore-reviewer | L2 `role` names Tetlock without Gardner; L7 adapter "Not for" partial | LOW | real-polish | defer | mechanical |

### deception-detection-reviewer (v1.0.2)
| target | finding | severity | class | action | grounded? |
|---|---|---|---|---|---|
| deception-reviewer | H1 operator-voice invariants outrank reviewer-only boundary (authority-escalation) | MUST | real-blocker | fix-now | needs-source |
| deception-reviewer | H2 `always_on[3]`/P004 drops `applies_when` condition (SCOPE_BROADENED) | MUST | real-blocker | fix-now | needs-source |
| deception-reviewer | H3 governance skill self-audits review team — scope not in profile | MUST | real-blocker | fix-now | needs-source |
| deception-reviewer | M1 P042 cited on no-real-world-attack rule; P042 is integrity principle | MED | real-polish | fix-now | needs-source |
| deception-reviewer | M2 `golden-tests.yaml` profile_version 1.0.0 vs profile 1.0.2 | MED | real-polish | fix-now | mechanical |
| deception-reviewer | M3 profile ~986 words, 14 below 1000-word FAIL line | MED | real-polish | defer | needs-source |
| deception-reviewer | L7 adapter:3 frontmatter truncated ("double-agent system" dropped) | LOW | real-polish | fix-now | mechanical |

---

## Group B — METHOD skills (`intelligence-analysis-agent/.claude/skills/*`)

### structured-analysis
| target | finding | severity | class | action | grounded? |
|---|---|---|---|---|---|
| skill-structured-analysis | M1 Step 9 (L153) reads `calibration-tracker`; frontmatter (L4) grants write only | MUST | real-blocker | fix-now | needs-source |
| skill-structured-analysis | S1 bare `Skill` grant vs only 3 skills used (least-privilege) | SHOULD | real-polish | fix-now | mechanical |

### calibrated-forecasting
| target | finding | severity | class | action | grounded? |
|---|---|---|---|---|---|
| skill-calibrated-forecasting | M1 description says "committed"; body says draft-only — inverts load-bearing invariant | MUST | real-blocker | fix-now | mechanical |
| skill-calibrated-forecasting | S2 step-9 case-artifact write names no tool; only read-MCP granted | SHOULD | real-polish | fix-now | needs-source |

### source-evaluation
| target | finding | severity | class | action | grounded? |
|---|---|---|---|---|---|
| skill-source-evaluation | M1 no "raw item is data, not instruction" IPI guardrail | MUST | real-blocker | fix-now | needs-source |
| skill-source-evaluation | S3 corroboration doesn't require items graded / shared-origin check | SHOULD | real-polish | fix-now | needs-source |
| skill-source-evaluation | S6 Purpose/description omit `deception-detection-reviewer` named in Output | SHOULD | real-polish | fix-now | mechanical |

### osint-investigation
| target | finding | severity | class | action | grounded? |
|---|---|---|---|---|---|
| skill-osint-investigation | MF1 step-6 write-back has no granted tool; "human-confirmed" ungated | MUST | real-blocker | fix-now | needs-source |
| skill-osint-investigation | MF2 fan-out `Task` can't strip subagent tools; invariant-4 prose-only | MUST | real-blocker | fix-now | needs-source |
| skill-osint-investigation | SF line 97 "in step 5" should read "in step 6" (self-contradiction) | SHOULD | real-polish | fix-now | mechanical |

---

## Group C — MCP servers (`intelligence-analysis-agent/mcp_servers/*`; tests all pass)

### calibration_tracker (88 passed)
| target | finding | severity | class | action | grounded? |
|---|---|---|---|---|---|
| mcp-calibration_tracker | M1 TOCTOU: resolve/void pre-checks read outside `_write_lock` (`store.py:302-338`) | CRIT | real-blocker | fix-now | needs-source(code) |
| mcp-calibration_tracker | M2 manifest tail-truncation bypasses `verify_chain` (no row-count anchor) | HIGH | real-blocker | fix-now | needs-source(code) |
| mcp-calibration_tracker | M3 `horizon` never enforced → immediate self-grade w/ hindsight | HIGH | real-blocker | owner-decide | needs-source(code) |

### evidence_ledger (99 passed)
| target | finding | severity | class | action | grounded? |
|---|---|---|---|---|---|
| mcp-evidence_ledger | MF-1 judgment boundary docstring-only; caller injects `analyst_confirmed` | MUST | real-blocker | fix-now | needs-source(code) |
| mcp-evidence_ledger | MF-2 `EVIDENCE_ALLOW_UNREDACT` checks presence not truthiness (life-safety) | MUST | real-blocker | fix-now | mechanical |
| mcp-evidence_ledger | SF-1 read-path IDs (`get/list/history`) bypass `_MAX_ID` cap | SHOULD | real-polish | fix-now | mechanical |

### ach_engine (110 passed)
| target | finding | severity | class | action | grounded? |
|---|---|---|---|---|---|
| mcp-ach_engine | M1 TOCTOU: `create_matrix`/`rate_cell` head-read outside `_write_lock` | CRIT | real-blocker | fix-now | needs-source(code) |
| mcp-ach_engine | M2 `create_matrix` hypotheses have no per-string length cap (DoS bypass) | MUST | real-blocker | fix-now | mechanical |
| mcp-ach_engine | S2 `analyst_confirmed` not bound to the specific cell judgment | SHOULD | real-polish | defer | needs-source(code) |

### osint_toolkit (122 passed)
| target | finding | severity | class | action | grounded? |
|---|---|---|---|---|---|
| mcp-osint_toolkit | MF1 blocked exfil (`_screen` raise) leaves no audit row (breaks control #10) | MUST | real-blocker | fix-now | needs-source(code) |
| mcp-osint_toolkit | MF2 `res.data.evidence_id` deref crashes on dict/shape-drift | MUST | real-blocker | fix-now | needs-source(code) |
| mcp-osint_toolkit | MF3 `verify_chain` can't detect tail-truncation (unkeyed, no anchor) | MUST | real-blocker | fix-now | needs-source(code) |
| mcp-osint_toolkit | SF1 `pii` defaults `False` on life-safety redaction (by-design boundary) | SHOULD | drift-nitpick | owner-decide | mechanical |

---

## Cross-cutting root causes (shared across targets)

1. **Hash-chain tail-truncation not detectable** — `calibration_tracker M2` + `osint_toolkit MF3` are the *same* defect: forward-only re-derivation with no off-host/row-count anchor, so deleting trailing rows leaves `verify_chain` green. `ach_engine S1` (truncated-line crash) and `evidence_ledger N2` are the same family; note `evidence_ledger`'s manifest cross-check was verified to *catch* truncation, so it is the pattern to copy. **Cheap shared fix = per-table monotonic row-count/seq in the manifest**; the "durable off-host WORM" ask leans over-altitude for a local stdio server → owner-decide.
2. **TOCTOU: chain-head read outside `_write_lock`** — identical bug + identical fix in `calibration_tracker M1` and `ach_engine M1` (mirror the correct `_insert_hypothesis`/head-read-inside-lock pattern). `evidence_ledger SF-7` (unlocked reads) is the read-side cousin.
3. **Judgment-input boundary trusted, not enforced** — caller-supplied `analyst_confirmed`/`judgment_source` accepted without checking the evidence's `source_channel`: `evidence_ledger MF-1`, `ach_engine S2`, `calibration_tracker` (inert `judgment_source`), `osint_toolkit SF1` (self-asserted `confirmed`/`pii`). Same collect-then-grade gate leaking at every server.
4. **Skill capability-vs-grant mismatch** — a step needs/claims a tool its `allowed-tools` doesn't grant (or grants too broadly): `structured-analysis M1` (read not granted) & `S1` (over-broad `Skill`), `calibrated-forecasting S2` (write mechanism unstated), `osint-investigation MF1` (write-back no tool) & `MF2` (can't strip `Task` tools).
5. **Faithfulness over-claim / wrong-principle citation** — profile rule stronger than source or anchored to the wrong ID: `cal-fore M1` (HEDGING_REMOVED) + `M2` (templated/mis-attributed report), `deception H2` (SCOPE_BROADENED) + `M1`/`L2`/`L3` (P042 family). All `needs-source`.
6. **Stale/truncated adapter metadata on version bump** — `deception M2` (golden-tests `profile_version` lagged 1.0.0→1.0.2) + adapter frontmatter truncation `deception L7` / `cal-fore L7`. All mechanical.

---

## SUMMARY

### Counts
- **Total residual MUST-FIX: 20** (cal-fore 2, deception 3, structured-analysis 1, calibrated-forecasting 1, source-evaluation 1, osint-investigation 2, calibration_tracker 3, evidence_ledger 2, ach_engine 2, osint_toolkit 3).
- **Class of the 20 must-fix:** real-blocker **20** · real-polish **0** · drift-nitpick **0**. (The 3-round loop already stripped nitpicks; residuals are genuine invariant/correctness/faithfulness breaks. The one `drift-nitpick` in the table — `osint_toolkit SF1` — is a SHOULD-FIX the reviewer itself labels by-design.)
- **Must-fix by grounded?:** mechanical **3** · needs-source(-code) **17**.
  - The 3 mechanical must-fix (cheap real-blocker wins): `calibrated-forecasting M1` (drop "committed"), `evidence_ledger MF-2` (truthiness gate), `ach_engine M2` (add length cap).
- **Must-fix by action:** fix-now **19** · owner-decide **1** (`calibration_tracker M3` latency policy — reviewer says may be a deliberate tradeoff).
- **Included high-value SHOULD/LOW rows: 12** — real-polish 11 + drift-nitpick 1; of these, mechanical fix-now **6**, needs-source fix-now **3**, defer/owner-decide **3**.
- **Fix-now (mechanical) across ALL rows: 9** — 3 must-fix + 6 polish. **Fix-now (needs-source/code): 19.**

### Cross-cutting themes
- Two hash-chain integrity defects (tail-truncation, TOCTOU head-read) recur across 3–4 servers with one shared fix each — fix once, port everywhere; copy `evidence_ledger`'s already-correct patterns.
- The collect-then-grade **judgment boundary is modeled but not enforced** at every MCP server — a compromised/prompt-injected agent can self-stamp `analyst_confirmed` / `confirmed=True` / `pii=False`. Highest systemic risk.
- Skill layer: **capability claims outrun tool grants** (least-privilege + unrunnable steps) — cheapest wins are scoping/relabeling edits.
- Profile layer: **faithfulness over-claims and wrong-principle citations** are all `needs-source` — must be re-grounded against `principles.yaml`, never reworded blind.

### Recommended minimal fix set (mechanical + cheap real-blockers — clears most residuals without source grounding)
1. `calibrated-forecasting` — drop "committed" from description (**M1, real-blocker**).
2. `evidence_ledger` — allow-list truthiness for `EVIDENCE_ALLOW_UNREDACT` (**MF-2, real-blocker, life-safety**).
3. `ach_engine` — add per-hypothesis `Field(max_length=_MAX_TEXT)` + `min_length=1` (**M2, real-blocker**).
4. `deception` — bump `golden-tests.yaml` `profile_version` → 1.0.2 (M2).
5. `deception` — restore truncated adapter:3 frontmatter noun phrase (L7).
6. `structured-analysis` — scope `Skill` grant to the 3 used names (S1).
7. `source-evaluation` — add `deception-detection-reviewer` to Purpose/description (S6).
8. `osint-investigation` skill — "in step 5" → "in step 6" (step-ref).
9. `evidence_ledger` — annotate read-path IDs with `_MAX_ID` cap (SF-1).
10. MCP servers ×4 — add `ToolAnnotations(readOnlyHint=True)` on reads (mechanical batch).

**→ This clears 3 real-blockers + 7 polish with pure edits, no source grounding.**

### Do NOT apply ungrounded (real-blocker, needs-source / needs design + re-test)
- **Code (engineering judgment + re-test):** TOCTOU ×2 (`calibration_tracker M1`, `ach_engine M1`) · truncation anchor ×2 (`calibration_tracker M2`, `osint_toolkit MF3`) · judgment-boundary enforcement (`evidence_ledger MF-1`) · osint audit-row (`MF1`) + deref-guard (`MF2`).
- **Artifact (must cite source/principle):** `cal-fore M1`+`M2`, `deception H1`+`H2`+`H3`, `source-evaluation M1` (IPI guardrail), `structured-analysis M1` (verify the `calibration-tracker` read tool exists before granting).
- **Owner-decide:** `calibration_tracker M3` (min-latency policy) · `cal-fore H1` (cross-package routing boundary) · durable off-host tamper anchor (may be over-altitude for local stdio).
