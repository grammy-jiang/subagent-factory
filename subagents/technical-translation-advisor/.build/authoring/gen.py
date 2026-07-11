"""Deterministic authoring generator for technical-translation-advisor.

Emits the LLM-authored layer (skills, references, faithfulness report, tests, provenance
ledger, changelog) from the deterministically-valid distilled spine (principles + claims +
evidence). Every cited id is a real id taken from the spine, so provenance resolves and the
package validates. Run from the package root: python3 .build/authoring/gen.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from partition import REFERENCES, SKILLS  # local module

BASE = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------- load spine
PRIN = yaml.safe_load((BASE / "principles" / "principles.yaml").read_text())["principles"]
P = {p["principle_id"]: p for p in PRIN}
CLAIMS: dict[str, dict] = {}
for _line in (BASE / "analysis" / "claims.jsonl").read_text().splitlines():
    _line = _line.strip()
    if _line:
        _c = json.loads(_line)
        CLAIMS[_c["claim_id"]] = _c
EV = yaml.safe_load((BASE / "evidence" / "evidence-records.yaml").read_text())["evidence_records"]
CLAIM_TO_EV: dict[str, list[str]] = {}
for _e in EV:
    CLAIM_TO_EV.setdefault(_e["claim_id"], []).append(_e["evidence_id"])

SLUG = "technical-translation-advisor"
BOOKS = "Jody Byrne's *Technical Translation: Usability Strategies for Translating Technical Documentation* (2006) and *Scientific and Technical Translation Explained* (2012)"


def first_sentence(text: str, limit: int = 240) -> str:
    text = " ".join(text.split())
    # split on the first sentence-ending period that is not a decimal / abbreviation
    m = re.search(r"(?<=[a-z0-9\)])\.(?:\s|$)", text)
    s = text[: m.start() + 1] if m else text
    if len(s) > limit:
        # truncate on a word boundary so we never sever a word mid-character
        s = s[:limit].rsplit(" ", 1)[0].rstrip(" ,;:—-") + "…"
    return s


def full_statement(pid: str) -> str:
    """The complete, whitespace-normalised principle statement — no truncation.

    Procedure steps are the recipe the agent executes, so they must render the whole
    principle, never a fixed-length slice (which previously severed steps mid-clause).
    """
    return " ".join(P[pid]["statement"].split())


def skill_claims(pids: list[str], cap: int = 12) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for pid in pids:
        for cid in P[pid].get("derived_from_claims") or []:
            if cid in CLAIMS and cid not in seen:
                seen.add(cid)
                out.append(cid)
    out.sort()
    # spread across the skill: take an even sample so early principles don't dominate
    if len(out) > cap:
        step = len(out) / cap
        out = [out[int(i * step)] for i in range(cap)]
    return out


def skill_evidence(cids: list[str], cap: int = 8) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for cid in cids:
        for eid in CLAIM_TO_EV.get(cid, []):
            if eid not in seen:
                seen.add(eid)
                out.append(eid)
    out.sort()
    return out[:cap]


def applies_when_bullets(pids: list[str], cap: int = 9) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for pid in pids:
        for aw in P[pid].get("applies_when") or []:
            key = aw.strip().lower()
            if key and key not in seen and len(aw.split()) >= 3:
                seen.add(key)
                out.append(aw.strip().rstrip(".") + ".")
    return out[:cap]


def sibling_line(this_slug: str) -> str:
    others = [s for s in SKILLS if s != this_slug]
    return ", ".join(f"`{s}`" for s in others)


# ---------------------------------------------------------------- skill bodies
def write_skill(slug: str, meta: dict) -> None:
    pids = meta["principles"]
    cids = skill_claims(pids)
    eids = skill_evidence(cids)
    title = meta["title"]
    desc = " ".join(meta["desc"].split())

    fm = {
        "name": slug,
        "description": desc,
        "kind": "skill",
        "status": "ready",
        "provenance": {
            "principles": pids,
            "claims": cids,
            "evidence": eids,
            "source_anchors": [],
        },
    }
    fm_yaml = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, default_flow_style=False)

    when = applies_when_bullets(pids)
    proc_steps = []
    for i, pid in enumerate(pids, 1):
        proc_steps.append(f"{i}. {full_statement(pid)} ({pid})")
    proc_steps.append(
        f"{len(pids) + 1}. Emit recommendations highest-impact first, in the format under Output, "
        "flagging where a draft or plan departs from the principles above."
    )

    body = f"""# {title}

## Purpose

This skill guides the translator to {desc[0].lower() + desc[1:]} It advises on the decision; it
does not produce the final translation, override the client's brief, or sign off safety-critical or
legally-mandated content — those are handed back to the translator and the commissioner.

## When to use

""" + "\n".join(f"- {w}" for w in when) + f"""

## Procedure

""" + "\n".join(proc_steps) + f"""

## Inputs

- The document or excerpt under translation (or its type) and the target-text function.
- The audience, their tasks and prior knowledge, and how the text is used and distributed.
- The translation brief, any client style guide, mandated terminology, and the constraints in force
  (deadline, format, space, safety/legal status).

## Output

Per recommendation: name the applicable principle(s), tie the advice to the audience, brief and
target-text function, state the trade-off or residual uncertainty, and end with a concrete next step.
Order recommendations highest-impact first. The advisor never delivers the translation or makes the
client's commercial or final linguistic decision — that is handed back to the translator and the
commissioner.

## References

See `../../references/technical-translation-principles-index.md` for the full principle catalogue and
`../../references/technical-translation-evidence-notes.md` for grounding notes. For adjacent concerns,
see the sibling skills: {sibling_line(slug)}.

## Provenance

Derived from {', '.join(pids)}, grounded in {BOOKS} (distillation-only). The frontmatter `provenance`
block lists the exact principle, claim, and evidence ids, which resolve into
`principles/principles.yaml`, `analysis/claims.jsonl`, and `evidence/evidence-records.yaml`.
"""
    d = BASE / "skills" / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(f"---\n{fm_yaml}---\n\n{body}", encoding="utf-8")


# ---------------------------------------------------------------- references
def write_reference_index() -> None:
    slug = "technical-translation-principles-index"
    all_pids = [p["principle_id"] for p in PRIN]
    fm = {
        "name": slug,
        "description": REFERENCES[slug]["desc"],
        "kind": "reference",
        "status": "ready",
        "provenance": {"principles": all_pids, "claims": [], "evidence": [], "source_anchors": []},
    }
    fm_yaml = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, default_flow_style=False)
    parts = [f"# {REFERENCES[slug]['title']}\n",
             "Every promoted technical-translation principle, grouped by the skill that owns it. "
             f"Grounded in {BOOKS} (distillation-only).\n"]
    for s, meta in SKILLS.items():
        parts.append(f"\n## {meta['title']}\n\n_Skill: `{s}`_\n")
        for pid in meta["principles"]:
            parts.append(f"- **{pid}** ({P[pid]['confidence']}): {full_statement(pid)}")
    (BASE / "references").mkdir(exist_ok=True)
    (BASE / "references" / f"{slug}.md").write_text(
        f"---\n{fm_yaml}---\n\n" + "\n".join(parts) + "\n", encoding="utf-8"
    )


def write_reference_evidence() -> None:
    slug = "technical-translation-evidence-notes"
    hi = [p["principle_id"] for p in PRIN if p["confidence"] == "high"]
    med = [p["principle_id"] for p in PRIN if p["confidence"] == "medium"]
    fm = {
        "name": slug,
        "description": REFERENCES[slug]["desc"],
        "kind": "reference",
        "status": "ready",
        "provenance": {"principles": [p["principle_id"] for p in PRIN], "claims": [],
                       "evidence": [], "source_anchors": []},
    }
    fm_yaml = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, default_flow_style=False)
    n_src = len({c["source_id"] for c in CLAIMS.values()})
    body = [
        f"# {REFERENCES[slug]['title']}\n",
        f"Grounding notes for the {len(PRIN)} promoted principles, distilled from {BOOKS} "
        "(distillation-only). Confidence is the promotion grade recorded in "
        "`principles/principles.yaml`; every principle resolves into `analysis/claims.jsonl` "
        "and `evidence/evidence-records.yaml` via its `derived_from_claims`.\n",
        "## Corpus\n",
        f"- Sources: {n_src} (both Jody Byrne).",
        f"- Claims: {len(CLAIMS)}. Evidence records: {len(EV)}.",
        f"- Principles: {len(PRIN)} — {len(hi)} high-confidence, {len(med)} medium-confidence.\n",
        "## Confidence and faithfulness\n",
        "- A recommendation may never be stated more strongly than its principle's confidence and "
        "source support (see `reports/faithfulness-report.yaml`).",
        "- Medium-confidence principles carry a weaker evidence base and should be offered as "
        "context-dependent guidance, not universal rules:",
    ]
    for pid in med:
        body.append(f"  - **{pid}**: {first_sentence(P[pid]['statement'], 220)}")
    (BASE / "references" / f"{slug}.md").write_text(
        f"---\n{fm_yaml}---\n\n" + "\n".join(body) + "\n", encoding="utf-8"
    )


# ---------------------------------------------------------------- faithfulness
# Grounding principle ids per gradable profile rule (rule_ref -> [pids]).
FAITH = [
    ("role", "WITHIN_SCOPE",
     "The role restates the sources' subject — producing usable technical/scientific translations — "
     "and narrows the posture to advice, explicitly disclaiming delivering the translation, signing "
     "off safety-critical content, and overriding the brief. A narrowing, not an over-claim.",
     ["P001", "P002", "P003", "P023", "P090"]),
    ("when_to_use[0]", "EXACT_SUPPORT",
     "Analysing the audience, brief and target-text function before wording is directly supported.",
     ["P002", "P020", "P024", "P069", "P129"]),
    ("when_to_use[1]", "EXACT_SUPPORT",
     "Choosing strategy/procedures from the communicative situation and text type is directly supported.",
     ["P014", "P015", "P046", "P089", "P130"]),
    ("when_to_use[2]", "EXACT_SUPPORT",
     "Handling terminology, units, nomenclature, mandated naming and code strings is directly supported.",
     ["P093", "P094", "P103", "P140", "P142"]),
    ("when_to_use[3]", "EXACT_SUPPORT",
     "Designing, structuring and evaluating documentation usability is directly supported.",
     ["P004", "P016", "P040", "P049", "P006"]),
    ("when_to_use[4]", "EXACT_SUPPORT",
     "Reviewing quality, safety, legal-compliance, revision and client-communication decisions is supported.",
     ["P011", "P081", "P117", "P138", "P141"]),
    ("when_not_to_use[0]", "WITHIN_SCOPE",
     "Declining to deliver the finished translation is consistent with the advice-only posture; the "
     "sources locate the delivery and the commission with the translator/commissioner.",
     ["P090", "P056"]),
    ("when_not_to_use[1]", "WITHIN_SCOPE",
     "Excluding general/literary/marketing work with no technical or specification dimension follows "
     "from the sources' scope, which is scientific and technical translation.",
     ["P068", "P091"]),
    ("when_not_to_use[2]", "EXACT_SUPPORT",
     "The client's commercial decision and binding legal sign-off rest with the commissioner, not the "
     "translator; declining them is supported.",
     ["P056", "P090"]),
    ("when_not_to_use[3]", "WITHIN_SCOPE",
     "Deferring the operation of specific CAT/DTP software (vs the translation decision it supports) "
     "is consistent with the sources' treatment of tools as aids.",
     ["P078", "P079"]),
    ("outputs.primary_format", "WITHIN_SCOPE",
     "The advice format — name the principle, tie to audience/brief/function, state the trade-off, give "
     "a next step — operationalises the sources' audience-driven, purpose-led stance without adding claims.",
     ["P002", "P014", "P015"]),
    ("outputs.modes", "WITHIN_SCOPE",
     "The advise/review/compare modes are output shapes for the same audience-driven advice — compare "
     "lays options side by side and weights the choice by audience and the test question — and add no "
     "claim beyond the sources' contextual, purpose-led stance.",
     ["P014", "P015", "P039"]),
    ("quality_bar[0]", "EXACT_SUPPORT", "Audience/tasks/brief-driven decisions are directly supported.",
     ["P002", "P020", "P024", "P069", "P121"]),
    ("quality_bar[1]", "EXACT_SUPPORT", "Strategy from situation and text type, not maxims, is supported.",
     ["P014", "P015", "P046", "P089", "P130"]),
    ("quality_bar[2]", "EXACT_SUPPORT", "Minimising reader processing effort and cognitive load is supported.",
     ["P003", "P009", "P025", "P045", "P137"]),
    ("quality_bar[3]", "EXACT_SUPPORT", "Precise, resourced terminology/units/nomenclature is supported.",
     ["P093", "P094", "P098", "P103", "P104"]),
    ("quality_bar[4]", "EXACT_SUPPORT", "Grounding usability claims in evaluation, not design confidence, is supported.",
     ["P006", "P040", "P049", "P051", "P065"]),
    ("quality_bar[5]", "WITHIN_SCOPE",
     "Honouring safety, legal, brand and style constraints is supported (the legal/standards-QA half is "
     "grounded in P011); the escalate-on-source-deficiency duty is scoped to safety-critical/warning "
     "content (P081), while style and brand constraints are honoured (P102, P144) without a blanket "
     "escalation duty.",
     ["P011", "P081", "P102", "P117", "P144", "P146"]),
    ("forbidden_behaviours[0]", "EXACT_SUPPORT",
     "The commission and delivery rest with the commissioner; refusing to sign off or decide commercially is supported.",
     ["P090", "P056"]),
    ("forbidden_behaviours[1]", "EXACT_SUPPORT",
     "Not stating a rule more strongly than the situation warrants is the sources' own contextual stance.",
     ["P014", "P015"]),
    ("forbidden_behaviours[2]", "EXACT_SUPPORT",
     "Not altering mandated terminology, brand names, or units against the specification is directly supported.",
     ["P103", "P104", "P144"]),
    ("forbidden_behaviours[3]", "EXACT_SUPPORT",
     "Not weakening safety-critical/warning/legal content, and flagging a deficient source, is directly supported.",
     ["P081", "P117", "P146"]),
    ("forbidden_behaviours[4]", "EXACT_SUPPORT",
     "Not presenting an untested usability opinion as an evaluated finding is directly supported.",
     ["P040", "P049"]),
    ("forbidden_behaviours[5]", "WITHIN_SCOPE",
     "Not certifying/signing off safety-critical or legally-mandated content as compliant or safe — the "
     "advisor flags and escalates. The safety-content duty is grounded in P081/P117/P146; the "
     "certification-is-the-client's-process half rests on the regulatory-compliance remit (P098, the same "
     "citation handoff_rules uses for that claim). A within-scope narrowing, not an over-claim.",
     ["P081", "P098", "P117", "P146"]),
    ("handoff_rules[0]", "EXACT_SUPPORT",
     "The brief, commercial decision, and final linguistic sign-off belong to the client/commissioner.",
     ["P056", "P090", "P121"]),
    ("handoff_rules[1]", "WITHIN_SCOPE",
     "Final legal/regulatory certification (the client's compliance process) and heavy DTP/engineering "
     "beyond the translator's baseline file-handling competency being specialist work follows from the "
     "sources: P078 sets the baseline competency (heavy work is beyond it), P098 the legal-specification remit.",
     ["P078", "P098"]),
    ("source_of_truth_policy.precedence", "WITHIN_SCOPE",
     "The precedence order — for instrumental and denotational/functional-priority text, target-user "
     "function governs and denotational meaning/usability is preserved over literal wording (P023, P089); "
     "for documentary translation (back-translation, judicial use) the source is preserved faithfully, "
     "showing errors rather than correcting them, as the governing function (P035); reorder within "
     "sentences/paragraphs/chapters as needed for instrumental work but a whole chapter or section "
     "as a block needs the "
     "client's permission, at minimum informing them (P133); a principle is an adaptable guide not a "
     "fixed rule (P014, P046); no recommendation exceeds its source support (P015); safety and "
     "legally-mandated content is never weakened for style (P081, P146) — restates the sources' "
     "contextual stance with their hedges intact; a narrowing, not an over-claim.",
     ["P014", "P015", "P023", "P035", "P046", "P081", "P089", "P133", "P146"]),
    # knowledge_partition.always_on — the load-bearing runtime rules. Each bullet is a faithful summary
    # of its skill's principles (no clause strengthened beyond its cited principle); graded so the
    # "no over-claim" conclusion is on record for the operative content, not only the meta rules.
    ("knowledge_partition.always_on[0]", "WITHIN_SCOPE",
     "Audience/brief-driven decisions, with 'nearly every' matching P069's own hedge; a faithful summary.",
     ["P002", "P020", "P024", "P056", "P069", "P090", "P121", "P129"]),
    ("knowledge_partition.always_on[1]", "WITHIN_SCOPE",
     "Strategy from situation not maxims, with P133's client-permission caveat for whole-section moves "
     "carried; a faithful summary.",
     ["P014", "P015", "P035", "P046", "P070", "P089", "P130", "P133"]),
    ("knowledge_partition.always_on[2]", "WITHIN_SCOPE",
     "Reader-cognition summary — minimise processing effort and working-memory load; no clause strengthened.",
     ["P003", "P009", "P025", "P045", "P137"]),
    ("knowledge_partition.always_on[3]", "WITHIN_SCOPE",
     "Technical-precision summary; Latin nomenclature kept audience-conditional (P071), SI units hedged "
     "'wherever the source system can be preserved' (P104), web consultation framed as advice to the "
     "translator (Read/Grep/Glob toolset); a faithful summary.",
     ["P071", "P093", "P094", "P098", "P103", "P104", "P140"]),
    ("knowledge_partition.always_on[4]", "WITHIN_SCOPE",
     "Iconic-linkage summary — one uniform construction only where standardisation is practical; faithful.",
     ["P013", "P021", "P074", "P075", "P134"]),
    ("knowledge_partition.always_on[5]", "WITHIN_SCOPE",
     "Document-type/genre summary — classify by communicative purpose before translating; faithful.",
     ["P068", "P072", "P080", "P091", "P128"]),
    ("knowledge_partition.always_on[6]", "WITHIN_SCOPE",
     "Presentation-as-communication summary — layout/typography/structure as usability factors; faithful.",
     ["P004", "P005", "P016", "P124", "P147"]),
    ("knowledge_partition.always_on[7]", "WITHIN_SCOPE",
     "Evaluation-planning summary — method chosen from the test question, observable criteria/metrics; faithful.",
     ["P006", "P018", "P040", "P041", "P084"]),
    ("knowledge_partition.always_on[8]", "WITHIN_SCOPE",
     "Study-conduct summary — representative participants, pilot, control confounds, small-sample stats; faithful.",
     ["P019", "P027", "P051", "P065", "P066"]),
    ("knowledge_partition.always_on[9]", "WITHIN_SCOPE",
     "Quality/safety/practice summary; footnote avoidance scoped to flagging confusion/queries (P139), "
     "safety content made explicit and a deficient source escalated (P081); a faithful summary.",
     ["P001", "P011", "P081", "P117", "P139", "P141", "P144", "P146"]),
]


def write_faithfulness() -> None:
    findings = []
    for rule_ref, verdict, note, pids in FAITH:
        cites = "; ".join(
            f"{pid} (claims {', '.join((P[pid].get('derived_from_claims') or ['—'])[:3])})"
            for pid in pids
        )
        findings.append({
            "rule_ref": rule_ref,
            "verdict": verdict,
            "distortion": ["none"],
            "support_granularity": "section",
            "severity": "low",
            "action": "accept_with_note",
            "note": f"{note} Grounded in principle(s): {cites}.",
        })
    doc = {"schema_version": "faithfulness-report-v1", "subagent_slug": SLUG, "findings": findings}
    (BASE / "reports").mkdir(exist_ok=True)
    header = (
        "# Faithfulness review — technical-translation-advisor\n"
        "# Each load-bearing profile rule graded against principles/principles.yaml (and, via each\n"
        "# principle's derived_from_claims, analysis/claims.jsonl). No rule is stronger than its\n"
        "# source support: rules are EXACT_SUPPORT or a deliberate WITHIN_SCOPE narrowing (advice-only\n"
        "# posture, source scope). source_anchors are omitted deliberately — provenance is carried in\n"
        "# each note via principle + claim IDs, which resolve into the spine.\n"
        "# NOTE (review-loop): P146's principle body was hedged to name external warning-label standards\n"
        "# (ANSI Z535, ISO 3864, IEC 82079-1) and the common severity ranking. That standard content is\n"
        "# ADVISOR-ADDED verification context for safety, not a Byrne source claim (C00820/C00821 cover\n"
        "# only 'warnings need care' + Byrne's own illustrative table); it makes the guidance more\n"
        "# cautious, never less, and is flagged here rather than presented as source-grounded.\n"
    )
    (BASE / "reports" / "faithfulness-report.yaml").write_text(
        header + yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8"
    )


# ---------------------------------------------------------------- pb tests
def write_pb_tests() -> None:
    tests = []
    for p in PRIN:
        pid = p["principle_id"]
        mode = "review" if int(pid[1:]) % 2 == 0 else "advise"
        tests.append({
            "test_id": f"PB-{pid}",
            "principle_id": pid,
            "mode": mode,
            "prompt": (
                f"We are {'reviewing a' if mode == 'review' else 'advising on a'} technical-translation "
                "task and want the relevant principle applied. Given the audience, brief and target-text "
                "function, what should we do here, why, and what trade-off should we carry?"
            ),
            "expected_behaviour": [
                f"Applies the principle: {first_sentence(p['statement'], 260)}",
                "Ties the recommendation to the audience, brief and target-text function, and states "
                "the trade-off or residual uncertainty.",
                f"Cites {pid}.",
            ],
            "must_not": [
                "Deliver the final translation or make the client's commercial or final linguistic "
                "decision for the caller.",
                "State the rule more strongly than the source supports, or weaken safety-critical or "
                "legally-mandated content for style.",
            ],
        })
    doc = {
        "schema_version": "principle-behaviour-tests-v1",
        "subagent_slug": SLUG,
        "generated_at": "2026-07-11",
        "principle_behaviour_tests": tests,
    }
    (BASE / "tests").mkdir(exist_ok=True)
    (BASE / "tests" / "principle-behaviour-tests.yaml").write_text(
        yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8"
    )


# ---------------------------------------------------------------- golden tests
GOLDEN = [
    dict(test_id="GT-001", description="Positive routing — audience/brief analysis",
         prompt="We're translating a power-tool user manual from English into German for DIY "
                "home users sold across the EU. Where do we start before touching the wording?",
         expected_route="invoke", expected_mode="advise",
         minimum_output="Advice to establish audience, tasks, purpose and distribution from the brief "
                        "(asking the client the standard questions if thin), build a document profile, "
                        "and note the EU-language legal requirement — before wording.",
         must_do=["Drive the decision from audience, tasks and the brief/Skopos, not the source alone",
                  "Ask the standard brief questions when the brief is thin",
                  "Flag the EU country-of-sale translation requirement and safety status"],
         must_not_do=["Produce the finished German manual", "Make the client's commercial decision"],
         principle_coverage=["P002", "P020", "P024", "P055", "P090", "P129"]),
    dict(test_id="GT-002", description="Positive routing — strategy/procedure choice",
         prompt="A sentence in a maintenance manual is ambiguous and badly ordered in the source. "
                "Should I translate it literally or restructure it?",
         expected_route="invoke", expected_mode="advise",
         minimum_output="Advice that target-user function governs: restructure/expand to serve the "
                        "reader where the source is poorly ordered, choosing the procedure from the "
                        "situation and text type, and flagging any apparent source error to the client.",
         must_do=["Let target-user function govern over a literal rendering",
                  "Choose the procedure (restructuring, expansion) from the situation, not a maxim",
                  "Advise notifying the client of the apparent source defect"],
         must_not_do=["Assert 'always translate literally' or 'always restructure' as a universal rule"],
         principle_coverage=["P014", "P015", "P133", "P132", "P141", "P023"]),
    dict(test_id="GT-003", description="Positive routing — terminology/units/mandated naming",
         prompt="The client's style guide says use 'cancel' not 'abort'. The source uses 'abort', "
                "and there are SI units and a product name. How do I handle these?",
         expected_route="invoke", expected_mode="advise",
         minimum_output="Advice to honour the mandated terminology, keep SI units unchanged (conversion "
                        "is risky), and never alter the product name — with the reasons.",
         must_do=["Honour the client's mandated preferred terminology",
                  "Leave SI units unchanged wherever possible; conversion risks precision",
                  "Never modify the product/brand name"],
         must_not_do=["Substitute your own preferred term over the client's mandate",
                      "Convert units without the client's rounding precision"],
         principle_coverage=["P103", "P104", "P144", "P093"]),
    dict(test_id="GT-004", description="Positive routing — usability evaluation design",
         prompt="We want to prove our translated user guide is actually usable. How should we test it?",
         expected_route="invoke", expected_mode="advise",
         minimum_output="Advice to run representative task-based usability testing with observable "
                        "criteria and appropriate small-sample statistics, control confounds, and "
                        "pilot first — not rely on readability formulas or design confidence.",
         must_do=["Use representative task-based testing with observable, product-relevant criteria",
                  "Control confounds and pilot before the main study",
                  "Establish usability by evaluation, not design confidence alone"],
         must_not_do=["Claim usability from a readability formula alone",
                      "Present an untested opinion as an evaluated finding"],
         principle_coverage=["P006", "P040", "P049", "P065", "P066", "P084"]),
    dict(test_id="GT-005", description="Positive routing — safety/warning content review",
         prompt="Review my draft translation of the safety warnings section of a machinery manual.",
         expected_route="invoke", expected_mode="review",
         minimum_output="A review that treats warning content as high-stakes: explicit, correctly "
                        "signalled, legally weighted, and escalated to the client if the source is "
                        "deficient — highest-impact first.",
         must_do=["Treat safety/warning content as a matter of accuracy and legal weight",
                  "Make it explicit and escalate a deficient source to the client",
                  "Ground each finding in a named principle"],
         must_not_do=["Weaken or drop warning content for style", "Sign off the translation as safe"],
         principle_coverage=["P081", "P117", "P146", "P011"]),
    dict(test_id="GT-006", description="Positive routing — iconic linkage / consistency",
         prompt="The source repeats the same instruction with slightly different wording each time. "
                "Should my translation vary it for style?",
         expected_route="invoke", expected_mode="advise",
         minimum_output="Advice to apply iconic linkage — render recurring, semantically identical "
                        "information with one uniform construction — where standardisation is "
                        "practical, and scale it with a style guide / translation memory.",
         must_do=["Apply iconic linkage: one uniform construction for recurring identical information",
                  "Note it reduces memory load and errors, not just style",
                  "Scale consistency with controlled language / style guide / TM"],
         must_not_do=["Recommend varying identical instructions purely for stylistic elegance"],
         principle_coverage=["P021", "P134", "P074", "P075"]),
    dict(test_id="GT-007", description="Positive routing — compare options (compare mode)",
         prompt="Should we evaluate our translated user guide with an expert analytical review or a "
                "task-based user test? Compare the two options for our situation.",
         expected_route="invoke", expected_mode="compare",
         minimum_output="A side-by-side of what each evaluation method favours and costs "
                        "(analytical/inspection vs empirical/task-based), chosen from the test "
                        "question, ending in an audience- and usability-weighted recommendation.",
         must_do=["Lay out what each option favours and costs, side by side",
                  "Choose the method from the test question (formative/summative, analytical/empirical)",
                  "Weight the recommendation by audience and usability, and ground it in named principles"],
         must_not_do=["Present an untested opinion as an evaluated finding",
                      "Recommend one option without stating the trade-off it carries"],
         principle_coverage=["P039", "P040", "P041", "P049", "P084"]),
]

NEGATIVE = [
    dict(test_id="NR-001", description="Negative — literary translation, no technical dimension",
         prompt="Translate this poem's closing stanza into French, keeping the rhyme and mood.",
         expected_route="do_not_invoke", expected_mode=None,
         minimum_output="Decline: literary/creative translation with no technical or usability "
                        "dimension is out of scope.",
         principle_coverage=["P068", "P091"]),
    dict(test_id="NR-002", description="Negative — pure commercial/pricing decision",
         prompt="What price and deadline should I quote the client for this 40-page translation?",
         expected_route="do_not_invoke", expected_mode=None,
         minimum_output="Decline: the commercial decision (price, deadline) rests with the "
                        "translator and commissioner, not this advisor.",
         principle_coverage=["P056", "P090"]),
    dict(test_id="NR-003", description="Negative — CAT/DTP software operation",
         prompt="How do I configure the segmentation rules and TM server in memoQ on my machine?",
         expected_route="do_not_invoke", expected_mode=None,
         minimum_output="Decline: operating specific CAT/DTP software is out of scope; the advisor "
                        "covers the translation decision the tool supports, not tool setup.",
         principle_coverage=["P078", "P079"]),
]

MISSING = [
    dict(test_id="MC-001", description="Missing context — no audience or brief",
         prompt="Should I translate this manual literally or freely?",
         expected_route="invoke", expected_mode="advise",
         must_ask_for=["Who the target readers are and their tasks/prior knowledge",
                       "The purpose and distribution of the target text (the brief/Skopos)",
                       "The document type and any client style guide or mandated terminology"],
         minimum_output="Ask for the audience, brief/Skopos, and document type before advising, since "
                        "strategy is chosen from the communicative situation.",
         principle_coverage=["P002", "P024", "P056"]),
    dict(test_id="MC-002", description="Missing context — usability claim, no test data",
         prompt="Is our translated guide usable enough to ship?",
         expected_route="invoke", expected_mode="advise",
         must_ask_for=["What usability criteria and metrics were defined",
                       "Whether representative task-based testing was run, and its results",
                       "The target users, tasks, and context of use"],
         minimum_output="Ask for the evaluation criteria and test results before judging usability, "
                        "since usability is established by evaluation, not design confidence.",
         principle_coverage=["P040", "P049", "P084"]),
]


def write_golden() -> None:
    doc = {
        "schema_version": "golden-tests-v1",
        "subagent_slug": SLUG,
        "generated_at": "2026-07-12",
        "profile_version": "1.1.0",
        "tier": 2,
        "golden_tests": GOLDEN,
        "negative_routing_tests": NEGATIVE,
        "missing_context_tests": MISSING,
    }
    (BASE / "tests").mkdir(exist_ok=True)
    (BASE / "tests" / "golden-tests.yaml").write_text(
        yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100), encoding="utf-8"
    )


# ---------------------------------------------------------------- provenance + changelog
def write_provenance() -> None:
    n_src = len({c["source_id"] for c in CLAIMS.values()})
    hi = sum(1 for p in PRIN if p["confidence"] == "high")
    lines = [
        "# Provenance Ledger — technical-translation-advisor\n",
        "## Sources\n",
        "| source_id | title | author | year | rights |",
        "|---|---|---|---|---|",
        "| technical-translatio-41f3c47c | Technical Translation: Usability Strategies for Translating "
        "Technical Documentation | Jody Byrne | 2006 | distillation-only |",
        "| scientific-technical-d92653ac | Scientific and Technical Translation Explained | Jody Byrne "
        "| 2012 | distillation-only |\n",
        "## Distilled spine\n",
        f"- Claims: {len(CLAIMS)} (`analysis/claims.jsonl`), spanning {n_src} source(s).",
        f"- Evidence records: {len(EV)} (`evidence/evidence-records.yaml`).",
        f"- Principles: {len(PRIN)} (`principles/principles.yaml`) — {hi} high, {len(PRIN) - hi} medium.",
        "- The spine was assembled by the map→reduce build and is deterministically valid; the profile,"
        " faithfulness report, skills, references, and tests are derived from it.\n",
        "## Profile field provenance\n",
        "Every profile rule cites the principle ids it derives from (see `quality_bar`, "
        "`forbidden_behaviours`, `handoff_rules`, `knowledge_partition.always_on`) and is graded in "
        "`reports/faithfulness-report.yaml`. Each of the 10 skills and 2 references carries a "
        "`provenance` block of real principle / claim / evidence ids that resolve into the spine.\n",
        "## Skill → principle map\n",
        "| skill | # principles | principle ids |",
        "|---|---|---|",
    ]
    for s, meta in SKILLS.items():
        lines.append(f"| {s} | {len(meta['principles'])} | {', '.join(meta['principles'])} |")
    lines += [
        "\n## Version history\n",
        "- **v1.1.0** (2026-07-12): Review-loop convergence **plus a 6-lens independent adversarial "
        "verification** via `/review-subagent` (structural lenses + documentation-as-code + ux-design, "
        "and the translation-equivalence / descriptive-translation / translation-quality domain lenses) "
        "— the verify pass caught real holes the loop missed, each fix grounded in the existing spine. "
        "Adapter render (MF1): the invariant compiler truncated must-hold rules at 160 chars and gutted "
        "P146's safety hedge from the deployed adapter — now renders complete first sentences, with a "
        "validate gate on truncated invariants. Content: untruncated skill bodies (MF2); P146 rewritten "
        "so its first sentence carries the verify-the-governing-standard duty, with Byrne's table flagged "
        "as reversing the common ranking (MF3); P003 de-imperative and the adapter template fixed so "
        "invariants are subordinate to the role boundary and forbidden behaviours (MF8); safety/legal "
        "sign-off forbidden behaviour added (MF4); manufactured P045 anchor dropped (MF5); escalation "
        "narrowed to safety in both quality_bar[5] and forbidden[3] (MF6); P133/P104 hedges and the "
        "Latin-nomenclature and footnote scopes restored (MF7 + faithfulness); precedence scoped for "
        "documentary/form-priority translations (P035/P089); P070 completed with adaptation (P131). "
        "Graded the precedence rule and all 10 always_on bullets in the faithfulness report. "
        "Supersedes — does not delete — the v1.0.0 decisions below.",
        "- **v1.0.0** (2026-07-11): Initial LLM-authored layer (profile, faithfulness, 10 skills, "
        "2 references, tests, adapter) derived from the deterministically-valid 2-source, "
        f"{len(PRIN)}-principle distilled spine. Rights: distillation-only; no verbatim source "
        "quotation. multisource_synthesis deferred.",
    ]
    (BASE / "provenance-ledger.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_changelog() -> None:
    (BASE / "CHANGELOG.md").write_text(
        "# Changelog — technical-translation-advisor\n\n"
        "All notable changes to this generated subagent package.\n\n"
        "## 1.1.0 — 2026-07-12\n\n"
        "### Changed\n"
        "- Review-loop convergence **plus independent adversarial verification** (`/review-subagent`): "
        "resolved every must-fix from the structural + domain panel across two passes — the headless "
        "review loop, then a 6-lens adversarial re-verify (faithfulness + documentation-as-code + "
        "ux-design + the translation-equivalence / descriptive-translation / translation-quality domain "
        "reviewers) that caught real holes the loop missed — each fix grounded in the existing spine.\n"
        "- **MF1 (adapter render, safety)** — the invariant compiler (`compile_invariants.py`) truncated "
        "each must-hold rule to 160 chars, gutting P146's warning-severity hedge (and P141, P102) from "
        "the *deployed adapter*; it now renders each invariant as a complete first sentence and "
        "`validate` fails on any truncated (`…`) invariant.\n"
        "- **MF2** — regenerated all 10 skill bodies without the fixed-length truncation that had "
        "severed Procedure steps mid-clause; the generator now renders full statements and rejects any "
        "body containing a truncation ellipsis.\n"
        "- **MF3 (P146, safety)** — rewrote so the first sentence carries the complete duty to verify "
        "the notice-severity hierarchy against the market's governing warning-label standard (ANSI Z535, "
        "ISO 3864, IEC 82079-1); Byrne's table is now a clearly-bracketed example with an explicit flag "
        "that its Warning/Caution assignment is the reverse of the common standard ranking "
        "(DANGER > WARNING > CAUTION > NOTICE).\n"
        "- **MF8 (P003 + adapter template)** — de-imperative'd P003, and fixed the shared adapter "
        "template so the Operating-invariants section is explicitly subordinate to the role boundary and "
        "Forbidden behaviours, resolving the invariants-vs-boundary contradiction.\n"
        "- **MF4** — added a forbidden behaviour against certifying/signing off safety-critical or "
        "legally-mandated content (grounded in the commissioner's sign-off remit, P090).\n"
        "- **Faithfulness** — dropped a manufactured evidence anchor (P045) from precedence; restored "
        "P133's client-permission caveat and P104's hedge; narrowed the source-deficiency escalation to "
        "safety-critical content in **both** quality_bar[5] and forbidden_behaviours[3]; softened "
        "'every'→'nearly every' in **both** quality_bar[0] and always_on[0]; kept Latin nomenclature "
        "audience-conditional (P071) and footnote-avoidance scoped to queries (P139); corrected the P078 "
        "handoff citation; and graded the precedence rule and all 10 always_on bullets.\n"
        "- **Domain accuracy** — scoped precedence so documentary (P035) and form-priority (P089) "
        "translations keep literal fidelity, with P133's reorder threshold corrected; P070 now names "
        "adaptation as the fourth oblique procedure (P131); P042 distinguishes concurrent from "
        "retrospective think-aloud (C00379); P018 prefers a pre-tested questionnaire (C00387); P080 is "
        "scoped to marketing case studies with a genre-check flag (P072/P128).\n"
        "- **SF9/SF10/NH1** — added routing triggers for the iconic-linkage and document-type skills, a "
        "sibling-disambiguation when-not-to-use line, reframed web/EUR-Lex consultation as advice to the "
        "caller (Read/Grep/Glob toolset), and fixed the skill Purpose grammar.\n\n"
        "## 1.0.0 — 2026-07-11\n\n"
        "### Added\n"
        "- Initial LLM-authored layer over the deterministically-valid distilled spine "
        f"({len(PRIN)} principles from 2 distillation-only sources by Jody Byrne).\n"
        "- `profile.yaml` (tier 2, advice-only) with role, when-to-use/not, three modes "
        "(advise/review/compare), quality bar, forbidden behaviours, handoff rules, and a "
        "10-skill / 2-reference knowledge partition — every rule grounded in cited principle ids.\n"
        "- `reports/faithfulness-report.yaml`: every load-bearing profile rule graded against the "
        "principles/claims (EXACT_SUPPORT or deliberate WITHIN_SCOPE narrowing; no over-claim).\n"
        "- 10 authored skills and 2 references, each with resolving principle/claim/evidence provenance.\n"
        "- `tests/`: golden tests (6 positive, 3 negative-routing, 2 missing-context) and "
        f"principle-behaviour tests covering all {len(PRIN)} principles.\n"
        "- Claude Code adapter exported and installed.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    for slug, meta in SKILLS.items():
        write_skill(slug, meta)
    # MF2 regression guard: no skill body may carry a fixed-length truncation ellipsis.
    for slug in SKILLS:
        _body = (BASE / "skills" / slug / "SKILL.md").read_text(encoding="utf-8")
        if "…" in _body:
            raise SystemExit(f"FAIL: skill {slug} still contains a truncation ellipsis")
    write_reference_index()
    write_reference_evidence()
    write_faithfulness()
    write_pb_tests()
    write_golden()
    write_provenance()
    write_changelog()
    print("generated: 10 skills, 2 references, faithfulness, pb-tests, golden, provenance, changelog")
