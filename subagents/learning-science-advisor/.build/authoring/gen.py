"""Deterministic authoring generator for learning-science-advisor.

Reads the already-assembled, deterministically-valid distilled spine
(principles/principles.yaml + analysis/claims.jsonl + evidence + anchors) and emits the
LLM-authored layer: profile.yaml, references/*, skills/*, tests/*, reports/faithfulness-report.yaml,
provenance-ledger.md, CHANGELOG.md. Every emitted id resolves into the spine.

Cloned from the research-career-advisor sibling generator (same recipe: one deterministic pass
over a pre-built Tier-2 spine). Run:  python3 .build/authoring/gen.py
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parents[2]  # subagents/learning-science-advisor
SLUG = "learning-science-advisor"
DISPLAY = "Learning Science Advisor"
VERSION = "1.0.0"
DATE = "2026-07-26"

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
MANIFEST = yaml.safe_load((BASE / "source-pack.manifest.yaml").read_text())


def pids(n: int) -> str:
    return f"P{n:03d}"


# ---------------------------------------------------------------------------- partition
# Each entry: (skill-slug (kebab, <=48 chars), [principle numbers]).
# Every principle 1..150 appears exactly once.
SKILLS: list[tuple[str, list[int]]] = [
    ("retrieval-practice-and-low-stakes-quizzing",
     [14, 26, 34, 50, 54, 59, 60, 66, 92, 107, 127, 135, 138]),
    ("spacing-distributed-practice-and-consolidation",
     [19, 24, 27, 40, 61, 65, 93, 110, 118, 125, 129, 144, 145]),
    ("interleaving-variation-and-discrimination",
     [1, 28, 35, 64, 106, 142]),
    ("elaboration-examples-and-self-explanation",
     [2, 4, 16, 58, 68, 73, 120, 137, 143, 147]),
    ("prior-knowledge-prediction-and-misconceptions",
     [6, 25, 42, 43, 78, 98, 100, 114, 150]),
    ("cognitive-load-worked-examples-and-scaffolding",
     [3, 12, 21, 47, 63, 67, 101, 112, 113, 121, 136, 149]),
    ("metacognition-study-habits-and-self-regulation",
     [13, 15, 32, 41, 48, 49, 71, 76, 85, 90, 126, 133, 148]),
    ("motivation-belonging-and-classroom-climate",
     [22, 23, 37, 38, 57, 69, 70, 79, 80, 94, 96, 139, 140, 141]),
    ("feedback-assessment-and-error-correction",
     [29, 31, 36, 51, 88, 91, 99]),
    ("evidence-appraisal-and-learning-myths",
     [7, 11, 17, 20, 33, 44, 53, 72, 74, 84, 103, 105, 109, 130]),
    ("expertise-development-and-transfer",
     [5, 9, 18, 39, 104, 108, 117, 122, 128, 131]),
    ("memory-mnemonics-and-recall-accuracy",
     [8, 45, 46, 116, 119]),
    ("course-design-technology-and-online-teaching",
     [10, 30, 52, 56, 62, 77, 81, 82, 83, 89, 102, 111, 123]),
    ("development-diversity-and-individual-differences",
     [87, 115, 124, 132, 134, 146]),
    ("collaborative-and-peer-learning",
     [55, 75, 86, 95, 97]),
]

# integrity: every principle exactly once
_seen: list[int] = []
for _slug, _nums in SKILLS:
    _seen += _nums
assert sorted(_seen) == list(range(1, N_PRINC + 1)), (
    f"partition mismatch; missing={sorted(set(range(1, N_PRINC + 1)) - set(_seen))} "
    f"dupes={sorted(n for n in set(_seen) if _seen.count(n) > 1)}")
assert len(set(s for s, _ in SKILLS)) == len(SKILLS), "duplicate skill slug"
for s, _ in SKILLS:
    assert len(s) <= 48, f"slug too long ({len(s)}): {s}"

REFS = [
    "learning-science-principles-index",
    "learning-science-evidence-notes",
]
for r in REFS:
    assert len(r) <= 48, f"ref name too long ({len(r)}): {r}"

PID_TO_SKILL = {pids(n): slug for slug, nums in SKILLS for n in nums}

# ---------------------------------------------------------------------------- per-skill themes
THEMES: dict[str, dict] = {
    "retrieval-practice-and-low-stakes-quizzing": dict(
        title="Retrieval Practice And Low-Stakes Quizzing",
        purpose=(
            "This skill designs and reviews retrieval practice — bringing knowledge back to mind "
            "rather than reviewing it. It prefers successful retrieval to equivalent restudy for "
            "durable learning, prefers generative recall or short answer to recognition when "
            "learners can produce a meaningful answer, and requires an unaided attempt before the "
            "answer is revealed. It insists that retrieval be paired with an accuracy check "
            "whenever learners cannot verify themselves, because uncorrected retrieval reinforces "
            "confident errors. It builds frequent low- or no-stakes cycles — mini-quizzes sampling "
            "priority items with prompt feedback and return to later practice, closed-resource exit "
            "prompts reviewed before the next meeting, individual observable attempts before peer "
            "or whole-class discussion — and it treats the responses as formative evidence of gaps "
            "and learner calibration. Format matters less than retrieving at all, so it chooses a "
            "sustainable format that still demands meaningful recall."),
        when=[
            "A study or review activity must be converted from rereading into genuine "
            "reconstruction from memory — questions, recall, maps, drawings, or explanation "
            "(P059, P127, P135, P054).",
            "Quizzing is being designed: item selection, recall versus recognition, "
            "multiple-choice alternatives that demand discrimination, and the feedback that "
            "follows (P026, P060, P066).",
            "Learners cannot check their own answers, so an accuracy check must be built in before "
            "errors are reinforced (P050, P107).",
            "Retrieval responses are available and should be used to reveal gaps, improve learner "
            "calibration, and steer the next session (P014, P034, P092, P138).",
        ],
        input="The activity, quiz, assignment, or study routine under review, plus who the learners "
              "are, what they must retain, and how their answers get checked."),
    "spacing-distributed-practice-and-consolidation": dict(
        title="Spacing, Distributed Practice And Consolidation",
        purpose=(
            "This skill schedules practice over time. It treats distributed practice as a "
            "high-utility default across ages, materials, and retention periods while preserving "
            "uncertainty for complex structured learning and higher-order outcomes; it sets the gap "
            "in relation to the desired retention horizon, using roughly one tenth to one fifth of "
            "that horizon as a provisional planning heuristic adjusted for deadlines and retrieval "
            "success. It repeats retrieval across intervals that permit some forgetting while "
            "keeping each attempt challenging but recoverable, revisits missed items sooner, "
            "expands intervals after success, and retains occasional long-interval checks. It makes "
            "prior learning recur across assignments, quizzes, and major exams instead of reserving "
            "cumulative retrieval for the final, keeps that cumulative load sustainable through a "
            "pruned reusable pool sampled rather than exhausted, and protects consolidation time — "
            "including sleep — rather than treating polished rapid repetitions as durable learning."),
        when=[
            "A revision, review, or homework schedule must be planned: when to start, how long the "
            "gaps should be, and how old material re-enters later sessions (P040, P061, P065, "
            "P125).",
            "Retrieval attempts must be scheduled adaptively — missed items sooner, successful "
            "items at expanding intervals, important material re-checked at long intervals (P110, "
            "P118, P144).",
            "Cumulative assessment is being designed and must stay sustainable for both learners "
            "and the person marking it (P027, P093, P129).",
            "Cramming, sleep loss, or massed rapid repetition is being relied on, or knowledge must "
            "be linked across episodes, contexts, and representations with consolidation between "
            "encounters (P019, P024, P145).",
        ],
        input="The syllabus, revision plan, or assessment calendar, the retention horizon that "
              "matters, and the time actually available to learners."),
    "interleaving-variation-and-discrimination": dict(
        title="Interleaving, Variation And Discrimination",
        purpose=(
            "This skill sequences practice so learners can tell related things apart and choose "
            "among them. It uses interleaved rather than blocked practice when learners must "
            "discriminate related categories or select among problem-solving strategies, and judges "
            "it by delayed discrimination and transfer rather than by fluency during practice. It "
            "introduces each new type with focused instruction and enough blocked practice for "
            "basic competence, then mixes it cumulatively with the previously learned types it must "
            "be distinguished from. It varies practice by shuffling relevant items, order, starting "
            "conditions, and contingencies, and practises applicability directly — mixed plausible "
            "problem types and contexts, context-to-skill and skill-to-context matching, option "
            "trade-offs, counterfactual variation — so learners must diagnose the situation, choose "
            "a strategy, and adapt it. It also recognises the opposite case: blocking can help when "
            "the immediate challenge is discovering common structure among dissimilar members of "
            "one category."),
        when=[
            "Learners can execute procedures but pick the wrong one, or confuse related categories, "
            "formulas, or problem types (P028, P142, P035).",
            "A new type or method is being introduced and the transition from focused blocked "
            "practice to cumulative mixing must be timed (P001, P064).",
            "Practice is too uniform — same items, same order, same starting conditions — to "
            "prepare learners for varied real demands (P106).",
            "Practice fluency looks good but delayed discrimination or transfer is the actual goal "
            "being claimed (P142, P035).",
        ],
        input="The practice set or problem sequence, the categories or strategies learners must "
              "discriminate, and how mastery will be measured and when."),
    "elaboration-examples-and-self-explanation": dict(
        title="Elaboration, Examples And Self-Explanation",
        purpose=(
            "This skill deepens processing by making learners build and articulate structure. It "
            "prompts learners to explain each problem-solving step so reasoning itself becomes an "
            "object of learning, and treats self-explanation as a broadly applicable, "
            "moderate-utility technique for memory, comprehension, inference, application, and near "
            "transfer while keeping far transfer, durability, classroom generality, and learner "
            "moderators explicitly uncertain. It has learners generate their own connections to "
            "prior cases, knowledge, and uses — cueing at first, then fading the prompts — rather "
            "than only receiving instructor-made connections. It makes meaningful relationships and "
            "organizational principles an explicit object of activity instead of assuming novices "
            "will infer expert structure, directs attention to the relation examples share, "
            "provides enough varied examples and side-by-side comparison for the abstraction to "
            "travel beyond the first case, and combines verbal and visual representations when both "
            "add relevant information, favouring accurate simple sketches over decorative artistry."),
        when=[
            "Learners can state facts but cannot explain why, or produce answers without exposing "
            "the reasoning behind them (P058, P143, P147).",
            "New content must be connected to prior knowledge, examples, or uses, and the "
            "connections should be learner-generated rather than supplied (P068, P120).",
            "An abstraction, rule, or relational structure must transfer beyond the example it was "
            "taught with (P004, P016, P002).",
            "Material is being organised or represented — key ideas, governing rules, concept maps, "
            "diagrams paired with text (P137, P073).",
        ],
        input="The content or explanation being taught, the examples currently used, and what "
              "learners are expected to do with the idea afterwards."),
    "prior-knowledge-prediction-and-misconceptions": dict(
        title="Prior Knowledge, Prediction And Misconceptions",
        purpose=(
            "This skill opens learning by surfacing what learners already believe and using it. It "
            "requires a brief prediction, attempted answer, problem solution, or skill trial before "
            "formal instruction, and structures prediction as a complete cycle: a reasoned "
            "commitment first, corrective content promptly, then reflection that revises the mental "
            "model. It uses predictions and pretests to diagnose prior knowledge, misconceptions, "
            "expected assessment demands, and mismatched study strategies before substantial "
            "instruction, and it probes emotional and cultural context, learner questions, and "
            "interpretations rather than assuming a shared presentation produced shared "
            "understanding. It corrects persistent misconceptions refutationally — leading with the "
            "accurate account, naming the misconception briefly, explaining its failure with "
            "evidence, and inoculating against the misleading arguments that will recur — and, "
            "where a model must be rebuilt, elicits the learner's current model as a prediction, "
            "tests it so the discrepancy and its failed assumptions become visible, then has the "
            "learner justify a more adequate alternative. It opens with a relevant stimulus and "
            "asks what learners notice and wonder, and connects new material to meaningful "
            "classifications, language roots, and repeated use so it can consolidate. Where a "
            "school or programme team designs what a reading-difficulty assessment or "
            "intervention screens for, it recommends that real-word reading, spelling ability, "
            "and word attack skills be among the measures collected."),
        when=[
            "A unit, lesson, or module is being opened and prior knowledge, curiosity, and "
            "prediction should do work before content is delivered (P025, P098, P114).",
            "Learners hold a persistent wrong model that survives ordinary explanation (P043, "
            "P078).",
            "Instruction is being planned without knowing what learners already know, expect, or "
            "misread — including cultural and emotional context (P042, P150).",
            "A school or programme team is deciding what a reading-difficulty assessment or "
            "intervention should screen for (P100).",
            "New terminology or classification must be connected to what learners already have so "
            "it consolidates into an adaptable model (P006).",
        ],
        input="The topic and its known misconceptions, the learners' likely starting point, and how "
              "the opening of the session or module is currently structured."),
    "cognitive-load-worked-examples-and-scaffolding": dict(
        title="Cognitive Load, Worked Examples And Scaffolding",
        purpose=(
            "This skill manages the limited working memory a learner brings to a task. It accounts "
            "for the cost of transient information — keeping essential state visible and pacing "
            "multistep work so learners need not hold and integrate more elements than working "
            "memory supports — and organizes elements into meaningful chunks grounded in prior "
            "knowledge, without assuming domain-specific memory-span training generalises. It uses "
            "worked examples, a problem statement plus the steps to its solution, so attention goes "
            "to the process rather than only the answer, scaffolds with models, think-alouds, "
            "prompts, checklists, and exemplars, coaches performance and fades support as "
            "competence grows while restoring it for exceptional difficulty, and teaches complex "
            "performance in manageable layers with early achievable component practice and process "
            "feedback before harder attempts. It builds reliable memory for prerequisite facts, "
            "concepts, and procedures rather than treating memory and higher-order learning as "
            "competing goals, practises stable recurring prerequisites toward automaticity, and "
            "verifies learners can retrieve what an inquiry task requires before demanding it. "
            "Difficulty is introduced only when the struggle is surmountable, relevant to the "
            "target, aligned with current knowledge, and supported by a viable path to progress."),
        when=[
            "Learners stall, overload, or lose the thread on multistep tasks, or must hold too much "
            "at once (P047, P063, P113).",
            "A hard procedure or genre must be taught: worked examples, models, think-alouds, "
            "checklists, and the plan for fading them (P101, P067, P112).",
            "Inquiry, critical analysis, or problem solving is being assigned before the "
            "prerequisite knowledge is reliably retrievable (P012, P136, P003).",
            "A task is being made deliberately harder and it must be checked that the difficulty is "
            "surmountable, on-target, and supported rather than merely painful (P021, P149, P121).",
        ],
        input="The task or lesson as currently set, the prerequisite knowledge learners actually "
              "hold, and the support materials available."),
    "metacognition-study-habits-and-self-regulation": dict(
        title="Metacognition, Study Habits And Self-Regulation",
        purpose=(
            "This skill develops learners who can steer their own learning and judge it accurately. "
            "It judges study methods by delayed performance rather than immediate confidence, "
            "familiarity, or ease, and designs for durable, independently retrievable capability "
            "rather than fluent practice performance. It calibrates self-directed learning with "
            "domain-specific criteria, unaided retrieval, contextual performance, external "
            "feedback, and objective stopping rules, and teaches effective learning strategies "
            "alongside domain content so learners know what works, when and how to use it, and how "
            "it depends on the knowledge they already have. It builds self-regulation through "
            "meaningful goals, capacity-matched challenges, targeted feedback, metacognitive "
            "prompts, and genuine responsibility for monitoring progress; makes planning explicit "
            "for complex tasks and transfers it to learner-created plans; makes otherwise invisible "
            "reasoning inspectable through annotations, process logs, or think-alouds; and "
            "structures reflection as a reconstruction of what happened, the connections and "
            "outcomes involved, and a specific adjustment to test next. It diagnoses a missing "
            "study routine as an unformed habit and a transfer barrier — setup cost, competing "
            "intermittent rewards — not as a moral failing, and follows up on whether the study "
            "actually happened, with what strategy and attention, and what to change."),
        when=[
            "Learners study hard but ineffectively, or feel confident and then perform badly (P126, "
            "P085, P015).",
            "Study strategies themselves must be taught and made portable rather than assumed "
            "(P071, P148, P013).",
            "A study routine must be established, followed up, or repaired, at home or "
            "independently (P076, P090, P041).",
            "Learners must plan, monitor, reflect on, and adjust their own work on complex tasks "
            "(P133, P048, P032, P049).",
        ],
        input="How the learner currently studies or plans, what evidence exists about whether it "
              "works, and the delayed outcome that actually matters."),
    "motivation-belonging-and-classroom-climate": dict(
        title="Motivation, Belonging And Classroom Climate",
        purpose=(
            "This skill diagnoses and supports the motivational and social conditions learning "
            "needs. It treats motivation across three interacting dimensions — the value placed on "
            "the work, the expectation of success, and the perceived supportiveness of the "
            "environment — and targets whichever is actually limiting engagement, treating "
            "motivation and ability beliefs as changeable interpretations shaped by structures, "
            "relationships, feedback, and experience rather than fixed traits. It raises value by "
            "connecting rigorous work to important issues, authentic consequences, and future use; "
            "builds expectancy through genuine challenges that appear attainable, scaffolded early "
            "success, and outcome framing in terms of controllable strategy, preparation, and "
            "effort with concrete alternatives after failure; and supports persistence with "
            "strategy trials, help-seeking, and improved course conditions rather than effort "
            "praise or mindset language alone. It treats belonging as part of instructional "
            "responsibility because isolation, threat, and persistent doubt consume the resources "
            "learning needs, monitors interaction for exclusion or derogation while preserving "
            "safely facilitated disagreement, and treats stereotype threat as a situational "
            "interaction to be reduced by auditing framing, examples, differential treatment, and "
            "cues — not as a learner deficit. It watches for performance orientation shrinking "
            "challenge, uses small external rewards cautiously and only for initially low-interest "
            "tasks, and keeps policies and negative feedback task-focused and non-demeaning."),
        when=[
            "Learners disengage, avoid challenge, or give up, and the limiting factor — value, "
            "expected success, or perceived support — must be identified (P140, P057, P037).",
            "Belonging, exclusion, identity threat, or an unsafe climate is affecting who can "
            "participate and learn (P070, P069, P023, P141).",
            "Feedback, grading policy, or failure is being communicated and the framing will shape "
            "what learners conclude about themselves (P022, P080, P094).",
            "Incentives, rewards, or 'make it relevant' interventions are being designed (P096, "
            "P079, P038, P139).",
        ],
        input="What learners are actually doing or avoiding, how the task and policies are framed "
              "for them, and what the climate and interactions look like in practice."),
    "feedback-assessment-and-error-correction": dict(
        title="Feedback, Assessment And Error Correction",
        purpose=(
            "This skill makes feedback and assessment do instructional work. It understands "
            "feedback's purpose as reducing the discrepancy between current understanding and the "
            "learning intention, with the strategy depending on which level it operates at, and "
            "requires feedback to give information about the task or the learning process that "
            "fills that gap rather than merely reporting correctness. It returns targeted feedback "
            "while learners can still apply it to related work, treating a grade alone as "
            "insufficient wherever further development is possible. It builds task-specific "
            "analytic rubrics that separate consequential components, reflect their intended "
            "weight, and expose class-wide as well as individual priorities. It supervises early "
            "practice closely enough to observe performance, interrupt error before it becomes "
            "entrenched, and give milestone feedback that prevents costly drift — unless "
            "independent error detection and repair are themselves the target, in which case it "
            "delays the intervention. It permits recoverable errors, corrects them promptly, and "
            "teaches learners to read struggle and failure as diagnostic information for the next "
            "attempt; and it supports problem solving with the least help needed — root-cause "
            "questions, learner-generated options, consequence analysis, visible progress — so the "
            "learner keeps ownership of the resolution."),
        when=[
            "Feedback is being designed or reviewed: what it says, which level it addresses, and "
            "whether it closes the gap or only reports a score (P051, P088, P099).",
            "A rubric or marking scheme must separate what actually matters and weight it (P036).",
            "Learners are practising a skill early and error is at risk of becoming entrenched — or "
            "self-correction is itself the goal (P091, P031).",
            "A learner is stuck and help must be sized so it enables rather than performs the work "
            "(P029).",
        ],
        input="The assignment or performance, the feedback or rubric currently given, and when "
              "learners next get to apply it."),
    "evidence-appraisal-and-learning-myths": dict(
        title="Evidence Appraisal And Learning Myths",
        purpose=(
            "This skill judges whether a claimed learning technique is actually supported. It "
            "selects teaching and study methods from empirical evidence rather than intuition, "
            "isolated successes, untested theory, or interested marketing, and revises the choice "
            "as evidence changes. It evaluates a technique across learning conditions, learner "
            "characteristics, material types, immediate and delayed outcomes, comprehension, "
            "application, and transfer before treating it as broadly useful, and reads a low or "
            "moderate utility rating as a limit on general use rather than proof of no valid niche. "
            "It defaults to practice testing and distributed practice as the broadly applicable "
            "techniques and replaces highlighting or rereading as primary methods when a stronger "
            "technique targets the same goal and is feasible. It refuses the recurring myths: it "
            "does not organise differentiated instruction around learning-style categories absent "
            "evidence of a stable crossover, does not prescribe preference-matched visual or verbal "
            "instruction, does not classify learners by left-brain/right-brain stereotypes, and "
            "does not map fine-grained brain findings onto instruction without an established "
            "cognitive bridge; presentation modality is chosen because it represents the content "
            "well, with accessibility accommodations provided on their own footing. It holds narrow "
            "or fast-fading techniques to their real limits, requires objective improvement on "
            "untrained outcomes before a far-transfer claim, and flags untested arguments as "
            "untested. Where the support offered for a technique is recollection — what people "
            "remember happening, or their agreement in recalling it — it does not infer truth from "
            "familiarity, vividness, confidence, hindsight, or that agreement, and verifies against "
            "independent evidence."),
        when=[
            "A technique, product, or training is being adopted and its evidence base must be "
            "appraised (P053, P007, P072, P020).",
            "Learning styles, modality matching, or left/right-brain claims are driving an "
            "instructional decision (P011, P044, P103, P074, P017).",
            "A brain-based, far-transfer, or 'works for everything' claim is being made (P033, "
            "P039, P105).",
            "A technique's advertised benefit must be checked against its actual scope and "
            "durability, or the support offered for it is recollection and reported agreement "
            "rather than independent evidence (P084, P130, P109).",
        ],
        input="The claim, product, or practice being proposed, the evidence offered for it, and the "
              "outcome it is supposed to improve."),
    "expertise-development-and-transfer": dict(
        title="Expertise Development And Transfer",
        purpose=(
            "This skill builds competence over the long run and checks that it travels. It matches "
            "support and practice to expertise — beginning novices with concrete representations, "
            "worked examples, blocked practice, and close spacing, then fading toward abstraction, "
            "independent problems, self-explanation, interleaving, and wider spacing as knowledge "
            "grows — and builds expertise through goal-directed practice on current weaknesses, "
            "accurate feedback, repeated diagnosis, and coaching rather than undirected repetition "
            "or an hours threshold. It treats capability as developable through focus, sustained "
            "practice, learned mental models, and environmental support while respecting biological "
            "and individual limits. For complex performance it diagnoses difficult components "
            "slowly, rehearses them from natural cues in multiple coordinated representations, and "
            "reintegrates them into the whole; for perceptual and motor expertise it uses extensive "
            "performance, rapid discriminations, immediate feedback, and juxtaposed near-contrast "
            "cases rather than explanation alone; and it uses hands-on or simulated practice that "
            "reproduces complete field decisions and action sequences, debriefing cues, choices, "
            "constraints, outcomes, and justification. It teaches the applicability boundaries of "
            "specialized meanings, conventions, and analogies as explicitly as their useful "
            "correspondences, requires objective improvement on untrained outcomes before accepting "
            "far transfer, and assesses analytical, creative, and practical competence and "
            "context-developed expertise rather than inferring everything from one static score."),
        when=[
            "A practice regime or curriculum must carry learners from novice to competent, and "
            "supports must be matched and faded (P009, P005, P108).",
            "A complex physical, perceptual, or professional performance must be trained and "
            "debriefed (P018, P131, P117, P104).",
            "A transfer claim is being made, or an analogy or convention is being used outside "
            "where it holds (P039, P122).",
            "Competence is being assessed or diagnosed (P128).",
        ],
        input="The target performance and current level, the practice and feedback available, and "
              "the setting the capability must eventually work in."),
    "memory-mnemonics-and-recall-accuracy": dict(
        title="Memory, Mnemonics And Recall Accuracy",
        purpose=(
            "This skill handles the memory layer directly: how large bodies of information are "
            "organised for retrieval, and how far a recollection can be trusted. It uses practiced "
            "mnemonic cue systems to organize and retrieve large bodies of information while "
            "assessing conceptual mastery separately, treats those cues as a practiced bridge from "
            "initial understanding to fluent whole-pattern performance rather than an effortless "
            "substitute for either, and — after material has been understood and synthesized into "
            "key ideas — attaches each idea to a distinctive cue within a stable, familiar ordered "
            "structure. It diagnoses an apparent memory failure by distinguishing absent attention, "
            "failed encoding, storage loss, and retrieval failure before choosing a remedy, so the "
            "fix matches the actual breakdown. Where a recollection carries consequences, it uses "
            "neutral prompts, preserves uncertainty and the source of each piece of information, "
            "and avoids leading wording or repeated imagination."),
        when=[
            "A large ordered body of material — terminology, sequences, taxonomies — must be made "
            "reliably retrievable (P008, P119, P116).",
            "Someone 'can't remember' and the remedy depends on which stage actually failed (P046).",
            "A recollection is being elicited where accuracy matters and the questioning itself "
            "could distort it (P045).",
            "A mnemonic system is being mistaken for conceptual mastery, or for an effortless "
            "shortcut around understanding (P008, P116).",
        ],
        input="The material or recollection at issue, how it is currently cued or elicited, and "
              "what depends on it being accurate."),
    "course-design-technology-and-online-teaching": dict(
        title="Course Design, Technology And Online Teaching",
        purpose=(
            "This skill designs the course-level container. It starts from substantive, "
            "demonstrable outcomes describing what learners should retain and use and plans "
            "backward, requires the curriculum to address how a common conception of progress is "
            "built across years rather than leaving each teacher to invent one, and builds "
            "high-structure courses: published objectives, required preparation and pre-result "
            "generation, quizzed foundations, learner-built explanations and integrative problems, "
            "and study revised from practice-test errors. It applies universal design as the "
            "default — flexible, intuitive, perceptible, low-effort, error-tolerant access built in "
            "from the start, foreseeable barriers removed, participation options added "
            "incrementally, individual accommodation still retained. It starts technology selection "
            "from the learning purpose and required level of thinking and then chooses the simplest "
            "tool whose stable pedagogical functions meet the need, synthesizes technology evidence "
            "by feature, goal, learner, task, context, access, and timing rather than by ranking "
            "tool categories, and judges distance and blended programmes by instructional design "
            "and the quality of interaction with peers and instructors rather than by delivery "
            "mode, adding in-person or study support where self-regulation is lacking. It makes "
            "instructor presence visible through frequent, useful, personal interactions and "
            "purpose-driven announcements organised into sustainable routines, uses brief "
            "objective-focused reflection early, periodically, and at close, translates a general "
            "principle through its mechanism before adapting it to local learners, format, "
            "workload, and institution, treats personal educational experience as context rather "
            "than proof, builds two-way research–practice partnership, and protects teaching "
            "vitality through peers, network, and continued review of evidence."),
        when=[
            "A course, module, or curriculum is being designed or revised from its outcomes "
            "(P089, P102, P111).",
            "A tool, platform, or online/blended format is being chosen or evaluated (P030, P083, "
            "P062).",
            "Access, participation, and accommodation must be built in rather than retrofitted "
            "(P052).",
            "An online or large course needs visible instructor presence, reflection points, and "
            "sustainable routines (P123, P081).",
            "A published research principle must be adapted to this institution, workload, and "
            "cohort, or a teaching practice justified by personal experience alone (P010, P077, "
            "P056, P082).",
        ],
        input="The course or programme as designed, its intended outcomes and delivery mode, and "
              "the real constraints on learners and staff."),
    "development-diversity-and-individual-differences": dict(
        title="Development, Diversity And Individual Differences",
        purpose=(
            "This skill handles who the learners are without converting group patterns into "
            "individual verdicts. It matches expectations and supports responsively to a learner's "
            "emerging competencies and demonstrated developmental readiness, treating timing as "
            "variable rather than a rigid age schedule while still providing supported challenge "
            "and time for growth. It advises protecting developmentally sensitive periods by preventing "
            "severe early deprivation and providing high-quality relational, linguistic, sensory, "
            "and educational input as early as possible, because substantial recovery is possible "
            "but time-sensitive. It designs for older learners from their individual cognitive "
            "profile and retained domain knowledge rather than an average age trend, treating "
            "unfamiliar-domain difficulty and age trends as hypotheses rather than capacity "
            "verdicts, and evaluates aging by function-specific trajectories and individual "
            "context, distinguishing cognitive resources from learning and weighing social "
            "connection, culture, community, and cohort. It treats cultures as changing and "
            "internally diverse, race as social rather than biological, and developmental "
            "benchmarks as context-sensitive rather than universal, and uses group categories only "
            "for bounded population inference — never converting them into individual capacity "
            "judgments — measuring plural cultural systems and socially produced conditions "
            "directly instead."),
        when=[
            "Expectations or supports are being set by age or grade rather than by demonstrated "
            "readiness (P087).",
            "Adult, older, or returning learners are being designed for (P115, P124).",
            "A group statistic — cultural, demographic, or age-based — is being applied to an "
            "individual learner (P134, P132).",
            "Early-childhood conditions, deprivation, or timing of intervention are at issue "
            "(P146).",
        ],
        input="The learner population and what is actually known about individuals in it, the "
              "assumption being made about them, and the decision it would drive."),
    "collaborative-and-peer-learning": dict(
        title="Collaborative And Peer Learning",
        purpose=(
            "This skill makes group work actually produce learning. It imposes structure on peer "
            "learning, since structure is what lets students collectively make and learn from "
            "errors and lets their conversations spell out the goals, learning intentions, and "
            "success criteria. It pairs individual accountability with group rewards and scripts "
            "the session with formal directions for running it, which helps particularly when new "
            "material is organized and elaborated. It trains collaboration explicitly — shared "
            "understanding, role organization, action protocols, constructive disagreement, "
            "monitoring, repair, and safeguards against dominance and nonparticipation — rather "
            "than assuming it. It uses preparation-to-teach and reciprocal teaching to make "
            "learners retrieve, organize, explain, question, clarify, summarize, and predict, and "
            "runs peer instruction as an individual answer, a reasoned peer comparison, a revised "
            "answer, and a whole-class debrief, using the revision evidence to advance or reteach."),
        when=[
            "Group work is unstructured, dominated by a few, or produces no visible learning "
            "(P095, P097, P075).",
            "A discussion or peer-instruction cycle is being designed and needs an individual "
            "commitment before and a debrief after (P055).",
            "Learners should teach, explain, or lead each other through material (P086).",
            "Collaboration itself must be taught rather than assumed as a background skill (P075).",
        ],
        input="The group activity as run, how individual contribution and understanding are made "
              "visible, and what the group work is meant to achieve."),
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


_US = "\x1f"  # unit separator: id <-> statement
_RS = "\x1e"  # record separator: between cited items

CLAIM_STATEMENTS: dict[str, str] = {}
for _line in (BASE / "analysis" / "claims.jsonl").read_text().splitlines():
    _line = _line.strip()
    if _line:
        _rec = json.loads(_line)
        CLAIM_STATEMENTS[_rec["claim_id"]] = _rec.get("statement", "")


def digest(nums: list[int], claims: list[str]) -> str:
    """sha256 over cited principle + claim statements — byte-identical to
    ``tools.subagent_factory.detect_stale._digest``, so a freshly authored body is not
    reported stale (that check compares content digests, not mtimes)."""
    parts: list[str] = []
    for pid in sorted(pids(n) for n in nums):
        parts.append(f"P:{pid}{_US}{P[pid]['statement']}")
    for cid in sorted(str(c) for c in claims):
        parts.append(f"C:{cid}{_US}{CLAIM_STATEMENTS.get(cid, '<MISSING>')}")
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


print(f"principles={N_PRINC} high={len(HI_IDS)} claims={len(CLAIM_IDS)} skills={len(SKILLS)}")

# ============================================================================ EMITTERS

_SRC_LINE = (
    "grounded in twelve distillation-only sources on the science of learning and its classroom "
    "application (Dunlosky et al.'s techniques review; *Make It Stick*; *Understanding How We "
    "Learn*; Rosenshine's *Principles of Instruction*; *How Learning Works*; *Why Don't Students "
    "Like School?*; *Powerful Teaching*; *Small Teaching* and *Small Teaching Online*; Hattie's "
    "*Visible Learning*; the Deans for Impact *Science of Learning*; and the National Academies' "
    "*How People Learn II*)")

# Human-readable source descriptors, keyed by the source_id already in the manifest.
SOURCE_INFO: dict[str, dict] = {
    "dunlosky-2013-improv-13b90eb5": dict(
        title="Improving Students' Learning With Effective Learning Techniques: Promising "
              "Directions From Cognitive and Educational Psychology",
        author="John Dunlosky, Katherine A. Rawson, Elizabeth J. Marsh, Mitchell J. Nathan and "
               "Daniel T. Willingham",
        year=2013),
    "brown-roediger-mcdan-9a1ca554": dict(
        title="Make It Stick: The Science of Successful Learning",
        author="Peter C. Brown, Henry L. Roediger III and Mark A. McDaniel", year=2014),
    "weinstein-sumeracki-5e470598": dict(
        title="Understanding How We Learn: A Visual Guide",
        author="Yana Weinstein and Megan Sumeracki", year=2018),
    "rosenshine-principle-98e74dd1": dict(
        title="Principles of Instruction: Research-Based Strategies That All Teachers Should Know",
        author="Barak Rosenshine", year=2012),
    "ambrose-how-learning-163bde10": dict(
        title="How Learning Works: Seven Research-Based Principles for Smart Teaching",
        author="Susan A. Ambrose, Michael W. Bridges, Michele DiPietro, Marsha C. Lovett and "
               "Marie K. Norman",
        year=2010),
    "willingham-why-dont-61f71765": dict(
        title="Why Don't Students Like School? A Cognitive Scientist Answers Questions About How "
              "the Mind Works and What It Means for the Classroom",
        author="Daniel T. Willingham", year=2009),
    "agarwal-bain-powerfu-5b75ae90": dict(
        title="Powerful Teaching: Unleash the Science of Learning",
        author="Pooja K. Agarwal and Patrice M. Bain", year=2019),
    "lang-small-teaching-1c0df7f4": dict(
        title="Small Teaching: Everyday Lessons from the Science of Learning",
        author="James M. Lang", year=2016),
    "darby-lang-small-tea-84140e5a": dict(
        title="Small Teaching Online: Applying Learning Science in Online Classes",
        author="Flower Darby with James M. Lang", year=2019),
    "hattie-visible-learn-aa5d2ed3": dict(
        title="Visible Learning: A Synthesis of Over 800 Meta-Analyses Relating to Achievement",
        author="John Hattie", year=2008),
    "deans-for-impact-sci-c50ecdcd": dict(
        title="The Science of Learning (2nd edition)",
        author="Deans for Impact", year=2019),
    "nasem-how-people-lea-a3bb4079": dict(
        title="How People Learn II: Learners, Contexts, and Cultures",
        author="National Academies of Sciences, Engineering, and Medicine", year=2018),
}


def build_sources() -> list[dict]:
    out = []
    for s in MANIFEST["sources"]:
        sid = s["source_id"]
        info = SOURCE_INFO[sid]
        out.append(dict(source_id=sid, title=info["title"], author=info["author"],
                        year=info["year"], rights_status="distillation-only",
                        sha256=s["sha256"]))
    return out


SOURCES = build_sources()
assert len(SOURCES) == 12, f"expected 12 sources, got {len(SOURCES)}"


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
        body.append(f"- {th['input']}\n")
        body.append("## Output\n")
        # DRY: the output contract lives once, in the profile (outputs + quality_bar). Restating it
        # verbatim in all 15 skills duplicated the profile and cost context at every invocation.
        body.append(
            "As set by the profile's `outputs` contract and quality bar. Advice only — the "
            "profile's forbidden behaviours and handoff rules govern what this skill will not "
            "do.\n")
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
        # DRY: the 12-source bibliography lives in provenance-ledger.md and the evidence notes.
        body.append(
            f"Derived from {idlist}; full source grounding in `../../provenance-ledger.md` and "
            f"`../../references/{REFS[1]}.md`. The frontmatter `provenance` block lists the exact "
            "principle and claim ids, which resolve into `principles/principles.yaml` and "
            "`analysis/claims.jsonl`.\n")
        w(BASE / "skills" / slug / "SKILL.md", "\n".join(body))


def emit_refs() -> None:
    claims = union_claims([n for _, nums in SKILLS for n in nums], cap=16)
    out = [frontmatter(REFS[0], "reference", list(range(1, N_PRINC + 1)), claims)]
    out.append("# Learning-Science Principles Index\n")
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
    out.append("# Learning-Science Evidence Notes\n")
    out.append("How the principles in this package are grounded, and how to keep advice faithful to "
               "the sources.\n")
    out.append("## Sources\n")
    out.append("Twelve distillation-only sources ground the package, spanning the research reviews, "
               "the trade syntheses that translate them for teachers, and the practitioner "
               "handbooks:\n")
    for s in SOURCES:
        yr = f", {s['year']}" if s["year"] else ""
        out.append(f"- *{s['title']}* — {s['author']}{yr}.")
    out.append("")
    out.append("Paraphrase and restructure only — no verbatim quotation (see "
               "`.claude/rules/rights-and-quotation-policy.md`, enforced by `quote_scan`).\n")
    out.append("## Faithfulness discipline\n")
    out.append("- No advice may state a rule more strongly than its source supports. Several "
               "principles carry their uncertainty in the statement itself — self-explanation's "
               "far transfer, durability, and classroom generality are explicitly uncertain "
               "(P143); distributed practice is a high-utility default but uncertain for complex "
               "structured learning and higher-order outcomes (P125); a low or moderate utility "
               "rating limits general use rather than proving no valid niche (P072). Carry that "
               "hedging through into the advice.")
    out.append("- Effect sizes and utility ratings are reported with their scope, not as universal "
               "rankings: the keyword mnemonic's delayed effect falls to about d = 0.19 (P084), "
               "and modality-matched instruction yields little or no gain (P103). Cite the limit "
               "with the number.")
    out.append("- A technique is evaluated across conditions, learners, materials, and both "
               "immediate and delayed outcomes before being called broadly useful (P007), and a "
               "far-transfer claim requires objective improvement on untrained outcomes (P039). "
               "Arguments the sources flag as untested stay flagged (P105).")
    out.append("- Group-level findings are never converted into individual capacity judgments "
               "(P134, P132), and no principle licenses diagnosing a learner or predicting an "
               "individual outcome.")
    out.append("- The advisor guides practice, it does not perform it: it does not teach the "
               "subject content, deliver the course, or mark the work for the caller (P010, "
               "P077).\n")
    out.append("## Grounding\n")
    out.append(f"Spine: {N_PRINC} principles ({len(HI_IDS)} high-confidence) over {len(CLAIM_IDS)} "
               f"atomic claims, with evidence records and chunk anchors. Every principle id "
               f"P001-P{N_PRINC:03d} resolves into `principles/principles.yaml`.\n")
    w(BASE / "references" / f"{REFS[1]}.md", "\n".join(out))


# A skill may legitimately route on a principle that its one-paragraph always_on purpose never
# restates. Citing it there is a false provenance link — the reader follows the id and lands on an
# unrelated rule. Excluded per (skill, principle); the skill itself keeps the principle.
ALWAYS_ON_EXCLUDE: set[tuple[str, int]] = set()


def _always_on() -> list[str]:
    out = []
    for slug, nums in SKILLS:
        ids = ", ".join(pids(n) for n in nums if (slug, n) not in ALWAYS_ON_EXCLUDE)
        out.append(f"{THEMES[slug]['purpose']} ({ids})")
    return out


# ---------------------------------------------------------------------------- profile content

ROUTER_DESCRIPTION = (
    "Advises on evidence-based learning science and how to apply it: retrieval practice and "
    "low-stakes quizzing, spacing and consolidation, interleaving and varied practice, "
    "elaboration and self-explanation, prior knowledge and misconception repair, cognitive load, "
    "worked examples and scaffolding, metacognition and study habits, motivation, belonging and "
    "climate, feedback and assessment, collaborative learning, course and online design, "
    "expertise and transfer, developmental and individual differences, and appraising a claimed "
    "technique or learning myth against its evidence. Advises and reviews practice; it does not "
    "teach the subject content, deliver the course, write the materials, or mark the work. Not for "
    "diagnosing a learning disability or clinical condition, making a placement, grading, "
    "admission, or employment decision, or subject-matter questions with no learning-design "
    "dimension.")

PROFILE_ROLE = (
    "An advisor on the science of learning and its instructional application, grounded in twelve "
    "distillation-only sources: cognitive-psychology reviews and syntheses (Dunlosky et al., "
    "Hattie, the National Academies, Deans for Impact, Rosenshine) and practitioner translations "
    "(*Make It Stick*, *Understanding How We Learn*, *How Learning Works*, Willingham, *Powerful "
    "Teaching*, *Small Teaching* and *Small Teaching Online*). It serves teachers, instructional "
    "designers, trainers, and self-directed learners deciding how to teach, how to study, or "
    "whether a claimed technique is supported. The invariants below are advisory criteria, not "
    "authority to act: the advice-only boundary and the forbidden behaviours override every one of "
    "them.")

WHEN_TO_USE = [
    "Designing or reviewing how something is taught or practised — lesson, activity, practice set, "
    "revision schedule, course, or online module — for durable, transferable learning rather than "
    "fluent practice performance.",
    "Diagnosing why learning is not sticking: confident learners who then fail, learners who can "
    "execute but not choose, a misconception surviving explanation, or hard but ineffective study.",
    "Judging whether a claimed technique, product, or training is evidence-supported and how far "
    "its benefit extends — including learning-styles, modality-matching, brain-based, and "
    "far-transfer claims.",
    "Designing feedback, quizzing, rubrics, or assessment so they close the gap to the learning "
    "intention instead of only reporting a score.",
    "Working on the conditions around learning — motivation, belonging, climate, group work, "
    "instructor presence, accessibility, and developmental or individual differences.",
]

WHEN_NOT_TO_USE = [
    "The caller wants the teaching performed — content taught, course delivered, materials "
    "written, or work marked; this advisor guides practice, it does not perform it.",
    "The caller wants a learner assessed, diagnosed, or labelled, or an individual capacity "
    "verdict inferred from a group pattern.",
    "The caller wants a placement, grading, admission, promotion, or employment decision made or "
    "predicted, or an outcome for a named individual guaranteed.",
    "The question is about the subject matter itself — what the correct answer is, rather than how "
    "it should be taught, practised, or assessed.",
    "The caller wants a binding ruling on education law, accreditation, safeguarding, or "
    "institutional policy, which requires the responsible authority.",
]

QUALITY_BAR = [
    "Durable learning is judged by delayed retrieval and explanation, never by immediate ease, "
    "fluency, or confidence (P085, P013, P126).",
    "Retrieval is genuine and checked: an unaided attempt precedes the answer, recall is preferred "
    "to recognition where feasible, and an accuracy check is paired with it when learners cannot "
    "verify themselves (P059, P060, P107, P050).",
    "Practice is distributed rather than massed, with the gap set against the retention horizon, "
    "and interleaved when learners must discriminate categories or select strategies (P125, P061, "
    "P142, P028).",
    "Support is matched to expertise and working memory, then faded, with prerequisite knowledge "
    "reliably retrievable before inquiry is demanded (P009, P101, P067, P047, P136).",
    "A technique is adopted from evidence across conditions, learners, materials, and delayed "
    "outcomes — never from intuition, one demonstration, marketing, a learning-style category, or "
    "a brain claim without a cognitive bridge (P053, P007, P011, P103, P033).",
    "Motivation, belonging, and feedback are treated as instructional conditions: the limiting "
    "motivational dimension is identified, climate and identity threat audited, and feedback fills "
    "the gap while it can still be applied (P140, P070, P023, P088, P099).",
]

FORBIDDEN = [
    "Teaching the subject content, delivering the course, writing the materials, or marking the "
    "work for the caller (P010, P077).",
    "Diagnosing a learner, or converting a group-level finding into an individual capacity "
    "judgment (P134, P132, P115).",
    "Making or predicting a placement, grading, admission, promotion, or employment outcome, or "
    "guaranteeing a result for a named learner (P128, P087).",
    "Stating a rule more strongly than its source supports — presenting an uncertain or "
    "moderate-utility technique as settled and universal (P072, P125, P143, P105).",
    "Recommending what the sources do not support — style- or modality-matched instruction, "
    "left/right-brain classification, or far transfer without gains on untrained outcomes (P011, "
    "P103, P074, P039).",
]

HANDOFF = [
    "The teacher, designer, or institution owns the curriculum, materials, delivery, and marks; "
    "this advisor informs the design reasoning and names the residual trade-off (P010, P077).",
    "Assessing or diagnosing an individual learner belongs to a qualified specialist, and "
    "placement, grading, admission, and employment decisions to the responsible body (P134, P128).",
]

PRECEDENCE = (
    "Where a source ties a technique to a purpose, a condition, or the learner's current "
    "knowledge, treat it as an adaptable guide, not an absolute (P072, P010, P009); carry the "
    "source's own hedging through, since several principles state their uncertainty for far "
    "transfer, durability, and complex structured learning (P143, P125, P105). Never turn a "
    "group-level finding into an individual verdict (P134). The advice-only boundary and forbidden "
    "behaviours override every invariant.")

MODES = [
    dict(name="advise",
         trigger="The caller faces a teaching, study, or learning-design decision and wants to "
                 "know which practice applies.",
         output="A recommendation tied to the situation, naming the principle(s), the condition it "
                "depends on, and the residual trade-off."),
    dict(name="review",
         trigger="The caller submits a lesson, course, assessment, study routine, or claimed "
                 "technique for critique.",
         output="A findings list keyed to area, each with the gap, correction, trade-off, and next "
                "step — highest-impact first."),
    dict(name="plan",
         trigger="The caller is building a course, unit, practice schedule, or study routine and "
                 "wants a grounded plan.",
         output="An ordered plan of steps, each tied to its principle and scoped to the retention "
                "horizon and time available."),
]

EXAMPLES = [
    dict(title="Turn a rereading-based revision week into durable practice",
         kind="happy-path",
         scenario=(
             "A teacher says 'my students revise by rereading their notes and highlighting, then "
             "bomb the exam. We have three weeks. What should they do instead?'"),
         ideal_response=(
             "Replace the primary method, keep it feasible. (a) Default to practice testing and "
             "distributed practice, and drop highlighting and rereading as primary methods since a "
             "stronger technique targets the same goal and is feasible here (P020, P059). (b) Make "
             "the revision genuine reconstruction from memory — questions, recall, maps, drawings, "
             "or explanation — with an unaided attempt before any answer is revealed, preferring "
             "short-answer recall to recognition where students can produce a meaningful answer "
             "(P135, P107, P060). (c) Because they cannot reliably check themselves, pair every "
             "retrieval attempt with an accuracy check, or uncorrected retrieval will reinforce "
             "confident errors (P050). (d) Spread it: with a three-week horizon, review after a "
             "modest delay, mix older material into later sessions, revisit missed items sooner "
             "and expand intervals after success, and keep a final review without making it the "
             "only study opportunity (P040, P118, P061). (e) Tell them the trade-off explicitly — "
             "this will feel harder and slower than rereading, and that felt difficulty is why "
             "judging by delayed performance rather than immediate ease matters (P126, P085). You "
             "own the revision plan and the materials; this is the design reasoning behind them.")),
    dict(title="Appraise a learning-styles training purchase",
         kind="happy-path",
         scenario=(
             "An L&D lead asks 'we're buying a platform that assesses each learner's style — "
             "visual, auditory, kinesthetic — and streams content to match. Is that a good "
             "investment?'"),
         ideal_response=(
             "The evidence does not support the mechanism being sold. (a) Do not organize "
             "differentiated instruction around a learning-style category unless evidence shows a "
             "stable crossover in which different methods reliably benefit different groups; that "
             "crossover is what a styles claim requires and it is not established (P011). (b) "
             "Matching instruction to a supposed auditory, visual, or kinesthetic preference "
             "yields little or no gain — around 0.18, 0.09 and 0.18 respectively — and the groups "
             "overlap so heavily that the preferences themselves are doubtful (P103). Preference "
             "is also not outcome evidence: liking a modality does not mean learning more from it "
             "(P044). (c) Choose visual, auditory, or physical presentation because it represents "
             "the target content well, and provide learner-specific accessibility accommodations "
             "on their own footing rather than as style matching (P017, P052). (d) Redirect the "
             "budget toward what does transfer across conditions: practice testing and distributed "
             "practice as defaults, with the platform judged by feature, goal, learner, task, "
             "context, access, and timing rather than by category (P020, P083, P030). Correction: "
             "if the vendor claims a styles effect, ask for delayed outcome data showing the "
             "crossover. The purchase decision stays with you.")),
    dict(title="Decline to diagnose a struggling learner and redirect to design",
         kind="failure-recovery",
         scenario=(
             "A parent writes 'my son can't remember anything he studies and gets distracted — "
             "does he have a learning disability? Tell me what he has and I'll act on it.'"),
         ideal_response=(
             "Decline the diagnosis — assessing or labelling an individual learner is outside this "
             "advisor's remit and belongs to a qualified specialist, and a group-level finding must "
             "never become an individual capacity verdict (forbidden behaviours, P134). What can be "
             "done is to diagnose the *study design*, not the child. (a) Distinguish what actually "
             "failed: absent attention, failed encoding, storage loss, or retrieval failure, since "
             "each has a different remedy (P046). (b) Check whether the material is ever retrieved "
             "at all, or only reread — genuine reconstruction from memory is what makes knowledge "
             "durable and flexible (P135, P059). (c) Treat a missing routine as an unformed habit "
             "and a transfer barrier — setup cost, competing intermittent rewards — rather than a "
             "personal or moral failure, and build an age-appropriate recurring routine at home "
             "that retrieves recent and older learning and adds or removes cues according to "
             "success (P076, P041). (d) Follow up on whether the study actually happened, with "
             "what strategy and attention level, and revise the schedule rather than repeating it "
             "(P090). If concerns persist after the routine changes, take them to the school and a "
             "qualified assessor — that referral, not a label from here, is the next step.")),
]


def emit_profile() -> None:
    profile = {
        "schema_version": "portable-profile-v1",
        "slug": SLUG,
        "display_name": DISPLAY,
        "agent_version": VERSION,
        "status": "ready",
        "tier": 2,
        "multisource_synthesis": "deferred",
        "router_description": ROUTER_DESCRIPTION,
        "role": PROFILE_ROLE,
        "when_to_use": WHEN_TO_USE,
        "when_not_to_use": WHEN_NOT_TO_USE,
        "inputs": {"required": [
            "The lesson, course, assessment, study routine, or claimed technique under discussion, "
            "plus who the learners are, what they must be able to do afterwards, and the time and "
            "support available."]},
        "outputs": {
            "primary_format": (
                "A structured recommendation or review that, per finding, names the gap and the "
                "principle it engages, gives the correction, and states the condition or residual "
                "trade-off — never a bare verdict, a diagnosis, or the taught content."),
            "modes": MODES,
        },
        "quality_bar": QUALITY_BAR,
        "minimum_useful_output": (
            "At least one finding that names a learning or teaching practice, ties it to a named "
            "principle, and states the condition it depends on or the residual trade-off."),
        "forbidden_behaviours": FORBIDDEN,
        "handoff_rules": HANDOFF,
        "source_of_truth_policy": {
            "canonical_owner": (
                "The teacher, instructional designer, or institution holds final authority over "
                "the curriculum, the materials, the delivery, and the marks; qualified specialists "
                "over the assessment or diagnosis of an individual learner; and the responsible "
                "body over placement, grading, admission, and employment decisions. The distilled "
                "principles from the twelve sources are the authority for the advisory criteria "
                "the advisor invokes."),
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

    qb_ids = ["P085/P013/P126", "P059/P060/P107/P050", "P125/P061/P142/P028",
              "P009/P101/P067/P047/P136", "P053/P007/P011/P103/P033",
              "P140/P070/P023/P088/P099"]
    qb_notes = [
        "Durability judged on delayed evidence; the principles state the delayed-measure "
        "requirement directly.",
        "Retrieval conditions restated with their own qualifiers (recall 'where feasible', "
        "accuracy check 'when learners cannot verify themselves').",
        "P125's high-utility default keeps its stated uncertainty for complex structured learning "
        "and higher-order outcomes; the spacing ratio stays a provisional heuristic (P061).",
        "Expertise-matched support and load management, each conditioned as in source.",
        "Evidence-appraisal criteria and the three refused myths, each stated as the principles "
        "state them.",
        "Motivational and feedback conditions restated as instructional responsibilities, not "
        "learner traits.",
    ]
    for i, ids in enumerate(qb_ids):
        add(f"quality_bar[{i}]", ids, qb_notes[i])

    fb_ids = ["P010/P077", "P134/P132/P115", "P128/P087", "P072/P125/P143/P105",
              "P011/P103/P074/P039"]
    fb_notes = [
        "Boundary restraint; the advisor adapts principles to a local setting rather than "
        "performing the teaching.",
        "Group-to-individual inference is prohibited by P134 explicitly; no strengthening.",
        "Boundary restraint on individual outcome prediction; P128 refuses inferring total "
        "competence from one static score.",
        "Anti-over-claim rule; each cited principle carries its own hedge in the statement.",
        "Refusals restated at exactly the strength of the source principles, including P039's "
        "untrained-outcome requirement.",
    ]
    for i, ids in enumerate(fb_ids):
        add(f"forbidden_behaviours[{i}]", ids, fb_notes[i])

    wt_ids = ["P013/P085/P009/P089", "P126/P028/P043/P076", "P053/P007/P011/P039",
              "P088/P099/P036/P050", "P140/P070/P095/P052/P087"]
    for i, ids in enumerate(wt_ids):
        add(f"when_to_use[{i}]", ids, "Routing trigger grounded in the cited principles.")

    wn_ids = ["P010/P077", "P134/P132", "P128/P087", "P010", "P052"]
    for i, ids in enumerate(wn_ids):
        add(f"when_not_to_use[{i}]", ids,
            "Exclusion grounded in the boundary the cited principles imply; no rule strengthened.")

    add("outputs.primary_format", "P072/P010",
        "Per-finding format names the condition and trade-off rather than a verdict or the taught "
        "content.")
    add("outputs.modes[advise].output", "P072/P009",
        "Requires the condition a technique depends on to be stated with the recommendation.")
    add("outputs.modes[review].output", "P051/P088",
        "Findings close the gap to the learning intention rather than reporting correctness.")
    add("outputs.modes[plan].output", "P061/P040",
        "Plans are scoped to the retention horizon and the time actually available, as the "
        "spacing principles require.")
    add("handoff_rules[0]", "P010/P077",
        "Curriculum, materials, delivery and marks stay with the teacher or institution.")
    add("handoff_rules[1]", "P134/P128",
        "Individual assessment routed to qualified specialists; decisions to the responsible body.")
    add("source_of_truth_policy.precedence", "P072/P010/P009/P143/P125/P105/P134",
        "Adaptable-guide + carry-the-hedging + no-group-to-individual, all source-grounded.")
    add("minimum_useful_output", "P072/P010",
        "Requires the condition or trade-off, which is what keeps the advice at source strength.")

    report = {
        "schema_version": "faithfulness-report-v1",
        "subagent_slug": SLUG,
        "findings": findings,
    }
    w(BASE / "reports" / "faithfulness-report.yaml",
      yaml.safe_dump(report, sort_keys=False, allow_unicode=True, width=100))


GOLDEN = [
    dict(test_id="GT-001", mode="advise",
         desc="Positive routing — replace rereading with retrieval and spacing",
         prompt="My students revise by rereading and highlighting their notes, then do badly in the "
                "exam. We have three weeks. What should they do instead?",
         must_do=["Default to practice testing and distributed practice and displace highlighting "
                  "or rereading as the primary method",
                  "Require genuine reconstruction from memory with an unaided attempt before the "
                  "answer is revealed",
                  "Pair retrieval with an accuracy check because learners cannot verify themselves",
                  "Spread review across the three weeks, revisiting missed items sooner and "
                  "expanding intervals after success"],
         must_not=["Promise that the exam grade will improve",
                   "Write the revision materials or teach the subject content"],
         cov=["P020", "P059", "P135", "P107", "P050", "P040", "P118"]),
    dict(test_id="GT-002", mode="review",
         desc="Positive routing — appraise a learning-styles platform",
         prompt="We're buying a platform that assesses each learner's visual/auditory/kinesthetic "
                "style and streams matching content. Review that decision.",
         must_do=["Refuse styles-based differentiation absent evidence of a stable crossover",
                  "Report that modality-matched instruction yields little or no gain and the "
                  "preference groups overlap heavily",
                  "Distinguish modality preference from outcome evidence",
                  "Choose presentation because it represents the content well, and treat "
                  "accessibility accommodations separately"],
         must_not=["Endorse learning-style matching as evidence-based",
                   "Make the purchase decision for the caller"],
         cov=["P011", "P103", "P044", "P017", "P052"]),
    dict(test_id="GT-003", mode="review",
         desc="Positive routing — students execute but choose the wrong method",
         prompt="My students can do each formula when I tell them which one, but on a mixed test "
                "they pick the wrong one. Review my practice sets.",
         must_do=["Recommend interleaved rather than blocked practice for discriminating among "
                  "types or strategies",
                  "Introduce each new type with enough blocked practice first, then mix it "
                  "cumulatively with what it must be distinguished from",
                  "Practise applicability directly by mixing plausible problem types and contexts",
                  "Judge the change by delayed discrimination and transfer, not practice fluency"],
         must_not=["Present interleaving as universally superior to blocking regardless of goal",
                   "Write the new problem sets for the caller"],
         cov=["P028", "P142", "P001", "P035", "P064"]),
    dict(test_id="GT-004", mode="plan",
         desc="Positive routing — design a course from outcomes with load and scaffolding managed",
         prompt="I'm building a new introductory module from scratch. Help me plan it so beginners "
                "aren't overwhelmed.",
         must_do=["Start from substantive demonstrable outcomes and plan backward",
                  "Use worked examples and scaffolds for novices and plan how they fade",
                  "Keep essential state visible and pace multistep work within working memory",
                  "Verify prerequisite knowledge is reliably retrievable before demanding inquiry "
                  "or problem solving"],
         must_not=["Write the module's content or lesson materials",
                   "Present one fixed course template as universally correct"],
         cov=["P089", "P101", "P067", "P047", "P136", "P009"]),
    dict(test_id="GT-005", mode="review",
         desc="Positive routing — feedback that reports a score instead of closing the gap",
         prompt="I return marked essays with a grade and a few comments at the end of term. Review "
                "my feedback practice.",
         must_do=["Treat feedback's purpose as reducing the discrepancy between current "
                  "understanding and the learning intention",
                  "Require feedback to give task or process information rather than only "
                  "correctness",
                  "Return targeted feedback while learners can still apply it to related work",
                  "Build a task-specific analytic rubric that separates and weights consequential "
                  "components"],
         must_not=["Mark the essays for the caller",
                   "Reduce the recommendation to giving more praise"],
         cov=["P051", "P088", "P099", "P036"]),
    dict(test_id="GT-006", mode="advise",
         desc="Positive routing — a misconception that survives explanation",
         prompt="Every year my class insists heavier objects fall faster, even after I explain it. "
                "What do I do?",
         must_do=["Use refutational teaching: lead with the accurate account, name the "
                  "misconception briefly, and explain its failure with evidence",
                  "Inoculate against the misleading arguments that will recur",
                  "Elicit the learner's current model as a prediction and test it so the "
                  "discrepancy and failed assumptions become visible",
                  "Require learners to justify the more adequate alternative"],
         must_not=["Assume a clearer explanation alone will replace the model",
                   "Teach the physics content itself in place of the design advice"],
         cov=["P043", "P078", "P025", "P114"]),
    dict(test_id="GT-007", mode="review",
         desc="Positive routing — unstructured group work",
         prompt="My group projects end with one student doing everything and the rest learning "
                "nothing. Review how I run them.",
         must_do=["Impose structure on the peer learning so goals, learning intentions and success "
                  "criteria get spelled out",
                  "Pair individual accountability with group rewards and script the session",
                  "Train collaboration explicitly, with safeguards against dominance and "
                  "nonparticipation",
                  "Require an individual observable attempt before peer or whole-class discussion"],
         must_not=["Assign the group roles or produce the project brief for the caller",
                   "Attribute the imbalance to fixed learner traits"],
         cov=["P095", "P097", "P075", "P138"]),
]

NEGATIVE = [
    dict(test_id="NR-001",
         prompt="Explain how photosynthesis works so I can put it in my slides.",
         reason="Asks for the subject content to be taught or written, not for learning-design "
                "advice."),
    dict(test_id="NR-002",
         prompt="Based on this description of my daughter's behaviour, does she have dyslexia or "
                "ADHD?",
         reason="Requests an individual diagnosis of a learner, which belongs to a qualified "
                "specialist."),
    dict(test_id="NR-003",
         prompt="Which of these two candidates should we admit to the programme?",
         reason="Requests an admission decision, which belongs to the responsible body."),
]

MISSING = [
    dict(test_id="MC-001",
         prompt="How should I teach this better?",
         ask=["What the learners must be able to do afterwards, and when that is measured",
              "What they already know and where they currently get stuck",
              "How the teaching and practice are structured now, and the time available"]),
    dict(test_id="MC-002",
         prompt="Is spaced repetition worth it?",
         ask=["The retention horizon the learning has to survive to",
              "The material and whether the goal is facts, discrimination, or higher-order use",
              "How much total practice time exists and whether retrieval is currently checked"]),
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
                               "correction, and the condition or residual trade-off, highest-impact "
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

    # one behaviour test per principle (all N → covers every promoted principle).
    # Where the spine's operational_mapping already names a test case, that descriptor IS the
    # test_id — validate_principles resolves every declared test_cases entry against tests/,
    # so the authored layer adopts the spine's name rather than the spine adopting ours.
    modes = ["advise", "review", "plan"]
    pb = []
    for idx, pid in enumerate(ALL_IDS):
        skill = PID_TO_SKILL[pid]
        declared = (P[pid].get("operational_mapping") or {}).get("test_cases") or []
        pb.append({
            "test_id": declared[0] if declared else f"PB-{pid}",
            "principle_id": pid,
            "mode": modes[idx % 3],
            "prompt": (
                f"We are working on a teaching, study, or learning-design question where "
                f"{THEMES[skill]['title'].lower()} is at issue. What should we check for, what is "
                f"the correction, and what condition or residual trade-off should we carry?"),
            "expected_behaviour": [
                f"Applies the principle: {lead(P[pid]['statement'], 300)}.",
                "Names the gap and the principle it engages, gives the correction, and states the "
                "condition it depends on or the residual trade-off.",
                f"Cites {pid}.",
            ],
            "must_not": [
                "Teach the subject content, deliver the course, write the materials, or mark the "
                "work for the caller.",
                "State the rule more strongly than the source supports, diagnose an individual "
                "learner, or convert a group-level finding into an individual capacity judgment.",
            ],
        })
        # A principle may name more than one test case; each must resolve to a test_id.
        for extra in declared[1:]:
            pb.append({
                "test_id": extra,
                "principle_id": pid,
                "mode": modes[idx % 3],
                "prompt": pb[-1]["prompt"],
                "expected_behaviour": [f"Carries out the declared check: {extra}.",
                                       f"Cites {pid}."],
                "must_not": pb[-1]["must_not"],
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

All twelve sources are **distillation-only**: paraphrase and restructure only, no verbatim
quotation (see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They span
three layers of the field: primary research reviews and syntheses (Dunlosky et al.'s techniques
review, Hattie's meta-analytic synthesis, the National Academies' *How People Learn II*, the Deans
for Impact consensus summary, Rosenshine's *Principles of Instruction*); cognitive-science
translations for practitioners (*Make It Stick*, *Understanding How We Learn*, *Why Don't Students
Like School?*); and applied teaching handbooks (*How Learning Works*, *Powerful Teaching*, *Small
Teaching*, *Small Teaching Online*).

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
  P001-P{N_PRINC:03d} / {len(CLAIM_IDS)} claims from twelve distillation-only sources).
- `profile.yaml` derived from the {N_PRINC} promoted principles: role, when/when-not-to-use, three
  modes (advise / review / plan), quality bar, forbidden behaviours, handoff rules, and a
  {len(SKILLS)}-skill / {len(REFS)}-reference `knowledge_partition` covering every principle exactly
  once.
- {len(SKILLS)} authored skills partitioning all {N_PRINC} principles; {len(REFS)} references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence; the sources' own hedging on far transfer,
  durability and classroom generality is carried through).
- `tests/golden-tests.yaml` ({len(GOLDEN)} golden, {len(NEGATIVE)} negative-routing,
  {len(MISSING)} missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, {N_PRINC} total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Fixed
- `sources/metadata/*.metadata.json`: `source_type` normalised from the map->reduce short form
  `md` to the schema enum value `markdown`.

### Grounding
- Twelve distillation-only sources: Dunlosky et al. (2013); *Make It Stick* (Brown, Roediger &
  McDaniel, 2014); *Understanding How We Learn* (Weinstein & Sumeracki, 2018); *Principles of
  Instruction* (Rosenshine, 2012); *How Learning Works* (Ambrose et al., 2010); *Why Don't Students
  Like School?* (Willingham, 2009); *Powerful Teaching* (Agarwal & Bain, 2019); *Small Teaching*
  (Lang, 2016); *Small Teaching Online* (Darby & Lang, 2019); *Visible Learning* (Hattie, 2008);
  *The Science of Learning* (Deans for Impact); and *How People Learn II* (NASEM, 2018).
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
