"""Deterministic authoring generator for instructional-design-advisor.

Reads the already-assembled, deterministically-valid distilled spine
(principles/principles.yaml + analysis/claims.jsonl + evidence + anchors) and emits the
LLM-authored layer: profile.yaml, references/*, skills/*, tests/*, reports/faithfulness-report.yaml,
provenance-ledger.md, CHANGELOG.md. Every emitted id resolves into the spine.

v1.1.0 fold-in: the spine was rebuilt over eleven sources (full *Multimedia Learning* replacing the
partial conversion, plus *Instructional-Design Theories and Models / In Action*), which renumbered
every principle. The 13-skill partition and every inline principle citation below were re-derived
against the new P001-P200 numbering — the v1.0.0 ids do not carry over.

Run:  python3 .build/authoring/gen.py
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parents[2]  # subagents/instructional-design-advisor
SLUG = "instructional-design-advisor"
VERSION = "1.1.0"
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
# Every principle 1..N appears exactly once. Re-derived for the v1.1.0 renumbered spine.
SKILLS: list[tuple[str, list[int]]] = [
    ("backward-design-and-constructive-alignment",
     [3, 8, 9, 13, 14, 20, 46, 55, 64, 88, 101, 111, 125, 135, 172]),
    ("learning-outcomes-and-taxonomy",
     [1, 31, 76, 77, 105, 115, 141, 142, 153, 161, 170, 173, 179, 182, 184, 188]),
    ("assessment-design-and-authentic-tasks",
     [12, 16, 17, 18, 21, 44, 47, 48, 67, 81, 84, 89, 97, 98, 110, 112, 114, 127, 128, 129, 132,
      167, 199]),
    ("feedback-and-formative-practice", [22, 33, 57, 113, 130, 165]),
    ("teaching-for-understanding-and-transfer",
     [23, 34, 45, 56, 58, 78, 116, 120, 131, 144, 154, 163, 171, 174, 196, 197, 198]),
    ("multimedia-and-elearning-design",
     [2, 7, 15, 26, 38, 40, 42, 92, 93, 124, 155, 156, 157, 158, 159, 160]),
    ("instructional-strategy-and-events",
     [5, 11, 19, 24, 25, 27, 28, 29, 32, 35, 36, 37, 39, 51, 52, 53, 54, 59, 60, 63, 74, 86, 117,
      118, 122, 123, 143, 146, 147, 150, 180, 181, 185, 189, 190]),
    ("motivation-and-learner-engagement", [30, 49, 80, 100, 133, 169]),
    ("needs-and-context-analysis",
     [50, 65, 70, 75, 79, 95, 102, 148, 187, 191, 192, 193]),
    ("iterative-prototyping-and-development", [10, 68, 73, 85, 87, 119, 151, 152, 195]),
    ("evaluation-transfer-and-impact",
     [41, 62, 66, 69, 71, 72, 82, 91, 94, 96, 99, 104, 106, 109, 140, 145, 149, 178, 194]),
    ("active-learning-and-group-formats",
     [61, 83, 103, 108, 126, 136, 137, 138, 139, 164, 166, 168, 175, 176, 177, 183, 186]),
    ("teaching-scholarship-and-quality", [4, 6, 43, 90, 107, 121, 134, 162, 200]),
]

# integrity: every principle exactly once
_seen: list[int] = []
for _slug, _nums in SKILLS:
    _seen += _nums
assert sorted(_seen) == list(range(1, N_PRINC + 1)), (
    f"partition mismatch: dup={sorted({n for n in _seen if _seen.count(n) > 1})} "
    f"missing={sorted(set(range(1, N_PRINC + 1)) - set(_seen))}")
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
            "programme, and graduate purposes are designed backward with the same elements; keeps "
            "outcomes few, integrated, and stated as what a learner will newly do and how well; "
            "refuses covering the content as a goal because it names what the teacher does; "
            "prioritises threshold and core content deliberately against stakeholder accretion; "
            "makes sure learners know what the learning eventually requires them to do; checks "
            "alignment goal-by-goal against the assessment and the activities that support it; and "
            "treats design as iterative, with earlier units rethought in light of later ones."),
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
            "performance actually requires, words objectives by intended cognition rather than by "
            "observable response format, separates remembering from understanding and refuses "
            "retention evidence as proof a design worked, distinguishes routine execution from "
            "adaptive implementation, and treats analysis, evaluation, and creation as either "
            "transfer targets or means to simpler learning. It uses taxonomy as an adaptable "
            "analytic heuristic rather than a literal reality or a teaching prescription, classifies "
            "a task for a stated learner group and prior-experience state, analyses intellectual "
            "performance at its actual transfer level, and resolves conflicting signals by comparing "
            "intended wording, enacted activity, assessed content, and scoring criteria."),
        when=[
            "An objective, outcome statement, or standard is too broad to design or assess against.",
            "A design must decide the cognitive level it is actually targeting, or whether a claimed "
            "higher-order verb survives contact with the enacted task.",
            "A taxonomy classification is disputed, or is being applied as a rule rather than a "
            "heuristic.",
            "Transfer-level or understanding outcomes must be stated in a form that can be taught, "
            "observed, and assessed with sufficiently novel material.",
        ],
        input="The objectives or outcome statements under discussion, the tasks and scoring criteria "
              "that enact them, and the learner group and its prior experience."),
    "assessment-design-and-authentic-tasks": dict(
        title="Assessment Design And Authentic Tasks",
        purpose=(
            "This skill designs and reviews the evidence side of a course: authentic tasks that "
            "require judgment on unstructured problems in a realistic context, explicit public "
            "criteria applied before judgment, rubric standards written as descriptions of "
            "performance rather than bare numbers, and forward-looking tasks that put learners where "
            "the knowledge is actually used rather than repeating a taught protocol with varied "
            "parameters. It expects evidence of understanding to be less direct than an objective "
            "test score, separates formative from summative purpose, separates task grades from "
            "outcome achievement, prefers criterion-referenced standards over forced distributions "
            "and false percentage precision, builds assessment as an accumulating scrapbook of "
            "varied evidence rather than one snapshot, and designs examinations, portfolios, "
            "rubrics, reassessment, and the whole assessment programme as one proportionate evidence "
            "system."),
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
            "This skill builds the loop between performance and improvement: cycles of performance, "
            "feedback, revision, and new performance; feedback that tells the learner the degree of "
            "correctness of what they did, whether built into the medium, learner-initiated, or "
            "supplied later; immediate self-checkable feedback inside embedded practice grounded in "
            "the authentic goal; and shared quality criteria used consistently across instructor, "
            "peer, and self-review as learners' judgment develops. It keeps formative feedback "
            "timely, two-way, and gap-closing — exposing both current performance and the intended "
            "standard while learners can still act on it — and treats a plan that cannot absorb "
            "feedback as a defect rather than a virtue."),
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
            "teaching around big ideas and the four senses of an essential question, reviews "
            "predictable misconceptions before teaching, evaluates instruction by transfer rather "
            "than memory because approaches look equivalent under recall measures alone, and refuses "
            "to count a task as transfer when it varies only quantities or symbols. It teaches "
            "metacognition, comprehension monitoring, and self-regulation explicitly as strategy "
            "knowledge plus monitoring and repair; builds understanding by connecting new learning "
            "to prior frameworks and revisiting ideas through varied, spaced encounters; repairs "
            "systematic misconceptions at the underlying categorization rather than by adding "
            "another definition; opens access to substantial material through conceptual bridges "
            "rather than lowered expectations; preserves warranted uncertainty in evidence-based "
            "judgment; and declines to read a call for inquiry around a big idea as a blanket "
            "endorsement of discovery learning."),
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
            "This skill applies the evidence on how people learn from words and pictures. It "
            "analyses a message by how the learner processes it — verbal versus pictorial "
            "presentation mode, auditory versus visual sensory modality — rather than by counting "
            "delivery devices; designs against dual channels, limited capacity, and active "
            "processing; and routes words away from the visual channel by preferring narration to "
            "concurrent on-screen text when a graphic must be processed at the same time. It strips "
            "seductive details, places printed words next to the graphic part they describe, "
            "eliminates split attention wherever the interface creates it, matches graphic type to "
            "what is being taught, aims for a schematic rather than photographic model, sets "
            "practice quantity from criticality and learner time cost, diagnoses whether the problem "
            "is extraneous, essential, or generative processing before prescribing a remedy, "
            "declines to design around learning styles or a universally best medium, requires a "
            "design principle to be both theory-grounded and evidence-based, and checks learner "
            "prior knowledge before applying any principle."),
        when=[
            "E-learning, slides, animation, video, or any words-plus-graphics material is being "
            "designed or reviewed.",
            "A medium or technology is being chosen, or is being adopted ahead of the pedagogy.",
            "A design appeals to learning styles, added delivery modes, or added interest as "
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
            "treats the nine events as a design checklist rather than a mandatory script, prescribes "
            "a method together with the situation it fits, and sequences like a zoom lens — an "
            "epitome of the whole, then elaboration of one part, then synthesis back to the whole. "
            "It sequences by prerequisite and manageable progression with entry checks and pretests, "
            "and matches technique to outcome type: concepts through varied instances and diagnostic "
            "non-instances with irrelevant shortcut cues removed, intellectual skills through "
            "activated prerequisites and progressive transfer cases, verbal information through "
            "organised prior-knowledge links, attitudes through credible models and delivered "
            "consequences, motor skills through part and whole practice. It scaffolds generative and "
            "complex performance from supported to independent work, fades prompts so contiguity is "
            "established with the intended cue, keeps every practice and test instance new, uses "
            "spaced retrieval rather than re-presentation, makes training conditions resemble "
            "retrieval conditions, builds strategy flexibility across multiple valid methods, and "
            "budgets time across the whole sequence."),
        when=[
            "The activities, examples, practice, and sequence of a unit or course must be chosen or "
            "reviewed.",
            "Different outcome types — concepts, intellectual skills, verbal information, attitudes, "
            "motor skills — need matching techniques.",
            "Learners must be scaffolded from supported work to independent production, or "
            "prerequisites are unmet.",
            "A recommended technique needs the situation, conditions, and time budget that make it "
            "the right one stated alongside it.",
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
            "accurate information about what these learners can and cannot do and pairs a "
            "challenging activity with the activities that build the skills it demands; combines "
            "autonomy and trust with clear goals, organised support, and fair safeguards while "
            "avoiding intimidation, arbitrary control, and cynical busy-work; and reads deep and "
            "surface approaches as task-and-context dependent, treating the familiar cluster of "
            "disengagement symptoms as evidence about the design rather than about the students."),
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
            "instruction and commits to needs assessment and design only for verified skill gaps, "
            "using proportionate analysis to separate capability deficits from accountability, "
            "incentive, tool, process, and culture causes. It traces a voiced problem to an "
            "organisational outcome and quantifies the desired-versus-actual gap with critical "
            "distance, multiple perspectives, and contrary evidence; operationalises vague goals "
            "into observable success behaviours confirmed by several knowledgeable contributors; "
            "triangulates unclear goal steps through self-performance, competent performers, "
            "workplace evidence, and authoritative procedures; uncovers the thought processes an "
            "expert actually uses by objective methods rather than self-report; describes learners, "
            "learning context, performance context, and tools from actual conditions; splits goals "
            "whose subperformances differ in structure; tests adoption fit against organisational "
            "goals and total cost; and gives a qualified content expert explicit structured review "
            "criteria rather than an unbounded opinion."),
        when=[
            "A training request arrives before anyone has established that instruction is the right "
            "response.",
            "A goal, its steps, or its success indicators are too vague to design or assess against.",
            "Learners, delivery technology, workplace conditions, or support arrangements must be "
            "established from actual conditions rather than assumed.",
            "Subject-matter accuracy or goal validity needs a content expert's review under explicit "
            "criteria.",
        ],
        input="The stated problem or training request, the organisational outcome behind it, what is "
              "known about the performers and their setting, and any analysis already done."),
    "iterative-prototyping-and-development": dict(
        title="Iterative Prototyping And Development",
        purpose=(
            "This skill develops the design in small, evidence-tested increments rather than by "
            "specification sign-off. It begins and ends every cycle with evaluation and keeps the "
            "first cycle to a thin slice connecting performance goals, objectives, appraisal, "
            "practical media, and representative treatments and content; uses experiential "
            "prototypes to align stakeholder expectations and test timing, transitions, media, "
            "interaction, and integration before misunderstanding reaches costly development; "
            "involves recent and representative learners while fundamental changes remain "
            "affordable, shifting review focus from treatment to wording, media, interface, "
            "navigation, and feedback as fidelity rises; drafts only enough objectives to prototype "
            "representative cases and prototypes each distinct objective-activity type rather than "
            "every instance; gates release progressively through design proof, alpha, and beta; "
            "converges as evidence stabilises and resists perfection and unplanned refinement; and "
            "estimates cost and duration honestly, phasing delivery or cutting to a coherent "
            "effective core rather than underfunding the whole solution."),
        when=[
            "A development approach must be chosen, or a project is heading for specification "
            "sign-off without a testable artefact.",
            "Prototypes, review cycles, or release gates need designing or are being skipped.",
            "Scope, cost, or schedule pressure is about to spread inadequate funding across the "
            "whole solution.",
            "A design is being refined past the point where evidence still justifies the change.",
        ],
        input="The development plan, the artefacts produced so far, who reviews them and when, and "
              "the resources and schedule committed."),
    "evaluation-transfer-and-impact": dict(
        title="Evaluation Transfer And Impact",
        purpose=(
            "This skill establishes what a design actually achieved. It distinguishes learner "
            "assessment from instructional evaluation — formative assessment to improve learning, "
            "staged formative evaluation to revise development, independent summative evaluation to "
            "support post-completion decisions — and formatively evaluates a usable draft through "
            "one-to-one, small-group, and field evidence, tracing learner difficulty back to the "
            "implicated design assumption. It gates expert judgment through congruence, content, "
            "design, and transfer analyses and stops when a material defect makes downstream "
            "evaluation unjustified; screens instruction for congruence, completeness, and strategy "
            "fit before funding an impact study; establishes with valid posttest evidence that "
            "learners could perform before reading absent workplace behaviour as a transfer failure; "
            "measures use by degree, frequency, context, and prior use and diagnoses nonuse across "
            "relevance, permission, support, resources, and opportunity; triangulates across "
            "learners, observers, records, and objective indicators; compares interventions only "
            "once each is mature and uses an independent evaluator when interests threaten "
            "impartiality; and reports purpose, questions, design, findings, and limits with an "
            "executive summary."),
        when=[
            "A design must be evaluated — formatively during development or summatively after "
            "completion.",
            "Training was delivered but the intended behaviour is not appearing at work.",
            "An impact, effectiveness, or return claim is being made or requested.",
            "Expert review, field trials, or a comparison between two interventions needs "
            "designing.",
        ],
        input="The design or programme under evaluation, the evidence already gathered, the "
              "organisational outcome it was meant to serve, and who will use the findings."),
    "active-learning-and-group-formats": dict(
        title="Active Learning And Group Formats",
        purpose=(
            "This skill designs what learners do together and over extended work. It treats broad "
            "formats as settings rather than methods, selecting different learner activities for "
            "different outcomes and reserving lectures for distinctive live value rather than "
            "routine information transfer. It structures group learning so members have relevant "
            "resources, responsibility, room to test interpretations, and a cognitively demanding "
            "agenda tied to assessed outcomes; uses group evidence only with visible individual "
            "contribution, whole-task understanding, individual reflection, and safeguards; sustains "
            "large classes with stable peer support, rapid formative evidence, and work-along "
            "activity that makes reasoning visible; designs peer-teaching programmes with explicit "
            "roles, selection, training, and continuous support; launches authentic projects through "
            "a credible example, investigated audiences and products, and stakeholder critique, and "
            "calibrates option choice for demand, workload, and scoring before grading it; designs "
            "problem-based learning and practica from their intended outcomes with aligned tutors, "
            "assessment, and organisational boundaries; and scaffolds extended creation by "
            "introducing purpose, audience, criteria, and source adequacy before drafting begins."),
        when=[
            "Group work, team projects, problem-based learning, practica, peer teaching, or a large "
            "class format is being designed or is failing.",
            "Individual contribution, free-riding, or the fairness of a group grade is in question.",
            "Learners choose among project options that differ in demand, workload, or scoring.",
            "An extended written, oral, or research product needs scaffolding before drafting.",
        ],
        input="The format, group arrangements, project or problem brief, criteria, and support in "
              "place, and the outcomes the format is meant to deliver."),
    "teaching-scholarship-and-quality": dict(
        title="Teaching Scholarship And Quality",
        purpose=(
            "This skill governs how a teacher or design team learns about its own practice and how "
            "quality claims are warranted. It grounds any claim that instruction is adequate in "
            "evidence about what students actually learn and how much they grow rather than in "
            "demand, enrolment, or satisfaction; prefers results replicated and synthesised across "
            "studies over any single study while noting that synthesis also pinpoints when an effect "
            "is strong; makes the teaching theory shaping the learning environment explicit and uses "
            "evidence and a coherent framework to adapt to local learners and constraints; "
            "investigates teaching through repeated action-research cycles — frame an observable "
            "learning problem, plan a change from theory and student evidence, apply it, evaluate, "
            "revise — triangulated across students and trusted colleagues; reads realistic teaching "
            "cases as provisional evidence, classifying intention, enactment, and assessment "
            "separately before evaluating; names the teacher's blind spot that teaching implies "
            "learning; treats instructional design as professional work requiring knowledge and "
            "practice; and chooses approaches by what the learning needs rather than by what the "
            "teaching finds comfortable, knowing each preference's characteristic failure mode."),
        when=[
            "A quality, effectiveness, or 'our teaching is fine' claim rests on enrolment, demand, "
            "satisfaction, or the teacher's own impression.",
            "Evidence from research is being cited to justify a design decision.",
            "A team wants to investigate and improve its own teaching systematically.",
            "Instructional approach is being chosen by habit, comfort, or seniority rather than by "
            "what the learning requires.",
        ],
        input="The quality or effectiveness claim being made, the evidence offered for it, and the "
              "team's current arrangements for investigating its own teaching."),
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
    "grounded in the eleven distillation-only sources (*Understanding by Design*; *Teaching for "
    "Quality Learning at University*; *Creating Significant Learning Experiences*; *A Taxonomy for "
    "Learning, Teaching, and Assessing*; *Principles of Instructional Design*; *First Principles of "
    "Instruction*; *The Systematic Design of Instruction*; *Leaving ADDIE for SAM*; *Multimedia "
    "Learning*; *e-Learning and the Science of Instruction*; and *Instructional-Design Theories and "
    "Models: A New Paradigm of Instructional Theory / In Action*)")


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
    out.append("Eleven distillation-only sources ground the package, spanning backward design and "
               "assessment for understanding (*Understanding by Design*), constructive alignment and "
               "university teaching (*Teaching for Quality Learning at University*), integrated "
               "course design (*Creating Significant Learning Experiences*), the revised taxonomy of "
               "knowledge and cognitive process (*A Taxonomy for Learning, Teaching, and "
               "Assessing*), systematic instructional design (*Principles of Instructional Design*, "
               "*The Systematic Design of Instruction*), demonstration-application-centred "
               "instruction (*First Principles of Instruction*), instructional-theory and "
               "elaboration sequencing (*Instructional-Design Theories and Models*), iterative "
               "successive-approximation development (*Leaving ADDIE for SAM*), and the cognitive "
               "science of learning from words and pictures (*Multimedia Learning*, *e-Learning and "
               "the Science of Instruction*). Paraphrase and restructure only — no verbatim "
               "quotation (see `.claude/rules/rights-and-quotation-policy.md`).\n")
    out.append("## Faithfulness discipline\n")
    out.append("- No advice may state a rule more strongly than its source supports: rules for "
               "teaching mental operations are conditional rather than absolute, so the conditions "
               "are stated with the rule, a method is prescribed together with the situation it "
               "fits, and a design principle's effect is checked against learner prior knowledge "
               "before it is applied (P011, P122, P042).")
    out.append("- A design principle is recommended only when it is both theory-grounded and "
               "evidence-based; when only one criterion holds, say which is missing (P092).")
    out.append("- Taxonomies and models are adaptable analytic heuristics, not literal reality, a "
               "source of educational aims, or a unique teaching prescription; a disputed "
               "classification is used to improve the design, not to win a labelling contest (P001, "
               "P182).")
    out.append("- Evidence about learning governs claims about quality: adequacy rests on what "
               "students actually learn and how much they grow, not on demand, enrolment, or "
               "satisfaction; added interest that is irrelevant reliably reduces learning; and "
               "disengagement symptoms are evidence about the design (P004, P093, P100).")
    out.append("- Constructive alignment is adapted to local context while its core relationship is "
               "preserved, and the design stays iterative — earlier decisions are rethought as later "
               "ones expose problems (P064, P055).")
    out.append("- The advisor guides the design; the teacher of record, the content expert, and the "
               "institution own the course, the subject matter, and the grades (P107, P193, "
               "P021).\n")
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
    "practice, teaching for understanding and transfer, instructional strategy and sequencing for "
    "each outcome type, multimedia and e-learning materials, motivation, needs and context "
    "analysis, iterative prototyping, evaluation of transfer and impact, group and project formats, "
    "and teaching scholarship. Use when designing or reviewing a course, unit, lesson, programme, "
    "training intervention, assessment scheme, or instructional material. Not for: building the "
    "course or materials, teaching or grading learners, ruling on subject-matter correctness, or "
    "accreditation and certification decisions."
)

PROFILE_ROLE = (
    "An advisor on instructional and course design, grounded in eleven distillation-only sources on "
    "backward design, constructive alignment, learning taxonomies, systematic instructional design, "
    "instructional theory and sequencing, iterative development, and multimedia learning. It helps "
    "designers and teachers analyse needs, set and level outcomes, design assessment and "
    "instructional strategy, prototype materials, and evaluate transfer and impact. The invariants "
    "below are advisory criteria, not authority to act: this advice-only boundary and the forbidden "
    "behaviours override every invariant, so the advisor never builds the course, teaches it, "
    "grades learners, or certifies a programme.")

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
    "the unit as the working focus and every goal, assessment, and activity checked against each "
    "other (P013, P003, P008, P172).",
    "Outcomes resolved to the knowledge subtype and cognitive process the performance actually "
    "requires, worded by intended cognition, with remembering separated from understanding and "
    "taxonomy used as a heuristic (P077, P115, P153, P001).",
    "Assessment authentic, criterion-referenced against public descriptive standards, and "
    "accumulated as varied evidence across a proportionate programme rather than one snapshot "
    "(P016, P017, P098, P199, P167).",
    "Understanding shown by transfer to new problems and settings rather than recall or coverage, "
    "with predictable misconceptions reviewed first (P196, P056, P198, P067).",
    "Materials follow the evidence on words and pictures — coherence, contiguity, modality, "
    "signalling — applied as theory-grounded, evidence-based guidance checked against learner prior "
    "knowledge (P093, P159, P157, P053, P042, P092).",
    "Instruction warranted by front-end analysis, prototyped experientially, and evaluated for "
    "learning and workplace transfer rather than enrolment or satisfaction (P148, P152, P140, "
    "P004).",
]

FORBIDDEN = [
    "Building the deliverable for the caller — the course, materials, or item bank produced end to "
    "end; the advisor supplies review criteria and the practitioner makes the teaching theory and "
    "the design their own (P193, P107).",
    "Certifying a design effective, a programme accredited, or learners competent in advance; "
    "impact is evaluated only after target learners can perform in context, on valid posttest "
    "evidence (P096, P109, P004).",
    "Stating a design principle more strongly than its source supports — omitting the conditions "
    "that make a rule hold, the situation a method fits, the learner prior knowledge that bounds it, "
    "or which of theory-grounding and evidence is missing (P011, P122, P042, P092).",
    "Treating enrolment, satisfaction, added interest, or learning-style fit as evidence that "
    "learning occurred, or reading disengagement as a fact about the students (P004, P093, P040, "
    "P100).",
]

HANDOFF = [
    "The teacher of record, the design team, and the institution own the course, the grades, and the "
    "decision to run it; the advisor informs the design, names the residual trade-off, and leaves "
    "criterion-based outcome judgement and its administrative constraints with them (P107, P021, "
    "P134).",
    "Subject-matter accuracy is referred to a qualified content expert against explicit structured "
    "review criteria, and impact judgments wait on evaluation evidence gathered once learners can "
    "perform in context (P193, P096).",
]

PRECEDENCE = (
    "What learners are meant to be able to do governs the design — desired results precede the "
    "evidence, and the evidence precedes the teaching (P013, P172); no principle is stated more "
    "strongly than its source supports, so the conditions that make a rule hold and the situation a "
    "method fits are named whenever it is invoked (P011, P122); and the teacher of record, the "
    "content expert, and the institution own the course, the subject matter, and the grades, which "
    "overrides every design invariant (P107, P193).")

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
             "(P013), keeping the unit as the design focus (P003); covering the chapters is not a "
             "learning goal because it names what the teacher does (P046). (2) 'Understand' is "
             "unresolved: state the knowledge subtype and cognitive process the performance actually "
             "requires (P077), and write the goal as what students will newly be able to do and how "
             "well (P125). (3) A multiple-choice quiz cannot show understanding — a right answer can "
             "come from rote recall, test-taking skill, or a lucky guess (P067), and retention "
             "evidence alone does not show the design worked (P153); test transfer on new problems "
             "and settings (P196) through an authentic task (P016) with explicit criteria applied "
             "before judgment (P017). (4) Enjoyed activities are not evidence: state the intended "
             "result and success criteria, connect them repeatedly to the activity, and show "
             "representative evidence (P111). (5) Ask what misconceptions learners bring before "
             "teaching (P198). Correction: rewrite the unit outcome, choose the evidence, then "
             "rebuild activities. Residual trade-off: authentic tasks cost marking time, so weight "
             "the assessment programme proportionally to educational importance (P167). The design "
             "and the grades stay with the teacher.")),
    dict(title="Decline to build the course and to certify its effectiveness",
         kind="failure-recovery",
         scenario=(
             "The caller says 'Just build the whole onboarding course for us — slides, workbook, and "
             "final exam — and confirm it will cut our error rate by half.'"),
         ideal_response=(
             "Decline both requests: this advisor guides design rather than authoring the "
             "deliverable, and no design can be certified effective in advance — impact is evaluated "
             "only after target learners can perform in context (forbidden behaviours, P096, P109). "
             "Redirect: first establish that instruction is warranted at all, beginning performance "
             "improvement without presuming it and separating capability deficits from "
             "accountability, incentive, tool, process, and culture causes (P148, P187), tracing the "
             "voiced problem to an organisational outcome and quantifying the gap (P191). If a skill "
             "gap is verified, set outcomes and the evidence of achievement before materials (P013), "
             "prototype experientially rather than approving specifications (P152), and formatively "
             "evaluate a usable draft through one-to-one, small-group, and field evidence (P140). "
             "Then scope an impact study that measures use by degree, frequency, context, and prior "
             "use and diagnoses nonuse across relevance, permission, support, resources, and "
             "adaptation opportunity (P062). Offer to review the team's drafts against these "
             "criteria; the build and the claims stay with the team.")),
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
    dict(source_id="mayer-multimedia-lea-40e2757d",
         title="Multimedia Learning",
         author="Richard E. Mayer", year=2009),
    dict(source_id="clark-mayer-elearnin-a0fa4bb7",
         title="e-Learning and the Science of Instruction",
         author="Ruth Colvin Clark and Richard E. Mayer", year=2016),
    dict(source_id="reigeluth-instructio-a562075c",
         title="Instructional-Design Theories and Models (In Action / A New Paradigm)",
         author="Charles M. Reigeluth (ed.)", year=1999),
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
                "over grades, credit, and certification. The distilled principles from the eleven "
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

    qb_ids = ["P013/P003/P008/P172", "P077/P115/P153/P001", "P016/P017/P098/P199/P167",
              "P196/P056/P198/P067", "P093/P159/P157/P053/P042/P092", "P148/P152/P140/P004"]
    for i, ids in enumerate(qb_ids):
        add(f"quality_bar[{i}]", ids, "Advisory criterion, not authority to act.")
    fb_ids = ["P193/P107", "P096/P109/P004", "P011/P122/P042/P092", "P004/P093/P040/P100"]
    for i, ids in enumerate(fb_ids):
        add(f"forbidden_behaviours[{i}]", ids, "Boundary restraint; no over-claim.")
    wt_ids = ["P013/P003/P172/P125", "P064/P077/P173/P135", "P148/P187/P191/P192",
              "P157/P159/P093/P042", "P140/P094/P096/P062"]
    for i, ids in enumerate(wt_ids):
        add(f"when_to_use[{i}]", ids, "Routing trigger grounded in the cited principles.")
    add("outputs.primary_format", "P017/P130",
        "Per-finding format with explicit criteria and a gap-closing correction; names the "
        "trade-off or referral rather than a bare verdict or a built deliverable.")
    add("handoff_rules[0]", "P107/P021/P134",
        "Ownership handed to the teacher of record, the design team, and the institution.")
    add("handoff_rules[1]", "P193/P096",
        "Subject-matter accuracy routed to a qualified content expert under explicit review "
        "criteria; impact judgments wait on evaluation evidence.")
    add("source_of_truth_policy.precedence", "P013/P172/P011/P122/P107/P193",
        "Backward-design ordering + state-the-conditions-and-situation (no over-claim) + "
        "practitioner-and-institution-own-the-course, all source-grounded.")
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
         cov=["P013", "P046", "P077", "P067", "P196", "P016", "P017"]),
    dict(test_id="GT-002", mode="review",
         desc="Positive routing — e-learning module with narrated text on screen and decoration",
         prompt="Review our e-learning module. Each screen narrates the text that's also printed on "
                "screen, has background music and stock photos, and the diagram labels are in a "
                "legend below.",
         must_do=["Prefer narration over concurrent on-screen text when a graphic must be processed "
                  "at the same time",
                  "Strip background music, decorative images, and other seductive details",
                  "Place printed words next to the graphic part they describe",
                  "Eliminate split attention across the interface"],
         must_not=["Rebuild the module for them",
                   "Justify the duplication as serving different learning styles"],
         cov=["P157", "P093", "P159", "P160", "P040", "P042"]),
    dict(test_id="GT-003", mode="advise",
         desc="Positive routing — training request before any analysis",
         prompt="Our error rate is up so we want a training course for the whole team. Where do we "
                "start?",
         must_do=["Begin performance improvement without presuming instruction",
                  "Commit to design only for a verified skill gap",
                  "Separate capability deficits from accountability, incentive, tool, process, and "
                  "culture causes",
                  "Trace the problem to an organisational outcome and quantify the gap"],
         must_not=["Start designing the course immediately",
                   "Promise the training will cut the error rate"],
         cov=["P148", "P187", "P191", "P192", "P075"]),
    dict(test_id="GT-004", mode="review",
         desc="Positive routing — assessment scheme graded on a curve with hidden criteria",
         prompt="Review our assessment scheme. We grade on a curve, the criteria live in the "
                "marker's head, and everything rides on one final exam.",
         must_do=["Replace the forced distribution with a standards model judged against public "
                  "criteria",
                  "Require explicit criteria identified before judgment",
                  "Gather evidence along the way by varied methods rather than one snapshot",
                  "Separate formative from summative purpose and label them unmistakably"],
         must_not=["Assign the grades or set the pass mark for them",
                   "Treat a single exam score as sufficient outcome evidence"],
         cov=["P098", "P017", "P199", "P089", "P167", "P110"]),
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
         cov=["P013", "P117", "P152", "P087", "P140", "P119"]),
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
         cov=["P103", "P108", "P183", "P164", "P166"]),
    dict(test_id="GT-007", mode="advise",
         desc="Positive routing — training delivered but the behaviour is not appearing at work",
         prompt="Everyone passed the training six months ago but we don't see the new procedure "
                "being used on the job. What now?",
         must_do=["Establish with valid posttest evidence that learners could perform every main "
                  "goal performance",
                  "Measure use by degree, frequency, context, and prior use",
                  "Diagnose nonuse across relevance, permission, support, resources, and adaptation "
                  "opportunity",
                  "Triangulate across learners and relevant workplace observers"],
         must_not=["Conclude the training failed without posttest evidence",
                   "Prescribe more training as the default remedy"],
         cov=["P109", "P062", "P069", "P082", "P096"]),
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
              "Whether a capability deficit has been distinguished from accountability, incentive, "
              "tool, process, and culture causes",
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

All eleven sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They are canonical
works on instructional and course design — backward design and assessment for understanding,
constructive alignment and university teaching, integrated course design, the revised taxonomy of
knowledge and cognitive process, systematic instructional design, first principles of instruction,
instructional theory and elaboration sequencing, iterative successive-approximation development, and
the cognitive science of multimedia learning.

## Distillation

Spine: {N_PRINC} promoted principles (P001-P{N_PRINC:03d}; {len(HI_IDS)} high-confidence) over
{len(CLAIM_IDS)} atomic claims, with evidence records and chunk anchors. The {N_PRINC} principles are
partitioned across {len(SKILLS)} skills, each principle owned by exactly one skill; the two
references index and ground them.

## Version History

- **1.0.0** (2026-07-26) — Initial LLM-authored layer over the pre-built distilled spine of 180
  principles from ten sources (*Multimedia Learning* present only as a partial conversion): profile,
  faithfulness report, 13 skills, 2 references, golden + principle-behaviour tests, and the exported
  Claude Code adapter.
- **{VERSION}** ({DATE}) — Source fold-in and full re-author over the rebuilt spine. Two source
  changes: the partial *Multimedia Learning* conversion was replaced by the full text
  (`mayer-multimedia-lea-f516bca0` -> `mayer-multimedia-lea-40e2757d`), and *Instructional-Design
  Theories and Models* (Reigeluth) was added — eleven sources, {N_PRINC} principles, {len(CLAIM_IDS)}
  claims. The map->reduce rebuild renumbered every principle, so the 1.0.0 principle ids do not carry
  over: the {len(SKILLS)}-skill partition, every inline citation in `quality_bar`,
  `forbidden_behaviours`, `handoff_rules`, `source_of_truth_policy.precedence`, the examples, the
  faithfulness report, and both test suites were re-derived against the new P001-P{N_PRINC:03d}
  numbering. No 1.0.0 profile decision was silently overwritten — the role, boundary, mode set, and
  skill partition survive; only their grounding ids and the sequencing/instructional-theory coverage
  contributed by the new sources changed.
"""
    w(BASE / "provenance-ledger.md", md)


def emit_changelog() -> None:
    md = f"""# Changelog — {SLUG}

All notable changes to this generated subagent package are recorded here. Versions follow the
`agent_version` field in `profile.yaml`.

## [{VERSION}] — {DATE}

### Added
- *Instructional-Design Theories and Models: A New Paradigm of Instructional Theory / In Action*
  (Reigeluth, ed.) folded in as an eleventh source, adding instructional-theory selection
  (prescribe a method together with the situation it fits) and elaboration sequencing (the
  epitome -> elaborate -> synthesize zoom-lens cycle).

### Changed
- *Multimedia Learning* (Mayer) re-ingested from the full text, replacing the partial conversion
  (`mayer-multimedia-lea-f516bca0` -> `mayer-multimedia-lea-40e2757d`); the multimedia principles no
  longer lean on *e-Learning and the Science of Instruction* to cover Mayer's own material.
- Distilled spine rebuilt over the eleven sources: {N_PRINC} principles (was 180) over
  {len(CLAIM_IDS)} claims (was 6851). The rebuild renumbered every principle.
- LLM-authored layer fully re-derived against the new P001-P{N_PRINC:03d} numbering — the
  {len(SKILLS)}-skill partition, `profile.yaml` (quality bar, forbidden behaviours, handoff rules,
  precedence, examples, `knowledge_partition.always_on`), `reports/faithfulness-report.yaml`, all
  {len(SKILLS)} skills, both references, `tests/golden-tests.yaml`, and
  `tests/principle-behaviour-tests.yaml` ({N_PRINC} tests, one per principle). The 1.0.0 principle
  ids do not carry over.
- Claude Code adapter re-exported to `adapters/claude-code/` and reinstalled under
  `.claude/agents/generated/`.

### Fixed
- `sources/metadata/*.metadata.json`: `source_type` written as `md` by the rebuild, which is not a
  member of the `source-metadata-v1` enum; normalised back to `markdown`.

## [1.0.0] — 2026-07-26

### Added
- Initial release of the **{SLUG}** subagent (Tier 2), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (180 principles / 6851 claims from ten
  distillation-only sources).
- `profile.yaml` derived from the promoted principles: role, router description,
  when/when-not-to-use, three modes (advise / review / plan), quality bar, forbidden behaviours,
  handoff rules, and a {len(SKILLS)}-skill / {len(REFS)}-reference `knowledge_partition` covering
  every principle exactly once.
- {len(SKILLS)} authored skills; {len(REFS)} references (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` and `tests/principle-behaviour-tests.yaml`.
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Eleven distillation-only sources: *Understanding by Design* (Wiggins & McTighe, 2005); *Teaching
  for Quality Learning at University* (Biggs & Tang, 2011); *Creating Significant Learning
  Experiences* (Fink, 2013); *A Taxonomy for Learning, Teaching, and Assessing* (Anderson &
  Krathwohl, 2001); *Principles of Instructional Design* (Gagné, Briggs & Wager, 1992); *First
  Principles of Instruction* (Merrill, 2002); *The Systematic Design of Instruction* (Dick, Carey &
  Carey, 2015); *Leaving ADDIE for SAM* (Allen, 2012); *Multimedia Learning* (Mayer, 2009);
  *e-Learning and the Science of Instruction* (Clark & Mayer, 2016); and *Instructional-Design
  Theories and Models* (Reigeluth, ed., 1999).
"""
    w(BASE / "CHANGELOG.md", md)


def fix_metadata() -> None:
    """The map->reduce rebuild writes source_type: 'md', which is not in the source-metadata-v1
    enum (it wants 'markdown'). Normalise before validation."""
    mdir = BASE / "sources" / "metadata"
    for mf in sorted(mdir.glob("*.metadata.json")):
        data = json.loads(mf.read_text())
        if data.get("source_type") == "md":
            data["source_type"] = "markdown"
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
