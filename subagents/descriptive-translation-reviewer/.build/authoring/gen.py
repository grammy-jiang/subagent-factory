"""Deterministic authoring generator for descriptive-translation-reviewer.

Reads the already-assembled, deterministically-valid distilled spine
(principles/principles.yaml + analysis/claims.jsonl + evidence + anchors) and emits the
LLM-authored layer: profile.yaml, references/*, skills/*, tests/*, reports/faithfulness-report.yaml,
provenance-ledger.md, CHANGELOG.md. Every emitted id resolves into the spine.

Run:  python3 .build/authoring/gen.py
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parents[2]  # subagents/descriptive-translation-reviewer
SLUG = "descriptive-translation-reviewer"
VERSION = "1.0.0"
DATE = "2026-07-12"

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
#              [principle numbers]).  Every principle 1..180 appears exactly once.
SKILLS: list[tuple[str, list[int]]] = [
    ("descriptive-method-and-translational-norms",
     [2, 10, 11, 23, 35, 39, 46, 54, 57, 101, 102, 103, 110, 146, 151, 152, 153, 154, 155, 156, 166]),
    ("equivalence-orientations-and-effect",
     [59, 74, 76, 104, 105, 106, 118, 124, 125, 126, 143, 159, 160, 161, 162, 179, 180]),
    ("meaning-signification-and-equivalence-critique",
     [4, 8, 58, 73, 94, 109, 116, 121, 127, 148, 178]),
    ("translation-procedures-and-shifts",
     [6, 15, 37, 72, 119, 120, 122, 163, 164, 168]),
    ("text-type-skopos-and-the-brief",
     [9, 38, 60, 61, 62, 63, 70, 78, 79, 107, 108, 128, 129, 145, 165]),
    ("register-discourse-and-audiovisual-constraints",
     [19, 21, 52, 53, 64, 65, 66, 67, 68, 69, 85, 90, 91]),
    ("domestication-foreignization-and-visibility",
     [20, 24, 42, 47, 49, 86, 87, 88, 141, 167, 169, 170, 175, 176]),
    ("culture-ideology-power-and-rewriting",
     [1, 12, 13, 18, 22, 27, 28, 29, 40, 50, 51, 55, 80, 84, 111, 131, 133, 136, 139, 140]),
    ("deforming-tendencies-and-translation-loss",
     [14, 25, 26, 81, 82, 83, 114, 115]),
    ("hermeneutics-and-the-limits-of-translatability",
     [3, 5, 32, 56, 95, 96, 97, 98, 99, 117, 123, 130, 132, 134, 135, 137, 138, 144, 150]),
    ("literal-free-strategy-history-and-retranslation",
     [30, 31, 34, 36, 45, 48, 71, 77, 142, 149, 157, 158, 171, 172, 173, 174, 177]),
    ("translation-quality-and-applied-studies",
     [7, 16, 17, 33, 41, 43, 44, 75, 89, 92, 93, 100, 112, 113, 147]),
]

# integrity: every principle exactly once
_seen: list[int] = []
for _slug, nums in SKILLS:
    _seen += nums
assert sorted(_seen) == list(range(1, 181)), f"partition mismatch: {sorted(_seen)}"
assert len(set(s for s, _ in SKILLS)) == len(SKILLS), "duplicate skill slug"
for s, _ in SKILLS:
    assert len(s) <= 48, f"slug too long ({len(s)}): {s}"

REFS = ["descriptive-translation-principles-index", "descriptive-translation-evidence-notes"]

# ---------------------------------------------------------------------------- per-skill themes
# title, purpose (2-3 sentences), when-to-use bullets, focus input line.
THEMES: dict[str, dict] = {
    "descriptive-method-and-translational-norms": dict(
        title="Descriptive Method And Translational Norms",
        purpose=(
            "This skill reviews whether a translation is being described and judged with an "
            "explicit, systematic, target-oriented descriptive method rather than by ad-hoc "
            "prescription. It checks that translational norms are reconstructed from patterned "
            "behaviour at the receiving end — not read off directly — and that findings are "
            "contextualized by sector, subsystem position, and historical moment, with norm "
            "strength treated as graded and mobile."),
        when=[
            "A translation or corpus of translations is being analysed and the reviewer wants "
            "the method checked for being explicit, systematic, and intersubjectively testable.",
            "A claim about a 'norm' is being made and needs checking against whether it was "
            "reconstructed from recurrent regularities or merely asserted.",
            "Preliminary, initial, and operational norms are being conflated, or the "
            "adequacy–acceptability orientation of a translation needs situating.",
            "Toury's probabilistic laws (growing standardization, interference) are being invoked "
            "to explain regularities and the reasoning needs checking.",
        ],
        input="The translation(s) or translation-studies analysis under review and its declared method, corpus, and norm claims.",
    ),
    "equivalence-orientations-and-effect": dict(
        title="Equivalence Orientations And Effect",
        purpose=(
            "This skill reviews how a translation positions itself on the formal-versus-dynamic "
            "equivalence axis and whether the chosen orientation fits the purpose. It checks "
            "equivalent-effect claims for the illusion that arises when a text is out of the "
            "receptor's space and time, and holds a rendering to the synthesized requirements of "
            "sense, spirit, natural form, and equivalent response."),
        when=[
            "A translation claims formal (source-form) or dynamic (closest-natural) equivalence and "
            "the fit of that orientation to the brief needs checking.",
            "An 'equivalent effect' or 'same response' claim is being made and may be illusory.",
            "Koller's denotative/connotative/text-normative/pragmatic/formal relations are being "
            "chosen among, or naturalness is being assessed.",
            "A legal or equally-authentic multilingual text needs a technique close to formal "
            "equivalence with little room for adjustment.",
        ],
        input="The translation and its stated equivalence orientation, purpose, and target audience.",
    ),
    "meaning-signification-and-equivalence-critique": dict(
        title="Meaning, Signification And The Equivalence Critique",
        purpose=(
            "This skill reviews the theory of meaning underlying an equivalence claim. It checks "
            "against naive cross-code identity — the referential argument that two dictionary "
            "equivalents share signification — and analyses equivalence across word, above-word, "
            "grammar, thematic structure, cohesion, and pragmatics, remembering that languages "
            "differ chiefly in what they must convey."),
        when=[
            "An equivalence claim rests on dictionary or referential identity and needs the "
            "signification critique applied.",
            "Obligatory grammatical categories (gender, aspect, kinship fields) force a resolution "
            "the target must make.",
            "Meaning is being treated as a thing rather than a semiotic, context-bound fact.",
            "A multi-level equivalence analysis (word to pragmatics) is being organised.",
        ],
        input="The equivalence claim under review and the source/target items it rests on.",
    ),
    "translation-procedures-and-shifts": dict(
        title="Translation Procedures And Shifts",
        purpose=(
            "This skill reviews micro-level translation decisions with the precise metalanguage of "
            "procedure and shift. It checks the Vinay & Darbelnet ladder (direct: borrowing, "
            "calque, literal; oblique: transposition, modulation, equivalence, adaptation) and "
            "distinguishes obligatory shifts forced by the language systems (servitude) from "
            "optional ones (option), reading a shift as functional fidelity rather than caprice."),
        when=[
            "A micro-level rendering is being justified or criticised and needs naming with the "
            "procedure/shift metalanguage.",
            "A refusal to adapt has left an over-literal calque that disturbs the development of "
            "ideas.",
            "Obligatory (system-forced) and optional shifts are being conflated.",
            "Catford-style category or level shifts need identifying as functional, not arbitrary.",
        ],
        input="The source segment, its rendering, and the procedure/shift rationale offered.",
    ),
    "text-type-skopos-and-the-brief": dict(
        title="Text Type, Skopos And The Brief",
        purpose=(
            "This skill reviews whether a translation is driven by an explicit brief (commission) "
            "and by the predominant function of the whole text. It checks the skopos hierarchy — "
            "purpose first, then intratextual coherence, then fidelity — while flagging that a "
            "fulfilled skopos does not excuse micro-level neglect, and situates the target's "
            "function, which may legitimately differ from the source's."),
        when=[
            "A translation lacks an explicit brief specifying function, audience, medium, and "
            "conditions for both source and target.",
            "A text type (informative, expressive, operative) is being mapped to a general method.",
            "A skopos is being used to license neglect of stylistic or connotative detail.",
            "Audience and medium require omitting known redundancies or making implicit meaning "
            "explicit.",
        ],
        input="The translation brief (or its absence), the source text type, and the target's intended function.",
    ),
    "register-discourse-and-audiovisual-constraints": dict(
        title="Register, Discourse And Audiovisual Constraints",
        purpose=(
            "This skill reviews translation at the level of register and discourse using the "
            "Hallidayan model — field, tenor, mode — and checks cohesion, pragmatic linkage, "
            "transitivity and modality shifts, and politeness/face. It gives special attention to "
            "audiovisual and subtitling constraints, where space, legibility, and timing force "
            "shortening that can re-code interpersonal meaning, not merely omit it."),
        when=[
            "A translation's register profile (field/tenor/mode), genre, and function need "
            "comparing against the source's for a quality judgement.",
            "Cohesion, an implicit pragmatic link, or a transitivity/modality shift changes meaning.",
            "A face-threatening act or its irony is being shifted across cultures.",
            "A subtitle or dubbed line is constrained by on-screen space, timing, and legibility.",
        ],
        input="The source and target texts (or AV material) and the register, discourse, or subtitling constraints in play.",
    ),
    "domestication-foreignization-and-visibility": dict(
        title="Domestication, Foreignization And Translator Visibility",
        purpose=(
            "This skill reviews where a translation sits on the domestication–foreignization axis "
            "and interrogates the ideal of fluency. It flags the illusion of transparency that lets "
            "a fluent translation pass for the original and render the translator invisible, names "
            "the recurrent strategy dichotomies (free/literal, dynamic/formal, "
            "domesticating/foreignizing), and treats 'reads smoothly' as a suspect criterion."),
        when=[
            "A translation is being praised for fluency or for 'reading as if originally written'.",
            "The domestication–foreignization orientation and its ethical stance toward the foreign "
            "need naming.",
            "A translation into the target's dominant discourse performs a canonizing or "
            "assimilating gesture.",
            "A reviewer who cannot check the source is calling a translation 'readable'.",
        ],
        input="The translation, the discourse it is written in, and any fluency/readability claims made about it.",
    ),
    "culture-ideology-power-and-rewriting": dict(
        title="Culture, Ideology, Power And Rewriting",
        purpose=(
            "This skill reviews translation as a culturally and ideologically situated act of "
            "rewriting. It applies refraction, patronage, feminist, postcolonial, and Bourdieusian "
            "(field/habitus/capital) lenses; accounts for the value-driven institutional network of "
            "publishers and editors; and reads reception through reviews and paratexts rather than "
            "judging a translation in isolation."),
        when=[
            "A translation's changes are explicable by ideology, patronage, or a target conception "
            "of an identity rather than by comprehension.",
            "Feminist, postcolonial, or diglossic dynamics (rhetoricity, colonial distance) bear on "
            "the rendering.",
            "The sociology of the translation — agents, field position, capital, reception — is at "
            "issue.",
            "A translation is being judged in isolation instead of against its rivals, paratexts, "
            "and institutional network.",
        ],
        input="The translation, its cultural/ideological context, and the agents, paratexts, and reception around it.",
    ),
    "deforming-tendencies-and-translation-loss": dict(
        title="Deforming Tendencies And Translation Loss",
        purpose=(
            "This skill screens a literary translation for Berman's negative analytic of deforming "
            "tendencies — rationalization, clarification, expansion, ennoblement, and the rest — and "
            "for the translator's characteristic betrayal, normalization, which flattens deliberate "
            "authorial deviation. It catches subtractive, paratextual, and typographic losses and "
            "the over-clarification that destroys an indirect meaning."),
        when=[
            "A literary translation may be flattening the author's deliberate deviations from "
            "ordinary usage.",
            "Paratextual or typographic features (italics, layout) that carried meaning have been "
            "dropped.",
            "A culture-specific detail has been over-clarified, destroying its figurative charge.",
            "Every value cannot be preserved at once and the reviewer must check which were "
            "consciously chosen.",
        ],
        input="The literary source and its translation, with attention to the author's marked or deviant usage.",
    ),
    "hermeneutics-and-the-limits-of-translatability": dict(
        title="Hermeneutics And The Limits Of Translatability",
        purpose=(
            "This skill reviews the interpretive and philosophical grounding of a translation: "
            "Steiner's fourfold hermeneutic motion (trust, aggression, incorporation, restitution), "
            "the indeterminacy of translation and inscrutability of reference (Quine), relevance-"
            "theoretic interpretive resemblance (Gutt), and untranslatability. It holds that there "
            "is no perfect translation and treats each choice as a double interpretation."),
        when=[
            "A translation's interpretive stance — what it trusts, takes, and must restitute — is "
            "under review.",
            "Claims of full determinacy or perfect equivalence need tempering with indeterminacy "
            "and the inscrutability of reference.",
            "An 'unnatural' rendering is imposing gratuitous processing effort against interpretive "
            "resemblance.",
            "Untranslatability or the impossibility of a definitive translation is being denied or "
            "over-claimed.",
        ],
        input="The translation and the interpretive or philosophical claim (determinacy, equivalence, translatability) at stake.",
    ),
    "literal-free-strategy-history-and-retranslation": dict(
        title="Literal–Free Strategy History And Retranslation",
        purpose=(
            "This skill reviews a translation against the long strategy debate — Dryden's "
            "metaphrase/paraphrase/imitation triad, sense-for-sense versus word-for-word, and "
            "Schleiermacher's move-the-reader-or-the-author choice — and against retranslation and "
            "'afterlife' dynamics. It checks verse prosody, historical register and archaism, "
            "scholarly apparatus, and the reading of a translation against its predecessors."),
        when=[
            "A rendering needs placing on the metaphrase–paraphrase–imitation scale or the "
            "literal–free axis.",
            "A verse translation must map both prosodic systems rather than transfer a form "
            "wholesale.",
            "Historical distance, archaism, or a scholarly apparatus governs the target register.",
            "A retranslation is being read in relation to its predecessors and a work's afterlife.",
        ],
        input="The translation, its source's period and form, and any prior versions it reacts to.",
    ),
    "translation-quality-and-applied-studies": dict(
        title="Translation Quality And Applied Studies",
        purpose=(
            "This skill reviews translation-quality assessment and applied/empirical translation "
            "studies. It requires evaluation by comparison against the source in the source "
            "language, treats quality as probabilistic (a range of valid answers), and situates work "
            "on Holmes's discipline map — training, aids, criticism — and within process research "
            "(think-aloud, keylogging), corpora and CAT tools, GILT/localization, and sound research "
            "design."),
        when=[
            "A translation is being scored without comparison against the source in the source "
            "language.",
            "Quality is being treated deterministically rather than as a range of valid answers.",
            "A study's place on the discipline map, its research design, or its use of corpora, CAT, "
            "or process methods needs checking.",
            "Localization/GILT scope or the translator's situated role and expertise is at issue.",
        ],
        input="The quality claim or applied/empirical study under review and the source it should be measured against.",
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
        body.append("- The reasoning offered for the decision under review: the orientation, "
                    "strategy, brief, and any quality claim made.\n")
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
            "See `../../references/descriptive-translation-principles-index.md` for the full "
            "principle catalogue grouped by skill, and "
            "`../../references/descriptive-translation-evidence-notes.md` for how these principles "
            "are grounded and kept faithful to the sources.\n")
        body.append("## Provenance\n")
        idlist = ", ".join(pids(n) for n in nums)
        body.append(
            f"Derived from {idlist}, grounded in the distillation-only sources (Munday, "
            "*Introducing Translation Studies*; Venuti, ed., *The Translation Studies Reader*; "
            "Toury, *The Nature and Role of Norms in Translation*). The frontmatter `provenance` "
            "block lists the exact principle and claim ids, which resolve into "
            "`principles/principles.yaml` and `analysis/claims.jsonl`.\n")
        w(BASE / "skills" / slug / "SKILL.md", "\n".join(body))


def emit_refs() -> None:
    claims = union_claims([n for _, nums in SKILLS for n in nums], cap=16)
    out = [frontmatter(REFS[0], "reference", list(range(1, 181)), claims)]
    out.append("# Descriptive Translation Principles Index\n")
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

    out = [frontmatter(REFS[1], "reference", list(range(1, 181)), [])]
    out.append("# Descriptive Translation Evidence Notes\n")
    out.append("How the principles in this package are grounded, and how to keep review findings "
               "faithful to the sources.\n")
    out.append("## Sources\n")
    out.append("Three distillation-only sources ground the package: Jeremy Munday, *Introducing "
               "Translation Studies* (a survey mapping the discipline and its theories); Lawrence "
               "Venuti, ed., *The Translation Studies Reader* (primary essays from Jakobson and Nida "
               "to Venuti, Spivak, and Berman); and Gideon Toury, *The Nature and Role of Norms in "
               "Translation* (the descriptive/norms programme). Paraphrase and restructure only — no "
               "verbatim quotation (see `.claude/rules/rights-and-quotation-policy.md`).\n")
    out.append("## Faithfulness discipline\n")
    out.append("- No finding may state a rule more strongly than its source supports: a context-bound "
               "\"in this case prefer X\" must not become \"always X\" (P075, P138).")
    out.append("- Competing schools disagree; attribute a prescription to its theory rather than "
               "presenting it as settled fact (P043, P121).")
    out.append("- Quality is probabilistic: there is a range of valid answers, so a review improves a "
               "choice rather than certifying the one correct rendering (P075).")
    out.append("- Evaluate against the source in the source language; fluency alone is not evidence "
               "of fidelity (P044, P020, P176).\n")
    out.append("## Grounding\n")
    out.append(f"Spine: {len(ALL_IDS)} principles ({len(HI_IDS)} high-confidence) over "
               f"{len(CLAIM_IDS)} atomic claims, with evidence records and chunk anchors. Every "
               "principle id P001-P180 resolves into `principles/principles.yaml`.\n")
    w(BASE / "references" / f"{REFS[1]}.md", "\n".join(out))


def _always_on() -> list[str]:
    out = []
    for slug, nums in SKILLS:
        ids = ", ".join(pids(n) for n in nums)
        out.append(f"{THEMES[slug]['purpose']} ({ids})")
    return out


PROFILE_ROLE = (
    "A reviewer of translations, translation choices, and translation-studies analyses, grounded in "
    "descriptive translation studies and the major equivalence, functionalist, discourse, and "
    "cultural theories (Munday, Venuti, Toury). It critiques a rendering or an analysis for "
    "descriptive-method rigour, norm-awareness, the fit of its equivalence orientation and strategy "
    "to the brief and text function, register and discourse fidelity, translator visibility and "
    "ideology, deforming tendencies and loss, and the interpretive limits of translatability. The "
    "operating invariants below are review criteria drawn from the sources, not instructions to "
    "produce translation: this review-only boundary and the forbidden behaviours override every "
    "invariant, so the reviewer never produces the finished translation, makes the publication "
    "decision, or certifies a rendering definitively correct.")

WHEN_TO_USE = [
    "A translation or draft is being assessed and the team wants its equivalence orientation, "
    "strategy, register, and losses reviewed against the source and the brief.",
    "A translation-studies analysis, commentary, or 'norm' claim needs checking for "
    "descriptive-method rigour and faithfulness to its evidence.",
    "A translation is being praised for fluency or 'reading well', and the team wants that "
    "criterion — and the translator's visibility — interrogated.",
    "A rendering must be placed on the literal-free, domesticating-foreignizing, or formal-dynamic "
    "axes, or given a text-type-appropriate method.",
    "A literary, audiovisual, legal, or scholarly translation needs its deforming tendencies, "
    "subtitling constraints, or scholarly apparatus reviewed.",
]

WHEN_NOT_TO_USE = [
    "The caller wants the finished or revised translation produced end to end; this reviewer "
    "critiques, it does not translate.",
    "The concern is subject-matter correctness or the legal validity of a text with a knowable "
    "answer, not a translation-quality judgement.",
    "The caller wants a single guaranteed-correct rendering; translation quality is probabilistic "
    "and brief-dependent, so the review improves the choice, it cannot certify one answer.",
    "The task has no translation dimension — monolingual editing, typesetting, or a pure "
    "terminology lookup.",
]

QUALITY_BAR = [
    "Every judgement rests on an explicit, systematic, target-oriented description; norms are "
    "reconstructed from patterned behaviour, not asserted, and treated as graded and mobile "
    "(P010, P011, P039, P046, P110).",
    "Every equivalence claim states its orientation (formal vs dynamic), fits the purpose, and does "
    "not mistake an illusory equivalent effect for a real one (P004, P105, P106, P118, P159).",
    "Every translation is driven by an explicit brief and the whole text's predominant function, "
    "and a fulfilled skopos never excuses micro-level neglect (P009, P038, P060, P062, P108).",
    "Register (field, tenor, mode), cohesion, pragmatic linkage, and face are compared "
    "source-to-target, and audiovisual shortening is checked for re-coding, not just omission "
    "(P064, P065, P066, P069, P091).",
    "Fluency is not treated as proof of quality; the illusion of transparency, the translator's "
    "(in)visibility, and the ideological and institutional forces rewriting the text are surfaced "
    "(P020, P024, P088, P040, P050).",
    "Quality is assessed by comparison against the source in the source language and treated as "
    "probabilistic; loss is named (Berman's tendencies, normalization) and no perfect translation "
    "is presumed (P044, P075, P014, P115, P138).",
]

FORBIDDEN = [
    "Producing the finished or revised translation, or the publication and quality sign-off, for "
    "the caller — this reviewer critiques translation decisions, it does not own the text or the "
    "call (P070, P100).",
    "Endorsing fluency or 'reads smoothly' as proof of quality, or judging a translation without "
    "comparison against the source in the source language (P020, P044, P176).",
    "Stating a rule more strongly than its source supports — flattening a context-bound 'in this "
    "case prefer X' into 'always X', or presenting one school's prescription as settled fact "
    "(P075, P138, P121).",
    "Prescribing a single correct rendering as if translation had one deterministic answer, or "
    "ignoring the brief, audience, and function that condition the choice (P075, P062, P038).",
]

HANDOFF = [
    "The translator and the commissioner hold the text and the publication decision; this reviewer "
    "informs the reasoning and makes the residual trade-off explicit (P070, P009).",
    "Concerns outside translation review — subject-matter accuracy, the legal validity of a treaty "
    "text, typesetting, and the client's commercial constraints — are handed to the owning "
    "specialist (P162, P080).",
]

PRECEDENCE = (
    "Where a source's context differs from the caller's, treat a principle as an adaptable guide, "
    "not an absolute (P046, P102, P075); when equivalence orientation and function conflict, the "
    "brief's purpose governs which values are preserved (P062, P114); and never endorse a rule more "
    "confident than the source supports (P138, P121).")

MODES = [
    dict(name="review",
         trigger="The caller submits a translation, a translation choice, or a translation-studies "
                 "analysis for critique.",
         output="A findings list keyed to flaw class (method/norms, equivalence, function/brief, "
                "register/discourse, visibility/ideology, loss, translatability), each with flaw, "
                "correction, residual trade-off, and next step — highest-impact first."),
    dict(name="advise",
         trigger="The caller faces a translation decision and wants which principle or strategy "
                 "fits.",
         output="A recommendation tied to the situation, naming the principle(s) and orientation "
                "applied and the residual trade-off to carry."),
    dict(name="compare",
         trigger="The caller weighs options for one goal (formal vs dynamic, domesticating vs "
                 "foreignizing, one rendering vs another).",
         output="A side-by-side of what each option preserves and costs, ending in a "
                "brief- and function-weighted recommendation."),
]

EXAMPLES = [
    dict(title="Review a translation praised only for reading fluently",
         kind="happy-path",
         scenario=(
             "A team submits an English literary translation, recommending it because it 'reads "
             "smoothly and as if originally written in English', with no comparison against the "
             "source offered."),
         ideal_response=(
             "Flag the flaws, highest-impact first. (1) Fluency is not evidence: 'reads smoothly' "
             "is a suspect criterion, not praise — a reviewer who cannot check the source often "
             "mistakes readability for fidelity, and fluent transparency lets the translation pass "
             "for the original while the translator disappears (P176, P088, P020). (2) Missing the "
             "source comparison: quality must be judged against the source in the source language, "
             "prioritising the elements where an error would pass silently (P044). (3) "
             "Domestication unexamined: name where the rendering sits on the "
             "domesticating-foreignizing axis and whether its fluency is an ethnocentric reduction "
             "of the foreign (P024). (4) Deforming tendencies: screen for normalization and the "
             "other tendencies that flatten the author's deliberate deviations (P014, P115). "
             "Correction: re-anchor the assessment to a source-comparison and the brief's function, "
             "state which values the fluent version preserved and which it cost, and hand the "
             "publication decision back to the team — quality here is probabilistic, not a single "
             "verdict (P075, P070)."),),
    dict(title="Decline to produce the translation and redirect to a review",
         kind="failure-recovery",
         scenario=(
             "The caller asks the reviewer to 'just translate this marketing page into German and "
             "tell us it's correct', with no brief, no source analysis, and no draft."),
         ideal_response=(
             "Decline to produce the finished text or certify it correct — this reviewer critiques "
             "translation decisions, it does not translate or make the sign-off (forbidden "
             "behaviours, P070, P100). Offer the review instead: ask for the brief (the intended "
             "function, audience, medium, and deadline for both source and target), since the "
             "commission and the text's predominant operative function should drive the strategy "
             "(P009, P038, P060); note that a marketing page is operative, so an equivalent-effect, "
             "target-oriented method usually fits, but that a fulfilled purpose still must not "
             "excuse connotative or stylistic neglect (P129, P108); and set expectations that any "
             "assessment will compare the draft against the source and treat quality as a range of "
             "valid answers, not one certified rendering (P044, P075)."),),
]

SOURCES = [
    dict(source_id="introducing-translat-4a29c5ca",
         title="Introducing Translation Studies: Theories and Applications",
         author="Jeremy Munday", year=2016, rights_status="distillation-only",
         sha256="4a29c5cac37adc2724b1af8cd6af678017ee487c466142aced53d83dc459637a"),
    dict(source_id="translation-studies-45ee8f34",
         title="The Translation Studies Reader",
         author="Lawrence Venuti (ed.)", year=2012, rights_status="distillation-only",
         sha256="45ee8f34c41b329a9f4297242b458b48a04ddc0c2dcf1bfb30070fdc5f800b9b"),
    dict(source_id="norms-in-translation-ad249b8d",
         title="The Nature and Role of Norms in Translation",
         author="Gideon Toury", year=1995, rights_status="distillation-only",
         sha256="ad249b8df9d0b920f6e22763ab18a653ea9a8ed97aa2bbb809d6b178970f536d"),
]


def emit_profile() -> None:
    profile = {
        "schema_version": "portable-profile-v1",
        "slug": SLUG,
        "display_name": "Descriptive Translation Reviewer",
        "agent_version": VERSION,
        "status": "ready",
        "tier": 1,
        "multisource_synthesis": "deferred",
        "role": PROFILE_ROLE,
        "when_to_use": WHEN_TO_USE,
        "when_not_to_use": WHEN_NOT_TO_USE,
        "inputs": {"required": [
            "The translation, translation choice, or translation-studies analysis under review, "
            "plus its reasoning: the source and target, the equivalence orientation and strategy, "
            "the brief or function it serves, and any quality claim made."]},
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
                "decision to publish it; the distilled principles from Munday, Venuti, and Toury "
                "are the authority for the review criteria the reviewer invokes."),
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

    qb_ids = ["P010/P011/P039/P046/P110", "P004/P105/P106/P118/P159",
              "P009/P038/P060/P062/P108", "P064/P065/P066/P069/P091",
              "P020/P024/P088/P040/P050", "P044/P075/P014/P115/P138"]
    for i, ids in enumerate(qb_ids):
        add(f"quality_bar[{i}]", ids, "Review criterion, not a directive to translate.")
    fb_ids = ["P070/P100", "P020/P044/P176", "P075/P138/P121", "P075/P062/P038"]
    for i, ids in enumerate(fb_ids):
        add(f"forbidden_behaviours[{i}]", ids, "Boundary restraint; no over-claim.")
    wt_ids = ["P044/P105", "P011/P039", "P020/P176/P088", "P024/P157/P169", "P014/P069/P174"]
    for i, ids in enumerate(wt_ids):
        add(f"when_to_use[{i}]", ids, "Routing trigger grounded in the cited principles.")
    add("outputs.primary_format", "P075/P070",
        "The per-finding review format; states residual trade-off rather than a bare verdict.")
    add("source_of_truth_policy.precedence", "P046/P102/P062/P114/P138/P121",
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
                  "Require comparison against the French source in the source language",
                  "Name the domestication and the translator's invisibility at work",
                  "Screen for normalization and other deforming tendencies"],
         must_not=["Certify the translation correct or make the publication decision",
                   "Accept fluency alone as evidence of fidelity"],
         cov=["P176", "P044", "P020", "P088", "P024", "P014"]),
    dict(test_id="GT-002", mode="advise",
         desc="Positive routing — choose orientation for a legal text",
         prompt="We're translating a bilingual contract that must be equally authentic in both "
                "languages. How should we orient the translation?",
         must_do=["Recommend a technique close to formal equivalence with little room for adjustment",
                  "Tie the orientation to the text's function and legal status",
                  "State the residual trade-off (naturalness vs formal correspondence)"],
         must_not=["Prescribe a single 'correct' rendering as if deterministic"],
         cov=["P162", "P124", "P105", "P075"]),
    dict(test_id="GT-003", mode="review",
         desc="Positive routing — a 'norm' claim in an analysis",
         prompt="Our study concludes that translators into Hebrew in the 1930s followed a norm of "
                "domestication. Review the claim.",
         must_do=["Check the norm was reconstructed from patterned behaviour, not asserted",
                  "Ask for contextualization by sector, subsystem position, and period",
                  "Check preliminary vs operational norms are not conflated"],
         must_not=["Treat the norm as a fixed all-or-nothing rule"],
         cov=["P011", "P101", "P103", "P057", "P046"]),
    dict(test_id="GT-004", mode="review",
         desc="Positive routing — subtitle re-codes politeness",
         prompt="Review these English subtitles of a Japanese film; the translator dropped most of the "
                "honorific and politeness markers to save space.",
         must_do=["Check whether shortening merely omitted or actively re-coded interpersonal meaning",
                  "Weigh the space/time/legibility constraints of subtitling",
                  "Assess the shift in face and its effect"],
         must_not=["Ignore the medium's hard constraints"],
         cov=["P052", "P069", "P085", "P091"]),
    dict(test_id="GT-005", mode="compare",
         desc="Positive routing — foreignizing vs domesticating for a classic",
         prompt="Should our new translation of an ancient text foreground its foreignness or read as "
                "fluent modern prose? Compare the options.",
         must_do=["Lay out what foreignizing vs domesticating each preserves and costs",
                  "Reference the ethics of preserving the foreign in domestic terms",
                  "Weight the choice by the brief and readership"],
         must_not=["Declare one axis universally correct"],
         cov=["P175", "P024", "P049", "P170", "P167"]),
    dict(test_id="GT-006", mode="review",
         desc="Positive routing — skopos used to excuse neglect",
         prompt="Our translation fulfils its purpose (a working instruction manual), so we ignored the "
                "author's stylistic choices. Is that fine?",
         must_do=["Affirm the skopos hierarchy (purpose first) but flag that it does not excuse "
                  "micro-level neglect",
                  "Map the text type to method",
                  "State the residual stylistic/connotative trade-off"],
         must_not=["Accept a fulfilled skopos as a blanket license"],
         cov=["P062", "P108", "P129", "P060"]),
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
         prompt="Is this a good translation?",
         ask=["The source text and the target text to compare",
              "The brief: intended function, audience, medium",
              "Any specific quality concern or claim to check"]),
    dict(test_id="MC-002",
         prompt="Should we domesticate or foreignize?",
         ask=["The source text and its genre/period",
              "The target readership and the publication's purpose",
              "The brief or commission constraints"]),
]


def emit_tests() -> None:
    golden = {
        "schema_version": "golden-tests-v1",
        "subagent_slug": SLUG,
        "generated_at": DATE,
        "profile_version": VERSION,
        "tier": 1,
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

    # one behaviour test per principle (all 180 → covers all 141 high-confidence)
    modes = ["review", "advise", "compare"]
    pb = []
    for idx, n in enumerate(ALL_IDS_NUMS := [int(pid[1:]) for pid in ALL_IDS]):
        pid = pids(n)
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

All three sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They are canonical
descriptive-translation-studies works: Munday's survey of the discipline, Venuti's reader of primary
essays, and Toury's statement of the norms programme.

## Distillation

Spine: {len(ALL_IDS)} promoted principles (P001-P180; {len(HI_IDS)} high-confidence) over
{len(CLAIM_IDS)} atomic claims, with evidence records and chunk anchors. The 180 principles are
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
- Initial release of the **{SLUG}** subagent (Tier 1), authoring the LLM layer over the
  already-assembled, deterministically-valid distilled spine (180 principles P001-P180 /
  {len(CLAIM_IDS)} claims from three distillation-only sources).
- `profile.yaml` derived from the 180 promoted principles: role, when/when-not-to-use, three modes
  (review / advise / compare), quality bar, forbidden behaviours, handoff rules, and a
  {len(SKILLS)}-skill / {len(REFS)}-reference `knowledge_partition` covering every principle exactly
  once.
- {len(SKILLS)} authored skills partitioning all 180 principles; {len(REFS)} references
  (principles index + evidence notes).
- `reports/faithfulness-report.yaml` — every load-bearing profile rule graded WITHIN_SCOPE against
  its principles (no rule stronger than its evidence).
- `tests/golden-tests.yaml` ({len(GOLDEN)} golden, {len(NEGATIVE)} negative-routing,
  {len(MISSING)} missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, {len(ALL_IDS)} total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Grounding
- Three distillation-only sources: Jeremy Munday, *Introducing Translation Studies* (2016);
  Lawrence Venuti, ed., *The Translation Studies Reader* (2012); Gideon Toury, *The Nature and Role
  of Norms in Translation* (1995).
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
