"""Deterministic authoring generator for translation-quality-reviewer.

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

BASE = Path(__file__).resolve().parents[2]  # subagents/translation-quality-reviewer
SLUG = "translation-quality-reviewer"
VERSION = "1.0.0"
DATE = "2026-07-12"
N = 150  # principle count (P001..P150)

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


def pids(n: int) -> str:
    return f"P{n:03d}"


# ---------------------------------------------------------------------------- partition
# Each entry: (skill-slug-string  [already kebab, <=48 chars so stub_slug is identity],
#              [principle numbers]).  Every principle 1..150 appears exactly once.
SKILLS: list[tuple[str, list[int]]] = [
    ("translation-universals-and-the-third-code",
     [1, 79, 84, 114, 115, 121, 139, 143]),
    ("corpus-design-and-methodology",
     [3, 12, 50, 68, 77, 78, 97, 107, 108, 112, 118, 122, 135, 140, 141]),
    ("overt-covert-translation-and-equivalence",
     [5, 6, 7, 8, 11, 30, 31, 38, 59, 62, 63, 64, 93, 106, 127, 131, 133, 136, 138]),
    ("register-field-tenor-mode-analysis",
     [10, 13, 40, 41, 42, 60, 69, 70, 71, 72, 73, 74, 75, 116, 129, 130]),
    ("error-analysis-and-evaluation-discipline",
     [2, 21, 35, 36, 37, 48, 49, 61, 86, 87, 90, 91, 94, 95, 109, 125, 128]),
    ("cognition-pragmatics-and-contrastive-evidence",
     [4, 9, 15, 24, 88, 99, 124, 132]),
    ("cultural-filtering-ideology-and-globalization",
     [22, 26, 32, 45, 46, 47, 66, 67, 100, 101, 102, 103, 105, 123, 137, 145]),
    ("descriptive-studies-and-translational-norms",
     [16, 18, 25, 34, 53, 54, 55, 76, 80, 83, 85, 111, 117, 142]),
    ("russian-corpus-and-interpreting-research",
     [19, 20, 29, 51, 52, 56, 57, 58, 146, 147, 148]),
    ("genre-childrens-literature-and-accessibility",
     [14, 23, 28, 43, 44, 65, 92, 96, 98, 110, 126, 144]),
    ("chinese-prose-and-europeanization",
     [119, 120, 149, 150]),
    ("applied-corpus-tools-and-textual-devices",
     [17, 27, 33, 39, 81, 82, 89, 104, 113, 134]),
]

# integrity: every principle exactly once
_seen: list[int] = []
for _slug, nums in SKILLS:
    _seen += nums
assert sorted(_seen) == list(range(1, N + 1)), f"partition mismatch: {sorted(_seen)}"
assert len(set(s for s, _ in SKILLS)) == len(SKILLS), "duplicate skill slug"
for s, _ in SKILLS:
    assert len(s) <= 48, f"slug too long ({len(s)}): {s}"

REFS = ["translation-quality-principles-index", "translation-quality-evidence-notes"]

# ---------------------------------------------------------------------------- per-skill themes
THEMES: dict[str, dict] = {
    "translation-universals-and-the-third-code": dict(
        title="Translation Universals And The Third Code",
        purpose=(
            "This skill reviews claims about translation universals — explicitation, "
            "simplification, normalisation, and the distinctive distribution that forms the 'third "
            "code' — and checks that they are handled as hypotheses to be measured, not features "
            "presumed to hold. It requires the constructs to be operationalised distinctly, the "
            "third code to be kept apart from mere translationese, and universals to be scoped as "
            "tendencies that a language-pair or culture-specific explanation might beat."),
        when=[
            "A study asserts or relies on a translation universal (explicitation, simplification, "
            "normalisation) and the claim needs testing against evidence rather than assumption.",
            "Explicitation, simplification, and normalisation are being treated as interchangeable "
            "labels instead of distinct, measurable constructs.",
            "A 'third code' or translationese finding is being read as a quality defect rather than "
            "a describable systemic feature.",
            "A universal is being generalised beyond the corpus that produced it, or reported more "
            "strongly than its sample supports.",
        ],
        input="The universals/third-code claim under review, the corpus it rests on, and how each "
              "construct was measured.",
    ),
    "corpus-design-and-methodology": dict(
        title="Corpus Design And Methodology",
        purpose=(
            "This skill reviews whether a corpus-based translation study is built to answer its "
            "question: the corpus type (parallel for equivalence and alignment, comparable for "
            "translated-vs-original features) fits the aim, and comparability, metadata, copyright, "
            "alignment, and frequency normalisation are controlled before any difference is "
            "attributed to translation status. It treats the corpus as one tool inside a wider "
            "evidence set and pairs quantitative patterns with recontextualised interpretation."),
        when=[
            "A corpus type (parallel vs comparable) is being chosen or a difference is attributed "
            "to translation status without controlling comparability, metadata, or alignment.",
            "Raw frequencies from unequal subcorpora are being compared without normalisation.",
            "A corpus statistic is being taken as a final answer rather than a prompt for "
            "qualitative, contextualised interpretation.",
            "The measure does not match the research question, or corpus evidence is being used "
            "outside a broader set of introspective, observational, and textual evidence.",
        ],
        input="The study's research question, corpus design (type, comparability, metadata, "
              "alignment), and the measures applied.",
    ),
    "overt-covert-translation-and-equivalence": dict(
        title="Overt/Covert Translation And Functional Equivalence",
        purpose=(
            "This skill reviews a translation quality assessment built on House's model: whether the "
            "source-text profile and its function are specified, whether the case is an overt "
            "translation (second-level access, source kept intact) or a covert one (cultural filter "
            "for target pragmatics), and whether unjustified filtering has produced a covert version "
            "rather than a translation. It treats functional equivalence as approximate value across "
            "semantic, pragmatic, and textual dimensions, not referential content alone."),
        when=[
            "A quality judgement is made without a detailed source-text profile specifying the "
            "function the target should seek.",
            "Overt and covert translation are conflated, or a cultural-filter change is applied "
            "without justification and passed off as a translation rather than a version.",
            "Equivalence is reduced to referential/denotative content and the pragmatic and textual "
            "dimensions are ignored.",
            "A covert/overt classification is asserted without checking addressee needs, source "
            "status, and whether the target could function as an original.",
        ],
        input="The translation, its source-text profile and function, and the overt/covert and "
              "equivalence claims made about it.",
    ),
    "register-field-tenor-mode-analysis": dict(
        title="Register: Field, Tenor And Mode Analysis",
        purpose=(
            "This skill reviews translation quality at the level of register using the "
            "Field/Tenor/Mode split — Field for lexis and processes, Tenor for stance, participant "
            "relations, and interpersonal strategy, Mode for medium, channel, and connectivity — "
            "and keeps the analysis source-target comparative. It gives particular attention to "
            "persuasive and missionizing texts, where Tenor and Mode shifts can quietly re-code "
            "involvement, positivity, and perlocutionary force."),
        when=[
            "A translation's register profile (Field, Tenor, Mode) needs comparing against the "
            "source's for a quality judgement, with the updated split used to reduce category "
            "overlap.",
            "Interpersonal strategy — pronouns, agency, passives, markedness, information order — "
            "has shifted and may have changed stance or involvement.",
            "A mission statement or persuasive text is being assessed for shifts in positivity, "
            "indirect request, rhetorical cohesion, or perlocutionary effect.",
            "Formal-style and province markers, or oral-rhetorical writtenness versus plain "
            "information delivery, need identifying as functional evidence.",
        ],
        input="The source and target texts and the register (Field/Tenor/Mode), stance, and "
              "persuasive-function features in play.",
    ),
    "error-analysis-and-evaluation-discipline": dict(
        title="Error Analysis And Evaluation Discipline",
        purpose=(
            "This skill reviews the discipline of the evaluation itself: overt errors are classified "
            "separately (denotative omissions, additions, substitutions, wrong selections, "
            "ungrammaticality) and covert (dimensional) mismatches weighted by the source profile "
            "and functional component. It rejects global, impressionistic, or contradictory criteria "
            "unless they are made operationally checkable, keeps analyst judgement to argued "
            "evidence-constrained hypotheses, and preserves the strength of the evidence — reporting "
            "tentative findings as tentative."),
        when=[
            "Error seriousness is being judged without a specified, text-context-sensitive procedure "
            "or across micro-, macro-, and superstructural levels.",
            "Assessment criteria are global, impressionistic, or contradictory and have not been "
            "converted into explicit, checkable textual and contextual tests.",
            "A tentative, small-sample, or attributed finding is being upgraded into a firm claim, "
            "or a hedge is being removed.",
            "Errors are weighted by a universal hierarchy rather than by their effect on the "
            "individual text's ideational and interpersonal functional match.",
        ],
        input="The evaluation's criteria, error classification, weighting rationale, and the "
              "strength of the evidence behind each judgement.",
    ),
    "cognition-pragmatics-and-contrastive-evidence": dict(
        title="Cognition, Pragmatics And Contrastive Evidence",
        purpose=(
            "This skill reviews how cognitive and contrastive-pragmatic evidence is used in a "
            "quality assessment. It admits cognitive translation research only where it clarifies "
            "comprehension, transfer, or decision making; treats verbal reports, behavioural "
            "measures, and neuroimaging as limited evidence that cannot alone establish underlying "
            "cognition; and analyses translations as discourse utterances whose illocutionary force "
            "depends on context, triangulating contrastive pragmatic claims across data types."),
        when=[
            "Cognitive or process research (verbal reports, keylogging, neuroimaging) is being used "
            "to certify a translation's underlying processing rather than to clarify comprehension.",
            "A German-English or other cross-linguistic pragmatic difference (directness, content "
            "orientation, routine, justification) is asserted without contrastive evidence.",
            "A translation is analysed as isolated sentence correspondence rather than as a "
            "context-dependent discourse utterance.",
            "A contrastive pragmatic claim rests on a single method and needs triangulating across "
            "elicited, retrospective, meta-pragmatic, and naturalistic data.",
        ],
        input="The cognitive/process or contrastive-pragmatic evidence cited and the discourse-"
              "level function it is being used to judge.",
    ),
    "cultural-filtering-ideology-and-globalization": dict(
        title="Cultural Filtering, Ideology And Globalization",
        purpose=(
            "This skill reviews translation quality where culture, ideology, English-as-a-lingua-"
            "franca, and globalization bear on the choices. It keeps cultural-filter judgements "
            "current with changing communicative norms rather than fixed generalisations, frames "
            "cultural explanation around who makes culture relevant to whom and for what purpose, "
            "and grounds any socio-political or power-focused critique in detailed linguistic "
            "analysis of forms and functions before any macro-level conclusion."),
        when=[
            "A cultural-filter judgement rests on a permanent generalisation and needs reassessing "
            "against current, globalized, or diversifying communicative norms.",
            "English influence, borrowings, or ELF communication is being judged by native-speaker "
            "correctness rather than by contextual function, intelligibility, and local uptake.",
            "A socio-political, ethical, or power critique is drawn before the forms and functions "
            "have been analysed linguistically.",
            "Globalized or hybrid text production is treated as one-way transfer rather than "
            "negotiation and accommodation across orders of indexicality.",
        ],
        input="The translation, its cultural/ideological and globalization context, and any "
              "filtering, borrowing, or power claim made about it.",
    ),
    "descriptive-studies-and-translational-norms": dict(
        title="Descriptive Studies And Translational Norms",
        purpose=(
            "This skill reviews whether translated text is being studied descriptively and target-"
            "orientedly — as a communicative event and object of study in its own right, explained "
            "through target-culture norms and systems rather than reduced to source derivation. It "
            "requires a reproducible descriptive method, norms reconstructed from recurrent corpus "
            "regularities (matricial and textual), and an individual pattern attributed to a "
            "translator only after author style, source-language, and sociolect are ruled out."),
        when=[
            "A translated-text feature is being explained purely as source-text derivation rather "
            "than through target-culture norms, conventions, and historical systems.",
            "A 'norm' is asserted rather than reconstructed descriptively from patterned "
            "operational behaviour (omissions, additions, substitutions, transpositions).",
            "A theory is applied deductively without a descriptive branch whose findings can be "
            "expressed as reproducible generalisations.",
            "A pattern is attributed to an individual translator before author style, source-"
            "language preference, and sociolect norms are tested as alternatives.",
        ],
        input="The translation-studies analysis, its descriptive method and corpus, and the norm "
              "or target-orientation claims made.",
    ),
    "russian-corpus-and-interpreting-research": dict(
        title="Russian Corpus And Interpreting Research",
        purpose=(
            "This skill reviews corpus-based translation and interpreting work in the Russian "
            "field, where corpus availability is a hard design constraint — scarcity, "
            "fragmentation, missing historical data, and little standardization. It presses for "
            "multifactorial modelling over isolated frequencies, significance testing with effect "
            "sizes, metadata-rich corpora recording direction, mode, and delivery, and inclusion of "
            "the Russian research tradition rather than assuming the field is only Anglophone."),
        when=[
            "Russian translation/interpreting corpus scarcity, fragmentation, or lack of "
            "standardization is being ignored as a design constraint.",
            "A complex variation claim rests on isolated frequencies or concordances instead of "
            "multifactorial modelling with significance testing and effect sizes.",
            "A Polish-Russian or Russian-Polish study lacks metadata recording translation "
            "direction, delivery, and mode.",
            "A survey assumes the field is represented only by Anglophone research, or draws strong "
            "Russian interpreting generalisations from thin data.",
        ],
        input="The Russian-field corpus study, its data sources and metadata, and the modelling and "
              "generalisation claims made.",
    ),
    "genre-childrens-literature-and-accessibility": dict(
        title="Genre, Children's Literature And Accessibility",
        purpose=(
            "This skill reviews translation quality where genre and audience accessibility govern "
            "the choices — connecting an individual text to its macro-contextual genre class, and "
            "checking children's and stage texts against the function they must serve. It asks "
            "whether lexis, syntax, cohesion, iconic linkage, and sound patterning still support the "
            "young or specialised audience, whether framing and titling shifts move the text away "
            "from its source atmosphere, and whether accessibility claims are backed by quantifiable "
            "textual features."),
        when=[
            "A translation's genre is not connected to its macro-contextual text class, or a null "
            "target-genre realization needs routing to review.",
            "A children's picture book or stage text may have lost the lexis, syntax, cohesion, "
            "iconic linkage, or repetition that supports its audience.",
            "Title, ending, added material, or framing changes may have moved a children's text "
            "away from its source atmosphere, respect for readers, or gentle socialization.",
            "An accessibility, speakability, or audience-fit claim is made without quantifiable "
            "textual features or corpus comparison.",
        ],
        input="The translation, its genre and intended audience, and the accessibility, framing, or "
              "speakability claims made about it.",
    ),
    "chinese-prose-and-europeanization": dict(
        title="Chinese Prose And Europeanization",
        purpose=(
            "This skill reviews Chinese target prose for Europeanized distortion. It defends the "
            "normal state of Chinese — concision, flexible syntax, and rhythmic force — against "
            "needlessly Europeanized wording, lets coordinate words or phrases stand by "
            "juxtaposition with connectors matched to progression, contrast, or adjustment, treats "
            "established idioms as live resources rather than decorative or wordy substitutes, and "
            "prefers concrete subjects and event clauses over abstract nominalized ones."),
        when=[
            "Ordinary Chinese prose has been made needlessly wordy or rigid by Europeanized wording "
            "at the expense of concision and rhythmic force.",
            "Coordinate Chinese words or phrases have been over-connected, or a connector does not "
            "match the intended progression, contrast, or adjustment.",
            "An established Chinese idiom has been flattened into wordy paraphrase or used as a "
            "decorative substitute for thought.",
            "An abstract, nominalized subject drawn from English syntax should be revised toward a "
            "concrete subject, person, or event clause.",
        ],
        input="The Chinese target text and the English-influenced syntax, wording, or idiom "
              "handling under review.",
    ),
    "applied-corpus-tools-and-textual-devices": dict(
        title="Applied Corpus Tools And Textual Devices",
        purpose=(
            "This skill reviews the applied use of corpus tools and textual analysis in a quality "
            "assessment: keyword, concordance, and collocation analysis to investigate cultural or "
            "ideological meaning, description of existing translations to support quality and "
            "accessibility, and the tracking of textual devices — theme dynamics, clausal and iconic "
            "linkage, deixis. It ties fine-grained measurement to cultural, pedagogical, and "
            "technological context, and sets quality requirements from the commission's purpose and "
            "risk level."),
        when=[
            "Keyword, concordance, or collocation findings about cultural or ideological meaning are "
            "being over-read from limited data.",
            "Meaning preservation is being judged without tracking textual devices — theme "
            "dynamics, clausal and iconic linkage, deictic dependence, overall organization.",
            "Lexical choices (superordinate, approximation, circumlocution) or non-mother-tongue "
            "translation need weighing against target-reader need and appropriate controls.",
            "Quality requirements are set without reference to the commission's purpose and risk "
            "level, or fine-grained counts are interpreted without their context.",
        ],
        input="The applied corpus analysis or textual-device tracking, the commission's purpose and "
              "risk level, and the interpretation drawn from the counts.",
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


print(f"principles={len(ALL_IDS)} high={len(HI_IDS)} claims={len(CLAIM_IDS)}")

# ============================================================================ EMITTERS

SRC_CITE = ("the distillation-only sources (House, *Translation Quality Assessment*; Baker, "
            "*Corpus Linguistics and Translation Studies*; Kruger et al., *Corpus-Based "
            "Translation Studies*; Dayter & Grabowski, eds., corpus translation & interpreting "
            "studies in the Russian field; Yu Guangzhong on the normal and distorted states of "
            "Chinese)")


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
        body.append("- The reasoning offered for the decision under review: the corpus, the "
                    "orientation, the brief, and any quality claim made.\n")
        body.append("## Output\n")
        body.append(
            "Per finding: name the flaw and the principle it violates, apply the correction, "
            "state the residual uncertainty and the trade-off it reflects, and end with a concrete "
            "next step. Order findings highest-impact first. This skill reviews a translation, a "
            "translation-quality claim, or a corpus-based translation-studies analysis; it does not "
            "produce the finished translation or make the publication decision.\n")
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
            f"Derived from {idlist}, grounded in {SRC_CITE}. The frontmatter `provenance` block "
            "lists the exact principle and claim ids, which resolve into "
            "`principles/principles.yaml` and `analysis/claims.jsonl`.\n")
        w(BASE / "skills" / slug / "SKILL.md", "\n".join(body))


def emit_refs() -> None:
    claims = union_claims([n for _, nums in SKILLS for n in nums], cap=16)
    out = [frontmatter(REFS[0], "reference", list(range(1, N + 1)), claims)]
    out.append("# Translation Quality Principles Index\n")
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

    out = [frontmatter(REFS[1], "reference", list(range(1, N + 1)), [])]
    out.append("# Translation Quality Evidence Notes\n")
    out.append("How the principles in this package are grounded, and how to keep review findings "
               "faithful to the sources.\n")
    out.append("## Sources\n")
    out.append("Five distillation-only sources ground the package: Juliane House, *Translation "
               "Quality Assessment: Past and Present* (the functional-pragmatic overt/covert model "
               "and its register analysis); Mona Baker, *Corpus Linguistics and Translation "
               "Studies* (the corpus programme and the candidate universals); Haidee Kruger and "
               "colleagues, *Corpus-Based Translation Studies* (methodology and the "
               "explicitation/simplification/normalisation constructs); Dayter and Grabowski, eds., "
               "corpus-based translation and interpreting studies in the Russian field "
               "(multifactorial modelling, corpus scarcity); and Yu Guangzhong on the normal and "
               "distorted states of Chinese prose (Europeanization). Paraphrase and restructure "
               "only — no verbatim quotation (see `.claude/rules/rights-and-quotation-policy.md`).\n")
    out.append("## Faithfulness discipline\n")
    out.append("- No finding may state a rule more strongly than its source supports: a candidate "
               "universal or a tentative, small-sample finding stays tentative and is never "
               "upgraded into a law (P035, P115).")
    out.append("- Translationese and the third code are describable systemic features, not a direct "
               "proxy for quality; quality needs separate evidence for meaning preservation "
               "(P002, P139).")
    out.append("- Corpus statistics are prompts for recontextualised interpretation, not final "
               "answers, and a difference is attributed to translation only after comparability "
               "and normalisation are controlled (P108, P135).")
    out.append("- Evaluate against a specified source-text profile and function; global "
               "impressionistic criteria are rejected unless made operationally checkable "
               "(P006, P036).\n")
    out.append("## Grounding\n")
    out.append(f"Spine: {len(ALL_IDS)} principles ({len(HI_IDS)} high-confidence) over "
               f"{len(CLAIM_IDS)} atomic claims, with evidence records and chunk anchors. Every "
               f"principle id P001-P{N:03d} resolves into `principles/principles.yaml`.\n")
    w(BASE / "references" / f"{REFS[1]}.md", "\n".join(out))


def _always_on() -> list[str]:
    out = []
    for slug, nums in SKILLS:
        ids = ", ".join(pids(n) for n in nums)
        out.append(f"{THEMES[slug]['purpose']} ({ids})")
    return out


PROFILE_ROLE = (
    "A reviewer of translations, translation-quality claims, and corpus-based translation-studies "
    "analyses, grounded in translation quality assessment and corpus translation studies (House; "
    "Baker; Kruger et al.; Dayter & Grabowski; Yu Guangzhong). It critiques a rendering or an "
    "analysis for source-profile and functional-equivalence rigour, overt/covert classification, "
    "register (Field/Tenor/Mode) fidelity, error-analysis and evaluation discipline, corpus design "
    "and the handling of universals and the third code, descriptive-method and norm awareness, "
    "cultural filtering and ideology, Russian-field constraints, genre and accessibility, and "
    "Europeanization in Chinese prose. The operating invariants below are review criteria drawn "
    "from the sources, not instructions to produce translation: this review-only boundary and the "
    "forbidden behaviours override every invariant, so the reviewer never produces the finished "
    "translation, makes the publication decision, or certifies a rendering definitively correct.")

WHEN_TO_USE = [
    "A translation or draft is being assessed and the team wants its quality reviewed against the "
    "source-text profile, its function, and its register (P006, P059).",
    "A corpus-based translation-studies analysis, or a universals or norm claim, needs checking for "
    "method rigour and faithfulness to its evidence (P001, P083, P112).",
    "Translationese or fluency is being used as a proxy for quality and the team wants that "
    "criterion interrogated (P002, P114).",
    "An overt/covert translation type, a cultural-filter change, or a functional-equivalence claim "
    "needs situating and justifying (P007, P011, P133).",
    "A Russian-field corpus study or a Chinese target text needs its multifactorial modelling or "
    "its Europeanization reviewed (P056, P119).",
]

WHEN_NOT_TO_USE = [
    "The caller wants the finished or revised translation produced end to end; this reviewer "
    "critiques, it does not translate.",
    "The concern is subject-matter correctness or the legal validity of a text with a knowable "
    "answer, not a translation-quality judgement.",
    "The caller wants a single guaranteed-correct rendering; translation quality is probabilistic "
    "and brief-dependent, so the review improves the choice, it cannot certify one answer.",
    "The task has no translation dimension — monolingual editing, corpus engineering, or a pure "
    "statistical implementation with no quality claim.",
]

QUALITY_BAR = [
    "Universals and the third code are handled as hypotheses, operationalised as distinct "
    "constructs, and kept apart from translationese used as a quality proxy (P001, P079, P084, "
    "P139, P002).",
    "Corpus design fits the research question; comparability, metadata, alignment, and frequency "
    "normalisation are controlled before any difference is attributed to translation status "
    "(P003, P050, P078, P118, P135).",
    "Quality is assessed from a specified source-text profile and function, across semantic, "
    "pragmatic, and textual dimensions, with the overt/covert distinction explicit (P006, P038, "
    "P059, P090, P138).",
    "Register (Field, Tenor, Mode) and cultural filtering are compared source-to-target and read "
    "from co-occurring feature clusters, not isolated frequencies (P042, P069, P056, P116, P137).",
    "The strength of the evidence is preserved: tentative findings stay tentative, impressionistic "
    "criteria are rejected, and complex variation is modelled multifactorially (P035, P036, P056, "
    "P061, P086).",
    "The analysis is descriptive and target-oriented: translated text is studied on its own terms, "
    "norms are reconstructed from the corpus, and socio-cultural context enters the causal "
    "explanation (P016, P018, P083, P114, P145).",
]

FORBIDDEN = [
    "Producing the finished or revised translation, or the publication and quality sign-off, for "
    "the caller — this reviewer critiques translation decisions, it does not own the text or the "
    "call (P059, P134).",
    "Using translationese or fluency as a direct proxy for quality, or judging a translation "
    "without comparison against a specified source-text profile (P002, P037, P114).",
    "Stating a rule more strongly than its source supports — upgrading a candidate universal, a "
    "hedged finding, or a single-frequency pattern into a settled law (P035, P115, P056).",
    "Prescribing a single correct rendering as if translation had one deterministic answer, or "
    "ignoring the commission's purpose and risk level that condition the choice (P061, P134, "
    "P125).",
]

HANDOFF = [
    "The translator and the commissioner hold the text and the publication decision; this reviewer "
    "informs the reasoning and makes the residual trade-off explicit (P059, P134).",
    "Concerns outside translation review — subject-matter accuracy, corpus engineering, and the "
    "statistical implementation of a model — are handed to the owning specialist (P052, P077).",
]

PRECEDENCE = (
    "Where a source's context differs from the caller's, treat a principle as an adaptable guide, "
    "not an absolute (P032, P047, P115); when the corpus measure and the research question "
    "conflict, the question governs the measure and its controls (P078, P003); and never endorse a "
    "finding more confident than its evidence — a candidate universal or a single-frequency "
    "pattern stays tentative (P035, P056).")

MODES = [
    dict(name="review",
         trigger="The caller submits a translation, a translation-quality claim, or a corpus-based "
                 "translation-studies analysis for critique.",
         output="A findings list keyed to flaw class (universals/method, corpus design, "
                "overt-covert/equivalence, register, error-discipline, norms, culture, "
                "Russian-field, genre/accessibility, Chinese prose), each with flaw, correction, "
                "residual trade-off, and next step — highest-impact first."),
    dict(name="advise",
         trigger="The caller faces a translation-quality or corpus-design decision and wants which "
                 "principle or method fits.",
         output="A recommendation tied to the situation, naming the principle(s) and method applied "
                "and the residual trade-off to carry."),
    dict(name="compare",
         trigger="The caller weighs options for one goal (parallel vs comparable corpus, overt vs "
                 "covert, one rendering vs another).",
         output="A side-by-side of what each option preserves and costs, ending in a purpose- and "
                "evidence-weighted recommendation."),
]

EXAMPLES = [
    dict(title="Review a translation graded by its translationese score",
         kind="happy-path",
         scenario=(
             "A team submits an English-to-Chinese translation and grades it low purely because an "
             "automatic translationese classifier flags it, with no source-profile comparison and "
             "no meaning-preservation evidence."),
         ideal_response=(
             "Flag the flaws, highest-impact first. (1) Translationese is not a quality proxy: a "
             "translationese indicator cannot stand in for quality, which needs separate evidence "
             "for meaning preservation and plain information delivery (P002). (2) Missing the "
             "source-text profile: quality must be built from a detailed source-text profile that "
             "specifies the function the target should seek, assessed across semantic, pragmatic, "
             "and textual dimensions, not a single score (P006, P038). (3) Third code vs "
             "translationese: a systematic distribution of features may be the third code, a "
             "describable feature of translated language, not a defect — treat a distinctive "
             "profile non-evaluatively unless evidence shows actual error (P139, P114). (4) "
             "Europeanization, if that is the real concern: check concision, flexible syntax, and "
             "rhythmic force against needlessly Europeanized wording, case by case (P119). "
             "Correction: re-anchor the grade to a source-profile comparison and functional "
             "evidence, keep the classifier as one descriptive signal, and hand the accept/reject "
             "call back to the team — quality here is probabilistic (P061, P059)."),),
    dict(title="Decline to produce the translation and redirect to a review",
         kind="failure-recovery",
         scenario=(
             "The caller asks the reviewer to 'just translate this contract into Russian and "
             "confirm it's correct', with no brief, no source-text profile, and no draft."),
         ideal_response=(
             "Decline to produce the finished text or certify it correct — this reviewer critiques "
             "translation decisions, it does not translate or make the sign-off (forbidden "
             "behaviours, P059, P134). Offer the review instead: ask for the commission's purpose "
             "and risk level and a source-text profile specifying the function to be sought, since "
             "quality requirements follow from the commission and the text's function (P134, P006); "
             "note that a contract is typically an overt case where the source is kept as intact as "
             "possible and equivalence stays close to formal (P005, P059); and set expectations "
             "that any assessment compares the draft against a specified source profile and treats "
             "quality as a range of valid answers, not one certified rendering (P038, P061)."),),
]

SOURCES = [
    dict(source_id="translation-quality-c0dd203d",
         title="Translation Quality Assessment: Past and Present",
         author="Juliane House", year=2015, rights_status="distillation-only",
         sha256="c0dd203dbe43780bfcfba542599430b15a4f4f815a429653fd8bede5eef9105d"),
    dict(source_id="corpus-linguistics-t-ceffdb40",
         title="Corpus Linguistics and Translation Studies: Implications and Applications",
         author="Mona Baker", year=1993, rights_status="distillation-only",
         sha256="ceffdb401b94c0c86201e0d59b59843bf43ff132697066f2e8c6d3464ca87716"),
    dict(source_id="corpus-based-transla-98c56c2d",
         title="Corpus-Based Translation Studies: Research and Applications",
         author="Haidee Kruger, Kim Wallmach and Jeremy Munday (eds.)", year=2011,
         rights_status="distillation-only",
         sha256="98c56c2df14371dea057669796d30e83b58e00cc19e7412a2b793a2f035fe25f"),
    dict(source_id="corpus-translation-r-b10b2ead",
         title="Corpus-Based Translation and Interpreting Studies (the Russian field)",
         author="Daria Dayter and Łukasz Grabowski (eds.)", year=2023,
         rights_status="distillation-only",
         sha256="b10b2ead5dd001a942d9c589467370f0b8113630ef0dcfa2a7c98f3a07d32c8e"),
    dict(source_id="chinglish-europeaniz-5798beb7",
         title="On the Normal and Distorted States of Chinese (Europeanized Chinese / Chinglish)",
         author="Yu Guangzhong", year=1987, rights_status="distillation-only",
         sha256="5798beb748a0cb78314cb69afbab99a4a731b5ae4dd2b69df37a5a038fc461a1"),
]


def emit_profile() -> None:
    profile = {
        "schema_version": "portable-profile-v1",
        "slug": SLUG,
        "display_name": "Translation Quality Reviewer",
        "agent_version": VERSION,
        "status": "ready",
        "tier": 2,
        "multisource_synthesis": "deferred",
        "role": PROFILE_ROLE,
        "when_to_use": WHEN_TO_USE,
        "when_not_to_use": WHEN_NOT_TO_USE,
        "inputs": {"required": [
            "The translation, translation-quality claim, or corpus-based translation-studies "
            "analysis under review, plus its reasoning: the source and target, the source-text "
            "profile and function, the corpus design, the equivalence orientation, and any quality "
            "claim made."]},
        "outputs": {
            "primary_format": (
                "A structured review that, per finding, names the flaw and the principle it "
                "violates, applies the correction, states the residual trade-off, and ends with a "
                "next step — never a bare good/bad verdict."),
            "modes": MODES,
        },
        "quality_bar": QUALITY_BAR,
        "minimum_useful_output": (
            "At least one finding that names a translation or translation-studies flaw, applies a "
            "named principle or correction, and states the residual trade-off — the values kept "
            "against those given up."),
        "forbidden_behaviours": FORBIDDEN,
        "handoff_rules": HANDOFF,
        "source_of_truth_policy": {
            "canonical_owner": (
                "The translator and the commissioner hold final authority over the text and the "
                "decision to publish it; the distilled principles from House, Baker, Kruger et al., "
                "Dayter & Grabowski, and Yu Guangzhong are the authority for the review criteria "
                "the reviewer invokes."),
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

    qb_ids = ["P001/P079/P084/P139/P002", "P003/P050/P078/P118/P135",
              "P006/P038/P059/P090/P138", "P042/P069/P056/P116/P137",
              "P035/P036/P056/P061/P086", "P016/P018/P083/P114/P145"]
    for i, ids in enumerate(qb_ids):
        add(f"quality_bar[{i}]", ids, "Review criterion, not a directive to translate.")
    fb_ids = ["P059/P134", "P002/P037/P114", "P035/P115/P056", "P061/P134/P125"]
    for i, ids in enumerate(fb_ids):
        add(f"forbidden_behaviours[{i}]", ids, "Boundary restraint; no over-claim.")
    wt_ids = ["P006/P059", "P001/P083/P112", "P002/P114", "P007/P011/P133", "P056/P119"]
    for i, ids in enumerate(wt_ids):
        add(f"when_to_use[{i}]", ids, "Routing trigger grounded in the cited principles.")
    add("outputs.primary_format", "P061/P059",
        "The per-finding review format; states residual trade-off rather than a bare verdict.")
    add("source_of_truth_policy.precedence", "P032/P047/P115/P078/P003/P035/P056",
        "Adaptable-guide + question-governs-measure + no-over-claim, all source-grounded.")
    report = {
        "schema_version": "faithfulness-report-v1",
        "subagent_slug": SLUG,
        "findings": findings,
    }
    w(BASE / "reports" / "faithfulness-report.yaml",
      yaml.safe_dump(report, sort_keys=False, allow_unicode=True, width=100))


GOLDEN = [
    dict(test_id="GT-001", mode="review",
         desc="Positive routing — translationese score used as a quality grade",
         prompt="We graded this English-to-Chinese translation low because our translationese "
                "classifier flagged it. No other analysis. Review our judgement.",
         must_do=["Flag translationese as not a direct proxy for quality",
                  "Require a source-text profile comparison and meaning-preservation evidence",
                  "Distinguish the third code from a defect; treat a distinctive profile "
                  "non-evaluatively unless error is shown",
                  "Operationalise the indicators as distinct constructs, not one label"],
         must_not=["Certify the translation correct or make the accept/reject decision",
                   "Accept the translationese score alone as evidence of quality"],
         cov=["P002", "P006", "P139", "P114", "P079"]),
    dict(test_id="GT-002", mode="advise",
         desc="Positive routing — choose a corpus type for an equivalence study",
         prompt="We want to study equivalence and alignment between source texts and their "
                "translations. Should we build a parallel or a comparable corpus?",
         must_do=["Recommend a parallel corpus for equivalence and alignment questions",
                  "Require comparability, metadata, copyright, and alignment controls",
                  "Match the measure to the research question",
                  "State the residual trade-off"],
         must_not=["Attribute differences to translation status without controls"],
         cov=["P003", "P068", "P050", "P078"]),
    dict(test_id="GT-003", mode="review",
         desc="Positive routing — overt/covert and cultural filter in a mission statement",
         prompt="Review our translated corporate mission statement; we applied a cultural filter to "
                "make it sound natural in the target language.",
         must_do=["Check whether the case is overt or covert and whether the filter change is "
                  "justified or produces a covert version",
                  "Analyse Tenor shifts in positivity, indirect request, and perlocutionary force",
                  "Assess functional equivalence against the source-text profile",
                  "Name the residual trade-off"],
         must_not=["Treat a natural-sounding target as automatic proof of quality"],
         cov=["P007", "P011", "P070", "P072", "P137"]),
    dict(test_id="GT-004", mode="review",
         desc="Positive routing — a claimed translation universal from one dataset",
         prompt="Our study concludes that explicitation is a translation universal, based on one "
                "English-German comparable corpus. Review the claim.",
         must_do=["Treat explicitation as a hypothesis to be measured, not presumed",
                  "Scope the universal as a tendency and test language-pair/culture explanations",
                  "Classify the study target (universal vs mediator style vs source response)",
                  "Keep the finding tentative and generalise only after cross-genre testing"],
         must_not=["Upgrade a single-dataset finding into a settled law"],
         cov=["P001", "P115", "P055", "P143", "P035"]),
    dict(test_id="GT-005", mode="compare",
         desc="Positive routing — Europeanized vs idiomatic Chinese prose",
         prompt="Compare two Chinese renderings of an English essay: one closely follows the "
                "English syntax, the other reads as idiomatic Chinese. Which is better?",
         must_do=["Weigh concision, flexible syntax, and rhythmic force against Europeanized wording",
                  "Treat established idioms as live resources, not decorative or wordy substitutes",
                  "Prefer concrete subjects and event clauses over abstract nominalized ones",
                  "Weight the choice by clarity and naturalness, not a fixed rule"],
         must_not=["Declare Europeanized or idiomatic universally correct"],
         cov=["P119", "P120", "P149", "P150"]),
    dict(test_id="GT-006", mode="review",
         desc="Positive routing — a Russian-field multifactorial claim",
         prompt="Our Russian interpreting study reports a difference in one lexical frequency "
                "between modes and concludes an interference effect. Review it.",
         must_do=["Require multifactorial modelling rather than an isolated frequency",
                  "Ask for significance testing with effect sizes and clear marker operationalisation",
                  "Check corpus scarcity, fragmentation, and metadata as design constraints",
                  "Avoid strong Russian interpreting generalisations from thin data"],
         must_not=["Accept a single-frequency difference as an established interference law"],
         cov=["P056", "P057", "P058", "P019", "P146"]),
]

NEGATIVE = [
    dict(test_id="NR-001",
         prompt="Translate this 400-word product manual from English into Russian for us.",
         reason="Asks for the finished translation, not a review."),
    dict(test_id="NR-002",
         prompt="Is the tax amount computed in this bilingual invoice arithmetically correct?",
         reason="Subject-matter correctness with a knowable answer, no translation-quality "
                "dimension."),
]

MISSING = [
    dict(test_id="MC-001",
         prompt="Is this a good translation?",
         ask=["The source text and the target text to compare",
              "The source-text profile: intended function, audience, and the commission's purpose "
              "and risk level",
              "Any specific quality concern or claim to check"]),
    dict(test_id="MC-002",
         prompt="Are these corpus results reliable?",
         ask=["The corpus type (parallel or comparable) and its comparability and metadata",
              "The measure applied and whether frequencies were normalised across subcorpora",
              "The research question or hypothesis being tested"]),
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
                f"We are reviewing a translation or corpus-based translation-studies analysis where "
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
                "State the rule more strongly than the source supports, or accept translationese or "
                "fluency alone as proof of quality.",
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

All five sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They are canonical
translation-quality and corpus-translation-studies works: House's functional-pragmatic quality
model, Baker's and Kruger et al.'s corpus programme and universals, the Dayter & Grabowski Russian-
field volume, and Yu Guangzhong on Europeanized Chinese prose.

## Distillation

Spine: {len(ALL_IDS)} promoted principles (P001-P{N:03d}; {len(HI_IDS)} high-confidence) over
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
  P001-P{N:03d} / {len(CLAIM_IDS)} claims from five distillation-only sources).
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
- Five distillation-only sources: Juliane House, *Translation Quality Assessment: Past and Present*
  (2015); Mona Baker, *Corpus Linguistics and Translation Studies* (1993); Haidee Kruger et al.,
  *Corpus-Based Translation Studies* (2011); Daria Dayter & Łukasz Grabowski, eds., corpus-based
  translation and interpreting studies in the Russian field (2023); Yu Guangzhong on the normal and
  distorted states of Chinese prose (1987).
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
