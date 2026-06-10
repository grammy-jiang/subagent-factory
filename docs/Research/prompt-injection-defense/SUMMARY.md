# Research Run Summary — Indirect Prompt-Injection Defenses

## 1. Final Report

```
indirect-prompt-injection-defenses-for-llm-systems-that-ingest-untrusted-documents-detection-content-isolation-and-spotlighting-sanitization-and-benchmarks-research-report.md
```

Size: 36 KB. 20 papers analyzed across 2 rounds.

---

## 2. Round History

| Round | Run ID | Topic / Gap Focus | New Papers | Gaps Addressed | Remaining Gaps |
|-------|--------|-------------------|------------|----------------|----------------|
| 1 | 29fbb1461495 | Original topic — indirect PI defenses (detection, isolation/spotlighting, sanitization, benchmarks) | 11 | Detection + isolation themes covered | 5 academic (G1-G5), 6 engineering (G6-G11), 1 out-of-scope (G12) |
| 2 | 435b9d59086b | Gap-closure: G1 (StruQ/SecAlign/spotlighting primary sources) + G2 (benchmark definition papers) + G4 (adaptive attacks) | 9 | G1 CLOSED, G2 CLOSED, G4 CLOSED; G3 reclassified LOW | 2 academic (G3 MEDIUM, G5 MEDIUM), 6 engineering (G6-G11), 3 out-of-scope (G1/G4/G12) |

**Stop reason**: Converged at round 2. No HIGH-priority ACADEMIC gaps remain. All engineering gaps are resolved inline from corpus evidence. Round cap not reached; early convergence per protocol.

---

## 3. Remaining Open Gaps

### ACADEMIC

| ID | Severity | Classification | Why Still Open |
|----|----------|---------------|----------------|
| G3 | MEDIUM | ACADEMIC | No standalone unified injection-payload taxonomy survey paper found. ASB and BIPIA partially address this (5 and 8 attack families respectively) but no cross-benchmark taxonomy paper exists. Reclassified LOW after round 2 papers partially addressed it. Suggested query: `"indirect prompt injection attack taxonomy adversarial string catalog systematic survey"` |
| G5 | MEDIUM | ACADEMIC | No paper measures FP rate under a realistic ~225:1 benign-to-attack base rate. MIPIAD [2605.07269] uses 10:1; all others omit base-rate analysis. This is an operational measurement gap — additional literature searches unlikely to resolve it; requires field instrumentation. Suggested query: `"prompt injection detector false positive rate realistic traffic base rate precision recall calibration"` |

### ENGINEERING (not resolved by literature; require implementation)

| ID | Severity | Summary |
|----|----------|---------|
| G6 | HIGH | Regex/heuristic denylist for imperative-override payloads (seeds from [2502.05174], [2601.04795], [2410.21492]) |
| G7 | HIGH | Obfuscation-normalization pass: base64, reverse-text, homoglyphs, emoji, substitution ciphers (sources: [2605.07269], [2410.21492]) |
| G8 | HIGH | CSS/HTML structural sanitizer: CSS-hidden text, DOM-fragmented spans (source: [2603.23791]) |
| G9 | HIGH | Format-conformance + minimality checker for tool results (source: [2601.04795]) |
| G10 | MEDIUM | HMAC per-query data-marking tagger — τ = HMAC_k(nonce‖session) (sources: [2410.21492], [2606.09549]) |
| G11 | HIGH | IFC trust-tag propagation + outbound HTTP-verb/origin allowlist (sources: [2409.19091], [2606.09549], [2603.23791]) |

### OUT OF SCOPE

| ID | Summary |
|----|---------|
| G1 | CLOSED: StruQ, SecAlign, Spotlighting now in corpus |
| G4 | CLOSED: Adaptive-attack paper [2503.00061] analyzed |
| G12 | White-box/internal-state defenses (KV-cache pruning, latent steering) — not applicable to text-level ingestion scan |

---

## 4. Top Findings Relevant to Downstream Use

Downstream use: deterministic regex/heuristic scan over ingested Markdown, adapter-policy scan, untrusted-source policy rule, attack fixtures for a factory that converts arbitrary PDFs/HTML into agent behaviour.

### F1 — Canonical injection phrase families (seeds the regex denylist, G6)
**Confidence**: High  
**Finding**: Six stable payload families appear verbatim across all benchmarks: (1) `ignore (previous|prior|former|above) instructions`, (2) `IMPORTANT!!!`, (3) `TODO:` prefixed action lines, (4) fake-completion markers (`### Response:`, `<<SYS>>`), (5) `disregard all previous`, (6) role-play/system overrides (`You are now...`).  
**Paper IDs**: [2403.02691], [2406.13352], [2410.02644], [2312.14197], [2502.05174]

### F2 — Deterministic effect-side gate is the only adaptive-attack-robust control
**Confidence**: High  
**Finding**: Defenses that gate side-effects by policy (SecureClaw's commit-path HMAC handles, IFC planner-executor isolation, Cognitive Firewall's origin+verb allowlist) reach 0–0.64% ASR and remain robust to GCG because they do not rely on the LLM recognizing injection text.  
**Paper IDs**: [2606.09549], [2409.19091], [2603.23791]

### F3 — HMAC per-query tags are unguessable; static delimiters are forgeable
**Confidence**: High  
**Finding**: Static or random delimiter tags (StruQ's `[MARK]`, simple XML tags) are defeated by adaptive attacks that inject a matching closing tag. FATH's `τ = HMAC_k(nonce‖session)` and SecureClaw's per-handle HMAC are not GCG-optimizable because the target is unknown at injection time.  
**Paper IDs**: [2410.21492], [2606.09549], [2402.06363]

### F4 — All LLM-based text-content detectors collapse under adaptive GCG
**Confidence**: High  
**Finding**: Multi-objective GCG drives LLM-based injection detectors from 80%+ detection rate to ~0%. Lexical/semantic detectors, sandwich prompts, and delimiting (without HMAC) are all defeated. The regex scan MUST be treated as a triage layer, not a blocking gate, and should route to escalation/quarantine rather than hard-reject.  
**Paper IDs**: [2503.00061], [2402.06363], [2403.14720]

### F5 — Format-verified field extraction drives ASR from 28.96% → 0.11%
**Confidence**: High  
**Finding**: ParseData module enforces `email=xxx@xxxx.com`, `date=YYYY-MM-DD`, numeric IDs — injected instructions cannot satisfy these predicates. Combined with CheckTool (LLM-based check), reduces AgentDojo ASR by 3 orders of magnitude. Apply to structured tool outputs and PDF metadata fields.  
**Paper IDs**: [2601.04795]

### F6 — CSS-hidden text and DOM-fragmented spans require pre-match normalization
**Confidence**: High  
**Finding**: Opacity-0, font-size-0, off-screen-positioned, and DOM-fragmented payload injection bypasses all text-level scans that operate on rendered text. Must reassemble DOM fragments and strip/flag CSS-hidden content BEFORE denylist matching.  
**Paper IDs**: [2603.23791]

### F7 — Injection at END of document content has highest ASR
**Confidence**: High  
**Finding**: BIPIA measures that placing the malicious instruction at the END of external content produces the highest ASR across all 5 task families and 25 LLMs tested. For the regex scanner: prioritize scanning the last 500–1000 characters of each ingested document chunk.  
**Paper IDs**: [2312.14197]

### F8 — Obfuscation is the primary denylist evasion vector
**Confidence**: High  
**Finding**: Base64 encoding, reverse-text, homoglyph substitution, emoji replacement, and substitution ciphers achieve the highest ASR against lexical detectors. The normalization pass (G7) must decode/fold all these before denylist matching or the lexical scan is trivially bypassed.  
**Paper IDs**: [2605.07269], [2410.21492]

### F9 — IFC integrity-label propagation achieves 0% ASR on InjecAgent (all 4 models)
**Confidence**: High  
**Finding**: Assign T=trusted to user principal + facilities; U=untrusted to all external PDF/HTML/tool responses. Apply lattice join `l(a‖b) = l(a) ⊔ l(b)`. Planner only dispatches tool calls whose result label is T. This is the untrusted-source policy rule (G11).  
**Paper IDs**: [2409.19091]

### F10 — Defense-in-depth across 3+ independent layers survives where single layers fail
**Confidence**: High  
**Finding**: No single shipped defense achieves satisfactory utility-security tradeoff (AgentDojo result). Three independent layers — ingestion provenance labeling, structural prompt separation, deterministic effect-side gate — together provide residual <1% ASR even under adaptive attacks.  
**Paper IDs**: [2603.23791], [2603.30016], [2606.09549], [2409.19091]

---

*Generated 2026-06-10. Research run complete.*
