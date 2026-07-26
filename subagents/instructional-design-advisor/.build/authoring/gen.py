"""Deterministic authoring generator for instructional-design-advisor.

Reads the already-assembled, deterministically-valid distilled spine
(principles/principles.yaml + analysis/claims.jsonl + evidence + anchors) and emits the
LLM-authored layer: profile.yaml, references/*, skills/*, tests/*, reports/faithfulness-report.yaml,
provenance-ledger.md, CHANGELOG.md. Every emitted id resolves into the spine.

Run:  python3 .build/authoring/gen.py
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parents[2]  # subagents/instructional-design-advisor
SLUG = "instructional-design-advisor"
VERSION = "1.0.0"
DATE = "2026-07-26"

# ---------------------------------------------------------------------------- spine load
PRINCIPLES = yaml.safe_load((BASE / "principles" / "principles.yaml").read_text())["principles"]
P = {p["principle_id"]: p for p in PRINCIPLES}
ALL_IDS = [p["principle_id"] for p in PRINCIPLES]
HI_IDS = [p["principle_id"] for p in PRINCIPLES if p.get("confidence") == "high"]
N_PRINC = len(ALL_IDS)
CLAIM_IDS = set()
CLAIM_STMT: dict[str, str] = {}
for line in (BASE / "analysis" / "claims.jsonl").read_text().splitlines():
    line = line.strip()
    if line:
        _c = json.loads(line)
        CLAIM_IDS.add(_c["claim_id"])
        CLAIM_STMT[str(_c["claim_id"])] = str(_c.get("statement", ""))

# sha256 per source_id from the manifest (avoid hand-transcription)
_MANIFEST = yaml.safe_load((BASE / "source-pack.manifest.yaml").read_text())
SHA = {s["source_id"]: s["sha256"] for s in _MANIFEST["sources"]}


def pids(n: int) -> str:
    return f"P{n:03d}"


# ---------------------------------------------------------------------------- partition
# Each entry: (skill-slug (kebab, <=48 chars), [principle numbers]).
# Every principle 1..N appears exactly once.
SKILLS: list[tuple[str, list[int]]] = [
    ("backward-design-and-constructive-alignment",
     [6, 10, 13, 19, 41, 47, 74, 86, 95, 96, 107, 116, 153, 160]),
    ("learning-outcomes-and-taxonomy",
     [11, 38, 59, 60, 67, 89, 100, 105, 123, 124, 142, 151, 154, 163, 165, 169]),
    ("assessment-design-and-authentic-tasks",
     [14, 15, 16, 18, 26, 32, 35, 36, 39, 65, 69, 71, 75, 82, 83, 94, 97, 99, 109, 110, 111, 114,
      136, 145, 148]),
    ("feedback-and-formative-practice", [17, 24, 27, 40, 98, 112, 146]),
    ("teaching-for-understanding-and-transfer",
     [3, 28, 33, 42, 61, 104, 113, 126, 135, 152, 155, 162, 176, 177, 178, 179]),
    ("multimedia-and-elearning-design",
     [1, 4, 5, 9, 20, 25, 43, 78, 134, 137, 138, 139, 140, 141]),
    ("instructional-strategy-and-events",
     [8, 29, 30, 37, 46, 57, 72, 101, 102, 103, 106, 119, 125, 129, 132, 144, 149, 158, 161, 166,
      167, 170, 171, 172]),
    ("motivation-and-learner-engagement", [12, 21, 63, 85, 115, 150]),
    ("needs-and-context-analysis", [2, 22, 48, 52, 54, 58, 62, 80, 127, 130, 168, 173]),
    ("iterative-prototyping-and-development", [23, 50, 56, 70, 73, 133, 175]),
    ("evaluation-transfer-and-impact",
     [45, 49, 51, 53, 55, 66, 77, 79, 81, 84, 88, 90, 93, 122, 128, 131, 159, 174]),
    ("active-learning-and-group-formats",
     [34, 44, 68, 87, 92, 108, 117, 118, 120, 147, 156, 157, 164]),
    ("teaching-scholarship-and-quality", [7, 31, 64, 76, 91, 121, 143, 180]),
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
    "instructional-design-principles-index",
    "instructional-design-evidence-notes",
]
for r in REFS:
    assert len(r) <= 48, f"ref name too long ({len(r)}): {r}"

PID_TO_SKILL = {pids(n): slug for slug, nums in SKILLS for n in nums}

# ---------------------------------------------------------------------------- per-skill themes
THEMES: dict[str, dict] = {
    "backward-design-and-constructive-alignment": dict(
        title="Backward Design And Constructive Alignment",
        purpose=(
            "This skill governs the order and the alignment of a design: desired results first, then "
            "the evidence that would show they were achieved, then the teaching and learning that "
            "gets learners there. It keeps the unit as the working design focus while course, "
            "programme, and graduate purposes are designed backward from outcomes; keeps outcomes "
            "few, integrated, and stated as what a learner will newly do and how well; prioritises "
            "threshold and core content deliberately against stakeholder accretion; makes sure "
            "learners know what the learning eventually requires them to do; and treats design as "
            "iterative, with earlier units rethought in light of later ones and every assessment "
            "criterion traceable to a course outcome and a programme specification."),
        when=[
            "A course, unit, lesson, or programme is being designed or redesigned and the order of "
            "design decisions is at issue.",
            "Outcomes must be written, pruned, or derived from graduate and professional purposes "
            "rather than from topics and available content.",
            "An existing design must be audited for alignment between stated outcomes, taught "
            "activity, and assessed performance.",
            "Content is accreting from stakeholders and important outcomes must be protected by "
            "explicit prioritisation.",
        ],
        input="The course, unit, or programme under design; its stated outcomes, assessments, and "
              "activities; and the graduate or professional purposes it serves."),
    "learning-outcomes-and-taxonomy": dict(
        title="Learning Outcomes And Taxonomy",
        purpose=(
            "This skill classifies and levels what learners are meant to achieve. It resolves broad "
            "objective language into the specific knowledge subtype and cognitive process the "
            "performance actually requires, begins objective-writing from the type of learning "
            "outcome intended, distinguishes routine execution from adaptive implementation, and "
            "separates conceptual understanding, analysis, evaluation, and creation as either "
            "transfer targets or means to simpler learning. It uses taxonomy as an adaptable "
            "analytic heuristic rather than a literal reality or a teaching prescription, classifies "
            "a task for a stated learner group and prior-experience state, samples objectives "
            "representatively at intermediate planning levels, and resolves conflicting signals by "
            "comparing intended wording, enacted activity, and scoring criteria."),
        when=[
            "An objective, outcome statement, or standard is too broad to design or assess against.",
            "A design must decide the cognitive level it is actually targeting, or whether a claimed "
            "higher-order verb survives contact with the enacted task.",
            "A taxonomy classification is disputed, or is being applied as a rule rather than a "
            "heuristic.",
            "Attitude, verbal-information, or transfer-level outcomes must be stated in a form that "
            "can be taught and observed.",
        ],
        input="The objectives or outcome statements under discussion, the tasks and scoring criteria "
              "that enact them, and the learner group and its prior experience."),
    "assessment-design-and-authentic-tasks": dict(
        title="Assessment Design And Authentic Tasks",
        purpose=(
            "This skill designs and reviews the evidence side of a course: authentic tasks that "
            "require judgment on unstructured problems in a realistic context, explicit public "
            "criteria applied before judgment, validity and reliability questions asked plainly, and "
            "forward-looking tasks that put learners where the knowledge is actually used rather "
            "than asking whether topics were covered. It separates formative from summative purpose, "
            "separates task grades from outcome achievement, prefers criterion-referenced standards "
            "over norm-referenced curves, builds assessment as an accumulating scrapbook of varied "
            "evidence rather than one snapshot, and designs examinations, portfolios, rubrics, "
            "reassessment, and the whole assessment programme as one proportionate evidence system."),
        when=[
            "An assessment task, rubric, examination, portfolio, or whole assessment programme is "
            "being designed or reviewed.",
            "Grades, standards, or pass marks must be set, calibrated, or defended.",
            "A design must show it is assessing understanding rather than recall, coverage, or "
            "test-taking skill.",
            "External or high-stakes assessment constrains the design and must be reconciled with "
            "local outcomes.",
        ],
        input="The assessment tasks, criteria, rubrics, and grading scheme under discussion, together "
              "with the outcomes they are meant to provide evidence for."),
    "feedback-and-formative-practice": dict(
        title="Feedback And Formative Practice",
        purpose=(
            "This skill builds the loop between performance and improvement: cheap recurring checks "
            "that reveal what learners took from a session, cycles of performance, feedback, "
            "revision, and new performance, immediate self-checkable feedback inside practice, "
            "response formats that do not force learners to answer against the person beside them, "
            "and shared quality criteria used consistently across instructor, peer, and self-review. "
            "It keeps formative feedback timely, two-way, and gap-closing — exposing both current "
            "performance and the intended standard while learners can still act on it — and treats a "
            "plan that cannot absorb feedback as a defect rather than a virtue."),
        when=[
            "Learners get results too late, too vaguely, or with no opportunity to revise and "
            "perform again.",
            "A design needs low-cost formative checks that show what learners actually understood.",
            "Peer, self, and instructor review need shared criteria and a workable division of "
            "labour.",
            "Practice needs feedback built into it rather than deferred to the graded event.",
        ],
        input="The feedback and practice arrangements in place, when learners receive them, and what "
              "learners are able to do with them before the graded performance."),
    "teaching-for-understanding-and-transfer": dict(
        title="Teaching For Understanding And Transfer",
        purpose=(
            "This skill targets durable understanding rather than covered content. It organises "
            "teaching around big ideas and essential questions, surfaces predictable misconceptions "
            "before teaching, tests understanding by appropriate application to newly posed "
            "questions, and refuses to count a task as transfer when it varies only quantities or "
            "symbols. It teaches metacognition and self-regulation explicitly as strategy knowledge "
            "plus monitoring and repair, builds understanding by connecting new learning to prior "
            "frameworks and revisiting ideas, preserves warranted uncertainty in evidence-based "
            "judgment, and names the teacher's blind spot — that teaching implies learning, and that "
            "a few visible successes and no questions do not mean the class understood."),
        when=[
            "A design covers content but cannot show that learners understand or can transfer it.",
            "Transfer, application, or 'real-world' claims need testing against what the tasks "
            "actually require.",
            "Misconceptions, shallow strategy use, or unmonitored learning are suspected.",
            "Big ideas, essential questions, or the connective structure of a unit need "
            "establishing.",
        ],
        input="The unit or course content, the tasks that stand as evidence of understanding, and "
              "what is known about learners' prior conceptions and strategies."),
    "multimedia-and-elearning-design": dict(
        title="Multimedia And E-Learning Design",
        purpose=(
            "This skill applies the evidence on how people learn from words and pictures. It prefers "
            "spoken narration to concurrent on-screen prose when animation and words must be "
            "processed together, refuses to duplicate narration with on-screen sentences merely to "
            "add a delivery mode, strips irrelevant words, decorative images, and background sound, "
            "places printed words next to the graphic part they describe, and eliminates split "
            "attention wherever the interface creates it. It signals what should drive selective "
            "perception, supplies or activates an organising structure, pretrains component names "
            "and behaviour for novices, sets practice quantity from criticality and learner time "
            "cost, treats high behavioural engagement as no evidence of learning, declines to design "
            "around learning styles, chooses pedagogy before technology, and states boundary "
            "conditions whenever it invokes one of these principles."),
        when=[
            "E-learning, slides, animation, video, or any words-plus-graphics material is being "
            "designed or reviewed.",
            "A medium or technology is being chosen, or is being adopted ahead of the pedagogy.",
            "A design appeals to learning styles, engagement, or added delivery modes as "
            "justification.",
            "Learners must split attention between text, graphic, question, and feedback.",
        ],
        input="The instructional material or interface under review, its learners' expertise, and the "
              "medium, pacing, and control the design assumes."),
    "instructional-strategy-and-events": dict(
        title="Instructional Strategy And Events",
        purpose=(
            "This skill selects and sequences what actually happens in instruction, derived from the "
            "goal, the analyses, the objectives, and the assessments rather than from habit. It "
            "covers motivation, presentation, examples, active practice, feedback, assessment, and "
            "transfer; sequences by prerequisite and manageable progression with entry checks and "
            "pretests; chooses the strategy by the information-processing stage it serves; and "
            "matches technique to outcome type — concepts through varied instances and negative "
            "instances, intellectual skills through activated prerequisites and progressive transfer "
            "cases, verbal information through organised prior-knowledge links, attitudes through "
            "modelled choices and consequences, motor skills through demonstration and physical "
            "practice. It scaffolds generative and complex performance from supported to independent "
            "work, uses spaced retrieval rather than re-presentation, makes training conditions "
            "resemble retrieval conditions, and budgets time across the whole sequence."),
        when=[
            "The activities, examples, practice, and sequence of a unit or course must be chosen or "
            "reviewed.",
            "Different outcome types — concepts, intellectual skills, verbal information, attitudes, "
            "motor skills — need matching techniques.",
            "Learners must be scaffolded from supported work to independent production, or "
            "prerequisites are unmet.",
            "Practice, repetition, and time budgets need setting against criticality and transfer "
            "conditions.",
        ],
        input="The objectives and assessments already fixed, the learners' entry performance, and the "
              "activities, examples, and practice currently planned."),
    "motivation-and-learner-engagement": dict(
        title="Motivation And Learner Engagement",
        purpose=(
            "This skill treats motivation as a design variable rather than a learner trait. It "
            "organises motivational design under attention, relevance, confidence, and satisfaction; "
            "connects the intended learning to goals learners value and makes success credible "
            "instead of manufacturing urgency through threatening assessment; sets challenge from "
            "accurate information about what these learners can and cannot do and adjusts it as "
            "progress shows; combines autonomy and trust with clear goals, organised support, and "
            "fair safeguards while avoiding intimidation, arbitrary control, and cynical busy-work; "
            "and reads deep and surface approaches as task-and-context dependent, treating the "
            "familiar cluster of disengagement symptoms as evidence about the design rather than "
            "about the students."),
        when=[
            "Attendance, preparation, discussion energy, or out-of-class study are falling and the "
            "cause is being attributed to learners.",
            "A design relies on assessment pressure, compliance, or busy-work to produce effort.",
            "Challenge level, autonomy, or support need calibrating to what these learners can "
            "currently do.",
            "Learners are taking a surface approach to work that requires a deep one.",
        ],
        input="The observed learner behaviour, the task and assessment conditions producing it, and "
              "the goals and support currently offered."),
    "needs-and-context-analysis": dict(
        title="Needs And Context Analysis",
        purpose=(
            "This skill runs the front end: it begins performance improvement without presuming "
            "instruction, observes the actual setting, consults frontline practitioners, and uses "
            "proportionate analysis to separate capability gaps from environmental, incentive, and "
            "systems causes. It derives training needs from documented discrepancies rather than "
            "felt needs alone, traces a voiced problem to an organisational outcome and quantifies "
            "the gap, operationalises vague goals into observable success behaviours confirmed by "
            "several knowledgeable contributors, triangulates unclear goal steps through "
            "performance, expert practitioners, and workplace evidence, describes learners and "
            "context from actual conditions, splits goals whose subperformances differ in structure, "
            "and has a qualified content expert review goals and skill frameworks against explicit "
            "structured criteria."),
        when=[
            "A training request arrives before anyone has established that instruction is the right "
            "intervention.",
            "A goal is stated too vaguely to design or assess against, or its steps are unclear.",
            "Learner characteristics, prior performance, technology, and workplace conditions must "
            "be established from actual evidence.",
            "A goal analysis or subordinate-skill breakdown needs expert review for accuracy, "
            "completeness, and job alignment.",
        ],
        input="The stated problem or training request, the organisational outcome behind it, and "
              "whatever is known about performers, setting, and prior performance systems."),
    "iterative-prototyping-and-development": dict(
        title="Iterative Prototyping And Development",
        purpose=(
            "This skill manages the build as successive approximation rather than a single "
            "specification handoff. It sets goals through early design-prototype-evaluation cycles "
            "and stabilises behavioural objectives before detailed development; uses experiential "
            "prototypes instead of specification-only approval to align stakeholders and test "
            "timing, transitions, media, interaction, and integration; involves recent and "
            "representative learners while fundamental change is still affordable; maps objectives "
            "to treatments and reuses treatments where context and criteria permit; and moves "
            "through progressive release gates — design proof, alpha, beta — converging as evidence "
            "stabilises, resisting perfectionism and unplanned refinement, releasing something fit "
            "for responsible use with correction capacity, and reopening approved design only for "
            "unacceptable defects. It treats the whole instructional system as interdependent and "
            "revised from outcome feedback."),
        when=[
            "A development effort must move from analysis and objectives into building materials.",
            "Stakeholders are approving specifications they cannot yet experience, or scope is "
            "expanding through unplanned refinement.",
            "Prototypes need learner exposure while change is still affordable.",
            "Release readiness must be judged and the design frozen or reopened.",
        ],
        input="The current state of the build, the objectives and treatments planned, the "
              "stakeholders and learners available for review, and the release constraints."),
    "evaluation-transfer-and-impact": dict(
        title="Evaluation, Transfer And Impact",
        purpose=(
            "This skill plans and reads evaluation across its stages. It distinguishes learner "
            "assessment from instructional evaluation, uses one-to-one, small-group, and field "
            "formative evidence on a usable draft and traces each learner difficulty back to the "
            "implicated design component, analyses learner-by-item-by-objective performance across "
            "pretest, practice, and posttest, and gates expensive downstream evaluation behind "
            "congruence, content, design, and transfer analyses. For impact it establishes with "
            "valid posttest evidence that learners could perform before reading absent workplace "
            "behaviour as transfer failure, measures use by degree, frequency, context, and prior "
            "use, diagnoses nonuse across relevance, permission, support, resources, and incentives, "
            "triangulates across learners and workplace observers, uses an independent evaluator "
            "where stakeholder interest threatens the judgment, and reports purpose, questions, "
            "design, findings, and limits with an executive summary."),
        when=[
            "A draft design must be formatively evaluated and revised from evidence.",
            "Learners completed training but the expected workplace behaviour is not appearing.",
            "An impact, transfer, or return study must be scoped, instrumented, and reported.",
            "Two interventions are being compared, or a summative judgment must be made about "
            "whether the originating problem was resolved.",
        ],
        input="The evaluation question, the stage the instruction has reached, the evidence and "
              "instruments available, and who owns the decision the evaluation informs."),
    "active-learning-and-group-formats": dict(
        title="Active Learning And Group Formats",
        purpose=(
            "This skill designs what learners do together and in what setting. It treats lectures, "
            "seminars, and online formats as settings rather than teaching methods and selects "
            "different learner activities for different outcomes; moves initial content acquisition "
            "out of contact time so the second task of learning to use the content gets the room it "
            "needs; structures group learning so members hold relevant resources, responsibility, "
            "psychological room to test interpretations, and a cognitively demanding agenda tied to "
            "assessed outcomes; launches authentic projects through credible examples, learner "
            "participation, stakeholder critique, and full support ecosystems; aligns problem-based "
            "learning end to end from outcomes through facilitation to assessment; designs "
            "peer-teaching around explicit outcomes, selection, training, and continuous support; "
            "and makes large classes work through stable peer support, rapid formative evidence, and "
            "visible reasoning."),
        when=[
            "Group work, project work, problem-based learning, practica, or peer teaching is being "
            "designed or is failing.",
            "Contact time is consumed by content delivery that could happen elsewhere.",
            "A large class must still elicit and observe learner reasoning.",
            "A format is being chosen as if it were a teaching method rather than a setting.",
        ],
        input="The format and group arrangements in place, the outcomes they are meant to serve, and "
              "the support, assessment, and class size that surround them."),
    "teaching-scholarship-and-quality": dict(
        title="Teaching Scholarship And Quality",
        purpose=(
            "This skill treats teaching improvement as disciplined inquiry and instructional design "
            "as professional work requiring knowledge and practice. It makes the teaching theory "
            "shaping an environment explicit, then uses evidence and a coherent framework to "
            "diagnose problems and adapt to local learners and constraints; runs repeated, "
            "systematic action-research cycles that frame an observable learning problem, plan a "
            "change from theory and student evidence, apply it, evaluate, and revise, triangulating "
            "across students and trusted colleagues; analyses teaching cases as provisional evidence "
            "by classifying intention, enactment, and assessment separately before evaluating; "
            "grounds any claim that instruction is adequate in what students actually learn rather "
            "than in demand, enrolment, or satisfaction; makes leadership an enabling system for "
            "department-wide alignment; and expects the right proportion of approaches to be one the "
            "teacher is not in the habit of using."),
        when=[
            "A teaching problem must be investigated systematically rather than adjusted by "
            "intuition.",
            "Quality, adequacy, or improvement claims rest on enrolment, demand, or satisfaction "
            "data.",
            "Department- or programme-level alignment needs leadership, resourcing, and staff "
            "engagement.",
            "A teacher's or designer's default approach needs examining against what the learning "
            "requires.",
        ],
        input="The teaching problem or quality claim under discussion, the evidence gathered so far, "
              "and the institutional constraints and leadership context around it."),
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
    # Don't let a hard truncation end on a dangling function word ("...from the").
    _DANGLE = {"the", "a", "an", "of", "to", "from", "and", "or", "with", "for", "in",
               "on", "by", "as", "that", "into", "than", "so", "its", "their"}
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


_US = "\x1f"  # unit separator: id <-> statement
_RS = "\x1e"  # record separator: between cited items


def digest(nums: list[int], claims: list[str]) -> str:
    """sha256 over cited principle + claim statements, matching detect_stale._digest so a re-run
    of this generator leaves the stale-maintenance gate green (no re-stamp needed)."""
    parts: list[str] = []
    for pid in sorted(pids(n) for n in nums):
        parts.append(f"P:{pid}{_US}{P[pid]['statement']}")
    for cid in sorted(str(c) for c in claims):
        parts.append(f"C:{cid}{_US}{CLAIM_STMT.get(cid, '')}")
    return hashlib.sha256(_RS.join(parts).encode("utf-8")).hexdigest()


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
    "grounded in the ten distillation-only sources (*Understanding by Design*; *Teaching for "
    "Quality Learning at University*; *Creating Significant Learning Experiences*; *A Taxonomy for "
    "Learning, Teaching, and Assessing*; *Principles of Instructional Design*; *First Principles of "
    "Instruction*; *The Systematic Design of Instruction*; *Leaving ADDIE for SAM*; *Multimedia "
    "Learning*; and *e-Learning and the Science of Instruction*)")


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
        body.append("- The reasoning offered for the design decision under review: the intended "
                    "learning, the learners and setting, the evidence already gathered, and any "
                    "claim of alignment, effectiveness, or readiness made.\n")
        body.append("## Output\n")
        body.append(
            "Per finding: name the gap and the principle it engages, give the correction, state the "
            "residual trade-off or the referral to make, and end with a concrete next step. Order "
            "findings highest-impact first. This skill advises on instructional design; it does not "
            "build the course, materials, or item bank for the caller, teach or grade learners, or "
            "certify a programme or its subject-matter content.\n")
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
    out.append("# Instructional-Design Principles Index\n")
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
    out.append("# Instructional-Design Evidence Notes\n")
    out.append("How the principles in this package are grounded, and how to keep advice faithful to "
               "the sources.\n")
    out.append("## Sources\n")
    out.append("Ten distillation-only sources ground the package, spanning backward design and "
               "assessment for understanding (*Understanding by Design*), constructive alignment and "
               "university teaching (*Teaching for Quality Learning at University*), integrated "
               "course design (*Creating Significant Learning Experiences*), the revised taxonomy of "
               "knowledge and cognitive process (*A Taxonomy for Learning, Teaching, and "
               "Assessing*), systematic instructional design (*Principles of Instructional Design*, "
               "*The Systematic Design of Instruction*), demonstration-application-centred "
               "instruction (*First Principles of Instruction*), iterative successive-approximation "
               "development (*Leaving ADDIE for SAM*), and the cognitive science of learning from "
               "words and pictures (*Multimedia Learning*, *e-Learning and the Science of "
               "Instruction*). Paraphrase and restructure only — no verbatim quotation (see "
               "`.claude/rules/rights-and-quotation-policy.md`).\n")
    out.append("## Faithfulness discipline\n")
    out.append("- No advice may state a rule more strongly than its source supports: the multimedia "
               "and e-learning principles are guidance consistent with how the mind works, not "
               "unbending rules, and their boundary conditions must be stated whenever one is "
               "invoked (P141).")
    out.append("- Taxonomies and models are adaptable analytic heuristics, not literal reality, a "
               "source of educational aims, or a unique teaching prescription; a disputed "
               "classification is used to improve the design, not to win a labelling argument (P067, "
               "P163).")
    out.append("- Evidence about learning governs claims about quality: adequacy rests on what "
               "students actually learn and how much they grow, not on demand, enrolment, or "
               "satisfaction, and behavioural engagement is not evidence of learning (P007, P005).")
    out.append("- Constructive alignment is adapted to local context while its core relationship is "
               "preserved, and the design stays iterative — earlier decisions are rethought as later "
               "ones expose problems (P047, P041).")
    out.append("- The advisor guides the design; the teacher of record, the content expert, and the "
               "institution own the course, the subject matter, and the grades (P173, P121).\n")
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


ROUTER_DESCRIPTION = (
    "Advises on instructional and course design: backward design and constructive alignment, "
    "learning outcomes and taxonomy level, authentic assessment and rubrics, feedback and formative "
    "practice, teaching for understanding and transfer, instructional strategy for each outcome "
    "type, multimedia and e-learning materials, motivation, needs and context analysis, iterative "
    "prototyping, evaluation of transfer and impact, group and project formats, and teaching "
    "scholarship. Use when designing or reviewing a course, unit, lesson, programme, training "
    "intervention, assessment scheme, or instructional material. Not for: building the course or "
    "materials, teaching or grading learners, ruling on subject-matter correctness, or accreditation "
    "and certification decisions."
)

PROFILE_ROLE = (
    "An advisor on instructional and course design, grounded in ten distillation-only sources on "
    "backward design, constructive alignment, learning taxonomies, systematic instructional design, "
    "iterative development, and multimedia learning. It helps designers and teachers analyse needs, "
    "set and level outcomes, design assessment and instructional strategy, prototype materials, and "
    "evaluate transfer and impact. The invariants below are advisory criteria, not authority to "
    "act: this advice-only boundary and the forbidden behaviours override every invariant, so the "
    "advisor never builds the course, teaches it, grades learners, or certifies a programme.")

WHEN_TO_USE = [
    "A course, unit, lesson, or training programme is being designed or redesigned and its outcomes, "
    "assessment, and activities must align.",
    "An existing design needs review for alignment, taxonomy level, assessment validity, or "
    "coverage-driven drift.",
    "A performance problem or training request must be analysed before anyone assumes instruction is "
    "the answer.",
    "Instructional materials, e-learning, or multimedia need review against evidence-based design "
    "principles.",
    "Formative or summative evaluation must be planned — of a draft design, of learner achievement, "
    "or of workplace transfer and impact.",
]

WHEN_NOT_TO_USE = [
    "The caller wants the deliverable built for them — the course, materials, slide deck, or item "
    "bank produced end to end; this advisor guides the design, it does not author it.",
    "The caller wants a ruling on the subject-matter correctness of the content, which belongs to a "
    "qualified content expert.",
    "The caller wants learners graded, a programme accredited, or a design certified effective; "
    "those belong to the teacher of record, the institution, and the accrediting body.",
    "The task has no instructional-design dimension — software, operations, or project work with no "
    "learning goal.",
]

QUALITY_BAR = [
    "Designed backward: desired results, then the evidence of achievement, then the teaching — with "
    "every assessment criterion traceable to an outcome (P013, P006, P153, P095).",
    "Outcomes resolved to the knowledge subtype and cognitive process the performance actually "
    "requires, with taxonomy used as a heuristic (P060, P038, P067, P100).",
    "Assessment authentic, criterion-referenced, and accumulated as varied evidence rather than one "
    "snapshot (P014, P015, P039, P136, P016).",
    "Understanding shown by application to newly posed questions, not coverage or recall, with "
    "predictable misconceptions surfaced first (P179, P042, P178, P104).",
    "Materials follow the evidence on words and pictures — coherence, contiguity, modality, "
    "signalling, pretraining — with boundary conditions stated (P078, P139, P001, P020, P141).",
    "Instruction warranted by analysis, prototyped iteratively, and evaluated for learning and "
    "workplace transfer, not enrolment or satisfaction (P130, P133, P122, P007).",
]

FORBIDDEN = [
    "Building the deliverable for the caller — the course, materials, or item bank produced end to "
    "end; the advisor guides the design, it does not author it (P173, P031).",
    "Certifying a design effective, a programme accredited, or learners competent; those judgments "
    "need evaluation evidence and belong to the institution (P081, P093, P007).",
    "Stating a design principle more strongly than its source supports, or invoking one without its "
    "boundary conditions (P141, P067).",
    "Treating engagement, enrolment, satisfaction, or learning-style fit as evidence that learning "
    "occurred (P005, P007, P043).",
]

HANDOFF = [
    "The teacher of record, the design team, and the institution own the course, the grades, and the "
    "decision to run it; the advisor informs the design and names the residual trade-off (P121, "
    "P031).",
    "Subject-matter accuracy is referred to a qualified content expert against explicit review "
    "criteria, and impact judgments wait on evaluation evidence (P173, P081).",
]

PRECEDENCE = (
    "What learners are meant to be able to do governs the design — outcomes precede evidence, and "
    "evidence precedes teaching (P013, P153); no principle is stated more strongly than its source "
    "supports, and its boundary conditions are named whenever it is invoked (P141, P067); and the "
    "teacher of record and the institution own the course and the grades, which overrides every "
    "design invariant (P121).")

MODES = [
    dict(name="advise",
         trigger="The caller faces an instructional-design decision and wants the applicable "
                 "principle.",
         output="A recommendation naming the principle(s) applied and the residual trade-off or "
                "referral to carry."),
    dict(name="review",
         trigger="The caller submits a course, unit, assessment, material, or evaluation plan for "
                 "critique.",
         output="A findings list by area (alignment, outcomes, assessment, strategy, materials, "
                "evaluation), each with the gap, correction, trade-off, and next step — "
                "highest-impact first."),
    dict(name="plan",
         trigger="The caller is setting up a design or evaluation effort and wants a grounded "
                 "sequence of design decisions.",
         output="An ordered plan of design decisions (analysis, outcomes, evidence, strategy, "
                "development, evaluation), each tied to its principle."),
]

EXAMPLES = [
    dict(title="Review a unit built from topics with a quiz bolted on the end",
         kind="happy-path",
         scenario=(
             "A teacher shares a five-week unit plan: a list of chapters to cover, a set of "
             "activities the class enjoys, and a multiple-choice quiz at the end. The stated aim is "
             "'students will understand supply and demand.'"),
         ideal_response=(
             "Flag the gaps, highest-impact first. (1) The design starts from the means: work "
             "backward from desired results, to the evidence that would show them, to the teaching "
             "(P013), keeping the unit as the design focus (P006). (2) 'Understand' is unresolved: "
             "state the knowledge subtype and cognitive process the performance actually requires "
             "(P060), and write the goal as what students will newly be able to do and how well "
             "(P160). (3) A multiple-choice quiz cannot show understanding — a right answer can come "
             "from recall, test-taking skill, or a guess (P071); test understanding by application "
             "to newly posed questions (P179) in an authentic task (P014) with explicit criteria "
             "(P015). (4) Enjoyed activities are not evidence: state the intended result and success "
             "criteria and connect them repeatedly to the activity (P096). (5) Ask what "
             "misconceptions learners bring before teaching (P178). Correction: rewrite the unit "
             "outcome, choose the evidence, then rebuild activities. Residual trade-off: authentic "
             "tasks cost marking time, so plan the assessment programme's workload proportionately "
             "(P148). The design and the grades stay with the teacher.")),
    dict(title="Decline to build the course and to certify its effectiveness",
         kind="failure-recovery",
         scenario=(
             "The caller says 'Just build the whole onboarding course for us — slides, workbook, and "
             "final exam — and confirm it will cut our error rate by half.'"),
         ideal_response=(
             "Decline both requests: this advisor guides design rather than authoring the "
             "deliverable, and no design can be certified effective in advance — impact claims wait "
             "on evaluation evidence gathered after learners can perform in context (forbidden "
             "behaviours, P081, P093). Redirect: first establish that instruction is warranted at "
             "all, by observing the setting and separating capability gaps from environment, "
             "incentive, and systems causes (P130, P168) and quantifying the desired-versus-actual "
             "gap (P054). If a skill gap is verified, set outcomes and evidence before materials "
             "(P013), prototype experientially rather than approving specifications (P133), and plan "
             "formative evaluation on a usable draft with one-to-one, small-group, and field "
             "evidence (P122). Then scope an impact study that measures use by degree, frequency, "
             "and context and diagnoses nonuse across relevance, permission, support, resources, and "
             "incentives (P045). Offer to review the team's drafts against these criteria; the build "
             "and the claims stay with the team.")),
]

SOURCES = [
    dict(source_id="wiggins-mctighe-unde-b6dc4e0e",
         title="Understanding by Design (expanded 2nd ed.)",
         author="Grant Wiggins and Jay McTighe", year=2005),
    dict(source_id="biggs-tang-teaching-108b0793",
         title="Teaching for Quality Learning at University",
         author="John Biggs and Catherine Tang", year=2011),
    dict(source_id="fink-creating-signif-cae1a56f",
         title="Creating Significant Learning Experiences",
         author="L. Dee Fink", year=2013),
    dict(source_id="anderson-krathwohl-t-2e6259ce",
         title="A Taxonomy for Learning, Teaching, and Assessing",
         author="Lorin W. Anderson and David R. Krathwohl (eds.)", year=2001),
    dict(source_id="gagne-briggs-wager-p-e2418d40",
         title="Principles of Instructional Design",
         author="Robert M. Gagné, Leslie J. Briggs, and Walter W. Wager", year=1992),
    dict(source_id="merrill-first-princi-dd2a4ed2",
         title="First Principles of Instruction",
         author="M. David Merrill", year=2002),
    dict(source_id="dick-carey-systemati-65eb3dad",
         title="The Systematic Design of Instruction",
         author="Walter Dick, Lou Carey, and James O. Carey", year=2015),
    dict(source_id="allen-leaving-addie-36548667",
         title="Leaving ADDIE for SAM",
         author="Michael Allen with Richard Sites", year=2012),
    dict(source_id="mayer-multimedia-lea-f516bca0",
         title="Multimedia Learning",
         author="Richard E. Mayer", year=2009),
    dict(source_id="clark-mayer-elearnin-a0fa4bb7",
         title="e-Learning and the Science of Instruction",
         author="Ruth Colvin Clark and Richard E. Mayer", year=2016),
]
for _s in SOURCES:
    _s["rights_status"] = "distillation-only"
    _s["sha256"] = SHA[_s["source_id"]]


def emit_profile() -> None:
    profile = {
        "schema_version": "portable-profile-v1",
        "slug": SLUG,
        "display_name": "Instructional Design Advisor",
        "agent_version": VERSION,
        "status": "ready",
        "tier": 2,
        "multisource_synthesis": "deferred",
        "router_description": ROUTER_DESCRIPTION,
        "role": PROFILE_ROLE,
        "when_to_use": WHEN_TO_USE,
        "when_not_to_use": WHEN_NOT_TO_USE,
        "inputs": {"required": [
            "The instructional artifact under discussion — a course, unit, lesson, programme, "
            "assessment, rubric, material, or evaluation plan — plus its reasoning: the intended "
            "learning, the learners and setting, the evidence gathered, and any claim of alignment, "
            "effectiveness, or readiness made."]},
        "outputs": {
            "primary_format": (
                "A structured recommendation or review that, per finding, names the gap and the "
                "principle it engages, gives the correction, and states the residual trade-off or "
                "the referral — never a bare good/bad verdict, a built deliverable, or a promise of "
                "effectiveness."),
            "modes": MODES,
        },
        "quality_bar": QUALITY_BAR,
        "minimum_useful_output": (
            "At least one recommendation or finding that names an instructional-design practice, "
            "ties it to a named principle, and states the residual trade-off or the referral to "
            "make."),
        "forbidden_behaviours": FORBIDDEN,
        "handoff_rules": HANDOFF,
        "source_of_truth_policy": {
            "canonical_owner": (
                "The teacher of record and the design team hold final authority over the course, its "
                "materials, and what is taught; a qualified content expert holds authority over "
                "subject-matter accuracy; the institution and any accrediting body hold authority "
                "over grades, credit, and certification. The distilled principles from the ten "
                "sources are the authority for the advisory criteria the advisor invokes."),
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

    qb_ids = ["P013/P006/P153/P095", "P060/P038/P067/P100", "P014/P015/P039/P136/P016",
              "P179/P042/P178/P104", "P078/P139/P001/P020/P141", "P130/P133/P122/P007"]
    for i, ids in enumerate(qb_ids):
        add(f"quality_bar[{i}]", ids, "Advisory criterion, not authority to act.")
    fb_ids = ["P173/P031", "P081/P093/P007", "P141/P067", "P005/P007/P043"]
    for i, ids in enumerate(fb_ids):
        add(f"forbidden_behaviours[{i}]", ids, "Boundary restraint; no over-claim.")
    wt_ids = ["P013/P006/P153/P160", "P047/P095/P100/P154", "P130/P168/P054/P002",
              "P078/P139/P140/P141", "P122/P090/P081/P045"]
    for i, ids in enumerate(wt_ids):
        add(f"when_to_use[{i}]", ids, "Routing trigger grounded in the cited principles.")
    add("outputs.primary_format", "P015/P017",
        "Per-finding format with explicit criteria and a gap-closing correction; names the "
        "trade-off or referral rather than a bare verdict or a built deliverable.")
    add("handoff_rules[0]", "P121/P031",
        "Ownership handed to the teacher of record, the design team, and the institution.")
    add("handoff_rules[1]", "P173/P081",
        "Subject-matter accuracy routed to a qualified content expert; impact judgments wait on "
        "evaluation evidence.")
    add("source_of_truth_policy.precedence", "P013/P153/P141/P067/P121",
        "Backward-design ordering + no-over-claim-beyond-boundary-conditions + "
        "institution-owns-the-course, all source-grounded.")
    report = {
        "schema_version": "faithfulness-report-v1",
        "subagent_slug": SLUG,
        "findings": findings,
    }
    w(BASE / "reports" / "faithfulness-report.yaml",
      yaml.safe_dump(report, sort_keys=False, allow_unicode=True, width=100))


GOLDEN = [
    dict(test_id="GT-001", mode="review",
         desc="Positive routing — unit built from topics with a quiz bolted on the end",
         prompt="Review our five-week unit plan. It lists the chapters we'll cover, the activities "
                "students enjoy, and ends with a multiple-choice quiz. The aim is 'students will "
                "understand supply and demand.'",
         must_do=["Work backward from desired results to evidence to teaching",
                  "Resolve 'understand' into the knowledge subtype and cognitive process required",
                  "Reject the multiple-choice quiz as sufficient evidence of understanding",
                  "Require an authentic task with explicit public criteria"],
         must_not=["Write the finished unit plan and quiz for them",
                   "Certify the unit as effective"],
         cov=["P013", "P060", "P071", "P179", "P014", "P015"]),
    dict(test_id="GT-002", mode="review",
         desc="Positive routing — e-learning module with narrated text on screen and decoration",
         prompt="Review our e-learning module. Each screen narrates the text that's also printed on "
                "screen, has background music and stock photos, and the diagram labels are in a "
                "legend below.",
         must_do=["Remove the on-screen duplication of narrated words",
                   "Strip background music, decorative images, and irrelevant words",
                   "Place printed words next to the graphic part they describe",
                   "Eliminate split attention across the interface"],
         must_not=["Rebuild the module for them",
                   "Justify the duplication as serving different learning styles"],
         cov=["P004", "P078", "P139", "P140", "P001", "P043"]),
    dict(test_id="GT-003", mode="advise",
         desc="Positive routing — training request before any analysis",
         prompt="Our error rate is up so we want a training course for the whole team. Where do we "
                "start?",
         must_do=["Begin performance improvement without presuming instruction",
                  "Observe the actual setting and consult frontline practitioners",
                  "Separate capability gaps from environment, incentive, and systems causes",
                  "Trace the problem to an organisational outcome and quantify the gap"],
         must_not=["Start designing the course immediately",
                   "Promise the training will cut the error rate"],
         cov=["P130", "P168", "P054", "P022", "P002"]),
    dict(test_id="GT-004", mode="review",
         desc="Positive routing — assessment scheme graded on a curve with hidden criteria",
         prompt="Review our assessment scheme. We grade on a curve, the criteria live in the "
                "marker's head, and everything rides on one final exam.",
         must_do=["Prefer criterion-referenced standards over norm-referenced grading on a curve",
                  "Require explicit public criteria applied before judgment",
                  "Gather evidence along the way by varied methods rather than one snapshot",
                  "Separate formative from summative purpose and label them unmistakably"],
         must_not=["Assign the grades or set the pass mark for them",
                   "Treat a single exam score as sufficient outcome evidence"],
         cov=["P039", "P015", "P136", "P075", "P083"]),
    dict(test_id="GT-005", mode="plan",
         desc="Positive routing — build a course from verified need to evaluation",
         prompt="We've confirmed a real skill gap. Plan how we get from here to a working course we "
                "can trust.",
         must_do=["Set outcomes and the evidence of achievement before building materials",
                  "Derive instructional strategy from the goal, analyses, objectives, and "
                  "assessments",
                  "Use experiential prototypes with representative learners while change is "
                  "affordable",
                  "Plan formative evaluation on a usable draft with one-to-one, small-group, and "
                  "field evidence"],
         must_not=["Build the materials for them",
                   "Treat specification sign-off as evidence the design works"],
         cov=["P013", "P102", "P133", "P073", "P122"]),
    dict(test_id="GT-006", mode="review",
         desc="Positive routing — group project failing with free-riding and vague outcomes",
         prompt="Review our group project. Teams pick their own topic, one person does the work, and "
                "we grade the final artefact as a group.",
         must_do=["Structure group learning with relevant resources, responsibility, and a "
                  "cognitively demanding agenda tied to assessed outcomes",
                  "Require visible individual contribution before using group evidence",
                  "Share functional product criteria before learners begin",
                  "Calibrate option choice for demand, workload, and scoring before grading it"],
         must_not=["Assign the group grades for them",
                   "Treat the format itself as the teaching method"],
         cov=["P087", "P092", "P164", "P145", "P147"]),
    dict(test_id="GT-007", mode="advise",
         desc="Positive routing — training delivered but the behaviour is not appearing at work",
         prompt="Everyone passed the training six months ago but we don't see the new procedure "
                "being used on the job. What now?",
         must_do=["Establish with valid posttest evidence that learners could perform every main "
                  "goal performance",
                  "Measure use by degree, frequency, context, and prior use",
                  "Diagnose nonuse across relevance, permission, support, resources, and incentives",
                  "Triangulate across learners and relevant workplace observers"],
         must_not=["Conclude the training failed without posttest evidence",
                   "Prescribe more training as the default remedy"],
         cov=["P093", "P045", "P051", "P066", "P131"]),
]

NEGATIVE = [
    dict(test_id="NR-001",
         prompt="Write the full slide deck, workbook, and final exam for our onboarding course.",
         reason="Asks for the deliverable to be built end to end, not instructional-design advice."),
    dict(test_id="NR-002",
         prompt="Grade these thirty student essays and give each one a mark out of 100.",
         reason="Asks for learners to be graded — the teacher of record's decision, not design "
                "advice."),
    dict(test_id="NR-003",
         prompt="Is the second law of thermodynamics stated correctly in this chapter?",
         reason="A subject-matter correctness question for a content expert, outside the design "
                "scope."),
]

MISSING = [
    dict(test_id="MC-001",
         prompt="Make our course better.",
         ask=["Which part — the outcomes, the assessment, the activities, or the materials",
              "The learners, the setting, and the delivery format",
              "What evidence exists that something is not working"]),
    dict(test_id="MC-002",
         prompt="Review my assessment.",
         ask=["The assessment tasks and criteria themselves",
              "The outcomes they are meant to provide evidence for",
              "Whether the purpose is formative, summative, or both"]),
    dict(test_id="MC-003",
         prompt="We need training.",
         ask=["The organisational outcome or problem behind the request",
              "Whether a capability gap has been distinguished from environment, incentive, and "
              "systems causes",
              "Who the performers are and what they can currently do"]),
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

    # one behaviour test per principle (all N → covers every high-confidence principle)
    modes = ["advise", "review", "plan"]
    pb = []
    for idx, pid in enumerate(ALL_IDS):
        skill = PID_TO_SKILL[pid]
        pb.append({
            "test_id": f"PB-{pid}",
            "principle_id": pid,
            "mode": modes[idx % 3],
            "prompt": (
                f"We are working on an instructional-design question where "
                f"{THEMES[skill]['title'].lower()} is at issue. What should we check for, what is "
                f"the correction, and what residual trade-off or referral should we carry?"),
            "expected_behaviour": [
                f"Applies the principle: {lead(P[pid]['statement'], 300)}.",
                "Names the gap and the principle it engages, gives the correction, and states the "
                "residual trade-off or the referral to make.",
                f"Cites {pid}.",
            ],
            "must_not": [
                "Build the course, materials, or item bank for the caller, grade learners, or "
                "certify the design effective.",
                "State the principle more strongly than the source supports, or rule on the "
                "subject-matter correctness of the content.",
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

All ten sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They are canonical
works on instructional and course design — backward design and assessment for understanding,
constructive alignment and university teaching, integrated course design, the revised taxonomy of
knowledge and cognitive process, systematic instructional design, first principles of instruction,
iterative successive-approximation development, and the cognitive science of multimedia learning.

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
  P001-P{N_PRINC:03d} / {len(CLAIM_IDS)} claims from ten distillation-only sources).
- `profile.yaml` derived from the {N_PRINC} promoted principles: role, router description,
  when/when-not-to-use, three modes (advise / review / plan), quality bar, forbidden behaviours,
  handoff rules, and a {len(SKILLS)}-skill / {len(REFS)}-reference `knowledge_partition` covering
  every principle exactly once.
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
- Ten distillation-only sources: *Understanding by Design* (Wiggins & McTighe, 2005); *Teaching for
  Quality Learning at University* (Biggs & Tang, 2011); *Creating Significant Learning Experiences*
  (Fink, 2013); *A Taxonomy for Learning, Teaching, and Assessing* (Anderson & Krathwohl, 2001);
  *Principles of Instructional Design* (Gagné, Briggs & Wager, 1992); *First Principles of
  Instruction* (Merrill, 2002); *The Systematic Design of Instruction* (Dick, Carey & Carey, 2015);
  *Leaving ADDIE for SAM* (Allen, 2012); *Multimedia Learning* (Mayer, 2009); and *e-Learning and
  the Science of Instruction* (Clark & Mayer, 2016).
"""
    w(BASE / "CHANGELOG.md", md)


def fix_metadata() -> None:
    mdir = BASE / "sources" / "metadata"
    for mf in mdir.glob("*.metadata.json"):
        data = json.loads(mf.read_text())
        changed = False
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
