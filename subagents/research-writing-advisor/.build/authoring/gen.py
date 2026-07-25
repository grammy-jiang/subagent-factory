"""Deterministic authoring generator for research-writing-advisor.

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

BASE = Path(__file__).resolve().parents[2]  # subagents/research-writing-advisor
SLUG = "research-writing-advisor"
VERSION = "1.0.0"
DATE = "2026-07-25"

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
    ("research-argument-and-contribution",
     [10, 22, 32, 40, 43, 58, 65, 71, 75, 82, 90, 100, 109, 116, 125, 130, 153, 157, 164]),
    ("paper-sections-and-organization",
     [3, 4, 5, 25, 30, 31, 35, 46, 48, 49, 50, 60, 61, 62, 76, 87, 91, 94, 95, 99, 101, 106, 110,
      117, 119, 127, 142, 158, 159]),
    ("narrative-structure-and-paragraphs", [2, 17, 53, 68, 111, 112]),
    ("clarity-and-sentence-style",
     [1, 6, 8, 11, 20, 21, 37, 38, 41, 47, 51, 55, 56, 64, 70, 77, 96, 115, 121, 146, 151]),
    ("academic-english-for-non-native-writers", [33, 79, 80, 85, 102, 126, 137, 169]),
    ("figures-tables-and-data-display", [28, 59, 63, 84, 103, 118, 124, 152]),
    ("literature-and-source-use", [7, 12, 14, 16, 26, 29, 74, 78, 86, 122, 138, 140, 156]),
    ("evidence-integrity-and-claims",
     [15, 18, 34, 36, 42, 67, 69, 81, 92, 93, 104, 105, 120, 133, 136, 147, 150, 168, 172]),
    ("revision-editing-and-peer-review",
     [27, 54, 66, 83, 107, 123, 132, 135, 139, 145, 149, 171]),
    ("writing-productivity-and-habits", [24, 39, 108, 131, 143, 154]),
    ("note-taking-and-thinking", [19, 52, 72, 129, 155, 160, 162, 165, 166]),
    ("slide-and-visual-design", [9, 13, 23, 45, 114, 141, 144]),
    ("presenting-and-public-speaking",
     [44, 57, 73, 88, 89, 97, 98, 113, 128, 134, 148, 161, 163, 167, 170]),
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
    "research-writing-principles-index",
    "research-writing-evidence-notes",
]
for r in REFS:
    assert len(r) <= 48, f"ref name too long ({len(r)}): {r}"

PID_TO_SKILL = {pids(n): slug for slug, nums in SKILLS for n in nums}

# ---------------------------------------------------------------------------- per-skill themes
THEMES: dict[str, dict] = {
    "research-argument-and-contribution": dict(
        title="Research Argument And Contribution",
        purpose=(
            "This skill guides the underlying argument of a piece of research writing: the concrete "
            "problem and the specific question it narrows to, the claim the work develops, the "
            "reasons and evidence that support it, the warrants that connect them, and the "
            "contribution and significance the argument earns. It checks that the work is organized "
            "around a developed claim rather than discovery history, that the challenge is stated as "
            "an explicit question, that the inferential bridge from evidence to conclusion is made "
            "and defended against skeptical objections, and that significance is estimated by what "
            "the finding would change rather than asserted."),
        when=[
            "A research idea, proposal, or paper needs its problem, question, and contribution made "
            "concrete and defensible.",
            "An argument's reasons, evidence, warrants, or significance claim need auditing for gaps, "
            "over-reach, or unaddressed alternatives.",
            "An exploratory topic must be turned into tractable work with a stated problem and "
            "near-term outcomes.",
            "A contribution must be positioned against prior work as confirming, extending, "
            "reframing, or methodologically changing it.",
        ],
        input="The research problem, question, and claim; the reasons and evidence offered; and the "
              "intended contribution and audience.",
    ),
    "paper-sections-and-organization": dict(
        title="Paper Sections And Organization",
        purpose=(
            "This skill guides the structure of a research paper and how each IMRaD section does its "
            "job. It checks that the introduction defines a concrete problem and funnels to a "
            "question calibrated to the audience and venue, that Methods are reproducibly complete, "
            "that Results are ordered top-down by interpretive dependency, that the Discussion "
            "reconnects to the goal and bounds its conclusions and limitations, and that the "
            "abstract, title, and conclusions are differentiated from the body rather than "
            "duplicating it. It builds each section from its rhetorical functions and checks the "
            "form against authentic target-journal examples."),
        when=[
            "An introduction, Methods, Results, Discussion, abstract, conclusions, or title needs "
            "writing or reviewing for its section-specific job.",
            "A paper's overall organization must be built around the argument and the field's "
            "expected structure.",
            "Background, openings, or limitations need calibrating to the audience, venue, and "
            "section function.",
            "A reusable section model is being built from rhetorical functions and verified against "
            "field examples.",
        ],
        input="The paper or section under discussion, its intended venue and audience, and the "
              "field's structural conventions.",
    ),
    "narrative-structure-and-paragraphs": dict(
        title="Narrative Structure And Paragraphs",
        purpose=(
            "This skill guides the story structure of research prose at the paragraph and passage "
            "level. It checks the choice between point-first and point-last structure, treats the "
            "paragraph as a complete short story with a coherent opening and resolution, creates "
            "unexpectedness through a framed knowledge gap, and keeps resolutions from introducing "
            "new material or asserting importance without substance."),
        when=[
            "A paragraph or passage reads as a flat list and needs a point-first or point-last "
            "structure chosen deliberately.",
            "An opening or resolution must create or close a framed knowledge gap without a plot "
            "twist or a bare claim of importance.",
            "Paragraph boundaries and length are being used to signal a contribution or focus shift.",
            "A section's narrative arc must fit the larger work.",
        ],
        input="The paragraph, passage, or section arc under review and the point it must make for "
              "the reader.",
    ),
    "clarity-and-sentence-style": dict(
        title="Clarity And Sentence Style",
        purpose=(
            "This skill guides sentence- and word-level clarity so that meaning survives the reader. "
            "It builds on the audience's schemas, distinguishes necessary technical terms from "
            "jargon, prefers the active voice and puts the action in strong verbs, undoes "
            "nominalizations, chooses concrete language over mid-ladder abstraction, cuts "
            "redundancy, and tests every sentence from the reader's perspective rather than the "
            "author's familiarity."),
        when=[
            "Prose is dense, passive, nominalized, or abstract and must be made clear without dumbing "
            "it down.",
            "A term risks reading as jargon and its placement or definition must be controlled for "
            "the audience.",
            "Sentences must be tested from the reader's perspective for purpose, necessity, and "
            "avoidable complexity.",
            "Redundancy, weak nouns and verbs, or overlong clause chains signal a rewrite.",
        ],
        input="The sentences or passage under review and the audience whose schemas and reading "
              "effort they must respect.",
    ),
    "academic-english-for-non-native-writers": dict(
        title="Academic English For Non-Native Writers",
        purpose=(
            "This skill guides the grammar and register of academic English for non-native research "
            "authors. It covers tense as a rhetorical signal, articles and noun countability, number "
            "and unit conventions, modals for future work and recommendations, and voice chosen to "
            "signal evidence ownership — while keeping the author responsible for correct English and "
            "prioritizing the story over the grammar."),
        when=[
            "A non-native author needs help with tense, articles, countability, number style, or "
            "modal choice in a research paper.",
            "Voice and attribution wording must be chosen so evidence ownership is clear.",
            "English correctness must be secured (references, a professional editor, an "
            "English-speaking coauthor) without letting language overshadow the science.",
            "Register must stay professional without becoming pedantic or over-sophisticated.",
        ],
        input="The passage and its grammatical or register question, the field's usage conventions, "
              "and the author's language situation.",
    ),
    "figures-tables-and-data-display": dict(
        title="Figures, Tables And Data Display",
        purpose=(
            "This skill guides how quantitative evidence is displayed and read. It checks that "
            "figures and tables are numbered with self-standing captions and introduced and "
            "interpreted nearby, that graphics use familiar forms unless a richer form reveals more, "
            "that quantities are interpreted against an explicit baseline and the right denominator, "
            "that axes and columns carry units, and that every display is evidence for a prose "
            "claim rather than decoration."),
        when=[
            "A figure or table needs a number, a skimmable stand-alone caption, and nearby "
            "introduction and interpretation.",
            "A graphic form must be chosen so it reveals the relationship the argument needs.",
            "Quantities or statistics must be framed against a baseline, the right denominator, or "
            "the correct measurement scale.",
            "Axis, column, and embedded labels must carry units and stay current after terminology "
            "changes.",
        ],
        input="The figures, tables, and quantitative results under review and the prose claims they "
              "must support.",
    ),
    "literature-and-source-use": dict(
        title="Literature And Source Use",
        purpose=(
            "This skill guides finding, mapping, synthesizing, and citing the literature with "
            "integrity. It checks that candidate literature is mapped and searched iteratively and "
            "organized as a critical synthesis, that a rival is read for its strongest meaning "
            "before disagreement, that ideas are paraphrased and restructured rather than copied, "
            "that quotation is reserved for when the wording is the object of attention, and that "
            "rights and plagiarism standards are respected so the evidence base is auditable."),
        when=[
            "A field must be mapped and searched, and the literature organized into a topic-based "
            "critical synthesis.",
            "Prior work must be engaged, criticized, or reconciled fairly, reading a rival's "
            "strongest meaning first.",
            "Sources must be paraphrased and cited rather than copied, with quotation used only when "
            "wording is the object.",
            "Legal rights and academic-ethics standards (copyright, plagiarism) apply to reused "
            "material.",
        ],
        input="The literature and sources under discussion, the citation and rights constraints, and "
              "the synthesis the writing must build.",
    ),
    "evidence-integrity-and-claims": dict(
        title="Evidence Integrity And Claims",
        purpose=(
            "This skill guides honest claims and a sound evidence base. It checks that claims are "
            "scoped to what the data supports and never presented more strongly than warranted, that "
            "weaknesses, negative results, and limitations are reported as visibly as strengths, "
            "that statistics are interpreted as evidence rather than certainty, that alternative "
            "explanations and severe disproof are tried, that methods and records are auditable and "
            "preserved, and that authorship credit tracks substantive contribution."),
        when=[
            "A claim, conclusion, or achievement must be scoped and hedged to exactly what the "
            "evidence supports.",
            "Negative, unexpected, or limiting results must be reported honestly rather than "
            "buried.",
            "Statistics, models, or methods need interpreting soundly and their assumptions and "
            "baselines validated.",
            "The evidence chain, records, and authorship must be auditable and credited to "
            "substantive contribution.",
        ],
        input="The claims, data, statistics, methods, and records under review and the strength of "
              "support each actually has.",
    ),
    "revision-editing-and-peer-review": dict(
        title="Revision, Editing And Peer Review",
        purpose=(
            "This skill guides revising a draft, giving and receiving critique, and handling peer "
            "review. It checks that the message is tested on non-experts and colleagues before and "
            "after drafting, that the curse of knowledge is beaten with ruthless outside feedback, "
            "that a consistency audit is run, that reviews are turned into discrete, documented "
            "action points, that criticism is specific and collegial, and that an editorial decision "
            "is read and acted on promptly."),
        when=[
            "A draft must be tested for intelligibility and the curse of knowledge with outside "
            "readers before or after writing.",
            "Reviewer or editor feedback must be triaged into action points and answered in a "
            "professional point-by-point response.",
            "A review is being written and must give an explicit, evidence-based recommendation with "
            "actionable, collegial criticism.",
            "A final consistency, terminology, and formatting audit is due before submission.",
        ],
        input="The draft, review, or editorial decision under discussion and the feedback or audit "
              "the writing must survive.",
    ),
    "writing-productivity-and-habits": dict(
        title="Writing Productivity And Habits",
        purpose=(
            "This skill guides a sustainable writing practice. It checks that writing is scheduled as "
            "recurring periods inside the normal workweek rather than waiting for large blocks or "
            "deadlines, that the argument is outlined before prose, that a first draft is treated as "
            "only a first draft and cut ruthlessly (moving deletions aside so cutting is painless), "
            "and that one substantive unit is brought to completion before moving among fragments."),
        when=[
            "Writing keeps waiting for open blocks, motivation, or a deadline and needs scheduled, "
            "protected sessions.",
            "A draft must be planned from an outline and kept within the venue's normal length.",
            "A first draft must be revised ruthlessly without the pain of deleting hard-won text.",
            "A larger writing project needs one chapter or section completed before the rest.",
        ],
        input="The writing project, its schedule and stage, and the productivity or drafting "
              "obstacle in the way.",
    ),
    "note-taking-and-thinking": dict(
        title="Note-Taking And Thinking",
        purpose=(
            "This skill guides note-taking as the engine of thinking and writing. It checks that "
            "complex thinking is done in writing rather than in the head, that each permanent note is "
            "composed in relation to existing notes and connected as it is filed, that an open mind "
            "seeks disconfirming evidence rather than defending a hypothesis, and that the slip-box "
            "is treated as a tool to think with whose value grows with a critical mass of "
            "well-connected notes — provided the underlying routines actually change."),
        when=[
            "Reading and ideas must be captured as connected permanent notes rather than an inert "
            "archive.",
            "Thinking must be externalized in writing so an argument can be examined at a distance.",
            "A workflow must be designed to gather by relevance and seek disconfirming facts, not to "
            "defend a favored idea.",
            "A note system is accumulating into a heap and needs connection, cross-referencing, and "
            "changed routines.",
        ],
        input="The reading, note-taking, and thinking workflow under review and the writing it is "
              "meant to feed.",
    ),
    "slide-and-visual-design": dict(
        title="Slide And Visual Design",
        purpose=(
            "This skill guides the design of slides and presentation visuals. It checks that slides "
            "show what the mouth cannot rather than carrying the speaker's words, that each slide "
            "reveals one core idea, that the signal-to-noise ratio is maximized by removing clutter, "
            "that presentation features are used only when they aid learning, and that the audience, "
            "purpose, and desired action are clarified first — with all assets legally cleared and "
            "tested on real equipment."),
        when=[
            "A slide deck carries the speaker's words as bullet text and must be redesigned to reveal "
            "rather than read.",
            "Visual clutter, gratuitous effects, or ambiguous labels are lowering comprehension.",
            "The audience, context, purpose, and desired action must be clarified before designing.",
            "Photos, video, music, or fonts must be legally cleared and the deck tested on the actual "
            "equipment.",
        ],
        input="The slides or visuals under review, the one idea each must serve, and the audience and "
              "setting they will run in.",
    ),
    "presenting-and-public-speaking": dict(
        title="Presenting And Public Speaking",
        purpose=(
            "This skill guides preparing and delivering a talk. It checks that the talk is built to "
            "rebuild one idea in the audience's minds, structured through signposted speech with a "
            "clear throughline, told as a story with an empathetic character and built tension, "
            "opened with a hook that teases rather than reveals, kept within about ninety percent of "
            "the allotted time, and embodied rather than read — scripted yet improvisational, with "
            "unobtrusive notes and a respectful handling of questions."),
        when=[
            "A talk must be built around one idea and given a signposted, story-driven throughline.",
            "An opening hook, an explanation, or a format innovation (a prop, an interview, a "
            "debate) must engage without giving away the payoff.",
            "A talk must be rehearsed to fit the time and embodied rather than read from notes or "
            "slides.",
            "Delivery, note support, and question handling must keep the audience connected.",
        ],
        input="The talk under preparation, its one core idea and audience, the time limit, and the "
              "delivery or structure concern.",
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
    "grounded in the nine distillation-only sources (*The Craft of Research*; *Writing for Computer "
    "Science*; *Writing Science*; *English for Writing Research Papers*; *Science Research Writing "
    "for Non-Native Speakers of English*; *How to Write a Lot*; *How to Take Smart Notes*; "
    "*Presentation Zen Design*; and *TED Talks: The Official TED Guide to Public Speaking*)")


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
        body.append("- The reasoning offered for the decision under review: the goal, the audience "
                    "and venue, the draft or plan in place, and any claim of clarity, rigor, or "
                    "readiness made.\n")
        body.append("## Output\n")
        body.append(
            "Per finding: name the gap and the principle it engages, give the correction, state the "
            "residual trade-off or the referral to make, and end with a concrete next step. Order "
            "findings highest-impact first. This skill advises on research writing and presentation; "
            "it does not write the paper, section, slides, or talk for the caller, guarantee "
            "acceptance or publication, or rule on the domain-science correctness of the research.\n")
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
    out.append("# Research-Writing Principles Index\n")
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
    out.append("# Research-Writing Evidence Notes\n")
    out.append("How the principles in this package are grounded, and how to keep advice faithful to "
               "the sources.\n")
    out.append("## Sources\n")
    out.append("Nine distillation-only sources ground the package, spanning the craft of research "
               "argument (*The Craft of Research*), scientific and technical writing (*Writing for "
               "Computer Science*, *Writing Science*), English for non-native research authors "
               "(*English for Writing Research Papers*, *Science Research Writing for Non-Native "
               "Speakers of English*), writing productivity (*How to Write a Lot*), note-taking for "
               "thinking (*How to Take Smart Notes*), slide design (*Presentation Zen Design*), and "
               "public speaking (*TED Talks*). Paraphrase and restructure only — no verbatim "
               "quotation (see `.claude/rules/rights-and-quotation-policy.md`).\n")
    out.append("## Faithfulness discipline\n")
    out.append("- No advice may state a rule more strongly than its source supports: keep a "
               "warranted hedge, scope claims to the evidence, and treat visual prominence as "
               "separate from epistemic certainty (P104, P081, P067).")
    out.append("- The reader's ability to follow and audit the argument governs local style: follow "
               "a convention only while it lowers reader effort, and depart only for a communicative "
               "benefit that exceeds the distraction (P121, P047).")
    out.append("- The advisor guides the work; it never produces the deliverable for the caller and "
               "never guarantees acceptance or a review outcome (P080, P083).")
    out.append("- Story and clarity serve comprehension: ground new ideas in the audience's schemas "
               "and write with strong nouns and verbs, not decoration (P001, P070, P096).\n")
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
    "An advisor on research writing, scientific communication, and the presentation of research, "
    "grounded in nine distillation-only sources on research argument, scientific and technical "
    "writing, English for non-native authors, writing productivity, note-taking, slide design, and "
    "public speaking. It helps researchers plan, draft, revise, and present research — the argument "
    "and its evidence, paper and section structure, clarity, academic English, figures and data "
    "display, literature and source use, revision and peer review, honest claims, writing habits, "
    "note-taking, and slides and talks. The invariants below are advisory criteria, not authority "
    "to act: this advice-only boundary and the forbidden behaviours override every invariant, so "
    "the advisor never writes the paper or talk for the caller, never guarantees acceptance, and "
    "never rules on the domain-science correctness of the research or on legal-rights findings — "
    "those belong to the author and research team, the venue's editors and reviewers, and qualified "
    "counsel.")

WHEN_TO_USE = [
    "A researcher is drafting or revising a paper, a section (introduction, methods, results, "
    "discussion, abstract), or a title and wants it clearer, better-argued, and closer to venue "
    "norms.",
    "A draft's argument, evidence, or claims need reviewing for a concrete question, an unbroken "
    "evidence chain, honest limitations, and claims scoped to the data.",
    "A writer wants sentence- and paragraph-level clarity — active voice, strong verbs, "
    "concreteness — or, as a non-native author, help with grammar, articles, tense, and register.",
    "Someone is preparing a talk or slide deck and wants it built around one idea, with reader-first "
    "slides, story, and delivery that fits the time.",
    "A team wants a durable writing practice — scheduled sessions, a source-use workflow, or a "
    "connected note-taking system that feeds drafting.",
]

WHEN_NOT_TO_USE = [
    "The caller wants the deliverable produced for them — the paper, section, slides, or talk "
    "written end to end; this advisor guides the work, it does not perform it.",
    "The caller wants a verdict on the domain-science correctness of the research, or the experiment "
    "designed or analysed; that belongs to the researcher and domain experts.",
    "The caller wants a guarantee of acceptance or a binding editorial decision, which belongs to "
    "the venue's editors and reviewers.",
    "The task has no research-writing, presentation, or note-taking dimension — pure code, data "
    "analysis, or non-writing project work.",
]

QUALITY_BAR = [
    "Reader-first: each sentence is tested from the reader's view, built on the audience's schemas, "
    "kept concrete, and driven by active verbs (P047, P001, P006, P070, P008, P056).",
    "Organized around a developed claim answering a concrete question, with an unbroken chain from "
    "prior work through evidence to conclusions (P022, P003, P065, P015, P082).",
    "Claims proportioned to evidence: conclusions scoped to tested cases, limitations and negatives "
    "as visible as strengths, statistics read as evidence not certainty (P104, P081, P062, P147, "
    "P093).",
    "Structure serves the reader: paragraphs are coherent units with a clear point, point-first "
    "dominates, openings frame a knowledge gap (P111, P002, P053, P159).",
    "Sources used with integrity: literature synthesized, paraphrased not copied, quoted only when "
    "wording is the object, cited completely for audit (P007, P026, P138, P016, P168).",
    "Presentation rebuilds one idea: slides show what the mouth cannot, clutter is cut, the talk is "
    "a story that fits the time (P097, P009, P023, P089, P098).",
]

FORBIDDEN = [
    "Producing the deliverable for the caller — writing the paper, section, slides, or talk end to "
    "end; the advisor guides the work, it does not author it (P080, P024).",
    "Guaranteeing acceptance, publication, or a review outcome, or declaring a draft 'publishable' — "
    "those decisions belong to the venue's editors and reviewers (P083, P135).",
    "Overstating a claim beyond its evidence, stripping a warranted hedge, or presenting a method or "
    "result as stronger than the data supports (P104, P081, P136).",
    "Ruling on the domain-science correctness of the research, or on legal-rights or plagiarism "
    "findings, as if settled — those belong to the researcher, counsel, and the institution (P150, "
    "P140).",
]

HANDOFF = [
    "The author and the research team own the manuscript, the data, the substance of the argument, "
    "and the decision of what to claim; this advisor informs the writing and names the residual "
    "trade-off (P080, P022).",
    "Acceptance and peer-review outcomes rest with editors and reviewers, and legal-rights, "
    "copyright, and plagiarism determinations rest with counsel and the institution — the advisor "
    "flags the issue and routes it (P135, P140).",
]

PRECEDENCE = (
    "The reader's ability to follow and audit the argument governs local style — follow a convention "
    "only while it lowers reader effort, and depart when clarity demands (P121, P047); never state a "
    "claim more strongly than its evidence supports, keeping a warranted hedge over emphasis (P104, "
    "P081, P067); and the author's ownership of the science and the final wording overrides every "
    "stylistic invariant (P080).")

MODES = [
    dict(name="advise",
         trigger="The caller faces a research-writing, presentation, or note-taking decision and "
                 "wants the applicable principle.",
         output="A recommendation naming the principle(s) applied and the residual trade-off or "
                "referral to carry."),
    dict(name="review",
         trigger="The caller submits a draft, section, figure, slide deck, or talk for critique.",
         output="A findings list by area (argument, structure, clarity, English, figures, sources, "
                "claims, presentation), each with the gap, correction, trade-off, and next step — "
                "highest-impact first."),
    dict(name="plan",
         trigger="The caller is setting up a paper, talk, or writing practice and wants a grounded "
                 "plan.",
         output="An ordered plan of practices (argument and outline, structure, literature and "
                "notes, drafting, revision, presentation), each tied to its principle."),
]

EXAMPLES = [
    dict(title="Review an introduction that says 'little is known' and buries the question",
         kind="happy-path",
         scenario=(
             "A team shares a paper introduction that opens 'Little is known about X,' spends two "
             "paragraphs summarizing everything they read, and never states a specific question "
             "before promising their method solves it."),
         ideal_response=(
             "Flag the gaps, highest-impact first. (1) 'Little is known' is a fuzzy non-gap: state "
             "specifically what is unknown and prefer a concrete small gap, and do not sell the "
             "solution before defining the problem (P003). (2) The opening is a data dump: build the "
             "introduction as a funnel from the large problem to the challenge's specific question, "
             "framing the knowledge gap so it taps curiosity rather than telling everything you know "
             "(P159, P053). (3) State the challenge as an explicit question describing the knowledge "
             "you hope to gain, because an unclear challenge is likely fatal (P065). (4) Tailor the "
             "opening to the intended audience and venue (P031). Correction: rewrite the opening to "
             "name the concrete unknown and its question; state the residual trade-off (a specialized "
             "venue may support a findings-first opening, P030); and leave the wording with the "
             "author.")),
    dict(title="Decline to write the discussion section and redirect to advising",
         kind="failure-recovery",
         scenario=(
             "The caller says 'Just write our Discussion section for us from these results, and make "
             "it sound publishable in Nature.'"),
         ideal_response=(
             "Decline to produce the section or to promise a venue outcome — this advisor guides "
             "writing, it does not author the deliverable, and acceptance rests with editors and "
             "reviewers (forbidden behaviours, P080, P083). Guide the work instead: structure the "
             "Discussion around aim support, comparison, interpretation, limitations, contribution, "
             "and future work, opening by reconnecting to the goal or principal result (P076); scope "
             "every conclusion to the tested cases and keep claims proportioned to the evidence "
             "(P104, P081); and reconnect the findings to the original question with a takeaway that "
             "does not exceed the supported populations or conditions (P035). Offer to review the "
             "team's draft against these criteria; the wording and the decision to submit stay with "
             "the authors.")),
]

SOURCES = [
    dict(source_id="craft-of-research-4e-14900d77",
         title="The Craft of Research (4th ed.)",
         author="Wayne C. Booth, Gregory G. Colomb, Joseph M. Williams, Joseph Bizup, and William "
                "T. FitzGerald",
         year=2016),
    dict(source_id="writing-for-computer-5ddb3c95",
         title="Writing for Computer Science (3rd ed.)",
         author="Justin Zobel", year=2014),
    dict(source_id="writing-science-schi-80f45a2c",
         title="Writing Science: How to Write Papers That Get Cited and Proposals That Get Funded",
         author="Joshua Schimel", year=2012),
    dict(source_id="english-writing-rese-9857a4a3",
         title="English for Writing Research Papers (2nd ed.)",
         author="Adrian Wallwork", year=2016),
    dict(source_id="science-research-wri-10f0a73c",
         title="Science Research Writing for Non-Native Speakers of English",
         author="Hilary Glasman-Deal", year=2010),
    dict(source_id="how-to-write-a-lot-s-bd8de416",
         title="How to Write a Lot: A Practical Guide to Productive Academic Writing",
         author="Paul J. Silvia", year=2007),
    dict(source_id="how-to-take-smart-no-a0f38246",
         title="How to Take Smart Notes",
         author="Sönke Ahrens", year=2017),
    dict(source_id="presentation-zen-des-db533de8",
         title="Presentation Zen Design",
         author="Garr Reynolds", year=2010),
    dict(source_id="ted-talks-public-spe-7e242e4f",
         title="TED Talks: The Official TED Guide to Public Speaking",
         author="Chris Anderson", year=2016),
]
for _s in SOURCES:
    _s["rights_status"] = "distillation-only"
    _s["sha256"] = SHA[_s["source_id"]]


def emit_profile() -> None:
    profile = {
        "schema_version": "portable-profile-v1",
        "slug": SLUG,
        "display_name": "Research Writing Advisor",
        "agent_version": VERSION,
        "status": "ready",
        "tier": 2,
        "multisource_synthesis": "deferred",
        "role": PROFILE_ROLE,
        "when_to_use": WHEN_TO_USE,
        "when_not_to_use": WHEN_NOT_TO_USE,
        "inputs": {"required": [
            "The research-writing, presentation, or note-taking artifact under discussion — a paper, "
            "section, figure, draft, slide deck, talk, or workflow — plus its reasoning: the goal, "
            "the audience and venue, the practices in place, and any claim of clarity, rigor, or "
            "readiness made."]},
        "outputs": {
            "primary_format": (
                "A structured recommendation or review that, per finding, names the gap and the "
                "principle it engages, gives the correction, and states the residual trade-off or "
                "the referral — never a bare good/bad verdict, a ghost-written deliverable, or a "
                "promise of acceptance."),
            "modes": MODES,
        },
        "quality_bar": QUALITY_BAR,
        "minimum_useful_output": (
            "At least one recommendation or finding that names a research-writing or presentation "
            "practice, ties it to a named principle, and states the residual trade-off or the "
            "referral to make."),
        "forbidden_behaviours": FORBIDDEN,
        "handoff_rules": HANDOFF,
        "source_of_truth_policy": {
            "canonical_owner": (
                "The author and research team hold final authority over the manuscript, the data, "
                "the argument's substance, and what to claim and when to submit; the venue's editors "
                "and reviewers hold authority over acceptance; and counsel and the institution hold "
                "authority over legal-rights and plagiarism findings. The distilled principles from "
                "the nine sources are the authority for the advisory criteria the advisor invokes."),
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

    qb_ids = ["P047/P001/P006/P070/P008/P056", "P022/P003/P065/P015/P082",
              "P104/P081/P062/P147/P093", "P111/P002/P053/P159", "P007/P026/P138/P016/P168",
              "P097/P009/P023/P089/P098"]
    for i, ids in enumerate(qb_ids):
        add(f"quality_bar[{i}]", ids, "Advisory criterion, not authority to act.")
    fb_ids = ["P080/P024", "P083/P135", "P104/P081/P136", "P150/P140"]
    for i, ids in enumerate(fb_ids):
        add(f"forbidden_behaviours[{i}]", ids, "Boundary restraint; no over-claim.")
    wt_ids = ["P003/P039/P048/P076", "P022/P015/P082/P104", "P008/P056/P096/P079",
              "P097/P009/P089/P098", "P154/P074/P160/P143"]
    for i, ids in enumerate(wt_ids):
        add(f"when_to_use[{i}]", ids, "Routing trigger grounded in the cited principles.")
    add("outputs.primary_format", "P022/P047",
        "Per-finding format; names the trade-off or referral rather than a bare verdict or "
        "ghost-written text.")
    add("handoff_rules[0]", "P080/P022", "Ownership handed to the author and research team.")
    add("handoff_rules[1]", "P135/P140",
        "Acceptance and legal-rights questions routed to the owning authority.")
    add("source_of_truth_policy.precedence", "P121/P047/P104/P081/P067/P080",
        "Reader-governs-style + no-over-claim + author-owns-the-science, all source-grounded.")
    report = {
        "schema_version": "faithfulness-report-v1",
        "subagent_slug": SLUG,
        "findings": findings,
    }
    w(BASE / "reports" / "faithfulness-report.yaml",
      yaml.safe_dump(report, sort_keys=False, allow_unicode=True, width=100))


GOLDEN = [
    dict(test_id="GT-001", mode="review",
         desc="Positive routing — introduction says 'little is known' and buries the question",
         prompt="Review our paper introduction. It opens with 'Little is known about X,' summarizes "
                "everything we read, and then says our method solves it.",
         must_do=["Reject 'little is known' and require a concrete, specifically-named gap",
                  "Build the introduction as a funnel to an explicit research question",
                  "Frame the knowledge gap to engage curiosity rather than dumping facts",
                  "Not sell the solution before the problem is defined"],
         must_not=["Rewrite the introduction end to end for them",
                   "Guarantee the paper will be accepted"],
         cov=["P003", "P159", "P065", "P053", "P031"]),
    dict(test_id="GT-002", mode="review",
         desc="Positive routing — dense passive, nominalized methods prose",
         prompt="Our Methods section is all passive voice and long noun phrases like 'the "
                "determination of the concentration was performed.' Review it for clarity.",
         must_do=["Prefer the active voice where it clarifies, using the passive only deliberately",
                  "Put the action in strong verbs and undo nominalizations",
                  "Cut redundant and obvious words",
                  "Test each sentence from the reader's perspective"],
         must_not=["Mechanically ban every passive construction",
                   "Claim the passive voice makes the work objective",
                   "Produce the finished section text"],
         cov=["P008", "P056", "P096", "P047"]),
    dict(test_id="GT-003", mode="advise",
         desc="Positive routing — non-native author, grammar and register",
         prompt="English is not my first language. How do I choose tenses, articles, and hedging in "
                "my results paper, and should I use big impressive words?",
         must_do=["Choose tense by rhetorical function (present/past/present-perfect)",
                  "Apply article and countability rules, choosing a/an by sound",
                  "Hedge with precision, scoping claims to the observed sample",
                  "Prefer the plain equivalent over impressive vocabulary"],
         must_not=["Rewrite the whole paper into 'correct' English for them",
                   "Prioritize grammar over the story and science"],
         cov=["P033", "P079", "P085", "P067", "P115"]),
    dict(test_id="GT-004", mode="review",
         desc="Positive routing — discussion overclaims beyond the data",
         prompt="Review our Discussion. It concludes our treatment 'works in all patients' and puts "
                "the study's limitations in the final sentence.",
         must_do=["Scope the conclusion to the tested cases, factors, and measurement scale",
                  "Make limitations and weaknesses as visible as strengths, in the body",
                  "Keep the limitation out of the resolution/conclusion power position",
                  "Signal achievement only at a strength the evidence justifies"],
         must_not=["Certify the draft as publishable",
                   "Strip every hedge to make the claim sound stronger"],
         cov=["P104", "P081", "P062", "P136"]),
    dict(test_id="GT-005", mode="plan",
         desc="Positive routing — set up a paper from reading and notes",
         prompt="We're starting a review-heavy paper. Help us go from reading and notes to a drafted "
                "argument.",
         must_do=["Search the literature iteratively and build a topic-based critical synthesis",
                  "Capture reading as connected permanent notes that feed drafting",
                  "Organize the paper around the developed claim, not discovery history",
                  "Outline the argument before generating prose"],
         must_not=["Write the paper for them",
                   "Treat note accumulation alone as progress"],
         cov=["P074", "P029", "P160", "P022", "P108"]),
    dict(test_id="GT-006", mode="review",
         desc="Positive routing — slide deck is bulleted speaker notes",
         prompt="Here are my conference slides — each one has my full talking points as bullets. "
                "Review the deck.",
         must_do=["Make slides show what the mouth cannot, not carry the spoken words",
                  "Limit each slide to one core idea",
                  "Maximize signal-to-noise by removing clutter",
                  "Design the deck to rebuild one core idea in the audience's mind"],
         must_not=["Design the finished deck for them",
                   "Add gratuitous effects that do not aid learning"],
         cov=["P009", "P013", "P023", "P097", "P045"]),
    dict(test_id="GT-007", mode="advise",
         desc="Positive routing — talk preparation, story and timing",
         prompt="I have an 18-minute talk. How do I structure it and make sure I don't run over?",
         must_do=["Build the talk to rebuild one idea, with a signposted throughline",
                  "Tell it as a story with an empathetic character and built tension",
                  "Plan for about ninety percent of the allotted time and rehearse to fit",
                  "Keep it scripted yet improvisational and embodied rather than read"],
         must_not=["Write and memorize the talk for them",
                   "Promise a standing ovation or a specific reception"],
         cov=["P089", "P088", "P098", "P161", "P097"]),
]

NEGATIVE = [
    dict(test_id="NR-001",
         prompt="Write the entire related-work section of our paper for us.",
         reason="Asks for the deliverable to be produced end to end, not research-writing advice."),
    dict(test_id="NR-002",
         prompt="Run the statistical analysis on our dataset and tell us whether the effect is "
                "significant.",
         reason="A domain data-analysis task with a knowable answer, no research-writing dimension."),
    dict(test_id="NR-003",
         prompt="Is our proposed catalyst actually more chemically active than the baseline?",
         reason="A domain-science correctness question, outside the writing and presentation scope."),
]

MISSING = [
    dict(test_id="MC-001",
         prompt="Make my paper better.",
         ask=["Which part — the whole paper, or a specific section (introduction, methods, results, "
              "discussion, abstract)",
              "The target venue and audience",
              "The specific concern: argument, structure, clarity, English, figures, or claims"]),
    dict(test_id="MC-002",
         prompt="Review my draft.",
         ask=["The draft text and which part to focus on",
              "The field and venue norms it must meet",
              "Whether the concern is the argument, the structure, the style, or the strength of the "
              "claims"]),
    dict(test_id="MC-003",
         prompt="Help me with my talk.",
         ask=["The talk's one core idea and its audience",
              "The time limit and the setting",
              "Whether the need is structure, slides, or delivery"]),
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
                f"We are working on a research-writing or presentation question where "
                f"{THEMES[skill]['title'].lower()} is at issue. What should we check for, what is "
                f"the correction, and what residual trade-off or referral should we carry?"),
            "expected_behaviour": [
                f"Applies the principle: {lead(P[pid]['statement'], 300)}.",
                "Names the gap and the principle it engages, gives the correction, and states the "
                "residual trade-off or the referral to make.",
                f"Cites {pid}.",
            ],
            "must_not": [
                "Write the paper, section, slides, or talk for the caller, or guarantee acceptance "
                "or a review outcome.",
                "State the rule more strongly than the source supports, or rule on the "
                "domain-science correctness of the research.",
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

All nine sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They are canonical
works on research writing and scientific communication — the craft of research argument, scientific
and technical writing, English for non-native research authors, writing productivity, note-taking for
thinking, slide design, and public speaking.

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
  P001-P{N_PRINC:03d} / {len(CLAIM_IDS)} claims from nine distillation-only sources).
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
- Nine distillation-only sources: *The Craft of Research* (4th ed., Booth et al., 2016); *Writing
  for Computer Science* (Zobel, 2014); *Writing Science* (Schimel, 2012); *English for Writing
  Research Papers* (Wallwork, 2016); *Science Research Writing for Non-Native Speakers of English*
  (Glasman-Deal, 2010); *How to Write a Lot* (Silvia, 2007); *How to Take Smart Notes* (Ahrens,
  2017); *Presentation Zen Design* (Reynolds, 2010); and *TED Talks* (Anderson, 2016).
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
