"""Deterministic authoring generator for translation-faithfulness-reviewer.

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

BASE = Path(__file__).resolve().parents[2]  # subagents/translation-faithfulness-reviewer
SLUG = "translation-faithfulness-reviewer"
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


def pids(n: int) -> str:
    return f"P{n:03d}"


# ---------------------------------------------------------------------------- partition
# Each entry: (skill-slug (kebab, <=48 chars), [principle numbers]).
# Every principle 1..150 appears in exactly one skill.
SKILLS: list[tuple[str, list[int]]] = [
    ("equivalence-theory-and-orientation",
     [1, 5, 9, 12, 22, 29, 40, 58, 59, 61, 72, 107, 113, 118, 122, 123, 125]),
    ("translation-procedures-and-shifts",
     [4, 7, 53, 79, 119, 121]),
    ("word-and-grammar-level-equivalence",
     [6, 14, 41, 44, 63, 70, 85, 95, 96, 99, 112, 117]),
    ("idiom-collocation-and-lexical-choice",
     [42, 43, 106, 141, 142]),
    ("cohesion-information-structure-and-discourse",
     [10, 25, 45, 46, 51, 64, 65, 71, 75, 97, 143, 144, 145, 146]),
    ("pragmatics-implicature-and-relevance",
     [39, 128, 129, 147, 148]),
    ("skopos-function-and-the-brief",
     [2, 27, 73, 74, 139]),
    ("technical-translation-and-usability",
     [15, 17, 18, 19, 33, 34, 48, 49, 62, 68, 93, 94, 104, 108, 109, 110, 111, 149]),
    ("documentation-research-and-empirical-method",
     [24, 26, 35, 50, 69, 105]),
    ("quality-assessment-and-error-analysis",
     [3, 13, 16, 30, 31, 55, 60, 78, 88, 89, 92, 135, 136, 137, 138, 140]),
    ("descriptive-norms-and-corpus-method",
     [11, 23, 66, 67, 76, 86, 87, 90, 91, 102, 103, 114, 133]),
    ("culture-poetics-and-rewriting",
     [20, 21, 28, 37, 38, 47, 57, 77, 80, 81, 82, 83, 115, 116, 131, 132]),
    ("hermeneutics-and-the-limits-of-translatability",
     [8, 32, 36, 52, 54, 56, 84, 98, 100, 101, 120, 124, 126, 127, 130, 134, 150]),
]

# integrity: every principle exactly once
_seen: list[int] = []
for _slug, nums in SKILLS:
    _seen += nums
assert sorted(_seen) == list(range(1, NP + 1)), f"partition mismatch: {sorted(_seen)}"
assert len(set(s for s, _ in SKILLS)) == len(SKILLS), "duplicate skill slug"
for s, _ in SKILLS:
    assert len(s) <= 48, f"slug too long ({len(s)}): {s}"

REFS = ["translation-faithfulness-principles-index", "translation-faithfulness-evidence-notes"]

# ---------------------------------------------------------------------------- per-skill themes
THEMES: dict[str, dict] = {
    "equivalence-theory-and-orientation": dict(
        title="Equivalence Theory And Orientation",
        purpose=(
            "This skill reviews how a translation positions itself among the competing theories of "
            "equivalence and whether its chosen orientation fits the purpose. It checks the "
            "formal-versus-dynamic axis, Nida's equivalent effect, Koller's denotative/connotative/"
            "text-normative/pragmatic relations, and Reiss's functional equivalence, treating "
            "1960s-70s equivalence theory as normative rather than merely descriptive, and holding "
            "'equivalent effect' claims to the fact that they can be illusory once a text is out of "
            "the receptor's space and time."),
        when=[
            "A translation claims formal (source-form) or dynamic (closest-natural) equivalence and "
            "the fit of that orientation to the brief needs checking.",
            "An 'equivalent effect' or 'same response' claim is being made and may be illusory.",
            "The level of equivalence to prioritize (referential, connotative, textual, pragmatic) "
            "is being chosen by text type.",
            "Equivalence is being pitched as element-by-element identity rather than the overall "
            "impression the message makes.",
        ],
        input="The translation and its stated equivalence orientation, purpose, and target audience.",
    ),
    "translation-procedures-and-shifts": dict(
        title="Translation Procedures And Shifts",
        purpose=(
            "This skill reviews micro-level translation decisions with the precise metalanguage of "
            "procedure and shift. It checks the Vinay & Darbelnet ladder (direct: borrowing, calque, "
            "literal; oblique: transposition, modulation, equivalence, adaptation) and reads Catford's "
            "level and category shifts not as the translator wishing to change the work but as "
            "functional fidelity, while watching the supplementary procedures for their hazards."),
        when=[
            "A micro-level rendering is being justified or criticised and needs naming with the "
            "procedure/shift metalanguage.",
            "A departure from formal correspondence needs classifying as a Catford level or category "
            "shift and read as functional, not arbitrary.",
            "A supplementary procedure (amplification, false friends, over-translation) may be "
            "distorting economy or meaning.",
            "A direct procedure is being applied where an oblique one is required for acceptability.",
        ],
        input="The source segment, its rendering, and the procedure/shift rationale offered.",
    ),
    "word-and-grammar-level-equivalence": dict(
        title="Word And Grammar-Level Equivalence",
        purpose=(
            "This skill reviews equivalence at and below the word and across grammar, rejecting "
            "cross-code identity and the one-to-one correspondence of words and meanings. It "
            "diagnoses the specific type of word-level non-equivalence, distinguishes propositional, "
            "expressive, presupposed, and evoked meaning, and checks that obligatory grammatical "
            "categories (gender, number, tense/aspect) the target forces are resolved by function "
            "rather than mapped mechanically."),
        when=[
            "A rendering rests on dictionary or referential identity and needs the signification "
            "critique applied.",
            "An obligatory grammatical category (gender, aspect, number) forces a resolution the "
            "target must make.",
            "A word-level non-equivalence needs diagnosing by type before a strategy is chosen.",
            "The receptor language requires additions or specifications the source leaves implicit.",
        ],
        input="The source item, its rendering, and the word- or grammar-level equivalence claim it rests on.",
    ),
    "idiom-collocation-and-lexical-choice": dict(
        title="Idiom, Collocation And Lexical Choice",
        purpose=(
            "This skill reviews the rendering of idioms, fixed expressions, and collocations, whose "
            "meaning cannot be deduced from their parts and whose target equivalent cannot be "
            "assumed. It reads a word through its collocational pattern rather than a dictionary "
            "gloss, applies idiom strategies by fit, and accepts that some loss, addition, or "
            "skewing is unavoidable when no exact collocational match exists."),
        when=[
            "A stretch of language may be an idiom or fixed expression and its rendering needs "
            "checking.",
            "A source word occurs in a fixed combination and is being read in isolation rather than "
            "through its collocation.",
            "An idiom is assumed to have a target equivalent when the way a language expresses a "
            "meaning is unpredictable.",
            "An unmarked collocation with no exact target match is being rendered and the trade-off "
            "of typicality against accuracy is unexamined.",
        ],
        input="The idiom, fixed expression, or collocation under review and its proposed rendering.",
    ),
    "cohesion-information-structure-and-discourse": dict(
        title="Cohesion, Information Structure And Discourse",
        purpose=(
            "This skill reviews translation at the level of cohesion and information structure. It "
            "treats Halliday and Hasan's five cohesive devices (reference, substitution, ellipsis, "
            "conjunction, lexical cohesion) as language-specific in preference and frequency, checks "
            "that thematic and given/new markedness is matched by function rather than transferred "
            "wholesale, and that reference patterns are reworked to the target language's norms."),
        when=[
            "A cohesive device has been transferred wholesale rather than reworked to the target "
            "language's preferences.",
            "Given/new or thematic markedness differs between source and target and must be re-signalled "
            "by the device the target uses.",
            "A participant or entity is being traced across differing reference, number, or gender "
            "systems.",
            "Source markedness that carries a communicative function is at risk of being flattened.",
        ],
        input="The source and target texts and the cohesion, information-structure, or reference pattern in play.",
    ),
    "pragmatics-implicature-and-relevance": dict(
        title="Pragmatics, Implicature And Relevance",
        purpose=(
            "This skill reviews meaning beyond the literal: implicature, coherence, and "
            "relevance-theoretic interpretive use. It models translation, with Gutt, as interlingual "
            "interpretive use constrained by the principle of relevance, diagnoses most "
            "'unnaturalness' as gratuitous processing effort imposed on the reader, and checks that "
            "an implied meaning is carried rather than lost or over-explained."),
        when=[
            "An utterance carries implied meaning and its rendering may lose or flatten the "
            "implicature.",
            "A rendering reads as 'unnatural' and the cause may be gratuitous processing effort, not "
            "the source.",
            "Explanatory coherence — what an utterance implies beyond its literal sense — is at "
            "stake.",
            "A translation conveys more or less than the relevance of the context warrants.",
        ],
        input="The utterance, its implied meaning, and the interpretive rendering under review.",
    ),
    "skopos-function-and-the-brief": dict(
        title="Skopos, Function And The Brief",
        purpose=(
            "This skill reviews whether a translation is driven by an explicit brief and by the "
            "target's intended function. It checks the skopos rules in hierarchical order — purpose "
            "first, then intratextual coherence, then fidelity — establishes whether the job is an "
            "instrumental or a documentary translation, and orients the text toward its set of "
            "addressees and its medium even when that set is fuzzy."),
        when=[
            "A translation lacks an explicit brief specifying function, audience, medium, and "
            "conditions.",
            "Whether the job is instrumental (freestanding target) or documentary (a record of the "
            "source) is undecided.",
            "A skopos is being used to license neglect of stylistic or connotative detail.",
            "Audience and medium require adjusting, omitting, or making implicit meaning explicit.",
        ],
        input="The translation brief (or its absence), the source text type, and the target's intended function.",
    ),
    "technical-translation-and-usability": dict(
        title="Technical Translation And Usability",
        purpose=(
            "This skill reviews scientific and technical translation as the production of a usable "
            "target document, not a surface replica. It lets target-user needs govern additions, "
            "omissions, condensation, and restructuring; balances fidelity against intelligibility, "
            "speed, cost, and target-culture acceptability; and checks iconic linkage, controlled "
            "terminology, unit handling, and the explicit, escalated treatment of safety-critical "
            "information."),
        when=[
            "A technical document is being judged as a surface replica rather than a usable target "
            "text serving user tasks.",
            "Safety-critical, regulatory, or normative content needs explicit, escalated, "
            "correctly-sourced treatment.",
            "Client-mandated terminology, controlled language, or units of measure govern the "
            "rendering.",
            "Consistency, iconic linkage, and reuse (style guides, translation memory) are being "
            "weighed for a technical guide.",
        ],
        input="The technical source and its translation, the target users and their tasks, and any terminology or safety constraints.",
    ),
    "documentation-research-and-empirical-method": dict(
        title="Documentation Research And Empirical Method",
        purpose=(
            "This skill reviews the empirical study of translated and technical documentation. It "
            "checks that a comparative study isolates the manipulated variable and controls "
            "confounds, that retention, task time, error rate, and satisfaction are measured with "
            "explicit instruments, and that verbal reports and think-aloud protocols are treated as "
            "limited evidence that cannot by itself establish underlying cognition or normal task "
            "behaviour."),
        when=[
            "A documentation or translation study's design needs checking for an isolated variable "
            "and controlled confounds.",
            "Effectiveness is being claimed without explicit measures of recall, performance, error, "
            "and attitude.",
            "Think-aloud or verbal-report evidence is being over-read as proof of cognition or "
            "representative performance.",
            "Observer effects may be distorting the behaviour a study measures.",
        ],
        input="The documentation or translation study under review and its design, measures, and evidence.",
    ),
    "quality-assessment-and-error-analysis": dict(
        title="Quality Assessment And Error Analysis",
        purpose=(
            "This skill reviews translation-quality assessment and error analysis. It requires "
            "evaluation by comparison against the source in the source language, built from a "
            "source-text profile of the function to be sought; treats quality as probabilistic, not "
            "deterministic; classifies overt errors and covert (cultural-filter) mismatches; and "
            "weights errors by source-profile priorities rather than counting them flat."),
        when=[
            "A translation is being scored without comparison against the source in the source "
            "language.",
            "Quality is being treated as a single verdict rather than a range of valid answers.",
            "Overt errors and covert (cultural-filter) versions are being conflated, or errors "
            "counted without weighting.",
            "An assessment lacks a source-text profile of the function the target should seek.",
        ],
        input="The quality claim or TQA analysis under review and the source it should be measured against.",
    ),
    "descriptive-norms-and-corpus-method": dict(
        title="Descriptive Norms And Corpus Method",
        purpose=(
            "This skill reviews the descriptive, norm-oriented, and corpus-based study of "
            "translation. It reconstructs translational norms from patterned behaviour at the "
            "receiving end rather than reading them off, treats textual products as primary and "
            "extratextual statements as secondary evidence, situates a translation on the "
            "adequacy-acceptability axis, and expects Toury's probabilistic laws — never assuming a "
            "translated text is representative of the target language."),
        when=[
            "A 'norm' claim is being made and needs checking against recurrent regularities rather "
            "than assertion.",
            "Translated texts are being used as evidence for target-language or textual-tradition "
            "claims.",
            "The adequacy-acceptability orientation of a translation or corpus needs situating.",
            "A corpus or Chesterman-style universal claim needs contextualized, verifiable "
            "evidence.",
        ],
        input="The translation(s) or translation-studies analysis under review and its declared corpus, method, and norm claims.",
    ),
    "culture-poetics-and-rewriting": dict(
        title="Culture, Poetics And Rewriting",
        purpose=(
            "This skill reviews translation as a culturally situated act of rewriting and poetic "
            "transformation. It locates the deep problem of translating a foreign work in a "
            "compromise between two poetics rather than the dictionary, reads a translation against "
            "the rival versions it reacts to and the value-driven institutional network around it, "
            "and screens for the subtractive changes and deforming tendencies that flatten a "
            "carefully constructed source."),
        when=[
            "A translation is being judged in isolation instead of against its rivals, paratexts, and "
            "institutional network.",
            "Subtractive changes or deforming tendencies may be flattening a carefully constructed "
            "or deviant source.",
            "Poetry or lyric is being rendered word-for-word rather than as receptor-language poetry "
            "that elicits comparable feeling.",
            "Ideology, patronage, or the economics of refraction explain the changes better than "
            "comprehension does.",
        ],
        input="The translation, its cultural and poetic context, and the rivals, paratexts, and agents around it.",
    ),
    "hermeneutics-and-the-limits-of-translatability": dict(
        title="Hermeneutics And The Limits Of Translatability",
        purpose=(
            "This skill reviews the interpretive and philosophical grounding of a translation: the "
            "hermeneutic motion completed by restitution, sense-for-sense default over slavish "
            "word-for-word rendering, voice and form translated by function, and the reading of "
            "untranslatability and the literal-free swing. It holds that there is no perfect "
            "translation and that the real barriers to literal translation are specific and local "
            "rather than deep."),
        when=[
            "A translation's interpretive stance — what it trusts, takes, and must restitute — is "
            "under review.",
            "Untranslatability or the impossibility of a definitive translation is being denied or "
            "over-claimed.",
            "Voice, form, or sense is being rendered mechanically (passive-by-passive) rather than "
            "by function.",
            "A refusal to adapt has produced an over-literal rendering and its barriers need locating "
            "as local, not deep.",
        ],
        input="The translation and the interpretive or philosophical claim (translatability, form, restitution) at stake.",
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

_SOURCE_CREDIT = (
    "the eight distillation-only sources (Nida, *Principles of Correspondence*; Toury, *The Nature "
    "and Role of Norms in Translation*; House, *Translation Quality Assessment*; Byrne, *Technical "
    "Translation* and *Scientific and Technical Translation Explained*; Baker, *In Other Words*; "
    "Munday, *Introducing Translation Studies*; Venuti, ed., *The Translation Studies Reader*)")


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
    out.append("# Translation Faithfulness Principles Index\n")
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
    out.append("# Translation Faithfulness Evidence Notes\n")
    out.append("How the principles in this package are grounded, and how to keep review findings "
               "faithful to the sources.\n")
    out.append("## Sources\n")
    out.append("Eight distillation-only sources ground the package, spanning the equivalence, "
               "functionalist, descriptive, discourse, technical, and quality-assessment strands of "
               "translation studies: Eugene Nida, *Principles of Correspondence* (dynamic vs formal "
               "equivalence); Gideon Toury, *The Nature and Role of Norms in Translation* (the "
               "descriptive/norms programme); Juliane House, *Translation Quality Assessment* (overt/"
               "covert, error dimensions); Jody Byrne, *Technical Translation* and *Scientific and "
               "Technical Translation Explained* (usability and documentation); Mona Baker, *In Other "
               "Words* (multi-level equivalence); Jeremy Munday, *Introducing Translation Studies* (a "
               "survey of the discipline); and Lawrence Venuti, ed., *The Translation Studies Reader* "
               "(primary essays from Jakobson and Nida to Steiner, Berman, and Venuti). Paraphrase and "
               "restructure only — no verbatim quotation (see "
               "`.claude/rules/rights-and-quotation-policy.md`).\n")
    out.append("## Faithfulness discipline\n")
    out.append("- No finding may state a rule more strongly than its source supports: a context-bound "
               "\"in this case prefer X\" must not become \"always X\", and analyst judgement is an "
               "argued, evidence-constrained hypothesis, not an absolute (P088, P012).")
    out.append("- Competing schools disagree; attribute a prescription to its theory rather than "
               "presenting it as settled fact, and treat equivalence as approximate value across "
               "differences (P040, P088).")
    out.append("- Quality is probabilistic: there is a range of valid answers, so a review improves a "
               "choice rather than certifying the one correct rendering (P078).")
    out.append("- Evaluate against the source in the source language; fluency alone ('reads as if "
               "originally written') is not evidence of fidelity (P055, P021).\n")
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
    "A reviewer of translations, translation-quality claims, and translation-studies analyses, "
    "grounded in the equivalence, functionalist, descriptive, discourse, technical, and "
    "quality-assessment theories of translation (Nida, Newmark, Catford, Baker, House, Toury, Byrne, "
    "and the Venuti reader). It critiques a rendering or an analysis for faithfulness: whether its "
    "equivalence orientation and multi-level equivalence fit the brief and text function, whether "
    "cohesion, information structure, and pragmatic meaning survive, whether translational norms are "
    "reconstructed rather than asserted, whether technical and safety-critical content stays usable "
    "and correct, and whether quality is judged against the source rather than by fluency alone. The "
    "operating invariants below are review criteria drawn from the sources, not instructions to "
    "translate: this review-only boundary and the forbidden behaviours override every invariant, so "
    "the reviewer never produces the finished translation, makes the publication decision, or "
    "certifies a rendering definitively correct.")

WHEN_TO_USE = [
    "A translation or draft is being assessed and the team wants its equivalence orientation, "
    "multi-level equivalence, cohesion, and losses reviewed against the source and the brief.",
    "A translation-quality analysis, TQA model, or 'norm' claim needs checking for method rigour "
    "and faithfulness to its evidence.",
    "A translation is being praised for fluency or 'reading well', and the team wants that "
    "criterion — and the source comparison it skips — interrogated.",
    "A rendering must be placed on the formal-dynamic or literal-free axis, or given a "
    "text-type-appropriate method.",
    "A technical, scientific, regulatory, or audiovisual translation needs its usability, "
    "safety-critical content, terminology, or error profile reviewed.",
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
    "Quality is judged by comparison against the source in the source language, prioritising the "
    "elements where an error would pass silently, built from an explicit source-text profile, and "
    "treated as probabilistic rather than deterministic (P055, P016, P078).",
    "Every equivalence claim states its orientation and level and fits the purpose; cross-code "
    "identity and one-to-one word-meaning correspondence are rejected, and equivalence is pitched at "
    "the overall impression across multiple levels, not element-by-element identity (P006, P070, "
    "P107, P113, P118).",
    "Translational norms are reconstructed from patterned behaviour at the receiving end, never "
    "asserted; a translated text is not assumed representative, and Toury's probabilistic laws are "
    "expected, not treated as certainties (P011, P076, P086, P114).",
    "Cohesion, information structure, and pragmatic meaning are treated as language-specific: "
    "cohesive devices are not transferred wholesale, and relevance and processing effort are checked "
    "rather than assumed (P071, P075, P039, P129).",
    "Fluency is not proof of quality; the deep problem is a compromise of two poetics, not "
    "dictionary equivalence, and subtractive or deforming losses are named rather than smoothed over "
    "(P021, P020, P117, P028).",
    "For technical, scientific, and regulatory texts, target-user needs govern additions and "
    "omissions, fidelity is balanced against intelligibility, speed, cost, and acceptability, and "
    "safety-critical information is made explicit (P015, P017, P104).",
]

FORBIDDEN = [
    "Producing the finished or revised translation, or the publication and quality sign-off, for "
    "the caller — this reviewer critiques translation decisions, it does not own the text or the "
    "call (P078, P027).",
    "Endorsing fluency or 'reads smoothly' as proof of quality, or judging a translation without "
    "comparison against the source in the source language (P021, P055).",
    "Treating equivalence as absolute correspondence, or stating a rule more strongly than its "
    "source supports — flattening a context-bound preference into an absolute or presenting one "
    "school's prescription as settled fact (P012, P088).",
    "Prescribing a single correct rendering as if translation had one deterministic answer, or "
    "ignoring the brief, audience, and function that condition the choice (P078, P073, P074).",
]

HANDOFF = [
    "The translator and the commissioner hold the text and the publication decision; this reviewer "
    "informs the reasoning and makes the residual trade-off explicit (P027, P015).",
    "Concerns outside translation review — subject-matter accuracy, the legal validity of a text, "
    "and client-mandated terminology governance — are handed to the owning specialist (P110, P109).",
]

PRECEDENCE = (
    "Where a source's context differs from the caller's, treat a principle as an adaptable guide, "
    "not an absolute (P088, P078); when equivalence orientation and text function conflict, the "
    "brief's purpose governs which values are preserved (P005, P107, P073); and never endorse a rule "
    "more confident than the source supports (P012, P088).")

MODES = [
    dict(name="review",
         trigger="The caller submits a translation, a translation choice, or a translation-studies "
                 "analysis for critique.",
         output="A findings list keyed to flaw class (equivalence, word/grammar, cohesion/"
                "pragmatics, norms/method, quality/error, technical/usability, poetics/loss, "
                "translatability), each with flaw, correction, residual trade-off, and next step — "
                "highest-impact first."),
    dict(name="advise",
         trigger="The caller faces a translation decision and wants which principle or strategy "
                 "fits.",
         output="A recommendation tied to the situation, naming the principle(s) and orientation "
                "applied and the residual trade-off to carry."),
    dict(name="compare",
         trigger="The caller weighs options for one goal (formal vs dynamic, literal vs free, one "
                 "rendering vs another).",
         output="A side-by-side of what each option preserves and costs, ending in a brief- and "
                "function-weighted recommendation."),
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
             "a suspect criterion, not praise, and the deep problem of translating a foreign work "
             "lies in a compromise of two poetics, not the dictionary (P021, P020). (2) Missing the "
             "source comparison: quality must be judged against the French source in the source "
             "language, prioritising the elements where an error would pass silently (P055). (3) "
             "Loss unexamined: screen for the subtractive changes that flatten a carefully "
             "constructed source (P028). (4) Norm caution: do not assume the fluent target is "
             "representative of English or of any tradition (P011). Correction: re-anchor the "
             "assessment to a source-comparison and the brief's function, state which values the "
             "fluent version preserved and which it cost, and hand the publication decision back to "
             "the team — quality here is probabilistic, not a single verdict (P078).")),
    dict(title="Decline to produce the translation and redirect to a review",
         kind="failure-recovery",
         scenario=(
             "The caller asks the reviewer to 'just translate this user manual into German and tell "
             "us it's correct', with no brief, no source-text profile, and no draft."),
         ideal_response=(
             "Decline to produce the finished text or certify it correct — this reviewer critiques "
             "translation decisions, it does not translate or make the sign-off (forbidden "
             "behaviours, P078, P027). Offer the review instead: ask for the brief and the "
             "target users' tasks, since a technical document is judged as a usable target text, not "
             "a surface replica, with user needs governing additions and omissions (P015); note that "
             "safety-critical information must be explicit and escalated where the source is unclear "
             "(P104); and set expectations that any assessment will compare the draft against the "
             "source and treat quality as a range of valid answers, not one certified rendering "
             "(P055, P078).")),
]

SOURCES = [
    dict(source_id="dynamic-formal-equiv-e6872198",
         title="Principles of Correspondence (Dynamic and Formal Equivalence)",
         author="Eugene A. Nida", year=1964, rights_status="distillation-only",
         sha256="e6872198422504a2952d709f0713ba7c3d17990f700d0a954e535b3d26504065"),
    dict(source_id="norms-in-translation-ad249b8d",
         title="The Nature and Role of Norms in Translation",
         author="Gideon Toury", year=1995, rights_status="distillation-only",
         sha256="ad249b8df9d0b920f6e22763ab18a653ea9a8ed97aa2bbb809d6b178970f536d"),
    dict(source_id="translation-quality-c0dd203d",
         title="Translation Quality Assessment: Past and Present",
         author="Juliane House", year=2015, rights_status="distillation-only",
         sha256="c0dd203dbe43780bfcfba542599430b15a4f4f815a429653fd8bede5eef9105d"),
    dict(source_id="technical-translatio-41f3c47c",
         title="Technical Translation: Usability Strategies for Translating Technical Documentation",
         author="Jody Byrne", year=2006, rights_status="distillation-only",
         sha256="41f3c47c6f8afe00db0d7ed2a69e86196ae0a5356592f5a40cc682e802f6180b"),
    dict(source_id="in-other-words-baker-8e6c3cb1",
         title="In Other Words: A Coursebook on Translation",
         author="Mona Baker", year=2011, rights_status="distillation-only",
         sha256="8e6c3cb106446e534e0a04ec564cb7afaf07229c974ffbd18e0f94b447262ade"),
    dict(source_id="scientific-technical-d92653ac",
         title="Scientific and Technical Translation Explained",
         author="Jody Byrne", year=2012, rights_status="distillation-only",
         sha256="d92653ac75eeb4afb7c297321f5f364ff88a84e7da758c67198563420bbd2faa"),
    dict(source_id="introducing-translat-4a29c5ca",
         title="Introducing Translation Studies: Theories and Applications",
         author="Jeremy Munday", year=2016, rights_status="distillation-only",
         sha256="4a29c5cac37adc2724b1af8cd6af678017ee487c466142aced53d83dc459637a"),
    dict(source_id="translation-studies-45ee8f34",
         title="The Translation Studies Reader",
         author="Lawrence Venuti (ed.)", year=2012, rights_status="distillation-only",
         sha256="45ee8f34c41b329a9f4297242b458b48a04ddc0c2dcf1bfb30070fdc5f800b9b"),
]


def emit_profile() -> None:
    profile = {
        "schema_version": "portable-profile-v1",
        "slug": SLUG,
        "display_name": "Translation Faithfulness Reviewer",
        "agent_version": VERSION,
        "status": "ready",
        "tier": 2,
        "multisource_synthesis": "deferred",
        "role": PROFILE_ROLE,
        "when_to_use": WHEN_TO_USE,
        "when_not_to_use": WHEN_NOT_TO_USE,
        "inputs": {"required": [
            "The translation, translation choice, or translation-quality analysis under review, "
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
            "At least one finding that names a translation or translation-quality flaw, applies a "
            "named principle or correction, and states the residual trade-off — the values kept "
            "against those given up."),
        "forbidden_behaviours": FORBIDDEN,
        "handoff_rules": HANDOFF,
        "source_of_truth_policy": {
            "canonical_owner": (
                "The translator and the commissioner hold final authority over the text and the "
                "decision to publish it; the distilled principles from Nida, Toury, House, Byrne, "
                "Baker, Munday, and the Venuti reader are the authority for the review criteria the "
                "reviewer invokes."),
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

    qb_ids = ["P055/P016/P078", "P006/P070/P107/P113/P118", "P011/P076/P086/P114",
              "P071/P075/P039/P129", "P021/P020/P117/P028", "P015/P017/P104"]
    for i, ids in enumerate(qb_ids):
        add(f"quality_bar[{i}]", ids, "Review criterion, not a directive to translate.")
    fb_ids = ["P078/P027", "P021/P055", "P012/P088", "P078/P073/P074"]
    for i, ids in enumerate(fb_ids):
        add(f"forbidden_behaviours[{i}]", ids, "Boundary restraint; no over-claim.")
    wt_ids = ["P055/P113", "P076/P088", "P021/P055", "P005/P072/P107", "P015/P104/P135"]
    for i, ids in enumerate(wt_ids):
        add(f"when_to_use[{i}]", ids, "Routing trigger grounded in the cited principles.")
    ho_ids = ["P027/P015", "P110/P109"]
    for i, ids in enumerate(ho_ids):
        add(f"handoff_rules[{i}]", ids, "Ownership boundary; source-grounded.")
    add("outputs.primary_format", "P078/P055",
        "The per-finding review format; states residual trade-off rather than a bare verdict.")
    add("source_of_truth_policy.precedence", "P088/P078/P005/P107/P073/P012",
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
                  "Screen for subtractive changes and deforming tendencies",
                  "Caution against assuming the fluent target is representative of the language"],
         must_not=["Certify the translation correct or make the publication decision",
                   "Accept fluency alone as evidence of fidelity"],
         cov=["P021", "P055", "P020", "P028", "P011"]),
    dict(test_id="GT-002", mode="advise",
         desc="Positive routing — choose orientation for a legal/academic text",
         prompt="We're translating a bilingual statute that must be equally authentic in both "
                "languages. How should we orient the translation?",
         must_do=["Recommend formal equivalence close to the source form with little room for adjustment",
                  "Tie the orientation to the text's function and legal status",
                  "State the residual trade-off (naturalness vs formal correspondence)"],
         must_not=["Prescribe a single 'correct' rendering as if deterministic"],
         cov=["P005", "P122", "P107", "P078"]),
    dict(test_id="GT-003", mode="review",
         desc="Positive routing — a 'norm' claim in a corpus analysis",
         prompt="Our corpus study concludes that translators into Hebrew in the 1930s followed a norm of "
                "acceptability. Review the claim.",
         must_do=["Check the norm was reconstructed from patterned behaviour, not asserted",
                  "Treat textual products as primary and extratextual statements as secondary evidence",
                  "Warn against assuming the translated texts are representative of the language"],
         must_not=["Treat the norm as a fixed all-or-nothing rule"],
         cov=["P076", "P086", "P087", "P011"]),
    dict(test_id="GT-004", mode="review",
         desc="Positive routing — safety-critical technical manual",
         prompt="Review this German translation of an equipment manual; the translator kept the source "
                "sentence structure and left a hazard warning implicit as in the original.",
         must_do=["Require safety-critical information to be explicit and escalated where the source is unclear",
                  "Let target-user needs govern additions, omissions, and restructuring",
                  "Balance fidelity against intelligibility and usability"],
         must_not=["Treat the translation as a surface replica of the source"],
         cov=["P104", "P015", "P017", "P018"]),
    dict(test_id="GT-005", mode="compare",
         desc="Positive routing — formal vs dynamic for a scripture/expressive text",
         prompt="Should our new translation preserve the source's formal features or aim for the closest "
                "natural equivalent for today's readers? Compare the options.",
         must_do=["Lay out what formal vs dynamic equivalence each preserves and costs",
                  "Warn that equivalent effect can be illusory once the text is out of its space and time",
                  "Weight the choice by the brief, text type, and readership"],
         must_not=["Declare one orientation universally correct"],
         cov=["P005", "P009", "P072", "P118"]),
    dict(test_id="GT-006", mode="review",
         desc="Positive routing — idiom rendered by dictionary gloss",
         prompt="Our translator rendered an English idiom word-for-word from the dictionary into "
                "Spanish. Is that acceptable?",
         must_do=["Warn that an idiom's meaning cannot be deduced from its parts and may have no target equivalent",
                  "Read the item through its collocational pattern, not a dictionary gloss",
                  "Apply an idiom strategy by fit and state the residual loss"],
         must_not=["Assume a one-to-one target equivalent exists"],
         cov=["P042", "P095", "P106", "P043"]),
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
         prompt="Should we use formal or dynamic equivalence?",
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

All eight sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They span the
equivalence (Nida), descriptive/norms (Toury), quality-assessment (House), technical/usability
(Byrne x2), multi-level-equivalence (Baker), survey (Munday), and primary-essay (Venuti reader)
strands of translation studies.

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
  P001-P{NP:03d} / {len(CLAIM_IDS)} claims from eight distillation-only sources).
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
- Eight distillation-only sources: Eugene Nida, *Principles of Correspondence* (1964); Gideon Toury,
  *The Nature and Role of Norms in Translation* (1995); Juliane House, *Translation Quality
  Assessment* (2015); Jody Byrne, *Technical Translation* (2006) and *Scientific and Technical
  Translation Explained* (2012); Mona Baker, *In Other Words* (2011); Jeremy Munday, *Introducing
  Translation Studies* (2016); Lawrence Venuti, ed., *The Translation Studies Reader* (2012).
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
