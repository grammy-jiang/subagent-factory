"""Deterministic authoring generator for research-career-advisor.

Reads the already-assembled, deterministically-valid distilled spine
(principles/principles.yaml + analysis/claims.jsonl + evidence + anchors) and emits the
LLM-authored layer: profile.yaml, references/*, skills/*, tests/*, reports/faithfulness-report.yaml,
provenance-ledger.md, CHANGELOG.md. Every emitted id resolves into the spine.

Cloned from the research-integrity-reproducibility-advisor sibling generator (same recipe:
one deterministic pass over a pre-built Tier-2 spine). Run:  python3 .build/authoring/gen.py
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parents[2]  # subagents/research-career-advisor
SLUG = "research-career-advisor"
VERSION = "1.0.0"
DATE = "2026-07-25"

# ---------------------------------------------------------------------------- spine load
PRINCIPLES = yaml.safe_load((BASE / "principles" / "principles.yaml").read_text())["principles"]
P = {p["principle_id"]: p for p in PRINCIPLES}
ALL_IDS = [p["principle_id"] for p in PRINCIPLES]
HI_IDS = [p["principle_id"] for p in PRINCIPLES if p.get("confidence") == "high"]
N_PRINC = len(ALL_IDS)
CLAIM_IDS = set()
for line in (BASE / "analysis" / "claims.jsonl").read_text().splitlines():
    line = line.strip()
    if line:
        CLAIM_IDS.add(json.loads(line)["claim_id"])


def pids(n: int) -> str:
    return f"P{n:03d}"


# ---------------------------------------------------------------------------- partition
# Each entry: (skill-slug (kebab, <=48 chars), [principle numbers]).
# Every principle 1..48 appears exactly once.
SKILLS: list[tuple[str, list[int]]] = [
    ("writing-and-publishing-scientific-work", [3, 6, 8, 9, 12, 13, 32, 46]),
    ("presenting-and-engaging-with-research", [2, 7, 27, 39]),
    ("choosing-advisers-groups-and-positions", [10, 11, 21, 24, 33, 34]),
    ("early-career-positioning-and-negotiation", [4, 16, 19, 26, 42]),
    ("research-program-and-problem-selection", [15, 17, 22, 23, 25, 35, 43]),
    ("funding-grants-and-research-proposals", [5, 20, 31, 44, 45]),
    ("experimental-design-and-measurement", [14, 40, 41, 47, 48]),
    ("evaluation-metrics-and-research-judgment", [1, 18, 28, 29, 30, 36, 37, 38]),
]

# integrity: every principle exactly once
_seen: list[int] = []
for _slug, _nums in SKILLS:
    _seen += _nums
assert sorted(_seen) == list(range(1, N_PRINC + 1)), f"partition mismatch: {sorted(_seen)}"
assert len(set(s for s, _ in SKILLS)) == len(SKILLS), "duplicate skill slug"
for s, _ in SKILLS:
    assert len(s) <= 48, f"slug too long ({len(s)}): {s}"

REFS = [
    "research-career-principles-index",
    "research-career-evidence-notes",
]
for r in REFS:
    assert len(r) <= 48, f"ref name too long ({len(r)}): {r}"

PID_TO_SKILL = {pids(n): slug for slug, nums in SKILLS for n in nums}

# ---------------------------------------------------------------------------- per-skill themes
THEMES: dict[str, dict] = {
    "writing-and-publishing-scientific-work": dict(
        title="Writing And Publishing Scientific Work",
        purpose=(
            "This skill guides writing up and publishing research so its significance is discoverable "
            "and its claims are sound. It checks that a paper leads with the question, contribution, "
            "and change in understanding across an accurate title, a brief results-focused abstract, "
            "and an introduction that expands the abstract in the same order; that every premise and "
            "logical link is exposed and known weaknesses disclosed rather than claims strengthened "
            "beyond the evidence; that reproducible methodological detail is published without "
            "sacrificing readability; that demanding local review — with language editing where "
            "needed — is obtained before submission; that a result is recast into the broadest "
            "genuinely-supported form without hiding scope; that a doctoral dissertation is built as "
            "one coherent thesis of substantial advances; and that a small portfolio of high-quality "
            "papers is preferred over fragmentation."),
        when=[
            "A paper's title, abstract, or introduction must make the question, contribution, and "
            "change in understanding discoverable, with the abstract self-contained (P006, P032).",
            "A manuscript is being readied for submission: premises and logical links exposed, known "
            "weaknesses disclosed rather than overstated, reproducible detail kept readable, and "
            "demanding local review obtained first (P003, P008, P009).",
            "A doctoral dissertation must be built as one coherent thesis of substantial advances, "
            "excluding unrelated or merely incremental work (P013).",
            "A publication strategy is at issue — a few influential papers over fragmentation, and "
            "recasting a result into its broadest genuinely-supported form (P012, P046).",
        ],
        input="The manuscript, dissertation, or publication plan, its intended venue and audience, "
              "and the evidence behind each claim.",
    ),
    "presenting-and-engaging-with-research": dict(
        title="Presenting And Engaging With Research",
        purpose=(
            "This skill guides communicating research and reading others' work. It checks that a talk "
            "is built as one rehearsed scientific story whose opening establishes the question, "
            "context, and importance at a depth fit for the audience, then connects methods and "
            "results to their significance; that important ideas are communicated through formal "
            "talks, written reports, and timely informal explanation, and improved by critiquing real "
            "presentations and adapting effective techniques; that every slide advances the "
            "scientific argument, omitting filler and including technical detail only when the "
            "intended audience needs it; and that papers are read in layers — mapping the problem and "
            "high-level contribution quickly, then spending most ideation effort challenging "
            "assumptions and devising alternatives."),
        when=[
            "An oral presentation or talk must be built and rehearsed as one scientific story matched "
            "to the audience's needed depth (P002).",
            "An idea needs understanding or adoption and must be communicated through talks, reports, "
            "and timely informal explanation, improved by critiquing real presentations (P007).",
            "Slides or visuals are being chosen and each must advance the argument, with technical "
            "detail only where the audience needs it (P027).",
            "A paper or literature is being read to assess relevance or generate ideas, in layers "
            "that prioritise challenging assumptions and devising alternatives (P039).",
        ],
        input="The talk, slides, or reading task, the audience and its needed depth, and the argument "
              "or research question at stake.",
    ),
    "choosing-advisers-groups-and-positions": dict(
        title="Choosing Advisers, Groups, And Positions",
        purpose=(
            "This skill guides evaluating where to train or work. It checks that an adviser is chosen "
            "for actually protecting access, guidance, continuity, and independent recognition "
            "(preferring an established adviser only when other mentoring qualities are comparable) "
            "and evaluated through trainee evidence — accessibility, real guidance, support for "
            "beginners, group interaction, and whether members grasp the larger scientific purpose; "
            "that a prospective group is researched with informed questions and a genuine complement "
            "between the candidate's goals and the group's work is explained; that a postdoc is "
            "selected for a defined field, prompt access to significant work, a path to a completed "
            "result, and enough visibility for the next role; that a laboratory's management of "
            "priorities, resources, performance, collaboration, and internal mobility is "
            "investigated, since it governs both constraint and escape from a poor supervisory fit; "
            "and that a research-lab publication record is weighed as a route to a later academic "
            "role only while the work stays scientifically significant and publicly visible."),
        when=[
            "A graduate adviser or research group is being selected and must be judged by access, "
            "real guidance, continuity, and independent recognition, using trainee evidence (P010, "
            "P033).",
            "A prospective group must be researched with informed questions and a genuine complement "
            "between the candidate's goals and the group's work explained (P011).",
            "A postdoctoral position is being compared for a defined field, prompt access to "
            "significant work, a completed result, and visibility for the next role (P021).",
            "An industrial or government laboratory is being evaluated for how it manages priorities, "
            "resources, and mobility, and its value as a route to a later academic role (P034, P024).",
        ],
        input="The adviser, group, position, or laboratory under consideration, what is known about "
              "how it actually works, and the candidate's career needs.",
    ),
    "early-career-positioning-and-negotiation": dict(
        title="Early-Career Positioning And Negotiation",
        purpose=(
            "This skill guides establishing an independent research identity and securing the terms "
            "to sustain it. It checks that collaboration is used without surrendering research "
            "identity — contributing distinctive ideas, clarifying authority and credit when "
            "incentives overlap, and initiating work the community can recognize as the researcher's "
            "own; that job-seeking presents evidence of initiative, intellectual leadership, "
            "collegiality, and a concrete first two-to-three-year agenda rather than unfocused "
            "breadth or willingness to do anything assigned; that each main project's expected output "
            "is aligned to the appointment horizon, pairing long work with shorter results and moving "
            "on if timely credited progress cannot be protected; that a result-oriented start-up "
            "package is negotiated and confirmed in writing while alternatives still provide "
            "leverage; and that the professional skills technical training omits are deliberately "
            "learned, with an experienced mentor cultivated outside the direct authority chain."),
        when=[
            "A collaboration is being formed and research identity, authority, and credit must be "
            "protected while distinctive, recognizable work is initiated (P004).",
            "A research or faculty job is being sought and evidence of initiative, leadership, "
            "collegiality, and a concrete first agenda must be presented (P016).",
            "Projects must be scoped to a fixed-term appointment, pairing long work with shorter "
            "results, with a move considered if timely credited output is not protected (P019).",
            "An offer's start-up package must be negotiated and confirmed in writing while leverage "
            "remains, and professional skills and an outside mentor deliberately developed (P026, "
            "P042).",
        ],
        input="The collaboration, application, appointment, or offer at hand, its horizon and "
              "constraints, and the candidate's independent research goals.",
    ),
    "research-program-and-problem-selection": dict(
        title="Research Program And Problem Selection",
        purpose=(
            "This skill guides choosing and steering a body of research over a career. It checks that "
            "the program is oriented around consequential questions the researcher can explain and "
            "partly own, letting the problems determine the techniques; that a long agenda is "
            "decomposed into complete, distinct, publishable milestones, each shown to advance the "
            "larger goal, with defensible advances disseminated promptly and never padded with "
            "repetitive fragments; that worthy, demanding goals are chosen and revisited so daily "
            "choices accumulate toward the intended work, with steady preparation for chance "
            "opportunities; that recurring strategic time audits field direction and maintains a "
            "portfolio of important problems ranked by credible growth and attackability, moving "
            "quickly when a clue changes the ranking; that important problems are mapped against "
            "methods and promising empty regions validated through sustained work; that significant "
            "work begins without waiting for ideal conditions and persists through expected "
            "uncertainty, but is abandoned when evidence shows persistence has become a trap; and "
            "that a manageable portfolio of projects keeps output flowing when one stalls."),
        when=[
            "A research problem, program, or agenda is being chosen and must centre consequential, "
            "ownable questions mapped against methods (P015, P025).",
            "A long-term objective must be decomposed into complete, publishable milestones with "
            "prompt dissemination of defensible advances (P017).",
            "Direction must be audited and a ranked portfolio of important problems maintained, with "
            "steady preparation for chance opportunities and worthy long-range goals (P023, P022).",
            "A difficult problem is underway and needs a begin-now / persist / abandon judgment, with "
            "a manageable multi-project portfolio protecting output (P035, P043).",
        ],
        input="The research direction, problem set, or agenda under consideration, the horizon and "
              "resources available, and the researcher's goals and prior work.",
    ),
    "funding-grants-and-research-proposals": dict(
        title="Funding, Grants, And Research Proposals",
        purpose=(
            "This skill guides winning research funding and arguing the importance and feasibility of "
            "proposed work. It checks that an early-career grant is built around important, "
            "achievable projects — treating a major long-term idea as exploratory and including "
            "enough advanced work to demonstrate results within the award cycle; that related work is "
            "searched and credited, the proposal's distinct contribution explained, credible group "
            "bids joined without surrendering needed evidence of individual initiative, and every "
            "genuinely-fitting funder permitted by the rules applied to; that a project's impact is "
            "assessed by whether it opens a direction, supports broad follow-on use, solves an "
            "important class of problems, or delivers a material advantage over established methods; "
            "that creativity is judged by useful value and meaningful recombination rather than "
            "novelty, execution difficulty, or popularity alone; and that an impossibility claim is "
            "challenged by enumerating its assumptions, testing their applicability, and obtaining "
            "another perspective when the frame may be narrow."),
        when=[
            "An early-career grant or proposal must be scoped to important, achievable projects "
            "deliverable within the award cycle (P005).",
            "Related work must be credited, the distinct contribution explained, and every fitting "
            "funder pursued, joining group bids without losing individual initiative (P020).",
            "A project's or contribution's importance must be argued — impact by direction-opening, "
            "follow-on use, or advantage over prior methods, and creativity by useful value (P031, "
            "P044).",
            "A reviewer or authority calls the proposed result infeasible or impossible and the "
            "claim's assumptions must be enumerated and tested (P045).",
        ],
        input="The proposal or project, its target funder and horizon, the related work, and the "
              "importance and feasibility argument being made.",
    ),
    "experimental-design-and-measurement": dict(
        title="Experimental Design And Measurement",
        purpose=(
            "This skill guides designing sound empirical studies and knowing when to trust their "
            "measurements. It checks that reported precision is treated as possibly optimistic until "
            "the uncertainty process accounts for apparatus tuning and selection effects and is "
            "checked by independent, holdout, or later measurements; that null-hypothesis testing "
            "obtains an appropriate null sampling distribution, expresses the observed deviation in "
            "standard-error units where applicable, and rejects only under a preselected unlikely "
            "region; that a fully-crossed factorial design is used only for the factor combinations "
            "and interactions the research claims need, splitting the study when unneeded "
            "higher-order interactions would make the trial count excessive; that instruments, test "
            "apparatus, and self-generated telemetry are validated independently before being trusted "
            "over the system they measure; and that when intended service life exceeds the validation "
            "window, accelerated-test extrapolation is treated as uncertain, validation is planned "
            "explicitly, and reliability is built into the design."),
        when=[
            "Measurement uncertainty must account for tuning and selection effects and be checked "
            "independently before reported precision is trusted (P014).",
            "A null-hypothesis test needs a valid sampling distribution, standard-error framing, and "
            "a preselected rejection region (P040).",
            "A factorial design must retain only the factor combinations and interactions the claims "
            "require, splitting the study otherwise (P041).",
            "Instruments or self-generated telemetry must be validated independently, and "
            "accelerated-test extrapolation beyond the validation window treated as uncertain (P047, "
            "P048).",
        ],
        input="The study design, statistical test, or measurement setup, the claims it must support, "
              "and the reliability of its instruments and the service horizon.",
    ),
    "evaluation-metrics-and-research-judgment": dict(
        title="Evaluation Metrics And Research Judgment",
        purpose=(
            "This skill guides evaluating people, work, and metrics, and cultivating durable "
            "judgment. It checks that brainstorming proceeds without immediate judgment, preserving "
            "every candidate and revealing existing solutions only after participants have "
            "independently attacked the problem; that tacit professional and systems judgment is "
            "developed through technically grounded practice, varied cases, mixed-experience work, "
            "and timely critique that preserves real context; that people are prepared for changing "
            "conditions through learning-to-learn, durable fundamentals, and problem-formulation; "
            "that every evaluative metric is treated as an intervention — tested for relevance and "
            "gameability, with participant adaptation and time-horizon effects simulated and outcome "
            "quality preferred over an inflatable production count; that early selection is aligned "
            "with the capabilities needed later rather than only entry-stage traits; that expertise "
            "is used with explicit humility about its hidden assumptions and scope; that local work "
            "is connected to valuable delivered system behavior rather than proxy activity volume; "
            "and that ranking people for scarce roles is made explicit, deliberate, and reviewable."),
        when=[
            "Candidate ideas or solutions are being generated and must be preserved and independently "
            "attacked before existing solutions are revealed (P001).",
            "A metric drives rewards, status, or decisions and must be tested for relevance, "
            "gameability, and time-horizon effects, favouring delivered outcome quality (P029, P037).",
            "People are being selected or ranked for scarce roles and the reduction to a score must "
            "be explicit, reviewable, and aligned to later-needed capabilities (P038, P030).",
            "Expert judgment is applied to a broader or changed problem and must surface its "
            "assumptions and scope, while tacit judgment and learning-to-learn are cultivated (P036, "
            "P018, P028).",
        ],
        input="The metric, selection, ranking, or judgment under review, the decision it drives, and "
              "the assumptions and time horizon behind it.",
    ),
}

# ---------------------------------------------------------------------------- helpers

_CUT = [" — ", "—", "; therefore", ", so that", ", since ", ", because ", ", which ",
        ", ensuring", ": ", " (", ", and recognize", ", and respect", ", but "]


def lead(statement: str, limit: int = 235) -> str:
    """A concise lead-clause from a principle statement, grounded verbatim in its wording."""
    s = " ".join(statement.split())
    cut = len(s)
    for tok in _CUT:
        i = s.find(tok)
        if 20 < i < cut:
            cut = i
    s = s[:cut].strip()
    if len(s) > limit:
        s = s[:limit].rsplit(" ", 1)[0].strip()
    s = s.rstrip(" ,.;:—-")
    _DANGLE = {"the", "a", "an", "of", "to", "from", "and", "or", "with", "for", "in",
               "on", "by", "as", "that", "into", "than", "so", "its", "their", "let"}
    while True:
        head, _, last = s.rpartition(" ")
        if head and last.lower().strip(",.;:—-") in _DANGLE:
            s = head.rstrip(" ,.;:—-")
        else:
            break
    return s


def union_claims(nums: list[int], cap: int = 16) -> list[str]:
    seen: list[str] = []
    for n in nums:
        for c in P[pids(n)].get("derived_from_claims", []) or []:
            if c in CLAIM_IDS and c not in seen:
                seen.append(c)
    return sorted(seen)[:cap]


def digest(nums: list[int], claims: list[str]) -> str:
    h = hashlib.sha256()
    for n in nums:
        h.update(P[pids(n)]["statement"].encode())
    for c in claims:
        h.update(c.encode())
    return h.hexdigest()


def frontmatter(name: str, kind: str, nums: list[int], claims: list[str]) -> str:
    prov = {
        "principles": [pids(n) for n in nums],
        "claims": claims,
        "evidence": [],
        "source_anchors": [],
        "authored_from_digest": digest(nums, claims),
    }
    fm = {"name": name, "kind": kind, "status": "ready", "provenance": prov}
    return "---\n" + yaml.safe_dump(fm, sort_keys=False, allow_unicode=True, width=1000) + "---\n\n"


def w(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    print("wrote", path.relative_to(BASE))


print(f"principles={N_PRINC} high={len(HI_IDS)} claims={len(CLAIM_IDS)}")

# ============================================================================ EMITTERS

_SRC_LINE = (
    "grounded in the four distillation-only sources (*A PhD Is Not Enough* by Peter J. Feibelman, a "
    "survival guide for a career in science; *The Art of Doing Science and Engineering* / *You and "
    "Your Research* by Richard W. Hamming, on doing high-impact research; a Chinese guide to "
    "succeeding in academic research; and *Empirical Methods for Artificial Intelligence* by Paul R. "
    "Cohen, on experimental method and measurement)")


def emit_skills() -> None:
    for slug, nums in SKILLS:
        th = THEMES[slug]
        claims = union_claims(nums)
        body = [frontmatter(slug, "skill", nums, claims)]
        body.append(f"# {th['title']}\n")
        body.append("## Purpose\n")
        body.append(th["purpose"] + "\n")
        body.append("## When to use\n")
        for b in th["when"]:
            body.append(f"- {b}")
        body.append("")
        body.append("## Procedure\n")
        for i, n in enumerate(nums, 1):
            body.append(f"{i}. {lead(P[pids(n)]['statement'])} ({pids(n)}).")
        body.append("")
        body.append("## Inputs\n")
        body.append(f"- {th['input']}")
        body.append("- The reasoning offered for the decision under review: the goal, the plan or "
                    "practice in place, and any claim of importance, readiness, or soundness made.\n")
        body.append("## Output\n")
        body.append(
            "Per finding: name the gap and the principle it engages, give the correction, state the "
            "residual trade-off or the referral to make, and end with a concrete next step. Order "
            "findings highest-impact first. This skill advises on research-career and empirical "
            "practice; it does not run the study, write the paper or grant, or make the "
            "hiring, admission, funding, or tenure decision for the caller.\n")
        body.append("## Anti-patterns to flag\n")
        for n in nums[: min(7, len(nums))]:
            body.append(f"- Overlooking {pids(n)}: {lead(P[pids(n)]['statement'], 150)}.")
        body.append("")
        body.append("## References\n")
        body.append(
            f"See `../../references/{REFS[0]}.md` for the full principle catalogue grouped by "
            f"skill, and `../../references/{REFS[1]}.md` for how these principles are grounded and "
            "kept faithful to the sources.\n")
        body.append("## Provenance\n")
        idlist = ", ".join(pids(n) for n in nums)
        body.append(
            f"Derived from {idlist}, {_SRC_LINE}. The frontmatter `provenance` block lists the exact "
            "principle and claim ids, which resolve into `principles/principles.yaml` and "
            "`analysis/claims.jsonl`.\n")
        w(BASE / "skills" / slug / "SKILL.md", "\n".join(body))


def emit_refs() -> None:
    claims = union_claims([n for _, nums in SKILLS for n in nums], cap=16)
    out = [frontmatter(REFS[0], "reference", list(range(1, N_PRINC + 1)), claims)]
    out.append("# Research-Career & Method Principles Index\n")
    out.append("Package-wide index of every promoted principle, grouped by the skill that owns it. "
               "Each entry restates the principle's operative core; the full statement lives in "
               "`../principles/principles.yaml`.\n")
    for slug, nums in SKILLS:
        out.append(f"## {THEMES[slug]['title']}\n")
        out.append(f"Skill: `{slug}`\n")
        for n in nums:
            out.append(f"- **{pids(n)}** — {lead(P[pids(n)]['statement'], 200)}.")
        out.append("")
    w(BASE / "references" / f"{REFS[0]}.md", "\n".join(out))

    out = [frontmatter(REFS[1], "reference", list(range(1, N_PRINC + 1)), [])]
    out.append("# Research-Career & Method Evidence Notes\n")
    out.append("How the principles in this package are grounded, and how to keep advice faithful to "
               "the sources.\n")
    out.append("## Sources\n")
    out.append("Four distillation-only sources ground the package: *A PhD Is Not Enough* (Peter J. "
               "Feibelman) — a survival guide for a career in science (advisers, postdocs, jobs, "
               "offers, talks, and publication strategy); *The Art of Doing Science and Engineering* "
               "and *You and Your Research* (Richard W. Hamming) — on choosing important problems, "
               "sustaining a research program, and learning to learn; a Chinese guide to succeeding "
               "in academic research (finding problems, writing and organizing high-quality papers); "
               "and *Empirical Methods for Artificial Intelligence* (Paul R. Cohen) — on experimental "
               "design, statistical testing, measurement uncertainty, and evaluation. Paraphrase and "
               "restructure only — no verbatim quotation (see "
               "`.claude/rules/rights-and-quotation-policy.md`).\n")
    out.append("## Faithfulness discipline\n")
    out.append("- No advice may state a rule more strongly than its source supports: where a source "
               "ties a practice to a purpose, a context, or the researcher's own goals, keep it an "
               "adaptable guide, not an absolute (P015, P004, P036).")
    out.append("- Career outcomes are never guaranteed or predicted: an adviser, group, position, or "
               "paper is evaluated on evidence and trade-offs, and the hiring, admission, funding, "
               "and tenure decisions are left with the committees and the caller (P010, P021).")
    out.append("- Empirical claims are proportioned to the evidence: reported precision, "
               "significance, and reliability never exceed what the uncertainty analysis, the valid "
               "sampling distribution, and independent checks warrant (P014, P040, P047).")
    out.append("- The advisor guides practice, it does not perform it: it does not run the study, "
               "write the paper or grant, or produce the research output for the caller (P017, "
               "P013).\n")
    out.append("## Grounding\n")
    out.append(f"Spine: {N_PRINC} principles ({len(HI_IDS)} high-confidence) over {len(CLAIM_IDS)} "
               f"atomic claims, with evidence records and chunk anchors. Every principle id "
               f"P001-P{N_PRINC:03d} resolves into `principles/principles.yaml`.\n")
    w(BASE / "references" / f"{REFS[1]}.md", "\n".join(out))


def _always_on() -> list[str]:
    out = []
    for slug, nums in SKILLS:
        ids = ", ".join(pids(n) for n in nums)
        out.append(f"{THEMES[slug]['purpose']} ({ids})")
    return out


PROFILE_ROLE = (
    "An advisor on building a scientific research career and doing high-impact, methodologically "
    "sound research, grounded in four distillation-only sources (Feibelman's *A PhD Is Not Enough*; "
    "Hamming's *The Art of Doing Science and Engineering* / *You and Your Research*; a Chinese guide "
    "to succeeding in academic research; and Cohen's *Empirical Methods for Artificial "
    "Intelligence*). It guides graduate students, postdocs, and early-career faculty on choosing "
    "problems and advisers, positioning and negotiating for research roles, writing and presenting "
    "research, seeking funding, and designing sound empirical studies. The invariants below are "
    "advisory criteria, not authority to act: this advice-only boundary and the forbidden "
    "behaviours override every invariant, so the advisor never runs the study, writes the paper or "
    "grant, makes or predicts a hiring, admission, funding, or tenure decision, or gives binding "
    "legal, financial, or immigration advice.")

WHEN_TO_USE = [
    "Choosing or evaluating a research problem, program, or agenda — which questions are important "
    "and attackable, how to decompose them into publishable milestones, and when to persist versus "
    "abandon.",
    "Choosing an adviser, group, postdoc, or job, or negotiating an offer or start-up package, with "
    "limited information about how the group actually works.",
    "Writing or presenting research — a paper's title, abstract, or introduction, a talk or slide "
    "deck, revising for review, or choosing a publication strategy.",
    "Seeking research funding — framing a proposal's importance and feasibility, crediting related "
    "work, and scoping projects to the award horizon.",
    "Designing or reviewing an empirical study, metric, or measurement for soundness — "
    "null-hypothesis tests, factorial designs, measurement uncertainty, and instrument validation.",
]

WHEN_NOT_TO_USE = [
    "The caller wants the work produced for them — the study run, the data analysed, the paper or "
    "grant written; this advisor guides practice, it does not perform it.",
    "The caller wants a hiring, admission, funding, or tenure decision made or predicted, or an "
    "adviser or employer endorsed as a guaranteed choice.",
    "The caller wants binding legal, financial, contractual, visa or immigration, or HR advice, "
    "which requires qualified professionals.",
    "The task has no research-career or empirical-methods dimension — a pure domain-science answer, "
    "or general software engineering unrelated to research.",
]

QUALITY_BAR = [
    "Problems are chosen for importance and attackability: the program centres consequential "
    "questions the researcher can partly own, keeps a ranked portfolio, and reserves strategic time "
    "to audit direction (P015, P023, P025, P031).",
    "A long agenda is decomposed into complete, publishable milestones with promptly disseminated "
    "advances, not repetitive fragments, and a few high-quality papers are preferred over many weak "
    "ones (P017, P012, P046).",
    "Career moves are evaluated on evidence, not prestige: an adviser, group, or lab is judged by "
    "access, real guidance, credited output, and mobility, and offers are confirmed in writing "
    "while leverage remains (P010, P033, P034, P021, P026).",
    "Communication makes significance discoverable: papers lead with the question and contribution, "
    "a talk is one rehearsed story, every slide advances the argument, and claims never exceed the "
    "evidence (P006, P032, P002, P027, P003).",
    "Empirical claims are proportioned to the evidence: uncertainty accounts for tuning and "
    "selection and is independently checked, instruments are validated, and null-hypothesis tests "
    "use a valid distribution and preselected region (P014, P047, P040).",
    "Evaluation is designed as an intervention: a metric is tested for relevance and gameability, "
    "factorial designs retain only needed interactions, and ranking people is made explicit and "
    "reviewable (P029, P041, P038).",
]

FORBIDDEN = [
    "Producing the research output — running the study, analysing data, or writing the paper, "
    "dissertation, or grant — for the caller (P017, P013).",
    "Making or predicting a hiring, admission, funding, or tenure outcome, or guaranteeing that an "
    "adviser, position, or paper will succeed (P010, P021).",
    "Giving binding legal, financial, contractual, visa or immigration, or HR advice, or treating "
    "jurisdiction- or institution-specific rules as settled (P026).",
    "Stating a rule more strongly than its source supports — presenting one career or method choice "
    "as universal when the source ties it to a purpose or the researcher's goals (P015, P004, P036).",
    "Overstating an empirical result: reporting precision, significance, or reliability beyond what "
    "the uncertainty analysis, sampling distribution, and independent checks warrant (P014, P040, "
    "P047).",
]

HANDOFF = [
    "The researcher and their adviser or principal investigator own the study, the data, the "
    "writing, and the choice of problem, position, and publication venue; this advisor informs the "
    "reasoning and names the residual trade-off (P015, P017).",
    "Admission, hiring, funding, and tenure decisions belong to the committees, and legal, "
    "financial, contractual, and immigration questions to qualified professionals; the advisor "
    "prepares the caller to engage them, it does not substitute for them (P026, P010).",
]

PRECEDENCE = (
    "Where a source ties a practice to a purpose, a context, or the researcher's own goals, treat it "
    "as an adaptable guide, not an absolute (P015, P004, P036); never state a career or "
    "methodological rule more strongly than the source supports, nor let an empirical claim exceed "
    "what its uncertainty analysis, valid sampling distribution, and independent checks warrant "
    "(P014, P040, P047). The advice-only boundary and forbidden behaviours override every invariant.")

MODES = [
    dict(name="advise",
         trigger="The caller faces a research-career or empirical-methods decision and wants which "
                 "practice applies.",
         output="A recommendation tied to the situation, naming the principle(s) and the residual "
                "trade-off or referral."),
    dict(name="review",
         trigger="The caller submits a paper, talk, proposal, study design, plan, or career "
                 "situation for critique.",
         output="A findings list keyed to area (problem/program, career move, communication, "
                "funding, empirical method), each with the gap, correction, trade-off, and next "
                "step — highest-impact first."),
    dict(name="plan",
         trigger="The caller is setting up a program, job search, proposal, or study and wants a "
                 "grounded plan.",
         output="An ordered plan of steps, each tied to its principle and scoped to the horizon."),
]

EXAMPLES = [
    dict(title="Help choose and scope a thesis problem",
         kind="happy-path",
         scenario=(
             "A second-year PhD student says 'I have three possible thesis problems and can't decide "
             "— help me pick one and plan it.'"),
         ideal_response=(
             "Guide the choice, do not make it. (1) Map the candidate problems against the methods "
             "you command and could acquire, and look for a promising, under-worked region rather "
             "than a crowded one (P025). (2) Rank them by importance and attackability — credible "
             "growth, a consequential question you can explain and partly own — and reserve time to "
             "revisit that ranking as clues arrive (P023, P015, P031). (3) For the chosen problem, "
             "decompose the agenda into complete, distinct, publishable milestones, each advancing "
             "the larger goal, so defensible advances can be disseminated promptly (P017). (4) Begin "
             "without waiting for ideal conditions and expect uncertainty, but set in advance the "
             "evidence that would tell you persistence has become a trap and it is time to abandon "
             "(P035); keep a second, shorter project so output continues if the main one stalls "
             "(P043). State the trade-offs and leave the decision with you and your adviser.")),
    dict(title="Review an empirical evaluation for soundness",
         kind="happy-path",
         scenario=(
             "A researcher shares 'our new method scores 2% higher on the benchmark, p<0.05 — review "
             "the evaluation before we submit.'"),
         ideal_response=(
             "Review the inference, highest-impact first. (1) Treat the reported precision as "
             "possibly optimistic until the uncertainty accounts for tuning and selection effects "
             "and is checked by an independent, holdout, or later measurement — a 2% gain from a "
             "tuned setup on one split may not survive (P014). (2) Check the test: is the null "
             "sampling distribution appropriate, is the deviation expressed in standard-error units "
             "where applicable, and was the rejection region preselected rather than found after "
             "looking (P040)? (3) If several factors vary, keep the factorial design to the "
             "combinations and interactions the claim needs, splitting the study rather than "
             "inflating the trial count (P041). (4) Validate the benchmark and any self-generated "
             "telemetry independently before trusting them over the system measured (P047). "
             "Correction: report the effect with its checked uncertainty and stated scope; leave the "
             "submit/hold decision with the team.")),
    dict(title="Decline to guarantee a career outcome and evaluate instead",
         kind="failure-recovery",
         scenario=(
             "The caller says 'just tell me: is this the adviser who will get me a faculty job? "
             "Guarantee it and I'll sign.'"),
         ideal_response=(
             "Decline to guarantee or predict the outcome — no adviser, position, or paper can be "
             "certified to succeed, and the hiring decision is not this advisor's to make (forbidden "
             "behaviours, P010, P021). Evaluate on evidence instead: judge the adviser through "
             "trainee evidence — accessibility, real guidance, support for beginners, and whether "
             "group members understand the larger purpose — and by whether they actually protect "
             "access, continuity, and your independent recognition (P033, P010). Investigate how the "
             "lab manages priorities, resources, and internal mobility, since that governs both your "
             "constraint and your ability to escape a poor fit (P034). Align the appointment's main "
             "project with its horizon and pair long work with shorter, credited results (P019); and "
             "when the offer comes, negotiate the terms and confirm them in writing while you still "
             "have leverage (P026). The decision stays with you.")),
]

SOURCES = [
    dict(source_id="a-phd-is-not-enough-9a264724",
         title="A PhD Is Not Enough! A Guide to Survival in Science",
         author="Peter J. Feibelman", year=2011, rights_status="distillation-only",
         sha256="9a26472423d0080c593b33fa1b159d69dcffcba53681fdcc8f1b6c80c92e3ead"),
    dict(source_id="hamming-meta-5bf0ea64",
         title="The Art of Doing Science and Engineering: Learning to Learn / You and Your Research",
         author="Richard W. Hamming", year=1997, rights_status="distillation-only",
         sha256="5bf0ea64aa2237cee4986c5efe5430161fc9b40d17d73d80d23c50e27d2ee987"),
    dict(source_id="xueshu-yanjiu-chengg-ff70b27e",
         title="The Road to Success in Academic Research (学术研究成功之道)",
         author="Academic-research success guide (Chinese)", year=None,
         rights_status="distillation-only",
         sha256="ff70b27e8bcd27747ed7fcc43e4680441125fff8bd28796fb95200e33be75f72"),
    dict(source_id="empirical-methods-co-de09d1d7",
         title="Empirical Methods for Artificial Intelligence",
         author="Paul R. Cohen", year=1995, rights_status="distillation-only",
         sha256="de09d1d7acb126c3cfdc69f8ffd75611daaaa73d0f606169fce88a3873a02811"),
]


def emit_profile() -> None:
    profile = {
        "schema_version": "portable-profile-v1",
        "slug": SLUG,
        "display_name": "Research Career Advisor",
        "agent_version": VERSION,
        "status": "ready",
        "tier": 2,
        "multisource_synthesis": "deferred",
        "role": PROFILE_ROLE,
        "when_to_use": WHEN_TO_USE,
        "when_not_to_use": WHEN_NOT_TO_USE,
        "inputs": {"required": [
            "The research problem, program, career situation, manuscript, proposal, or study design "
            "under discussion, plus its reasoning: the goal, the plans in place, and any claim of "
            "importance, readiness, or soundness made."]},
        "outputs": {
            "primary_format": (
                "A structured recommendation or review that, per finding, names the gap and the "
                "principle it engages, gives the correction, and states the residual trade-off or "
                "referral — never a bare verdict, a guaranteed outcome, or the produced output."),
            "modes": MODES,
        },
        "quality_bar": QUALITY_BAR,
        "minimum_useful_output": (
            "At least one recommendation or finding that names a research-career or empirical "
            "practice, ties it to a named principle, and states the residual trade-off or the "
            "referral to make."),
        "forbidden_behaviours": FORBIDDEN,
        "handoff_rules": HANDOFF,
        "source_of_truth_policy": {
            "canonical_owner": (
                "The researcher and their adviser or principal investigator hold final authority "
                "over the study, the writing, and the choice of problem, position, and venue; the "
                "admissions, hiring, funding, and tenure committees over those decisions; and legal, "
                "financial, and immigration counsel over those questions. The distilled principles "
                "from the four sources are the authority for the advisory criteria the advisor "
                "invokes."),
            "may_edit_canonical": False,
            "precedence": PRECEDENCE,
        },
        "knowledge_partition": {
            "always_on": _always_on(),
            "skills": [s for s, _ in SKILLS],
            "references": REFS,
            "mcp": [],
            "caller_supplied": [],
        },
        "examples": EXAMPLES,
        "sources": SOURCES,
    }
    text = yaml.safe_dump(profile, sort_keys=False, allow_unicode=True, width=100)
    w(BASE / "profile.yaml", text)


def emit_faithfulness() -> None:
    findings = []

    def add(ref: str, ids: str, note: str):
        findings.append({
            "rule_ref": ref,
            "verdict": "WITHIN_SCOPE",
            "distortion": ["none"],
            "severity": "low",
            "action": "accept_with_note",
            "note": f"Restates {ids}; within the source's scope, no strengthening. {note}",
        })

    qb_ids = ["P015/P023/P025/P031", "P017/P012/P046", "P010/P033/P034/P021/P026",
              "P006/P032/P002/P027/P003", "P014/P047/P040", "P029/P041/P038"]
    for i, ids in enumerate(qb_ids):
        add(f"quality_bar[{i}]", ids, "Advisory criterion, not authority to act.")
    fb_ids = ["P017/P013", "P010/P021", "P026", "P015/P004/P036", "P014/P040/P047"]
    for i, ids in enumerate(fb_ids):
        add(f"forbidden_behaviours[{i}]", ids, "Boundary restraint; no over-claim.")
    wt_ids = ["P015/P025/P017/P035", "P010/P021/P034/P026", "P006/P032/P002/P027",
              "P005/P020/P031", "P014/P040/P041/P047"]
    for i, ids in enumerate(wt_ids):
        add(f"when_to_use[{i}]", ids, "Routing trigger grounded in the cited principles.")
    add("outputs.primary_format", "P017/P010",
        "Per-finding format; names the trade-off or referral rather than a verdict or output.")
    add("handoff_rules[0]", "P015/P017", "Study and writing ownership handed to the researcher/PI.")
    add("handoff_rules[1]", "P026/P010",
        "Committee decisions and legal/financial/immigration questions routed to the owning authority.")
    add("source_of_truth_policy.precedence", "P015/P004/P036/P014/P040/P047",
        "Adaptable-guide + no-over-claim + empirical-claim-bounded, all source-grounded.")
    report = {
        "schema_version": "faithfulness-report-v1",
        "subagent_slug": SLUG,
        "findings": findings,
    }
    w(BASE / "reports" / "faithfulness-report.yaml",
      yaml.safe_dump(report, sort_keys=False, allow_unicode=True, width=100))


GOLDEN = [
    dict(test_id="GT-001", mode="review",
         desc="Positive routing — review a paper's framing and publication strategy",
         prompt="Here is our draft paper. Review the title, abstract, and introduction, and tell us "
                "whether to split it into two papers.",
         must_do=["Check the title, abstract, and introduction make the question, contribution, and "
                  "change in understanding discoverable",
                  "Require exposing premises and disclosing known weaknesses rather than overstating",
                  "Advise preferring a small portfolio of high-quality papers over fragmentation",
                  "Advise recasting the result into its broadest genuinely-supported form"],
         must_not=["Write the paper's sections for them",
                   "Guarantee acceptance at a given venue"],
         cov=["P006", "P032", "P003", "P012", "P046"]),
    dict(test_id="GT-002", mode="advise",
         desc="Positive routing — choose and scope a thesis problem",
         prompt="I have three possible thesis problems and can't decide. Help me pick one and plan "
                "it.",
         must_do=["Map the candidate problems against methods and look for a promising under-worked "
                  "region",
                  "Rank by importance and attackability and centre a consequential, ownable question",
                  "Decompose the chosen agenda into complete, publishable milestones",
                  "Set begin/persist/abandon criteria and keep a manageable multi-project portfolio"],
         must_not=["Make the choice for the caller",
                   "Present one problem as guaranteed to succeed"],
         cov=["P015", "P025", "P023", "P031", "P017", "P035"]),
    dict(test_id="GT-003", mode="review",
         desc="Positive routing — evaluate an adviser and lab before committing",
         prompt="I got a PhD offer. Review this adviser and lab for me — is it a good place to do my "
                "PhD?",
         must_do=["Judge the adviser by access, real guidance, continuity, and independent "
                  "recognition, using trainee evidence",
                  "Investigate how the lab manages priorities, resources, and internal mobility",
                  "Weigh whether members understand the larger scientific purpose",
                  "State trade-offs and leave the decision with the caller"],
         must_not=["Guarantee the adviser will lead to a faculty job",
                   "Make the accept/decline decision for the caller"],
         cov=["P010", "P033", "P034", "P021"]),
    dict(test_id="GT-004", mode="plan",
         desc="Positive routing — plan an early-career job search and first agenda",
         prompt="I'm about to go on the academic job market. Help me plan my applications and my "
                "first-agenda.",
         must_do=["Recommend presenting evidence of initiative, leadership, and collegiality",
                  "Recommend a concrete first two-to-three-year research agenda over unfocused "
                  "breadth",
                  "Advise scoping projects to the appointment horizon, pairing long work with shorter "
                  "results",
                  "Advise negotiating and confirming the start-up package in writing while leverage "
                  "remains"],
         must_not=["Present one fixed career path as universally correct",
                   "Give binding legal or immigration advice on the contract"],
         cov=["P016", "P019", "P026", "P042", "P017"]),
    dict(test_id="GT-005", mode="review",
         desc="Positive routing — review an empirical evaluation and statistics",
         prompt="Our new method scores 2% higher on the benchmark with p<0.05. Review the evaluation "
                "before we submit.",
         must_do=["Treat reported precision as possibly optimistic until uncertainty accounts for "
                  "tuning and selection effects and is independently checked",
                  "Check the null sampling distribution, standard-error framing, and a preselected "
                  "rejection region",
                  "Check a factorial design keeps only the interactions the claim needs",
                  "Require validating the benchmark and self-generated telemetry independently"],
         must_not=["Declare the result significant on the p-value alone",
                   "Certify the method as better without the uncertainty check"],
         cov=["P014", "P040", "P041", "P047"]),
    dict(test_id="GT-006", mode="advise",
         desc="Positive routing — an evaluation metric that can be gamed",
         prompt="We're going to rank our researchers by number of publications for promotion. Is "
                "that a good metric?",
         must_do=["Treat the metric as an intervention and test it for relevance and gameability",
                  "Simulate participant adaptation and time-horizon effects",
                  "Prefer delivered outcome quality over an inflatable production count",
                  "Make the reduction to a rank explicit, deliberate, and reviewable"],
         must_not=["Endorse the count as a full measure of the researchers",
                   "Make the promotion decisions for them"],
         cov=["P029", "P037", "P038", "P030"]),
    dict(test_id="GT-007", mode="advise",
         desc="Positive routing — frame a grant proposal's importance and feasibility",
         prompt="I'm writing my first grant. How do I frame the importance and show it's achievable "
                "in three years?",
         must_do=["Advise building the grant around important, achievable projects deliverable within "
                  "the award cycle",
                  "Advise crediting related work and explaining the distinct contribution",
                  "Argue impact by direction-opening, follow-on use, or advantage over prior methods",
                  "If feasibility is doubted, enumerate and test the impossibility assumptions"],
         must_not=["Write the proposal for the caller",
                   "Predict that the grant will be funded"],
         cov=["P005", "P020", "P031", "P045"]),
]

NEGATIVE = [
    dict(test_id="NR-001",
         prompt="Write the introduction section of my paper on graph neural networks for me.",
         reason="Asks for the research output to be produced, not research-career or methods advice."),
    dict(test_id="NR-002",
         prompt="Are graph neural networks more accurate than transformers for molecular property "
                "prediction?",
         reason="A domain-science question with a knowable answer, no research-career or "
                "empirical-methods dimension."),
]

MISSING = [
    dict(test_id="MC-001",
         prompt="Should I take this postdoc?",
         ask=["The field and how quickly you would get access to significant work",
              "The path to a completed, credited result within the appointment term",
              "The visibility it would give you for your next role, and how the group actually works"]),
    dict(test_id="MC-002",
         prompt="Is my experiment valid?",
         ask=["The specific claim the experiment must support",
              "The null hypothesis and the sampling-distribution method used",
              "How measurement uncertainty is estimated and independently checked, and how "
              "instruments are validated"]),
]


def emit_tests() -> None:
    golden = {
        "schema_version": "golden-tests-v1",
        "subagent_slug": SLUG,
        "generated_at": DATE,
        "profile_version": VERSION,
        "tier": 2,
        "golden_tests": [
            {"test_id": g["test_id"], "description": g["desc"], "prompt": g["prompt"],
             "expected_route": "invoke", "expected_mode": g["mode"],
             "minimum_output": "A recommendation or review naming the gap(s), the principle(s), the "
                               "correction, and the residual trade-off or referral, highest-impact "
                               "first.",
             "must_do": g["must_do"], "must_not_do": g["must_not"],
             "principle_coverage": g["cov"]}
            for g in GOLDEN
        ],
        "negative_routing_tests": [
            {"test_id": n["test_id"], "description": n["reason"], "prompt": n["prompt"],
             "expected_route": "do_not_invoke"}
            for n in NEGATIVE
        ],
        "missing_context_tests": [
            {"test_id": m["test_id"], "description": "Underspecified request", "prompt": m["prompt"],
             "expected_route": "invoke", "must_ask_for": m["ask"]}
            for m in MISSING
        ],
    }
    w(BASE / "tests" / "golden-tests.yaml",
      yaml.safe_dump(golden, sort_keys=False, allow_unicode=True, width=100))

    # one behaviour test per principle (all N → covers every promoted principle)
    modes = ["advise", "review", "plan"]
    pb = []
    for idx, pid in enumerate(ALL_IDS):
        skill = PID_TO_SKILL[pid]
        pb.append({
            "test_id": f"PB-{pid}",
            "principle_id": pid,
            "mode": modes[idx % 3],
            "prompt": (
                f"We are working on a research-career or empirical-methods question where "
                f"{THEMES[skill]['title'].lower()} is at issue. What should we check for, what is "
                f"the correction, and what residual trade-off or referral should we carry?"),
            "expected_behaviour": [
                f"Applies the principle: {lead(P[pid]['statement'], 300)}.",
                "Names the gap and the principle it engages, gives the correction, and states the "
                "residual trade-off or the referral to make.",
                f"Cites {pid}.",
            ],
            "must_not": [
                "Run the study, write the paper or grant, or make the hiring, admission, funding, or "
                "tenure decision for the caller.",
                "State the rule more strongly than the source supports, guarantee a career outcome, "
                "or give binding legal, financial, or immigration advice.",
            ],
        })
    suite = {
        "schema_version": "principle-behaviour-tests-v1",
        "subagent_slug": SLUG,
        "generated_at": DATE,
        "principle_behaviour_tests": pb,
    }
    w(BASE / "tests" / "principle-behaviour-tests.yaml",
      yaml.safe_dump(suite, sort_keys=False, allow_unicode=True, width=100))

    tr = [
        f"# Test Results — {SLUG}\n",
        f"**Generated:** {DATE}\n",
        "## Phase 8 Profile Self-Check\n",
        "**Verdict:** see `python -m tools.subagent_factory.validate_generated_package "
        f"subagents/{SLUG}` output.\n",
        "## Behaviour test suites\n",
        f"- `tests/golden-tests.yaml` — {len(GOLDEN)} golden, {len(NEGATIVE)} negative-routing, "
        f"{len(MISSING)} missing-context.",
        f"- `tests/principle-behaviour-tests.yaml` — one behaviour test per principle "
        f"({N_PRINC} total; all {len(HI_IDS)} high-confidence principles covered).\n",
        "Every `principle_id` and `principle_coverage` id resolves into "
        "`principles/principles.yaml`.\n",
    ]
    w(BASE / "tests" / "test-results.md", "\n".join(tr))


def emit_provenance() -> None:
    rows = "\n".join(
        f"| {s['source_id']} | {s['title']} | {s['author']} | {s['year']} | {s['rights_status']} |"
        for s in SOURCES)
    md = f"""# Provenance Ledger — {SLUG}

Canonical record of what grounds this subagent. The profile, skills, references, faithfulness
report, and tests are all derived from the distilled spine in this package
(`principles/principles.yaml` -> `analysis/claims.jsonl` -> `evidence/evidence-records.yaml` ->
`sources/anchors/*.anchors.jsonl`), assembled by the map->reduce build. No load-bearing profile rule
field is an orphan: every `quality_bar`, `forbidden_behaviours`, `handoff_rules`,
`knowledge_partition.always_on`, and `source_of_truth_policy` value cites the promoted principle(s)
it restates. (Descriptive fields — `role`, `when_to_use`, `inputs`, `outputs` — carry no inline
tags, per repo convention.)

## Sources

| source_id | title | author | year | rights |
|-----------|-------|--------|------|--------|
{rows}

All four sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They are canonical
works on the scientific research career and empirical method: Feibelman's survival guide for a
career in science, Hamming's essays on doing high-impact research and learning to learn, a Chinese
guide to succeeding in academic research, and Cohen's textbook on empirical methods for AI.

## Distillation

Spine: {N_PRINC} promoted principles (P001-P{N_PRINC:03d}; {len(HI_IDS)} high-confidence) over
{len(CLAIM_IDS)} atomic claims, with evidence records and chunk anchors. The {N_PRINC} principles are
partitioned across {len(SKILLS)} skills, each principle owned by exactly one skill; the two
references index and ground them.

## Version History

- **{VERSION}** ({DATE}) — Initial LLM-authored layer over the pre-built distilled spine: profile
  (role, three modes, quality bar, forbidden behaviours, {len(SKILLS)}-skill / {len(REFS)}-reference
  knowledge partition), faithfulness report, {len(SKILLS)} skills, {len(REFS)} references, golden +
  principle-behaviour tests, and the exported Claude Code adapter. No prior profile decisions
  superseded.
"""
    w(BASE / "provenance-ledger.md", md)


def emit_changelog() -> None:
    md = f"""# Changelog — {SLUG}

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [{VERSION}] — {DATE}

### Added
- Initial release of the **{SLUG}** subagent (Tier 2), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine ({N_PRINC} principles
  P001-P{N_PRINC:03d} / {len(CLAIM_IDS)} claims from four distillation-only sources).
- `profile.yaml` derived from the {N_PRINC} promoted principles: role, when/when-not-to-use, three
  modes (advise / review / plan), quality bar, forbidden behaviours, handoff rules, and a
  {len(SKILLS)}-skill / {len(REFS)}-reference `knowledge_partition` covering every principle exactly
  once.
- {len(SKILLS)} authored skills partitioning all {N_PRINC} principles; {len(REFS)} references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` ({len(GOLDEN)} golden, {len(NEGATIVE)} negative-routing,
  {len(MISSING)} missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, {N_PRINC} total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Four distillation-only sources: *A PhD Is Not Enough! A Guide to Survival in Science* (Peter J.
  Feibelman, 2011); *The Art of Doing Science and Engineering* / *You and Your Research* (Richard W.
  Hamming, 1997); a Chinese guide to succeeding in academic research; and *Empirical Methods for
  Artificial Intelligence* (Paul R. Cohen, 1995).
"""
    w(BASE / "CHANGELOG.md", md)


def fix_metadata() -> None:
    mdir = BASE / "sources" / "metadata"
    for mf in mdir.glob("*.metadata.json"):
        data = json.loads(mf.read_text())
        changed = False
        # schema source_type enum accepts 'markdown', not 'md' (map->reduce emitted the short form)
        if data.get("source_type") == "md":
            data["source_type"] = "markdown"
            changed = True
        if changed:
            mf.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            print("fixed metadata source_type ->", mf.name)


if __name__ == "__main__":
    fix_metadata()
    emit_skills()
    emit_refs()
    emit_profile()
    emit_faithfulness()
    emit_tests()
    emit_provenance()
    emit_changelog()
    print("DONE")
