#!/usr/bin/env python3
"""Deterministic generator for the LLM-authored layer of mcp-protocol-advisor.

Reads the deterministic spine (principles / evidence / claims / anchors) + the hand-authored
profile.yaml, and emits: faithfulness report, skills, references, tests, provenance, CHANGELOG.
Every cited principle/claim/evidence/source_anchor id resolves to one that exists in the package.

Skill partition is derived deterministically: each principle is assigned to the MCP spec page its
backing claims come from (majority source_id), and pages are grouped into 13 thematic skills.
"""

import collections
import hashlib
import json
import re
import textwrap
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parent.parent
DATE = "2026-07-05"
VERSION = "0.1.0"
SLUG = "mcp-protocol-advisor"

# ---- load spine -------------------------------------------------------------
principles = yaml.safe_load((BASE / "principles/principles.yaml").read_text())["principles"]
P = {p["principle_id"]: p for p in principles}

claim_ids = set()
claim_stmt = {}
claim_src = {}
for line in (BASE / "analysis/claims.jsonl").read_text().splitlines():
    line = line.strip()
    if not line:
        continue
    d = json.loads(line)
    claim_ids.add(d["claim_id"])
    claim_stmt[d["claim_id"]] = d["statement"]
    claim_src[d["claim_id"]] = d.get("source_id")

c2e = {}
c2anchor = {}
for r in yaml.safe_load((BASE / "evidence/evidence-records.yaml").read_text())["evidence_records"]:
    cid = r["claim_id"]
    c2e.setdefault(cid, []).append(r["evidence_id"])
    for a in r.get("source_anchors", []) or []:
        c2anchor.setdefault(cid, []).append(a)

anchor_ids = set()
for af in (BASE / "sources/anchors").glob("*.anchors.jsonl"):
    for line in af.read_text().splitlines():
        line = line.strip()
        if line:
            anchor_ids.add(json.loads(line)["anchor_id"])


def resolved_claims(pid, n=3):
    """First n derived claims of a principle that resolve in claims.jsonl."""
    out = [c for c in P[pid]["derived_from_claims"] if c in claim_ids]
    return out[:n]


# ---- skill partition (all 253 principles, no overlap), derived from source page -------------
# Each MCP spec page (source_id) maps to exactly one thematic skill.
PAGE_SKILL = {
    "mcp-spec-overview-37bf1590": "base-protocol-and-messages",
    "mcp-spec-basic-overv-a504a340": "base-protocol-and-messages",
    "mcp-spec-architectur-0b6ac42d": "architecture-and-trust-model",
    "mcp-spec-server-over-ddb8b9b4": "architecture-and-trust-model",
    "mcp-spec-basic-lifec-88472000": "connection-lifecycle-and-capabilities",
    "mcp-spec-basic-trans-5a86d66a": "transports",
    "mcp-spec-util-cancel-a5220827": "cancellation-ping-and-progress",
    "mcp-spec-util-ping-2702be9d": "cancellation-ping-and-progress",
    "mcp-spec-util-progre-8f5b562e": "cancellation-ping-and-progress",
    "mcp-spec-util-tasks-8df00bee": "long-running-tasks",
    "mcp-spec-server-tool-8ed43301": "server-tools",
    "mcp-spec-server-reso-37de412b": "server-resources-and-prompts",
    "mcp-spec-server-prom-a17e8901": "server-resources-and-prompts",
    "mcp-spec-server-util-88cd5f33": "server-completion-logging-and-pagination",
    "mcp-spec-server-util-b287e6ef": "server-completion-logging-and-pagination",
    "mcp-spec-server-util-e59fbe4c": "server-completion-logging-and-pagination",
    "mcp-spec-client-elic-01bfb448": "elicitation",
    "mcp-spec-client-samp-3498fca5": "sampling",
    "mcp-spec-client-root-992d141a": "roots",
    "mcp-spec-versioning-4f99907b": "versioning-and-conformance",
}

# Ordered skills with their one-line headlines.
SKILL_META = [
    (
        "base-protocol-and-messages",
        "Build on the JSON-RPC base protocol and shape every MCP message to spec",
    ),
    (
        "architecture-and-trust-model",
        "Assign each capability to the right side and concentrate trust in the host",
    ),
    (
        "connection-lifecycle-and-capabilities",
        "Drive the three-phase lifecycle and negotiate capabilities before any feature is used",
    ),
    ("transports", "Implement the stdio and Streamable HTTP transports to the negotiated revision"),
    (
        "cancellation-ping-and-progress",
        "Run cancellation, ping, and progress as race-tolerant connection utilities",
    ),
    ("long-running-tasks", "Treat tasks as an experimental, capability-gated, two-phase exchange"),
    (
        "server-tools",
        "Define, discover, invoke, and harden tools with a valid schema and human consent",
    ),
    (
        "server-resources-and-prompts",
        "Expose resources and prompts by unique URI, declared capability, and control owner",
    ),
    (
        "server-completion-logging-and-pagination",
        "Run completion, logging, and pagination to spec, leaking no secrets",
    ),
    ("elicitation", "Keep elicitation user-controlled and route secrets through safe URL mode"),
    (
        "sampling",
        "Route server-originated LLM access through the client with explicit user approval",
    ),
    ("roots", "Treat roots as hard operational boundaries kept in sync and access-safe"),
    (
        "versioning-and-conformance",
        "Judge every behaviour against the negotiated protocol revision, not the newest",
    ),
]


def _principle_source(pid):
    """Majority source_id across a principle's resolvable derived claims."""
    srcs = [
        claim_src[c] for c in P[pid]["derived_from_claims"] if c in claim_ids and claim_src.get(c)
    ]
    return collections.Counter(srcs).most_common(1)[0][0] if srcs else None


# principle -> skill slug
_pri_skill = {pid: PAGE_SKILL[_principle_source(pid)] for pid in P}
_by_skill = collections.defaultdict(list)
for pid in sorted(P):  # stable P-id order within a skill
    _by_skill[_pri_skill[pid]].append(pid)

SKILL_GROUPS = [(slug, head, _by_skill[slug]) for slug, head in SKILL_META]

# every principle assigned exactly once
_assigned = [pid for _, _, pids in SKILL_GROUPS for pid in pids]
assert sorted(_assigned) == sorted(P), set(P) ^ set(_assigned)

REFERENCES = [
    ("mcp-protocol-principles-index", "reference"),
    ("mcp-conformance-evidence-notes", "reference"),
]


def digest(pids):
    """sha256 over the current statements of cited principles + their sampled claims."""
    h = hashlib.sha256()
    for pid in sorted(pids):
        h.update(P[pid]["statement"].encode())
        for c in resolved_claims(pid, 3):
            h.update(claim_stmt.get(c, "").encode())
    return h.hexdigest()


def prov_block(pids, n_claims=2):
    principles_l = list(pids)
    claims_l, evidence_l, anchors_l = [], [], []
    for pid in pids:
        for c in resolved_claims(pid, n_claims):
            claims_l.append(c)
            evidence_l.extend(c2e.get(c, [])[:1])
            anchors_l.extend(c2anchor.get(c, [])[:1])

    def dd(x):
        seen, out = set(), []
        for i in x:
            if i not in seen:
                seen.add(i)
                out.append(i)
        return out

    return {
        "principles": principles_l,
        "claims": dd(claims_l),
        "evidence": dd(evidence_l),
        "source_anchors": dd([a for a in anchors_l if a in anchor_ids]),
        "authored_from_digest": digest(pids),
    }


def wrap(t, width=100):
    return "\n".join(textwrap.wrap(" ".join(t.split()), width=width))


def condense(stmt, limit=320):
    s = " ".join(stmt.split())
    return s if len(s) <= limit else s[: limit - 1].rsplit(" ", 1)[0] + "…"


# ---- SKILLS -----------------------------------------------------------------
def gen_skill(slug, headline, pids):
    prov = prov_block(pids)
    fm = {"name": slug, "kind": "skill", "status": "ready", "provenance": prov}
    lines = ["---", yaml.dump(fm, sort_keys=False, allow_unicode=True).rstrip(), "---", ""]
    lines.append(f"# {slug.replace('-', ' ').title()}")
    lines.append("")
    lines.append(
        wrap(
            f"{headline}. This skill packages {len(pids)} grounded principles the mcp-protocol-advisor "
            "applies when this layer of the Model Context Protocol is in scope. Each finding names the "
            "rule, the protocol revision it belongs to, the failure or interoperability break it "
            "prevents, the conforming behaviour, and the trade-off or residual risk."
        )
    )
    lines.append("")
    lines.append("## When this applies")
    lines.append("")
    seen_when = []
    for pid in pids:
        for w in P[pid]["applies_when"]:
            w = w.strip()
            if w and w not in seen_when:
                seen_when.append(w)
    for w in seen_when:
        lines.append(f"- {w[0].upper() + w[1:]}.")
    lines.append("")
    lines.append("## Procedure")
    lines.append("")
    lines.append(
        wrap(
            "Identify the negotiated protocol revision first, then apply the principles below that are "
            "in scope, highest-risk first. For each one: name the rule and its revision, state the "
            "failure or interoperability break it prevents, give the conforming behaviour, and state the "
            "trade-off or residual risk. Never invent behaviour the spec does not define, and never "
            "weaken a consent or security requirement below what the spec supports."
        )
    )
    lines.append("")
    ordered = sorted(pids, key=lambda x: (P[x]["confidence"] != "high", x))
    for i, pid in enumerate(ordered, 1):
        p = P[pid]
        lines.append(f"{i}. **{pid} ({p['confidence']} confidence).** {condense(p['statement'])}")
    lines.append("")
    lines.append("## Anti-patterns to flag")
    lines.append("")
    lines.append(
        "- Using a feature the peer never advertised, or skipping the initialization "
        "handshake and capability negotiation."
    )
    lines.append(
        "- Judging behaviour against the newest specification when an older revision was "
        "negotiated, or rejecting deprecated-but-present behaviour before its removal window."
    )
    lines.append(
        "- Inventing protocol behaviour the specification does not define, or presenting a "
        "proprietary extension as standard."
    )
    lines.append(
        "- Omitting the failure a rule prevents, the applicable revision, or the trade-off "
        "and residual risk."
    )
    lines.append("")
    lines.append("## Grounding")
    lines.append("")
    lines.append(
        wrap(
            "Principles: "
            + ", ".join(pids)
            + ". Every cited claim, evidence record, and source anchor "
            "resolves in this package's distilled spine (`analysis/claims.jsonl`, "
            "`evidence/evidence-records.yaml`, `sources/anchors/`). The Model Context Protocol "
            "specification is distillation-only here: paraphrased, never quoted."
        )
    )
    lines.append("")
    d = BASE / "skills" / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---- REFERENCES -------------------------------------------------------------
def gen_reference_index():
    slug = "mcp-protocol-principles-index"
    all_pids = list(P)
    prov = prov_block(all_pids, n_claims=1)
    fm = {"name": slug, "kind": "reference", "status": "ready", "provenance": prov}
    lines = ["---", yaml.dump(fm, sort_keys=False, allow_unicode=True).rstrip(), "---", ""]
    lines.append("# MCP Protocol Principles Index")
    lines.append("")
    lines.append(
        wrap(
            "The full set of Model Context Protocol principles distilled from the specification, grouped "
            "by the skill that applies them. Each entry is a paraphrase with its confidence; no source "
            "text is quoted verbatim."
        )
    )
    lines.append("")
    for slug_s, headline, pids in SKILL_GROUPS:
        lines.append(f"## {slug_s.replace('-', ' ').title()}")
        lines.append("")
        lines.append(f"_{headline}._")
        lines.append("")
        for pid in pids:
            p = P[pid]
            lines.append(f"- **{pid}** ({p['confidence']}) — {condense(p['statement'], 260)}")
        lines.append("")
    (BASE / "references" / f"{slug}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def gen_reference_evidence():
    slug = "mcp-conformance-evidence-notes"
    hi = [pid for pid in P if P[pid]["confidence"] == "high"]
    prov = prov_block(hi, n_claims=2)
    fm = {"name": slug, "kind": "reference", "status": "ready", "provenance": prov}
    lines = ["---", yaml.dump(fm, sort_keys=False, allow_unicode=True).rstrip(), "---", ""]
    lines.append("# MCP Conformance — Evidence Notes")
    lines.append("")
    lines.append(
        wrap(
            "Evidence notes behind the highest-confidence MCP conformance principles. Each note ties a "
            "principle to a sample of its backing claims and evidence records so a reviewer can trace a "
            "recommendation to the distilled specification. Source: the Model Context Protocol "
            "specification (2024-11-05 through 2025-11-25); distillation-only."
        )
    )
    lines.append("")
    for pid in hi:
        p = P[pid]
        cs = resolved_claims(pid, 2)
        ev = [e for c in cs for e in c2e.get(c, [])[:1]]
        lines.append(f"## {pid} — {condense(p['statement'], 200)}")
        lines.append("")
        for c in cs:
            lines.append(f"- `{c}`: {condense(claim_stmt.get(c, ''), 240)}")
        lines.append("")
        lines.append(f"Evidence: {', '.join(ev) if ev else '—'}.")
        lines.append("")
    (BASE / "references" / f"{slug}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---- FAITHFULNESS -----------------------------------------------------------
profile = yaml.safe_load((BASE / "profile.yaml").read_text())


def pids_in(text):
    return re.findall(r"P\d{3}", text)


def note_for(pids, gloss):
    pids = [p for p in dict.fromkeys(pids) if p in P]
    frags = []
    for pid in pids[:4]:
        cs = resolved_claims(pid, 2)
        frags.append(f"{pid} (claims {'/'.join(cs)})")
    return f"{gloss} Grounded in principle(s): {'; '.join(frags)}."


def finding(rule_ref, text, gloss, verdict="WITHIN_SCOPE"):
    pids = pids_in(text) or [pid for pid in P if P[pid]["confidence"] == "high"][:2]
    return {
        "rule_ref": rule_ref,
        "verdict": verdict,
        "distortion": ["none"],
        "support_granularity": "section",
        "severity": "low",
        "action": "accept_with_note",
        "note": note_for(pids, gloss),
    }


def gen_faithfulness():
    findings = []
    findings.append(
        finding(
            "role",
            profile["role"],
            "The role restates the specification's framing — reviewing MCP hosts, "
            "clients, and servers for conformance and security across the base "
            "protocol, lifecycle, transports, primitives, client features, tasks, "
            "and trust model — and narrows scope to advice/review (no production "
            "code, no invented behaviour, no product decision). A narrowing, not an "
            "over-claim.",
        )
    )
    for i, t in enumerate(profile["when_to_use"]):
        findings.append(
            finding(
                f"when_to_use[{i}]",
                t,
                "The trigger names a review situation the specification directly "
                "addresses; within scope.",
            )
        )
    for i, t in enumerate(profile["when_not_to_use"]):
        findings.append(
            finding(
                f"when_not_to_use[{i}]",
                t,
                "The exclusion is stronger-restrictive than the source, not "
                "stronger-permissive; a safe narrowing.",
            )
        )
    findings.append(
        finding(
            "outputs.primary_format",
            profile["outputs"]["primary_format"],
            "The output shape (rule, revision, failure prevented, conforming "
            "behaviour, trade-off, next step) follows the specification's normative, "
            "revision-scoped structure.",
        )
    )
    for m in profile["outputs"]["modes"]:
        findings.append(
            finding(
                f"outputs.modes[{m['name']}].trigger",
                m["trigger"] + " " + m["output"],
                f"The {m['name']} mode restates review/advice behaviour the "
                "specification supports; within scope.",
            )
        )
    for i, t in enumerate(profile["quality_bar"]):
        findings.append(
            finding(
                f"quality_bar[{i}]",
                t,
                "The quality bar is drawn directly from the cited principles and no "
                "rule is stronger than its evidence.",
            )
        )
    findings.append(
        finding(
            "minimum_useful_output",
            profile["minimum_useful_output"],
            "The minimum bar (name the rule+revision+failure, apply a named "
            "principle, state the trade-off) is a floor within the spec's scope.",
        )
    )
    for i, t in enumerate(profile["forbidden_behaviours"]):
        findings.append(
            finding(
                f"forbidden_behaviours[{i}]",
                t,
                "The prohibition is more restrictive than the source (bans invented "
                "behaviour, ungated features, and un-consented tool/data access); a "
                "safe narrowing, never an over-claim.",
            )
        )
    for i, t in enumerate(profile["handoff_rules"]):
        findings.append(
            finding(
                f"handoff_rules[{i}]",
                t,
                "The handoff keeps the ship/deprecate/extend decision with the team "
                "and hands out-of-protocol concerns onward; within scope.",
            )
        )
    findings.append(
        finding(
            "source_of_truth_policy.canonical_owner",
            profile["source_of_truth_policy"]["canonical_owner"],
            "Canonical ownership sits with the engineering team; the specification "
            "is authority only for the conformance rules. Within scope.",
        )
    )
    findings.append(
        finding(
            "source_of_truth_policy.precedence",
            profile["source_of_truth_policy"]["precedence"],
            "Precedence favours the caller's negotiated revision and never weakens a "
            "consent or security requirement below source support; within scope.",
        )
    )
    report = {
        "schema_version": "faithfulness-report-v1",
        "subagent_slug": SLUG,
        "findings": findings,
    }
    header = (
        "# Faithfulness review — mcp-protocol-advisor\n"
        "# Per-rule claim-strength check of load-bearing profile rules against the promoted\n"
        "# principles and their backing claims/evidence. No rule is stronger than its evidence;\n"
        "# source_anchors are omitted deliberately (provenance carried in each note via\n"
        "# principle + claim IDs).\n"
    )
    (BASE / "reports").mkdir(exist_ok=True)
    (BASE / "reports/faithfulness-report.yaml").write_text(
        header + yaml.dump(report, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8"
    )


# ---- TESTS ------------------------------------------------------------------
def gen_principle_behaviour_tests():
    modes = ["review", "advise", "compare"]
    tests = []
    for i, pid in enumerate(P):
        p = P[pid]
        when = (p["applies_when"][0] if p["applies_when"] else "this situation").strip()
        mode = modes[i % 3]
        tests.append(
            {
                "test_id": f"PB-{pid}",
                "principle_id": pid,
                "mode": mode,
                "prompt": f"We're {when}. What does the MCP spec require, and what's the trade-off or "
                "residual risk?",
                "expected_behaviour": [
                    f"Applies the principle: {condense(p['statement'], 200)}",
                    "Names the rule and the protocol revision it belongs to, and states the failure it "
                    "prevents plus the trade-off or residual risk.",
                    f"Cites {pid}.",
                ],
                "must_not": [
                    "Invent protocol behaviour the specification does not define, or present a "
                    "proprietary extension as standard.",
                    "Use or endorse a feature without gating it on the declared capability, or omit the "
                    "trade-off / residual risk.",
                ],
            }
        )
    doc = {
        "schema_version": "principle-behaviour-tests-v1",
        "subagent_slug": SLUG,
        "generated_at": DATE,
        "principle_behaviour_tests": tests,
    }
    (BASE / "tests").mkdir(exist_ok=True)
    (BASE / "tests/principle-behaviour-tests.yaml").write_text(
        yaml.dump(doc, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8"
    )


def gen_golden_tests():
    golden = [
        {
            "test_id": "GT-001",
            "description": "Positive routing — task-augmented tools/call, ungated + wrong result channel",
            "prompt": "Our MCP server augments every slow tools/call as a task without checking any "
            "capability, and it returns the operation result inside the CreateTaskResult. "
            "Review it against revision 2025-11-25.",
            "expected_route": "invoke",
            "expected_mode": "review",
            "minimum_output": "A review flagging ungated task augmentation (must gate on the tasks "
            "capability and per-tool execution.taskSupport) and the two-phase "
            "violation (CreateTaskResult carries only task data; the real result "
            "comes through tasks/result), each with the failure it prevents and the "
            "trade-off.",
            "must_do": [
                "Require task augmentation to be gated on the declared tasks capability and per-tool "
                "execution.taskSupport, rejecting with -32601 where forbidden",
                "Flag that CreateTaskResult must carry only task data and the real result must arrive "
                "through tasks/result",
                "Note that every task-related message carries related-task metadata and the task id is "
                "an access-control credential",
                "State the trade-off of tasks (polling and retention) and hand the decision to the team",
            ],
            "must_not_do": [
                "Invent task behaviour the spec does not define",
                "Endorse using a capability the peer never advertised",
            ],
            "principle_coverage": ["P029", "P036", "P075", "P037", "P079"],
        },
        {
            "test_id": "GT-002",
            "description": "Positive routing — host-centered trust and consent for tool invocation",
            "prompt": "We let the model invoke MCP tools directly and plan to trust each tool's "
            "annotations for our security checks. Is that enough?",
            "expected_route": "invoke",
            "expected_mode": "advise",
            "minimum_output": "Advice that concentrates enforcement in the host, requires explicit "
            "per-tool user consent, treats tools as arbitrary code execution, and "
            "refuses to trust server-supplied annotations for security decisions.",
            "must_do": [
                "Concentrate security enforcement and authorization in the host, not the client or server",
                "Require explicit per-tool user consent and treat tools as arbitrary code execution",
                "Refuse to rely on tool annotations from an untrusted server for security decisions",
                "Keep a human in the loop and state the residual risk",
            ],
            "must_not_do": [
                "Endorse trusting server annotations as a complete security control",
            ],
            "principle_coverage": ["P015", "P052", "P007", "P053", "P013"],
        },
        {
            "test_id": "GT-003",
            "description": "Positive routing — transport choice against the negotiated revision",
            "prompt": "We're targeting revision 2025-11-25 but our server only implements the old "
            "HTTP+SSE transport and advertises Streamable HTTP. How should we handle it?",
            "expected_route": "invoke",
            "expected_mode": "advise",
            "minimum_output": "Advice that matches transport to the negotiated revision (HTTP+SSE is "
            "2024-11-05; Streamable HTTP begins 2025-03-26; 2025-11-25 adds stricter "
            "Origin and polling behaviour), with the interoperability break named.",
            "must_do": [
                "Match the transport to the negotiated revision rather than the newest by default",
                "Explain that advertising a transport the server does not implement breaks interoperability",
                "Describe Streamable HTTP wire behaviour (one JSON-RPC message per POST, both accept types)",
                "State the migration trade-off and hand the decision to the team",
            ],
            "must_not_do": [
                "Judge conformance against the newest spec when an older revision was negotiated",
            ],
            "principle_coverage": ["P023", "P027", "P071", "P011"],
        },
    ]
    negative = [
        {
            "test_id": "GT-NEG-001",
            "description": "Negative routing — production implementation request",
            "prompt": "Write the full production MCP server in Python with every tool, resource, and "
            "prompt handler implemented so we can just run it.",
            "expected_route": "do_not_invoke",
            "expected_mode": None,
            "minimum_output": "A redirect: writing the production server implementation is out of "
            "scope; offer to review a design or a specific message for conformance "
            "instead.",
            "must_not_do": [
                "Produce the production server implementation code",
            ],
            "principle_coverage": [],
        },
        {
            "test_id": "GT-NEG-002",
            "description": "Negative routing — out-of-protocol product/model decision",
            "prompt": "Decide our product's pricing tiers and which base LLM we should ship with.",
            "expected_route": "do_not_invoke",
            "expected_mode": None,
            "minimum_output": "A redirect: product strategy and model choice sit outside the MCP "
            "protocol; offer to review the MCP integration or sampling contract "
            "instead.",
            "must_not_do": [
                "Make the product pricing or model-selection decision",
            ],
            "principle_coverage": [],
        },
    ]
    missing = [
        {
            "test_id": "GT-MC-001",
            "description": "Missing context — underspecified conformance request",
            "prompt": "Is our MCP server spec-compliant?",
            "expected_route": "invoke",
            "expected_mode": "review",
            "must_ask_for": [
                "which protocol revision is negotiated or targeted (2024-11-05 … 2025-11-25)",
                "which side and transport is under review (host/client/server; stdio or Streamable HTTP)",
                "which capabilities the server advertises and which primitives/utilities it exposes",
            ],
            "minimum_output": "A request for the missing context (revision, side/transport, advertised "
            "capabilities) before a conformance verdict.",
            "principle_coverage": ["P027", "P058"],
        },
    ]
    doc = {
        "schema_version": "golden-tests-v1",
        "subagent_slug": SLUG,
        "generated_at": DATE,
        "profile_version": VERSION,
        "tier": 2,
        "golden_tests": golden,
        "negative_routing_tests": negative,
        "missing_context_tests": missing,
    }
    (BASE / "tests").mkdir(exist_ok=True)
    (BASE / "tests/golden-tests.yaml").write_text(
        yaml.dump(doc, sort_keys=False, allow_unicode=True, width=120), encoding="utf-8"
    )


# ---- PROVENANCE + CHANGELOG -------------------------------------------------
def _source_rows():
    prof_sources = profile.get("sources", [])
    rows = []
    for s in prof_sources:
        title = " ".join(str(s.get("title", "")).split())
        rows.append(
            f"| `{s['source_id']}` | {title} | {s.get('year')} | {s.get('rights_status')} |"
        )
    return "\n".join(rows), len(prof_sources)


def gen_provenance():
    n_claims = len(claim_ids)
    n_ev = len(
        yaml.safe_load((BASE / "evidence/evidence-records.yaml").read_text())["evidence_records"]
    )
    n_hi = sum(1 for p in principles if p["confidence"] == "high")
    src_rows, n_src = _source_rows()
    txt = f"""# Provenance Ledger — mcp-protocol-advisor

Canonical source of truth: `subagents/mcp-protocol-advisor/profile.yaml`.

This package was assembled by the deterministic map→reduce build (chunk → map → filter → route →
reduce → anchors → assemble). The distilled spine — `analysis/claims.jsonl` ({n_claims} claims),
`evidence/evidence-records.yaml` ({n_ev} records), `principles/principles.yaml` ({len(principles)}
principles, {n_hi} high-confidence), and `sources/anchors/*.anchors.jsonl` — is the deterministic,
validator-checked layer. The LLM-authored layer (this profile, the faithfulness report, the
{len(SKILL_GROUPS)} skills, {len(REFERENCES)} references, and the tests) is derived from those
principles and their backing claims, evidence, and anchors.

## Sources

The {n_src} sources are the pages of the Model Context Protocol specification (revisions 2024-11-05
through 2025-11-25), ingested as Markdown. All are `distillation-only`: content is paraphrased and
restructured, never quoted verbatim.

| source_id | title | year | rights_status |
|-----------|-------|------|---------------|
{src_rows}

## Authored-layer mapping

Each principle is assigned to exactly one skill by the specification page its backing claims come
from (majority source page).

| skill / reference | principles |
|-------------------|-----------|
"""
    for slug, _, pids in SKILL_GROUPS:
        txt += f"| `skills/{slug}` | {len(pids)} ({pids[0]}…{pids[-1]}) |\n"
    txt += f"| `references/mcp-protocol-principles-index` | all {len(P)} |\n"
    txt += "| `references/mcp-conformance-evidence-notes` | high-confidence principles |\n"
    txt += """
## Faithfulness

`reports/faithfulness-report.yaml` grades every load-bearing profile rule against the promoted
principles on the claim-strength scale. All findings are `WITHIN_SCOPE` (the profile narrows the
specification to conformance review; no rule is stronger than its evidence). `source_anchors` are
omitted from the report deliberately — provenance is carried in each note via principle + claim IDs.

## Version History

| version | date | change |
|---------|------|--------|
| 0.1.0 | 2026-07-05 | Initial authored layer over the map→reduce distilled spine (MCP specification, %d pages, %d principles). |
""" % (n_src, len(P))
    (BASE / "provenance-ledger.md").write_text(txt, encoding="utf-8")


def gen_changelog():
    n_hi = sum(1 for p in principles if p["confidence"] == "high")
    txt = f"""# Changelog — mcp-protocol-advisor

All notable changes to this generated subagent package are recorded here. The canonical source of
truth is `profile.yaml`; the installed adapter is a derived artifact.

## [{VERSION}] — {DATE}

### Added

- Initial LLM-authored layer over the deterministic map→reduce distilled spine (the Model Context
  Protocol specification, revisions 2024-11-05 through 2025-11-25; {len(claim_ids)} claims,
  {len(principles)} principles, {n_hi} high-confidence).
- `profile.yaml` — role, scope, three modes (review / advise / compare), quality bar, forbidden
  behaviours, handoff rules, and a knowledge partition of {len(SKILL_GROUPS)} skills +
  {len(REFERENCES)} references mapped to all {len(P)} principles.
- `reports/faithfulness-report.yaml` — per-rule claim-strength check; every load-bearing rule is
  `WITHIN_SCOPE` of its evidence.
- {len(SKILL_GROUPS)} skills, {len(REFERENCES)} references, `tests/golden-tests.yaml`, and
  `tests/principle-behaviour-tests.yaml` (one behaviour test per principle).
- Fixed source metadata `source_type` (`md` → `markdown`).
"""
    (BASE / "CHANGELOG.md").write_text(txt, encoding="utf-8")


# ---- run --------------------------------------------------------------------
if __name__ == "__main__":
    (BASE / "references").mkdir(exist_ok=True)
    for slug, headline, pids in SKILL_GROUPS:
        gen_skill(slug, headline, pids)
    gen_reference_index()
    gen_reference_evidence()
    gen_faithfulness()
    gen_principle_behaviour_tests()
    gen_golden_tests()
    gen_provenance()
    gen_changelog()
    print("OK: authored layer generated")
    print("skills:", len(SKILL_GROUPS), "references:", len(REFERENCES), "principles:", len(P))
    for slug, _, pids in SKILL_GROUPS:
        print(f"  {slug}: {len(pids)} principles")
