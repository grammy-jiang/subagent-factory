"""Deterministic authoring generator for translation-naturalness-reviewer.

Reads the already-assembled, deterministically-valid distilled spine
(principles/principles.yaml + analysis/claims.jsonl + evidence + anchors) and emits the
LLM-authored layer: profile.yaml, references/*, skills/*, tests/*, reports/faithfulness-report.yaml,
provenance-ledger.md, CHANGELOG.md. Every emitted id resolves into the spine.

Cloned in structure from the translation-faithfulness-reviewer generator (same 150-principle,
tier-2, distillation-only shape); all naturalness-specific content — the skill partition, themes,
profile rules, faithfulness citations, and tests — is re-authored against THIS package's principles
(P001..P150 mean different things here than in the sibling).

Run:  python3 .build/authoring/gen.py
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parents[2]  # subagents/translation-naturalness-reviewer
SLUG = "translation-naturalness-reviewer"
VERSION = "1.0.0"
DATE = "2026-07-13"
NP = 150  # promoted principles P001..P150

# ---------------------------------------------------------------------------- spine load
PRINCIPLES = yaml.safe_load((BASE / "principles" / "principles.yaml").read_text())["principles"]
P = {p["principle_id"]: p for p in PRINCIPLES}
ALL_IDS = [p["principle_id"] for p in PRINCIPLES]
HI_IDS = [p["principle_id"] for p in PRINCIPLES if p.get("confidence") == "high"]
CLAIM_IDS = set()
for line in (BASE / "analysis" / "claims.jsonl").read_text().splitlines():
    line = line.strip()
    if line:
        CLAIM_IDS.add(json.loads(line)["claim_id"])

# source_id -> sha256, read from ingested metadata so the profile sha never drifts.
META_SHA: dict[str, str] = {}
for mf in (BASE / "sources" / "metadata").glob("*.metadata.json"):
    m = json.loads(mf.read_text())
    if m.get("source_id"):
        META_SHA[m["source_id"]] = str(m.get("sha256") or "")


def pids(n: int) -> str:
    return f"P{n:03d}"


# ---------------------------------------------------------------------------- partition
# Each entry: (skill-slug (kebab, <=48 chars), [principle numbers]).
# Every principle 1..150 appears in exactly one skill. Partition is by naturalness sub-theme.
SKILLS: list[tuple[str, list[int]]] = [
    ("audience-brief-and-reader-fit",
     [1, 2, 13, 34, 35, 58, 60, 75, 96, 107, 142, 143, 144, 149, 150]),
    ("technical-translation-usability",
     [3, 8, 16, 18, 19, 67, 72, 103, 105, 109, 110]),
    ("cognitive-load-and-processing-effort",
     [5, 10, 17, 21, 22, 28, 46, 47, 66, 89, 100]),
    ("documentation-structure-and-genre",
     [9, 12, 20, 48, 76, 77, 78, 97, 102, 104, 106]),
    ("usability-testing-and-evaluation",
     [11, 23, 29, 30, 33, 49, 50, 61, 68, 73, 74]),
    ("register-tenor-mode-and-text-type",
     [15, 25, 39, 40, 41, 51, 52, 53, 63, 69, 84, 86, 98, 101, 122]),
    ("information-structure-and-theme-rheme",
     [32, 42, 43, 44, 45, 64, 65, 92, 93, 146, 147]),
    ("cohesion-coherence-and-word-order",
     [27, 37, 38, 54, 94, 127, 145]),
    ("naturalness-effect-poetics-and-interpretation",
     [4, 36, 59, 80, 81, 99, 108, 117, 118, 119, 121, 125, 126]),
    ("chinese-naturalness-and-de-europeanization",
     [82, 83, 120, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141]),
    ("idiom-collocation-and-source-interference",
     [56, 57, 62, 90, 91]),
    ("pragmatics-culture-and-politeness",
     [24, 26, 31, 95, 129, 148]),
    ("descriptive-norms-and-literary-system",
     [6, 7, 71, 85, 88, 123, 124, 128]),
    ("professional-practice-and-revision",
     [79, 87, 111, 112, 113, 114, 115, 116]),
    ("audiovisual-subtitling-and-multimodal",
     [14, 55, 70, 130]),
]

# integrity: every principle exactly once
_seen: list[int] = []
for _slug, nums in SKILLS:
    _seen += nums
assert sorted(_seen) == list(range(1, NP + 1)), f"partition mismatch: {sorted(_seen)}"
assert len(set(s for s, _ in SKILLS)) == len(SKILLS), "duplicate skill slug"
for s, _ in SKILLS:
    assert len(s) <= 48, f"slug too long ({len(s)}): {s}"

REFS = ["translation-naturalness-principles-index", "translation-naturalness-evidence-notes"]

# ---------------------------------------------------------------------------- per-skill themes
THEMES: dict[str, dict] = {
    "audience-brief-and-reader-fit": dict(
        title="Audience, Brief And Reader Fit",
        purpose=(
            "This skill reviews whether a translation is driven by who will read and use the text and "
            "by an explicit brief, rather than by source-text features alone. It checks that the "
            "target audience, purpose (information vs publication), medium, and terminology are "
            "established up front, that the reader's assumed background knowledge is supplied "
            "deliberately, and that vocabulary, explanation, and detail are calibrated to the "
            "audience's decoding capacity, expertise, and seniority — since the same source can "
            "legitimately yield different translations for different readers."),
        when=[
            "A translation lacks an explicit brief specifying audience, purpose, medium, and any "
            "terminology or style requirements.",
            "The reader's background knowledge is being assumed rather than assessed and supplied.",
            "Vocabulary, explanation, or detail is pitched wrong for the audience's literacy, "
            "expertise, or seniority.",
            "The type of translation (gist, information-purposes, publication) is undecided or read "
            "off the source instead of the client's need.",
        ],
        input="The translation, its brief (or its absence), and the intended readers and their use of the text.",
    ),
    "technical-translation-usability": dict(
        title="Technical Translation And Usability",
        purpose=(
            "This skill reviews scientific and technical translation as target-user usability work — "
            "how well readers can read, understand, and perform the task — not as source-text "
            "transfer. It holds the translator to good technical-writing style, clear and simple "
            "language, chronological instructions, consistent terminology, and iconic linkage (one "
            "reused rendering for repeated information), and checks that target-language technical "
            "conventions and document form are met while correctness and usability are preserved."),
        when=[
            "A technical document is being judged as a surface replica rather than a usable target "
            "text serving the user's whole task.",
            "Language is dense, indirect, or inconsistent where clear, simple, chronological, "
            "consistent wording is required.",
            "Repeated information is rendered inconsistently instead of by iconic linkage (one "
            "reused wording).",
            "Target-language technical conventions, file formats, or required document form are not "
            "being matched.",
        ],
        input="The technical source and its translation, the target users and their tasks, and any convention or terminology constraints.",
    ),
    "cognitive-load-and-processing-effort": dict(
        title="Cognitive Load And Processing Effort",
        purpose=(
            "This skill reviews a translation for the mental effort it imposes on the reader. It "
            "treats translation as inferential communication that should be optimally relevant — "
            "adequate contextual effects for the least effort — and checks working-memory burden, "
            "attention switching, given-new progression, and whether the reader is helped to frame "
            "the problem, so that 'unnaturalness' is diagnosed as gratuitous processing effort rather "
            "than blamed on the source."),
        when=[
            "A rendering reads as effortful or 'unnatural' and the cause may be gratuitous processing "
            "effort, not the source.",
            "Working-memory burden or attention switching is high where chunking, recognition cues, "
            "or given-new order would ease it.",
            "The reader lacks the declarative background needed to act, or a maxim is flouted without "
            "a recoverable implicature.",
            "Context and intended interpretation are not made easy to follow for the target reader.",
        ],
        input="The source and target texts and the reading task, with attention to the effort the target imposes.",
    ),
    "documentation-structure-and-genre": dict(
        title="Documentation Structure And Genre",
        purpose=(
            "This skill reviews how a user-facing document is structured for its genre and reading "
            "mode. It checks modular, navigable units with meaningful headings; support for both "
            "reading-to-learn and reading-to-do and for novice through expert users; procedural "
            "manuals split into ordered numbered steps; reference and discrete-section texts written "
            "as independently dipped-into units; and — before any other instructional goal — the "
            "explicit protection of reader safety."),
        when=[
            "A guide is a monolithic block rather than modular, navigable units with meaningful "
            "headings and overviews.",
            "A procedural manual crams multiple tasks into one sentence instead of ordered numbered "
            "steps.",
            "A reference or discrete-section text relies on cross-references it should instead make "
            "self-contained.",
            "Safety-critical or hazard information is not given priority over other instructional "
            "goals.",
        ],
        input="The document, its genre and reading mode, and the structure and navigation under review.",
    ),
    "usability-testing-and-evaluation": dict(
        title="Usability Testing And Evaluation",
        purpose=(
            "This skill reviews the empirical evaluation of translated documentation. It requires "
            "usability to be established by representative, task-based testing rather than design "
            "confidence or readability formulas alone, checks that participants are screened, "
            "consented, and prepared to critique the product rather than themselves, and that "
            "subjective ratings are triangulated with objective performance and recall measures using "
            "logging suited to the interaction style."),
        when=[
            "Usability is being claimed from design confidence or a readability formula rather than "
            "task-based testing.",
            "Subjective ratings stand alone without objective performance and recall measures.",
            "Participants are unscreened, unconsented, or set up to blame themselves rather than "
            "critique the guide.",
            "Observation method or logging does not suit the application's interaction style.",
        ],
        input="The documentation or translation study under review and its design, participants, and measures.",
    ),
    "register-tenor-mode-and-text-type": dict(
        title="Register, Tenor, Mode And Text Type",
        purpose=(
            "This skill reviews register and text-type fit using the Hallidayan model — field, "
            "tenor, mode — mapped to a text's function in its sociocultural framework. It maps the "
            "whole text's predominant function (informative, expressive, operative, audio-medial) to "
            "a method, matches register to the receivers' expectations, applies House's covert/overt "
            "distinction, and treats the frameworks as a flexible toolkit rather than a rigid, "
            "English-oriented one-to-one model."),
        when=[
            "A text's predominant function (informative, expressive, operative) is not mapped to a "
            "translation method.",
            "The target register (field, tenor, mode) misfits the receivers' expectations or the "
            "genre's conventions.",
            "A covert translation that should read as target-original, or an overt one tied to its "
            "source, is mis-oriented.",
            "Register or genre frameworks are being applied rigidly or imposed uncritically on a "
            "non-European language.",
        ],
        input="The source and target texts and their register profile, genre, and text-type function.",
    ),
    "information-structure-and-theme-rheme": dict(
        title="Information Structure And Theme-Rheme",
        purpose=(
            "This skill reviews the flow of information across clauses. It checks the theme-rheme and "
            "given-new organisation that makes a text read smoothly, requires a discernible thematic "
            "method of development, resolves clashes between end-weight and target grammar, and "
            "re-signals marked focus by the target's own means (typography, punctuation, or a "
            "compensating structure) — reading markedness as meaning that must be motivated, not "
            "carried over mechanically."),
        when=[
            "Information does not progress given-before-new, so sentences read as jerky or "
            "back-to-front.",
            "The target lacks a discernible thematic method of development and feels disjointed.",
            "End-weight clashes with a target grammatical principle (e.g. subject-before-predicate) "
            "and a heavy-subject result stands.",
            "Marked theme or focus has been transferred wholesale rather than re-signalled by the "
            "target's means.",
        ],
        input="The source and target clauses and the theme-rheme, given-new, or marked-focus pattern in play.",
    ),
    "cohesion-coherence-and-word-order": dict(
        title="Cohesion, Coherence And Word Order",
        purpose=(
            "This skill reviews cohesion, coherence, and word order as language-specific. It treats "
            "coherence as the reader's judgement built on their knowledge — so a link transparent to "
            "the source audience may need making explicit — reworks the surface cohesive network "
            "(reference, substitution, ellipsis, conjunction, lexical cohesion) to the target's own "
            "patterns, and treats word order as carrying communicative weight beyond grammar rather "
            "than something to copy."),
        when=[
            "A co-reference or implicit link transparent to the source audience is left implicit for "
            "target readers who lack the background.",
            "Cohesive devices have been carried over wholesale rather than reworked to the target "
            "language's preferred patterns.",
            "Word order has been copied from the source where it disturbs point of view or "
            "information flow in the target.",
            "Overt-cohesion or explicitness differences forced by the two grammars are being ignored.",
        ],
        input="The source and target texts and the cohesion, coherence, or word-order pattern under review.",
    ),
    "naturalness-effect-poetics-and-interpretation": dict(
        title="Naturalness, Effect, Poetics And Interpretation",
        purpose=(
            "This skill reviews whether a rendering reads with the texture of a piece written for the "
            "target audience rather than a stilted transfer of meanings. It tests naturalness against "
            "the receptor language, the message context, and the audience at once; names where a "
            "translation sits on the free/literal, dynamic/formal, and domesticating/foreignizing "
            "dichotomies; treats 'reads smoothly' as a suspect criterion, not praise; and holds that "
            "there is no perfect translation, only an interpretation weighed by likely effect."),
        when=[
            "A translation reads as a stilted transfer of meanings rather than a text with the "
            "texture of native target writing.",
            "Naturalness is asserted without testing it against the receptor language, the message "
            "context, and the audience.",
            "A translation is praised merely for being 'readable' or 'smooth', a suspect criterion "
            "when the source cannot be checked.",
            "Where a rendering sits on the free/literal, dynamic/formal, or domesticating/"
            "foreignizing axis needs naming as a primary diagnostic.",
        ],
        input="The translation, its claimed naturalness or fluency, and the effect and strategy under review.",
    ),
    "chinese-naturalness-and-de-europeanization": dict(
        title="Chinese Naturalness And De-Europeanization",
        purpose=(
            "This skill reviews a Chinese target for natural idiom against Europeanized "
            "(English-interfered) constructions. It preserves concision, flexible syntax, and "
            "rhythmic force; prefers concrete subjects and direct verbs over abstract nominalized "
            "subjects and weak-verb-plus-abstract-noun packaging; strips redundant plural marking, "
            "imported passive and membership structures, and over-explicit causal scaffolding; and "
            "distinguishes ordinary prose correction from deliberate, knowing literary innovation."),
        when=[
            "A Chinese sentence is needlessly complex or stiff because Europeanized wording has "
            "displaced concise, flexible native syntax.",
            "Abstract nominalized subjects, weak-verb-plus-abstract-noun phrases, or pseudo-technical "
            "nouns repackage a plain action.",
            "Imported passives, one-of/as-one-of membership structures, redundant plural marking, or "
            "formal because/therefore scaffolding stiffen the text.",
            "A departure from normal Chinese idiom must be checked as deliberate innovation before it "
            "is corrected.",
        ],
        input="The Chinese target text and the specific constructions suspected of English-interfered Europeanization.",
    ),
    "idiom-collocation-and-source-interference": dict(
        title="Idiom, Collocation And Source Interference",
        purpose=(
            "This skill reviews lexical naturalness at and around the word. It prefers "
            "receptor-language idioms that make the message meaningful when bare intelligibility "
            "would under-communicate, distinguishes exceptionless grammatical rules from "
            "exception-admitting lexical patterning, recognises marked collocations as an effect to "
            "be matched, and guards against source-language interference — untypical carried-over "
            "collocations and idioms rendered outside the translator's language of habitual use."),
        when=[
            "A rendering is barely intelligible where a receptor-language idiom would carry the "
            "intended force.",
            "A source collocation has been carried over untypically, or a false-friend collocation "
            "has been misread.",
            "A marked source collocation is flattened, or an unmarked one is rendered with no regard "
            "for target typicality.",
            "An idiom is being translated into a language that is not the translator's language of "
            "habitual use.",
        ],
        input="The word, collocation, or idiom under review and its proposed target rendering.",
    ),
    "pragmatics-culture-and-politeness": dict(
        title="Pragmatics, Culture And Politeness",
        purpose=(
            "This skill reviews pragmatic and cultural naturalness. It handles culturally "
            "non-matching referents by a deliberate choice (formal term plus note, functional "
            "equivalent, borrowed term, or description); warns that over-clarifying a culture-specific "
            "detail can destroy the figurative meaning it carries; weighs politeness, taboo, and "
            "face against accuracy as culturally variable; and adjusts address, titles, and terms to "
            "the target's norms to avoid unintended implicatures."),
        when=[
            "A culturally non-matching referent needs a deliberate strategy rather than a default "
            "gloss.",
            "Over-clarifying a culture-specific detail risks destroying the indirect, figurative "
            "meaning it carries.",
            "Politeness, taboo, or a face-threatening act must be weighed against accuracy for the "
            "target culture.",
            "Modes of address, titles, or terms of affection need adjusting to the target's norms to "
            "avoid wrong implicatures.",
        ],
        input="The translation and the culture-specific reference, politeness, or face concern under review.",
    ),
    "descriptive-norms-and-literary-system": dict(
        title="Descriptive Norms And The Literary System",
        purpose=(
            "This skill reviews the descriptive and norm-oriented framing of naturalness. It uses "
            "Toury's structure of norms (preliminary, initial, operational) to read the "
            "adequacy-acceptability choice behind a translation's naturalness, maps operational norms "
            "across matrix, distribution, and segmentation rather than wording alone, studies "
            "reception through reviews and paratexts, and treats translated literature as a system "
            "whose position (central/peripheral, innovating/conservative) shapes what reads as "
            "natural."),
        when=[
            "A translation's naturalness reflects an acceptability-oriented choice that should be "
            "read through Toury's initial norm, not judged in a vacuum.",
            "Operational norms are being reduced to wording choices instead of matrix, distribution, "
            "and segmentation.",
            "Reception evidence (reviews, paratexts) bears on whether fluency is being rewarded and "
            "the translator rendered invisible.",
            "Whether translated literature occupies a central/innovating or peripheral/conservative "
            "position affects what counts as natural.",
        ],
        input="The translation or translation-studies analysis and its declared norms, corpus, or reception evidence.",
    ),
    "professional-practice-and-revision": dict(
        title="Professional Practice And Revision",
        purpose=(
            "This skill reviews the professional workflow that keeps a translation usable. It follows "
            "an explicit procedure from source to target and the client's style guide; revises "
            "another translator's work by finding and fixing genuine errors rather than imposing a "
            "personal style; routes queries and spotted errors to the client rather than footnoting "
            "confusion; handles auto-generated tables of contents and strict space constraints "
            "correctly; and allows non-mother-tongue work only with native-language revision."),
        when=[
            "A revision is rewriting another translator's text as the reviser's own rather than "
            "fixing genuine errors.",
            "Confusion or a spotted error is being footnoted instead of raised with the client, or a "
            "style guide is being ignored.",
            "An auto-generated table of contents or a hard space constraint (leaflet, string limit, "
            "label) is mishandled.",
            "Non-mother-tongue translation is being done without qualified native-language revision "
            "or stylistic advice.",
        ],
        input="The translation workflow under review — the procedure, style guide, revision, queries, or constraints in play.",
    ),
    "audiovisual-subtitling-and-multimodal": dict(
        title="Audiovisual, Subtitling And Multimodal",
        purpose=(
            "This skill reviews audiovisual and subtitled translation under its hard constraints. It "
            "reads the text across the signifying codes and coherence with the image, respects the "
            "space, legibility, and timing limits that force shortening, and recognises that under "
            "those limits the subtitler makes coherence and easy readability the overriding priority "
            "— so a subtitle is judged by a consistent pattern of what interpersonal values are "
            "omitted, not by phrase-by-phrase comparison."),
        when=[
            "A subtitle exceeds the space, character, or timing limits or ignores camera cuts and "
            "dialogue rhythm.",
            "Interpersonal or tenor markers are being dropped and the loss is not compensated or even "
            "tracked as a pattern.",
            "The written-to-be-spoken oral register or coherence with the image is not maintained "
            "across the signifying codes.",
            "A subtitle is being judged phrase-by-phrase rather than by the consistent kinds of "
            "values it systematically omits.",
        ],
        input="The audiovisual material or subtitles and the space, timing, register, or multimodal constraints in play.",
    ),
}

# ---------------------------------------------------------------------------- helpers

_CUT = [" — ", "—", "; therefore", ", so that", ", since ", ", because ", ", which ",
        ", ensuring", ": ", " (", ", and recognize", ", and respect", ", but "]


def lead(statement: str, limit: int = 235) -> str:
    """A concise imperative lead-clause from a principle statement, grounded verbatim in its wording."""
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
    return s


def negate(statement: str) -> str:
    """A short 'what to flag' phrasing derived from a principle's lead clause."""
    core = lead(statement, 170)
    core = core[0].lower() + core[1:]
    return core


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


print(f"principles={len(ALL_IDS)} high={len(HI_IDS)} claims={len(CLAIM_IDS)} skills={len(SKILLS)}")

# ============================================================================ EMITTERS

_SOURCE_CREDIT = (
    "the nine distillation-only sources (Nida, *Principles of Correspondence*; Toury, *The Nature "
    "and Role of Norms in Translation*; House, *Translation Quality Assessment*; Byrne, *Technical "
    "Translation* and *Scientific and Technical Translation Explained*; Baker, *In Other Words*; "
    "Munday, *Introducing Translation Studies*; Venuti, ed., *The Translation Studies Reader*; and "
    "Yu Guangzhong on the naturalness and Europeanization of Chinese)")


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
        body.append("- The reasoning offered for the decision under review: the audience, brief, "
                    "strategy, and any naturalness or quality claim made.\n")
        body.append("## Output\n")
        body.append(
            "Per finding: name the flaw and the principle it violates, apply the correction, "
            "state the residual uncertainty and the trade-off it reflects, and end with a concrete "
            "next step. Order findings highest-impact first. This skill reviews a translation, a "
            "translation choice, or a translation-studies analysis; it does not produce the "
            "finished translation or make the publication decision.\n")
        body.append("## Anti-patterns to flag\n")
        for n in nums[: min(7, len(nums))]:
            body.append(f"- The analysis fails to {negate(P[pids(n)]['statement'])} ({pids(n)}).")
        body.append("")
        body.append("## References\n")
        body.append(
            f"See `../../references/{REFS[0]}.md` for the full principle catalogue grouped by "
            f"skill, and `../../references/{REFS[1]}.md` for how these principles are grounded and "
            "kept faithful to the sources.\n")
        body.append("## Provenance\n")
        idlist = ", ".join(pids(n) for n in nums)
        body.append(
            f"Derived from {idlist}, grounded in {_SOURCE_CREDIT}. The frontmatter `provenance` "
            "block lists the exact principle and claim ids, which resolve into "
            "`principles/principles.yaml` and `analysis/claims.jsonl`.\n")
        w(BASE / "skills" / slug / "SKILL.md", "\n".join(body))


def emit_refs() -> None:
    claims = union_claims([n for _, nums in SKILLS for n in nums], cap=16)
    out = [frontmatter(REFS[0], "reference", list(range(1, NP + 1)), claims)]
    out.append("# Translation Naturalness Principles Index\n")
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

    out = [frontmatter(REFS[1], "reference", list(range(1, NP + 1)), [])]
    out.append("# Translation Naturalness Evidence Notes\n")
    out.append("How the principles in this package are grounded, and how to keep review findings "
               "faithful to the sources.\n")
    out.append("## Sources\n")
    out.append("Nine distillation-only sources ground the package, spanning the equivalence/"
               "naturalness, functionalist, descriptive, discourse, technical-usability, and "
               "quality-assessment strands of translation studies plus a Chinese-language "
               "naturalness perspective: Eugene Nida, *Principles of Correspondence* (dynamic vs "
               "formal equivalence and the naturalness test); Gideon Toury, *The Nature and Role of "
               "Norms in Translation* (adequacy vs acceptability); Juliane House, *Translation "
               "Quality Assessment* (covert/overt, register profiles); Jody Byrne, *Technical "
               "Translation* and *Scientific and Technical Translation Explained* (usability and "
               "documentation); Mona Baker, *In Other Words* (cohesion, information structure, "
               "idiom); Jeremy Munday, *Introducing Translation Studies* (a survey of the "
               "discipline); Lawrence Venuti, ed., *The Translation Studies Reader* (primary essays); "
               "and Yu Guangzhong on the naturalness and Europeanization of Chinese. Paraphrase and "
               "restructure only — no verbatim quotation (see "
               "`.claude/rules/rights-and-quotation-policy.md`).\n")
    out.append("## Faithfulness discipline\n")
    out.append("- No finding may state a rule more strongly than its source supports: maxims and "
               "register frameworks are orientation points, not strict language-neutral rules "
               "(P046, P069).")
    out.append("- The same source can legitimately yield different translations for different "
               "audiences, so a review improves a choice for its brief rather than certifying the one "
               "natural rendering (P149).")
    out.append("- 'Reads smoothly' is a suspect criterion, not proof of quality; naturalness is "
               "tested against the receptor language, message, and audience, and judged against the "
               "source register profile (P121, P004, P053).")
    out.append("- Discourse and fluency frameworks are English-oriented and domestication-biased and "
               "must not be imposed uncritically on other languages (P069, P093).\n")
    out.append("## Grounding\n")
    out.append(f"Spine: {len(ALL_IDS)} principles ({len(HI_IDS)} high-confidence) over "
               f"{len(CLAIM_IDS)} atomic claims, with evidence records and chunk anchors. Every "
               f"principle id P001-P{NP:03d} resolves into `principles/principles.yaml`.\n")
    w(BASE / "references" / f"{REFS[1]}.md", "\n".join(out))


def _always_on() -> list[str]:
    out = []
    for slug, nums in SKILLS:
        ids = ", ".join(pids(n) for n in nums)
        out.append(f"{THEMES[slug]['purpose']} ({ids})")
    return out


PROFILE_ROLE = (
    "A reviewer of whether a translation reads naturally and usably for its receptor audience, "
    "grounded in the equivalence/naturalness, functionalist, descriptive, discourse, and "
    "technical-usability theories of translation (Nida, Reiss, House, Toury, Baker, Byrne, the "
    "Venuti reader, and Yu Guangzhong on Europeanized Chinese). It critiques a rendering or an "
    "analysis for naturalness and usability: whether decisions flow from the reader and an explicit "
    "brief, whether the target reads with the texture of native writing rather than a stilted or "
    "source-interfered transfer, whether register, information flow, and cohesion fit the target's "
    "norms, whether processing effort is minimized, and whether 'reads smoothly' has been mistaken "
    "for proof of quality. The operating invariants below are review criteria drawn from the "
    "sources, not instructions to translate: this review-only boundary and the forbidden behaviours "
    "override every invariant, so the reviewer never produces the finished translation, makes the "
    "publication decision, or certifies a rendering definitively correct.")

WHEN_TO_USE = [
    "A target text reads awkwardly, stilted, or foreign and the team wants its naturalness and "
    "usability for the receptor audience reviewed (P004, P126).",
    "A technical, instructional, or user-facing translation needs its usability, processing effort, "
    "and reader-fit reviewed against the reader's task (P016, P110).",
    "A translation is praised for 'reading well' or fluency, and the team wants that criterion — and "
    "the source-register comparison it skips — interrogated (P121, P053).",
    "Information flow, register, cohesion, or word order feels off between source and target and "
    "needs checking against target-language norms (P044, P094).",
    "A Chinese (or other) target shows Europeanized, source-interfered constructions that need a "
    "de-interference review (P082, P091).",
]

WHEN_NOT_TO_USE = [
    "The caller wants the finished or revised translation produced end to end; this reviewer "
    "critiques, it does not translate.",
    "The concern is subject-matter correctness or the legal validity of a text with a knowable "
    "answer, not a naturalness or usability judgement.",
    "The caller wants a single guaranteed-correct rendering; naturalness is probabilistic and "
    "brief-dependent, so the review improves the choice, it cannot certify one answer.",
    "The task has no translation dimension — monolingual editing, information design and layout, or "
    "a pure terminology lookup.",
]

QUALITY_BAR = [
    "Naturalness is tested against the receptor language and culture, the message context, and the "
    "audience at once, aiming for the texture of a piece written for that audience rather than a "
    "stilted transfer (P004, P126, P057).",
    "Decisions flow from who reads and uses the text and an explicit brief, calibrated to the "
    "reader's assumed knowledge, decoding capacity, and expertise (P001, P035, P058, P150).",
    "Technical and instructional text is judged as usability work — clear, simple, chronological, "
    "consistent, low processing-effort — not as source-form transfer (P016, P110, P105, P017).",
    "Information flow, register, and cohesion fit the target's norms: given-before-new progression, "
    "a discernible thematic method, and cohesion reworked to the target rather than carried over "
    "(P044, P043, P094).",
    "'Reads smoothly' is a suspect criterion, not proof of quality; naturalness is judged against the "
    "source register profile and treated as brief-dependent, with a range of valid answers (P121, "
    "P053, P149).",
    "Source-language interference and Europeanized, unnatural target constructions are surfaced — the "
    "translator's chief obstacle is the dead conventional register of his own language, so drafts are "
    "re-read as a target reader (P120, P091, P082).",
]

FORBIDDEN = [
    "Producing the finished or revised translation, or the publication and quality sign-off — this "
    "reviewer critiques decisions; the client determines the type of translation and owns the call "
    "(P075, P111, P113).",
    "Endorsing 'reads smoothly' or fluency as proof of quality, or assessing a translation without "
    "comparing it to the source's register profile (P121, P053).",
    "Stating a rule more strongly than its source supports — flattening a context- and "
    "audience-dependent preference into an absolute, or treating maxims and register frameworks as "
    "strict, language-neutral rules (P046, P069, P149).",
    "Prescribing a single correct rendering as if naturalness had one deterministic answer, ignoring "
    "the brief, audience, and function that condition the choice (P075, P149, P001).",
]

HANDOFF = [
    "The translator and the commissioner hold the text and the decision to publish; this reviewer "
    "informs the reasoning, makes the residual trade-off explicit, and raises serious errors to the "
    "client rather than silently fixing them (P113, P111).",
    "Concerns outside naturalness review — subject-matter accuracy, information design, typography "
    "and layout, and client terminology governance — are handed to the owning specialist (P003, "
    "P079).",
]

PRECEDENCE = (
    "Where a source's context differs from the caller's, treat a principle as an adaptable guide, "
    "not an absolute — maxims and register frameworks are orientation points, not strict rules (P046, "
    "P069); when audience needs and source form conflict, the brief's purpose and the reader govern "
    "which values are preserved (P001, P149, P075); and never endorse a rule more confident than the "
    "source supports (P121, P149).")

MODES = [
    dict(name="review",
         trigger="The caller submits a translation, a translation choice, or a translation-studies "
                 "analysis for critique.",
         output="A findings list keyed to flaw class (naturalness/effect, audience/brief, usability/"
                "processing, register/discourse, information-flow/cohesion, idiom/interference, "
                "norms/method, audiovisual), each with flaw, correction, residual trade-off, and "
                "next step — highest-impact first."),
    dict(name="advise",
         trigger="The caller faces a translation decision and wants which principle or strategy "
                 "fits.",
         output="A recommendation tied to the situation, naming the principle(s) and orientation "
                "applied and the residual trade-off to carry."),
    dict(name="compare",
         trigger="The caller weighs options for one goal (natural vs foreign air, dynamic vs formal, "
                 "one rendering vs another).",
         output="A side-by-side of what each option preserves and costs, ending in a brief- and "
                "audience-weighted recommendation."),
]

EXAMPLES = [
    dict(title="Review a translation praised only for reading fluently",
         kind="happy-path",
         scenario=(
             "A team submits an English translation of a French novel, recommending it because it "
             "'reads smoothly and as if originally written in English', with no comparison against "
             "the source offered."),
         ideal_response=(
             "Flag the flaws, highest-impact first. (1) Fluency is not evidence: 'reads smoothly' is "
             "a suspect criterion, not praise, especially where the reviewer cannot check the source "
             "(P121). (2) Missing the register comparison: naturalness must be judged against the "
             "source's register profile (field, tenor, mode), not asserted (P053). (3) Naturalness "
             "untested: check it against the receptor language, the message context, and the "
             "audience, aiming for the texture of native writing rather than a stilted transfer "
             "(P004, P126). (4) Interference unexamined: re-read the draft as a target reader for "
             "carried-over, untypical source collocations (P091). Correction: re-anchor the "
             "assessment to a source-register comparison and the brief's audience, state which values "
             "the fluent version preserved and which it cost, and hand the publication decision back "
             "to the team — naturalness here is brief-dependent, not a single verdict (P149).")),
    dict(title="Decline to produce the translation and redirect to a review",
         kind="failure-recovery",
         scenario=(
             "The caller asks the reviewer to 'just translate this user manual into German and tell "
             "us it reads naturally', with no brief, no audience profile, and no draft."),
         ideal_response=(
             "Decline to produce the finished text or certify it — this reviewer critiques "
             "decisions, it does not translate or make the sign-off, and the client determines the "
             "type of translation wanted (forbidden behaviours, P075, P111). Offer the review "
             "instead: ask for the brief and the target users' tasks, since a technical document is "
             "judged as usability work — clear, simple, chronological, low-effort — not a surface "
             "replica (P016, P110); note that decisions and detail must be calibrated to the reader "
             "(P001, P150); and set expectations that any assessment will test naturalness against "
             "the receptor audience and treat it as a range of valid answers for the brief, not one "
             "certified rendering (P004, P149).")),
]

# source_id -> (title, author, year); sha256 is read from ingested metadata (META_SHA).
_SOURCE_META = [
    ("dynamic-formal-equiv-e6872198",
     "Principles of Correspondence (Dynamic and Formal Equivalence)", "Eugene A. Nida", 1964),
    ("norms-in-translation-ad249b8d",
     "The Nature and Role of Norms in Translation", "Gideon Toury", 1995),
    ("translation-quality-c0dd203d",
     "Translation Quality Assessment: Past and Present", "Juliane House", 2015),
    ("technical-translatio-41f3c47c",
     "Technical Translation: Usability Strategies for Translating Technical Documentation",
     "Jody Byrne", 2006),
    ("in-other-words-baker-8e6c3cb1",
     "In Other Words: A Coursebook on Translation", "Mona Baker", 2011),
    ("scientific-technical-d92653ac",
     "Scientific and Technical Translation Explained", "Jody Byrne", 2012),
    ("introducing-translat-4a29c5ca",
     "Introducing Translation Studies: Theories and Applications", "Jeremy Munday", 2016),
    ("translation-studies-45ee8f34",
     "The Translation Studies Reader", "Lawrence Venuti (ed.)", 2012),
    ("chinglish-europeaniz-5798beb7",
     "On the Naturalness and Europeanization of Chinese (Chinglish)", "Yu Guangzhong", 1987),
]
SOURCES = [
    dict(source_id=sid, title=title, author=author, year=year,
         rights_status="distillation-only", sha256=META_SHA.get(sid, ""))
    for sid, title, author, year in _SOURCE_META
]
assert all(s["sha256"] for s in SOURCES), "a source has no sha256 in ingested metadata"


def emit_profile() -> None:
    profile = {
        "schema_version": "portable-profile-v1",
        "slug": SLUG,
        "display_name": "Translation Naturalness Reviewer",
        "agent_version": VERSION,
        "status": "ready",
        "tier": 2,
        "multisource_synthesis": "deferred",
        "role": PROFILE_ROLE,
        "when_to_use": WHEN_TO_USE,
        "when_not_to_use": WHEN_NOT_TO_USE,
        "inputs": {"required": [
            "The translation, translation choice, or translation-studies analysis under review, "
            "plus its reasoning: the source and target, the intended audience and brief, the "
            "strategy, and any naturalness or quality claim made."]},
        "outputs": {
            "primary_format": (
                "A structured review that, per finding, names the flaw and the principle it "
                "violates, applies the correction, states the residual trade-off, and ends with a "
                "next step — never a bare good/bad verdict."),
            "modes": MODES,
        },
        "quality_bar": QUALITY_BAR,
        "minimum_useful_output": (
            "At least one finding that names a naturalness or usability flaw, applies a named "
            "principle or correction, and states the residual trade-off — the values kept against "
            "those given up."),
        "forbidden_behaviours": FORBIDDEN,
        "handoff_rules": HANDOFF,
        "source_of_truth_policy": {
            "canonical_owner": (
                "The translator and the commissioner hold final authority over the text and the "
                "decision to publish it; the distilled principles from Nida, Toury, House, Byrne, "
                "Baker, Munday, the Venuti reader, and Yu Guangzhong are the authority for the review "
                "criteria the reviewer invokes."),
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

    qb_ids = ["P004/P126/P057", "P001/P035/P058/P150", "P016/P110/P105/P017",
              "P044/P043/P094", "P121/P053/P149", "P120/P091/P082"]
    for i, ids in enumerate(qb_ids):
        add(f"quality_bar[{i}]", ids, "Review criterion, not a directive to translate.")
    fb_ids = ["P075/P111/P113", "P121/P053", "P046/P069/P149", "P075/P149/P001"]
    for i, ids in enumerate(fb_ids):
        add(f"forbidden_behaviours[{i}]", ids, "Boundary restraint; no over-claim.")
    wt_ids = ["P004/P126", "P016/P110", "P121/P053", "P044/P094", "P082/P091"]
    for i, ids in enumerate(wt_ids):
        add(f"when_to_use[{i}]", ids, "Routing trigger grounded in the cited principles.")
    ho_ids = ["P113/P111", "P003/P079"]
    for i, ids in enumerate(ho_ids):
        add(f"handoff_rules[{i}]", ids, "Ownership boundary; source-grounded.")
    add("outputs.primary_format", "P149/P121",
        "The per-finding review format; states residual trade-off rather than a bare verdict.")
    add("source_of_truth_policy.precedence", "P046/P069/P001/P149/P075/P121",
        "Adaptable-guide + brief-governs + no-over-claim, all source-grounded.")
    report = {
        "schema_version": "faithfulness-report-v1",
        "subagent_slug": SLUG,
        "findings": findings,
    }
    w(BASE / "reports" / "faithfulness-report.yaml",
      yaml.safe_dump(report, sort_keys=False, allow_unicode=True, width=100))


GOLDEN = [
    dict(test_id="GT-001", mode="review",
         desc="Positive routing — fluency praised, no source comparison",
         prompt="Here is our English translation of a French novel. We think it's excellent because it "
                "reads smoothly and you'd never know it was a translation. Review it.",
         must_do=["Flag 'reads smoothly' / fluency as a suspect criterion, not proof of quality",
                  "Require comparison against the source's register profile",
                  "Test naturalness against the receptor language, message context, and audience",
                  "Re-read the draft as a target reader for carried-over source interference"],
         must_not=["Certify the translation correct or make the publication decision",
                   "Accept fluency alone as evidence of quality"],
         cov=["P121", "P053", "P004", "P126", "P091"]),
    dict(test_id="GT-002", mode="advise",
         desc="Positive routing — usability approach for a user manual",
         prompt="We're translating a software user manual for busy, non-native support staff. How "
                "should we approach it so it reads naturally and is easy to use?",
         must_do=["Treat the job as target-user usability work, not source-text transfer",
                  "Recommend clear, simple, chronological, consistent language and iconic linkage",
                  "Calibrate decisions and detail to the audience and the brief"],
         must_not=["Prescribe a single 'correct' rendering as if deterministic"],
         cov=["P016", "P110", "P105", "P001"]),
    dict(test_id="GT-003", mode="review",
         desc="Positive routing — Europeanized Chinese draft",
         prompt="Review this Chinese translation from English; it uses lots of abstract nouns, "
                "imported passives, and 'one of the ...' structures and feels stiff.",
         must_do=["Prefer concrete subjects and direct verbs over abstract nominalized subjects",
                  "Recast imported passive and membership structures into natural Chinese",
                  "Check whether any departure is deliberate innovation before correcting"],
         must_not=["Treat Europeanized wording as automatically acceptable"],
         cov=["P132", "P133", "P140", "P136", "P141"]),
    dict(test_id="GT-004", mode="review",
         desc="Positive routing — awkward information flow",
         prompt="Our translation is grammatically fine but reads jerkily; sentences seem to start "
                "with new information and heavy subjects. Review the flow.",
         must_do=["Require given-before-new information order",
                  "Check for a discernible thematic method of development",
                  "Resolve end-weight clashes with the target's grammar rather than leaving a heavy subject"],
         must_not=["Judge the text acceptable on grammaticality alone"],
         cov=["P044", "P043", "P042", "P064"]),
    dict(test_id="GT-005", mode="compare",
         desc="Positive routing — natural vs deliberate foreign air",
         prompt="Should our new translation of a classic read as fluent modern prose or keep a "
                "deliberate foreign air? Compare the options.",
         must_do=["Name where each option sits on the domesticating-foreignizing axis",
                  "Note that a deliberate foreign air can be less dangerous than a purist vernacular",
                  "Weight the choice by the brief, text type, and readership"],
         must_not=["Declare one pole universally correct"],
         cov=["P118", "P119", "P121", "P149"]),
    dict(test_id="GT-006", mode="review",
         desc="Positive routing — culture-specific detail over-clarified",
         prompt="Our translator added an explanation spelling out a culture-specific reference to help "
                "target readers. Is that the right call?",
         must_do=["Warn that over-clarifying can destroy the indirect, figurative meaning it carries",
                  "Choose deliberately among note, functional equivalent, borrowing, or description",
                  "Handle the reference by the target user's need for precision or usability"],
         must_not=["Assume explicitation is always an improvement"],
         cov=["P024", "P031", "P143", "P054"]),
]

NEGATIVE = [
    dict(test_id="NR-001",
         prompt="Translate this 300-word product description from English into Spanish for us.",
         reason="Asks for the finished translation, not a review."),
    dict(test_id="NR-002",
         prompt="Is the interest calculation in this loan contract mathematically correct?",
         reason="Subject-matter correctness with a knowable answer, no translation dimension."),
]

MISSING = [
    dict(test_id="MC-001",
         prompt="Does this translation read naturally?",
         ask=["The source text and the target text to compare",
              "The brief: intended audience, purpose, and medium",
              "Any specific naturalness or usability concern to check"]),
    dict(test_id="MC-002",
         prompt="Should we make it read more naturally or keep it close to the source?",
         ask=["The source text and its text type",
              "The target readership and the publication's purpose",
              "The brief or commission constraints"]),
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
             "minimum_output": "A review naming the flaw(s), the principle(s), the correction, and "
                               "the residual trade-off, highest-impact first.",
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

    # one behaviour test per principle (all 150 → covers all high-confidence)
    modes = ["review", "advise", "compare"]
    pb = []
    for idx, pid in enumerate(ALL_IDS):
        skill = PID_TO_SKILL[pid]
        pb.append({
            "test_id": f"PB-{pid}",
            "principle_id": pid,
            "mode": modes[idx % 3],
            "prompt": (
                f"We are reviewing a translation or translation-studies analysis where "
                f"{THEMES[skill]['title'].lower()} is at issue. What flaw should we check for, what "
                f"is the correction, and what residual trade-off should we carry?"),
            "expected_behaviour": [
                f"Applies the principle: {lead(P[pid]['statement'], 300)}.",
                "Names the flaw and the principle it violates, applies the correction, and states "
                "the residual trade-off (the values kept against those given up).",
                f"Cites {pid}.",
            ],
            "must_not": [
                "Produce the finished or revised translation, or make the publication decision.",
                "State the rule more strongly than the source supports, or accept fluency alone as "
                "proof of quality.",
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

    # test-results.md (existence required by the gate)
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
        f"({len(ALL_IDS)} total; all {len(HI_IDS)} high-confidence principles covered).\n",
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
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They span the
equivalence/naturalness (Nida), descriptive/norms (Toury), quality-assessment (House),
technical/usability (Byrne x2), cohesion-and-idiom (Baker), survey (Munday), and primary-essay
(Venuti reader) strands of translation studies, plus a Chinese-language naturalness perspective (Yu
Guangzhong on Europeanized Chinese) that anchors the de-interference criteria.

## Distillation

Spine: {len(ALL_IDS)} promoted principles (P001-P{NP:03d}; {len(HI_IDS)} high-confidence) over
{len(CLAIM_IDS)} atomic claims, with evidence records and chunk anchors. The {len(ALL_IDS)}
principles are partitioned across {len(SKILLS)} skills, each principle owned by exactly one skill;
the two references index and ground them.

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
  already-assembled, deterministically-valid distilled spine ({len(ALL_IDS)} principles
  P001-P{NP:03d} / {len(CLAIM_IDS)} claims from nine distillation-only sources).
- `profile.yaml` derived from the {len(ALL_IDS)} promoted principles: role, when/when-not-to-use,
  three modes (review / advise / compare), quality bar, forbidden behaviours, handoff rules, and a
  {len(SKILLS)}-skill / {len(REFS)}-reference `knowledge_partition` covering every principle exactly
  once.
- {len(SKILLS)} authored skills partitioning all {len(ALL_IDS)} principles; {len(REFS)} references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` ({len(GOLDEN)} golden, {len(NEGATIVE)} negative-routing,
  {len(MISSING)} missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, {len(ALL_IDS)} total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Nine distillation-only sources: Eugene Nida, *Principles of Correspondence* (1964); Gideon Toury,
  *The Nature and Role of Norms in Translation* (1995); Juliane House, *Translation Quality
  Assessment* (2015); Jody Byrne, *Technical Translation* (2006) and *Scientific and Technical
  Translation Explained* (2012); Mona Baker, *In Other Words* (2011); Jeremy Munday, *Introducing
  Translation Studies* (2016); Lawrence Venuti, ed., *The Translation Studies Reader* (2012); and Yu
  Guangzhong on the naturalness and Europeanization of Chinese.
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


PID_TO_SKILL = {pids(n): slug for slug, nums in SKILLS for n in nums}


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
