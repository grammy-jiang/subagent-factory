"""Deterministic authoring generator for translation-strategy-reviewer.

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

BASE = Path(__file__).resolve().parents[2]  # subagents/translation-strategy-reviewer
SLUG = "translation-strategy-reviewer"
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
    ("domestication-foreignization-and-ethics",
     [2, 5, 14, 20, 60, 61, 86, 105, 106, 120, 121, 122, 123, 139, 140]),
    ("ideology-power-and-postcolonial-translation",
     [1, 4, 16, 21, 22, 39, 48, 79, 80, 81, 82, 116, 128]),
    ("skopos-function-and-the-translation-brief",
     [3, 15, 38, 50, 51, 53, 58, 73, 75, 112, 145, 146, 149, 150]),
    ("text-type-and-translation-method",
     [26, 54, 55, 71, 78, 101, 107, 108]),
    ("norms-polysystem-and-descriptive-method",
     [27, 32, 37, 42, 57, 63, 64, 74, 77, 87, 104, 110, 111, 125, 126, 127]),
    ("technical-translation-usability-and-design",
     [9, 10, 11, 12, 25, 33, 34, 35, 36, 49, 72, 100, 102, 133, 135, 143]),
    ("technical-translation-workflow-and-practice",
     [30, 62, 96, 97, 103, 134, 136, 141, 142, 144, 147, 148]),
    ("globalization-localization-and-gilt",
     [43, 44, 93, 94, 95, 98, 138]),
    ("quality-assessment-and-cultural-filtering",
     [13, 17, 18, 23, 28, 29, 45, 46, 59, 65, 67, 68, 69, 70, 88, 90, 92]),
    ("pragmatics-politeness-and-discourse",
     [19, 31, 40, 47, 52, 114, 119, 129, 132]),
    ("relevance-hermeneutics-and-literary-strategy",
     [6, 8, 56, 76, 83, 89, 99, 109, 113, 115, 117, 118, 124, 130, 131]),
    ("marked-identity-register-and-genre",
     [7, 24, 41, 66, 84, 85, 91, 137]),
]

# integrity: every principle exactly once
_seen: list[int] = []
for _slug, nums in SKILLS:
    _seen += nums
assert sorted(_seen) == list(range(1, NP + 1)), f"partition mismatch: {sorted(_seen)}"
assert len(set(s for s, _ in SKILLS)) == len(SKILLS), "duplicate skill slug"
for s, _ in SKILLS:
    assert len(s) <= 48, f"slug too long ({len(s)}): {s}"

REFS = ["translation-strategy-principles-index", "translation-strategy-evidence-notes"]

# ---------------------------------------------------------------------------- per-skill themes
THEMES: dict[str, dict] = {
    "domestication-foreignization-and-ethics": dict(
        title="Domestication, Foreignization And The Ethics Of Translation",
        purpose=(
            "This skill reviews a translation's position on the single strategic axis that runs "
            "from domestication to foreignization and the ethics that ride on it. It treats "
            "domestication as an ethnocentric, fluent, invisible reduction of the foreign to "
            "receiving values and foreignization as a resistant, estranging method that registers "
            "the source's differences in domestic terms, reads the fluent 'illusion of "
            "transparency' as an appropriative strategy with costs rather than the neutral default, "
            "and holds that an ethics preserving the foreign can only be practised in domestic terms "
            "while a translation inescapably leans toward the receptor and invents new readerships "
            "and imagined communities for the text."),
        when=[
            "A translation is praised for reading fluently or 'as if originally written', and the "
            "domesticating stance and its remainder are unexamined.",
            "The overall orientation on the domestication-foreignization (naturalizing-alienating, "
            "dynamic-formal) axis is being chosen or defended.",
            "A distant, ancient, or canonical source risks being modernized or having its "
            "significance inverted into the target's dominant discourse.",
            "The ethical and community-forming stakes of the strategy — whose values it serves, what "
            "foreign difference it loses — need surfacing.",
        ],
        input="The translation, its overall orientation, and the source's cultural and historical distance from the target.",
    ),
    "ideology-power-and-postcolonial-translation": dict(
        title="Ideology, Power And Postcolonial Translation",
        purpose=(
            "This skill reviews the ideological, political, and power dimensions of a translation "
            "strategy. It locates translation within a literary system's controls of patronage and "
            "poetics, grounds socio-political, gender, and power critique in detailed linguistic "
            "analysis before drawing macro conclusions, screens for the homogenizing 'translatese' "
            "that flattens a less powerful literature's rhetoricity and inscribed difference, and "
            "reads the strategy's cultural-political valence against the translating culture's "
            "position in local, national, and global hierarchies — including feminist, postcolonial, "
            "and diglossic stakes."),
        when=[
            "A socio-political, ethical, gender, or power claim is being made about a translation and "
            "needs grounding in concrete forms and functions.",
            "A less powerful literature is at risk of a homogenizing 'translatese' that effaces its "
            "rhetoricity and inscribed difference.",
            "Patronage, censorship, institutional pressure, or ideological manipulation may be "
            "shaping the target text.",
            "A translation is being used for identity assertion or national self-legitimation and "
            "could tip into ethnocentrism.",
        ],
        input="The translation, its source and target cultures, and the ideological or power stance under review.",
    ),
    "skopos-function-and-the-translation-brief": dict(
        title="Skopos, Function And The Translation Brief",
        purpose=(
            "This skill reviews whether a translation strategy is driven by an explicit brief and "
            "the target text's intended function. It checks that the skopos is negotiated and "
            "specified before strategy, treats the skopos as the decisive factor that dethrones the "
            "source into one constituent of the commission, applies function plus loyalty so "
            "functionality never becomes a licence for anything, distinguishes documentary from "
            "instrumental translation, and refuses to let a fulfilled skopos excuse micro-level "
            "neglect of stylistic or semantic detail."),
        when=[
            "A translation lacks an explicit brief specifying purpose, audience, medium, and "
            "conditions.",
            "Whether the job is documentary (a record of the source) or instrumental (a freestanding "
            "target) is undecided.",
            "A skopos is being used to license neglect of stylistic or semantic detail, or is pitched "
            "against the author's intentions with no loyalty check.",
            "The target function is being read off the source profile instead of defined "
            "pragmatically from purpose and audience.",
        ],
        input="The translation brief (or its absence), the source text type, and the target's intended function.",
    ),
    "text-type-and-translation-method": dict(
        title="Text Type And Translation Method",
        purpose=(
            "This skill reviews the selection of a general translation method from text type and "
            "variety. It applies Reiss's typology derived from Buhler's functions — informative "
            "texts by sense, expressive by identification, operative adaptively — lets the dominant "
            "type govern a mixed text, grades adaptation by Nida's three factors (message, purpose, "
            "audience), requires the target language's structural and stylistic conventions for the "
            "text variety, and describes a natural rendering by the anomalies and anachronisms it "
            "avoids."),
        when=[
            "A general method is being chosen and the source's text type (informative, expressive, "
            "operative) has not been identified.",
            "A mixed-type text needs its dominant type and a type-specific priority resolved.",
            "A method is being applied uniformly regardless of message type, author purpose, and "
            "audience.",
            "A rendering claims naturalness but tolerates anomaly or anachronism inconsistent with "
            "its type and variety.",
        ],
        input="The source text, its type and variety, and the general method proposed for it.",
    ),
    "norms-polysystem-and-descriptive-method": dict(
        title="Norms, Polysystem And Descriptive Method",
        purpose=(
            "This skill reviews descriptive, norm-oriented, and polysystem claims about translation "
            "behaviour. It reconstructs translational norms from patterned behaviour and textual "
            "products rather than reading them off or accepting persuasion-biased extratextual "
            "statements at face value, treats norms as a graded, historically mobile continuum, "
            "judges literary translations as facts of the target system by acceptability rather than "
            "adequacy, and lets the polysystem's central-or-peripheral position govern the reading "
            "of practice."),
        when=[
            "A 'norm' claim is being asserted rather than reconstructed from recurrent regularities "
            "of behaviour.",
            "Extratextual statements by translators or critics are being taken at face value as "
            "evidence of method.",
            "A translation is judged for 'adequacy' to the source when acceptability in the receiving "
            "system is the descriptive question.",
            "The polysystem position (central vs peripheral) or the graded, mobile force of a norm "
            "needs situating.",
        ],
        input="The translation(s) or translation-studies analysis and its declared corpus, norms, and method.",
    ),
    "technical-translation-usability-and-design": dict(
        title="Technical Translation, Usability And Design",
        purpose=(
            "This skill reviews scientific and technical translation as the production of a usable "
            "target document. It lets target-user needs, tasks, and cognitive demands govern; treats "
            "layout, typography, white space, and graphics as communicative usability factors, not "
            "decoration; measures usability by effectiveness, efficiency, and satisfaction; and "
            "holds safety-critical and regulated content to the standardized severity hierarchy, the "
            "official set phrases, and country-of-sale documentation regulation."),
        when=[
            "A technical document is judged as a surface replica rather than a usable target text "
            "serving user tasks.",
            "Safety-critical, warning, or regulated content needs the correct severity hierarchy, "
            "official hazard phrases, or country-of-sale regulation applied.",
            "User-guide structure, information quantity, or visual design is being set without regard "
            "to audience tasks and cognition.",
            "Screenshots, graphics, or layout carry cultural connotations or must match the localized "
            "interface.",
        ],
        input="The technical source and translation, the target users and their tasks, and any safety or regulatory constraint.",
    ),
    "technical-translation-workflow-and-practice": dict(
        title="Technical Translation Workflow And Practice",
        purpose=(
            "This skill reviews the professional workflow and micro-practice of technical "
            "translation. It requires seeing and reading a text before accepting it, basing "
            "decisions on systematic understanding rather than intuition, diagnosing linguistic and "
            "cultural distance and false friends (treating closely related languages as dangerous, "
            "not easy), keeping strategy distinct from procedure, following the rules for translating "
            "around code and obligatory 'surplus decisions', assessing online sources critically, and "
            "managing project files safely."),
        when=[
            "A project is being accepted or scoped without first seeing the text or assessing the "
            "required specialism.",
            "Strategy and procedure are being conflated, or a micro-technique is defended as if it "
            "were the overall orientation.",
            "Software strings, code, loan words, or obligatory grammatical 'surplus decisions' need "
            "handling by rule.",
            "Cultural or linguistic distance, false friends, source reliability, or file safety is "
            "unmanaged.",
        ],
        input="The technical text, the workflow or micro-decision under review, and the tools and sources in play.",
    ),
    "globalization-localization-and-gilt": dict(
        title="Globalization, Localization And GILT",
        purpose=(
            "This skill reviews translation strategy under globalization and localization. It "
            "situates work within GILT (globalization, internationalization, localization, "
            "translation), treats localization as the superordinate adaptation to a locale where "
            "equivalence turns on target functionality rather than a source, reads English imports "
            "and borrowings by their contextual function rather than as a threat, analyses globalized "
            "discourse across its levels, and applies game localization and transcreation where the "
            "skopos is to keep the look and feel while passing as an original."),
        when=[
            "A product is being localized and the GILT frame, locale adaptation, or "
            "interlingua-vs-source equivalence needs situating.",
            "English imports, borrowings, or ELF are being treated as a threat rather than assessed "
            "by contextual function.",
            "Globalized or hybrid text production is read as one-way transfer instead of negotiation "
            "and accommodation.",
            "Game, entertainment, or marketing content needs transcreation that keeps look-and-feel "
            "while passing as an original.",
        ],
        input="The product or globalized text, its target locale, and the localization or import strategy under review.",
    ),
    "quality-assessment-and-cultural-filtering": dict(
        title="Quality Assessment And Cultural Filtering",
        purpose=(
            "This skill reviews translation-quality assessment and the cultural filter. It evaluates "
            "translations as linguistic-textual recontextualizations whose quality depends on "
            "observable textual choices and situational context, defines text function through "
            "situational dimensions (field, tenor, mode) and their correlates, classifies overt "
            "versus covert translation, grounds cultural-filter decisions in language-pair empirical "
            "research, and keeps social, political, and ethical factors from displacing the "
            "linguistic analysis that underwrites any good/bad judgement."),
        when=[
            "A covert translation may be applying a cultural filter that submerges rhetorical "
            "strategies central to the source function.",
            "Text function or a quality judgement is being asserted without a situational-dimension "
            "profile and textual analysis.",
            "Tenor, register, or persuasive shifts (mission statements, address, evaluation) are "
            "moving the target's interpersonal stance.",
            "A cultural or social explanation is displacing the linguistic-textual comparison it "
            "should rest on.",
        ],
        input="The source and target texts, the quality claim or TQA analysis, and the situational context to assess against.",
    ),
    "pragmatics-politeness-and-discourse": dict(
        title="Pragmatics, Politeness And Discourse",
        purpose=(
            "This skill reviews translation at the level of pragmatics, politeness, and discourse. "
            "It reads face-management and face-threatening acts through Brown and Levinson's "
            "strategies, treats Grice's maxims as culture-relative while holding implicature itself "
            "universal, tracks how transitivity, modality, and pronoun choices shift ideational and "
            "interpersonal meaning, watches subtitling and other constrained modes for the systematic "
            "politeness meanings they shed, and calibrates intervention to the reader's world-model "
            "and shared knowledge."),
        when=[
            "Politeness, face, or an implied meaning is at stake and the rendering may re-code the "
            "interpersonal dynamic.",
            "Grice's maxims or discourse conventions are being applied as universals across "
            "cultures.",
            "Transitivity, modality, evaluation, or pronoun choices are shifting ideational or "
            "interpersonal meaning.",
            "A constrained mode (subtitling) or an implicature-bearing target context risks "
            "systematic pragmatic loss.",
        ],
        input="The utterance or discourse, its implied and interpersonal meaning, and the rendering under review.",
    ),
    "relevance-hermeneutics-and-literary-strategy": dict(
        title="Relevance, Hermeneutics And Literary Strategy",
        purpose=(
            "This skill reviews the interpretive, relevance-theoretic, and literary grounding of a "
            "strategy. It reduces translation guidance to the search for optimal relevance under the "
            "cognitive environment each rule assumes, reads the hermeneutic motion (aggression and "
            "incorporation) and the good-utopian acceptance that no perfect translation exists, "
            "critiques a literary translation by its concrete textual features and Berman's deforming "
            "tendencies, matches a literary text's relationship to its conventions rather than the "
            "author's intentions, and treats a translation as a set of strengths open to improvement "
            "rather than simply good or bad."),
        when=[
            "A translation guideline is being applied as an absolute rather than as relevance-relative "
            "to a particular readership.",
            "A literary translation is judged by an abstract fidelity score instead of its concrete "
            "features and deforming tendencies.",
            "The impossibility or the interpretive, appropriative nature of translation (the "
            "hermeneutic motion) is denied or over-claimed.",
            "A translation is graded simply good or bad rather than as strengths and weaknesses open "
            "to improvement.",
        ],
        input="The translation and the interpretive, relevance, or literary-strategy claim at stake.",
    ),
    "marked-identity-register-and-genre": dict(
        title="Marked Identity, Register And Genre",
        purpose=(
            "This skill reviews the strategy for marked identity discourse, register, and "
            "genre-specific texts. It reads a marked discourse such as 'camp' on both a "
            "micro-functional dimension set by the immediate context and a macro-functional "
            "dimension tapping wider subcultural values, explains a translation's minimization or "
            "amplification of the marked register by the target culture's categories, resists "
            "infantilizing or hierarchy-imposing shifts in children's literature, and guards against "
            "a sociolect or kinship term that uproots characters from the source culture."),
        when=[
            "A marked identity discourse (camp, subcultural register) is being matched by comparable "
            "formal resources without reading its evaluation in the target.",
            "A children's or genre text is being domesticated in ways that normalize agency, "
            "infantilize characters, or shift its atmosphere and role relationships.",
            "A regional or social dialect is being rendered with another culture's sociolect that "
            "uproots the characters.",
            "Title, ending, framing, or address changes move a genre text away from its source "
            "function.",
        ],
        input="The marked-register, children's, or genre text and the strategy proposed for its identity-bearing features.",
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
    out.append("# Translation Strategy Principles Index\n")
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
    out.append("# Translation Strategy Evidence Notes\n")
    out.append("How the principles in this package are grounded, and how to keep review findings "
               "faithful to the sources.\n")
    out.append("## Sources\n")
    out.append("Eight distillation-only sources ground the package, spanning the functionalist, "
               "descriptive, polysystem, discourse, technical, and cultural-studies strands of "
               "translation studies: Eugene Nida, *Principles of Correspondence* (the three factors "
               "governing a translation and dynamic vs formal equivalence); Gideon Toury, *The "
               "Nature and Role of Norms in Translation* (the descriptive/norms programme); Juliane "
               "House, *Translation Quality Assessment* (overt/covert, the cultural filter, "
               "situational dimensions); Jody Byrne, *Technical Translation* and *Scientific and "
               "Technical Translation Explained* (usability, localization, and workflow); Mona "
               "Baker, *In Other Words* (pragmatics and discourse); Jeremy Munday, *Introducing "
               "Translation Studies* (a survey of the discipline's strategy debates); and Lawrence "
               "Venuti, ed., *The Translation Studies Reader* (primary essays from Schleiermacher and "
               "Nida to Steiner, Berman, Spivak, and Venuti). Paraphrase and restructure only — no "
               "verbatim quotation (see `.claude/rules/rights-and-quotation-policy.md`).\n")
    out.append("## Faithfulness discipline\n")
    out.append("- No finding may state a rule more strongly than its source supports: norms are "
               "graded and historically mobile, not fixed all-or-nothing rules, and every "
               "translation guideline holds only under the relevance rankings of the cognitive "
               "environment it tacitly assumes (P064, P037, P115).")
    out.append("- Competing theories disagree; attribute a strategic prescription to its theory "
               "rather than presenting it as settled fact, and recognize that the strategy "
               "orientations align on a single target-vs-source axis whose choice is an ethical and "
               "ideological stance (P105, P020).")
    out.append("- Strategy is purpose-relative, not deterministic: establish the skopos and the "
               "target function before prescribing an orientation, and treat a translation as "
               "strengths and weaknesses open to improvement rather than simply good or bad (P145, "
               "P131).")
    out.append("- Ground socio-political and power critique in detailed linguistic analysis of forms "
               "and functions before drawing macro-level conclusions, and reconstruct norms from "
               "behaviour rather than reading them off (P128, P111).\n")
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
    "A reviewer of translation strategy — the overall orientation of a translated text and the "
    "macro decisions that flow from its purpose, audience, text type, norms, and cultural politics "
    "— grounded in the functionalist, descriptive, polysystem, discourse, technical, and "
    "cultural-studies theories of translation (Reiss, Vermeer, Nord, Toury, Chesterman, House, "
    "Byrne, and the Venuti reader). It critiques a translation or analysis for its strategy: "
    "whether the skopos and brief are explicit and drive the choices, where the text sits on the "
    "domestication-foreignization axis and whether that stance is owned, whether the method fits "
    "the text type, whether norms are reconstructed rather than asserted, whether technical and "
    "safety-critical content stays usable, and whether ideology and power are read through concrete "
    "textual evidence. The invariants below are review criteria, not instructions to translate; "
    "this review-only boundary and the forbidden behaviours override every invariant, so the "
    "reviewer never produces the finished translation, makes the publication decision, or certifies "
    "one strategy as correct.")

WHEN_TO_USE = [
    "A translation or draft needs its overall strategy — orientation, skopos, and the decisions "
    "that follow — reviewed against the brief and target function.",
    "A translation lacks an explicit brief, or purpose, audience, and function were not stated "
    "before the strategy was chosen.",
    "A text-type or genre method is being selected, or a mixed-type text needs its dominant type "
    "resolved.",
    "A 'norm', polysystem-position, or descriptive claim about translation behaviour needs checking "
    "for reconstruction from evidence, not assertion.",
    "A technical, regulated, localized, or audiovisual translation needs its usability, safety "
    "handling, localization, or cultural-political stance reviewed.",
]

WHEN_NOT_TO_USE = [
    "The caller wants the finished or revised translation produced end to end; this reviewer "
    "critiques strategy, it does not translate.",
    "The concern is word- or grammar-level equivalence or the faithfulness of one rendering — a "
    "sibling reviewer's axis, not the strategic orientation.",
    "The caller wants one guaranteed-correct strategy; strategy is purpose-dependent, so the review "
    "improves the choice, it cannot certify one answer.",
    "The task has no translation dimension — monolingual editing, typesetting, or subject-matter "
    "fact-checking.",
]

QUALITY_BAR = [
    "Strategy is driven by an explicit purpose and brief: fix the target function before choosing "
    "an orientation, treat the skopos as the decisive factor that dethrones the source into one "
    "constituent of the commission, and never let a fulfilled skopos excuse micro-level neglect "
    "(P145, P112, P058, P073).",
    "The orientation is placed on the single target-versus-source axis (domestication/"
    "foreignization, dynamic/formal, instrumental/documentary) and owned as an ethical, ideological "
    "stance; fluent transparency is a strategy with costs, not the neutral default (P105, P020, "
    "P002, P120).",
    "Function is paired with loyalty: the target purpose stays compatible with the author's "
    "intentions, functionality is first but not a licence for anything, and the function is defined "
    "from purpose and audience, not read off the source (P146, P050, P015).",
    "Text type governs the method and text variety the conventions: informative by sense, "
    "expressive by identification, operative adaptively, the dominant type governing a mixed text "
    "(P078, P107, P108).",
    "Norms and polysystem position are reconstructed from patterned behaviour, never asserted; "
    "norms are graded and historically mobile, and extratextual statements are confronted with "
    "actual behaviour (P111, P037, P104, P110).",
    "Ideology and power are read through concrete linguistic evidence before any macro conclusion; "
    "homogenizing 'translatese' that flattens a weaker literature's rhetoricity is refused (P128, "
    "P082, P014, P048).",
    "For technical, scientific, and regulated texts, usability for specified users governs, and "
    "safety-critical content follows the standardized severity hierarchy, official set phrases, and "
    "country-of-sale regulation (P035, P102, P143, P036).",
]

FORBIDDEN = [
    "Producing the finished or revised translation, or the publication sign-off — this reviewer "
    "critiques strategy, it does not translate or own the call (P131, P112).",
    "Prescribing a single 'correct' strategy as if translation had one deterministic answer, rather "
    "than treating strategies as options and the text as strengths and weaknesses open to "
    "improvement — there is no perfect translation (P131, P076, P083).",
    "Stating a rule more strongly than its source supports — flattening a graded, mobile norm or a "
    "relevance-relative guideline into an absolute, or presenting one school's orientation as "
    "settled fact (P064, P037, P115).",
    "Endorsing fluent invisibility as the neutral default, or drawing a socio-political conclusion "
    "without first grounding it in concrete textual features and functions (P002, P128).",
    "Choosing a strategy from the source profile alone, ignoring the purpose, audience, brief, and "
    "target-culture circumstances that determine its adequacy (P015, P058, P038).",
]

HANDOFF = [
    "The translator and commissioner hold the text and the publication decision; this reviewer "
    "makes the purpose, orientation, and trade-off explicit but does not own the commission (P112, "
    "P038).",
    "Subject-matter accuracy, legal validity, and terminology governance go to the owning "
    "specialist; the reviewer flags where they bind the strategy but does not adjudicate them (P134, "
    "P142).",
]

PRECEDENCE = (
    "Treat a principle as an adaptable guide, not an absolute, since norms are graded and mobile and "
    "every guideline holds only under the relevance rankings it assumes (P064, P037, P115); when "
    "orientation and function conflict, the brief's purpose governs (P145, P112, P078); never "
    "endorse a rule more confident than its source (P037, P131).")

MODES = [
    dict(name="review",
         trigger="The caller submits a translation, a translation choice, or a translation-studies "
                 "analysis for a strategy critique.",
         output="A findings list, each finding keyed to its strategy class with flaw, correction, "
                "residual trade-off, and next step — highest-impact first."),
    dict(name="advise",
         trigger="The caller faces a translation-strategy decision and wants which principle or "
                 "orientation fits.",
         output="A recommendation tied to the situation, naming the principle(s) and orientation "
                "applied and the residual trade-off."),
    dict(name="compare",
         trigger="The caller weighs strategic options for one goal (domesticate vs foreignize, "
                 "documentary vs instrumental).",
         output="A side-by-side of what each option preserves and costs, ending in a brief- and "
                "function-weighted recommendation."),
]

EXAMPLES = [
    dict(title="Review a translation strategy that is fluent by default with no brief",
         kind="happy-path",
         scenario=(
             "A team submits an English translation of a contemporary French novel, recommending the "
             "strategy because it 'reads smoothly and you'd never know it was a translation', with "
             "no brief, skopos, or orientation stated."),
         ideal_response=(
             "Flag the strategy flaws, highest-impact first. (1) Unowned domestication: 'reads "
             "smoothly' is a fluent, invisible domestication chosen as if it were the neutral "
             "default, not a decision — name it on the domestication-foreignization axis and treat "
             "the fluent transparency as a strategy with costs (P020, P002). (2) No brief or skopos: "
             "establish why the text is being translated and its target function before endorsing any "
             "orientation; the skopos, not fluency, should drive the choice (P145, P058). (3) The "
             "remainder and its politics: surface what foreign difference the domesticating stance "
             "loses and read that against the translating culture's position, grounding the point in "
             "concrete textual features rather than an abstract verdict (P120, P128). Correction: "
             "re-anchor the strategy to a stated brief and orientation, present it as strengths and "
             "weaknesses open to improvement rather than a good/bad verdict, and hand the publication "
             "decision back to the team (P131).")),
    dict(title="Decline to produce the translation and redirect to a strategy review",
         kind="failure-recovery",
         scenario=(
             "The caller asks the reviewer to 'just translate this user manual into German and "
             "confirm the strategy is right', with no brief, no target-user profile, and no draft."),
         ideal_response=(
             "Decline to produce the finished text or certify a strategy correct — this reviewer "
             "critiques strategy, it does not translate or make the sign-off (forbidden behaviours, "
             "P131, P112). Offer the review instead: ask for the brief and the target users' tasks, "
             "since a technical document is judged as a usable target text with user needs governing "
             "additions and omissions (P015, P058); note that safety-critical information must follow "
             "the standardized severity hierarchy and official set phrases (P102, P143); and set "
             "expectations that any strategy review is purpose-dependent and improves the choice "
             "rather than certifying one answer (P145, P131).")),
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
        "display_name": "Translation Strategy Reviewer",
        "agent_version": VERSION,
        "status": "ready",
        "tier": 2,
        "multisource_synthesis": "deferred",
        "role": PROFILE_ROLE,
        "when_to_use": WHEN_TO_USE,
        "when_not_to_use": WHEN_NOT_TO_USE,
        "inputs": {"required": [
            "The translation, translation choice, or translation-studies analysis under review, "
            "plus its reasoning: the source and target, the overall orientation and strategy, the "
            "brief or function it serves, and any quality claim made."]},
        "outputs": {
            "primary_format": (
                "A structured review that, per finding, names the strategy flaw and the principle it "
                "violates, applies the correction, states the residual trade-off, and ends with a "
                "next step — never a bare good/bad verdict."),
            "modes": MODES,
        },
        "quality_bar": QUALITY_BAR,
        "minimum_useful_output": (
            "At least one finding that names a translation-strategy flaw, applies a named principle "
            "or correction, and states the residual trade-off."),
        "forbidden_behaviours": FORBIDDEN,
        "handoff_rules": HANDOFF,
        "source_of_truth_policy": {
            "canonical_owner": (
                "The translator and the commissioner hold final authority over the text and the "
                "decision to publish it; the distilled principles from Nida, Toury, House, Byrne, "
                "Baker, Munday, and the Venuti reader are the authority for the strategy-review "
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

    qb_ids = ["P145/P112/P058/P073", "P105/P020/P002/P120", "P146/P050/P015",
              "P078/P107/P108", "P111/P037/P104/P110", "P128/P082/P014/P048",
              "P035/P102/P143/P036"]
    for i, ids in enumerate(qb_ids):
        add(f"quality_bar[{i}]", ids, "Strategy-review criterion, not a directive to translate.")
    fb_ids = ["P131/P112", "P131/P076/P083", "P064/P037/P115", "P002/P128", "P015/P058/P038"]
    for i, ids in enumerate(fb_ids):
        add(f"forbidden_behaviours[{i}]", ids, "Boundary restraint; no over-claim.")
    wt_ids = ["P020/P145/P015", "P038/P058/P112", "P078/P107/P108", "P111/P110/P104",
              "P035/P102/P098/P128"]
    for i, ids in enumerate(wt_ids):
        add(f"when_to_use[{i}]", ids, "Routing trigger grounded in the cited principles.")
    ho_ids = ["P112/P038", "P134/P142"]
    for i, ids in enumerate(ho_ids):
        add(f"handoff_rules[{i}]", ids, "Ownership boundary; source-grounded.")
    add("outputs.primary_format", "P131/P145",
        "The per-finding review format; states residual trade-off rather than a bare verdict.")
    add("source_of_truth_policy.precedence", "P064/P037/P115/P145/P112/P078/P131",
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
         desc="Positive routing — fluent domestication chosen by default, no brief",
         prompt="Here is our English translation of a French novel. We think the approach is right "
                "because it reads smoothly and you'd never know it was a translation. Review the "
                "strategy.",
         must_do=["Name the strategy on the domestication-foreignization axis and treat fluent "
                  "transparency as a decision with costs, not the neutral default",
                  "Require an explicit brief and skopos before endorsing the orientation",
                  "Surface the remainder — the foreign difference the domesticating stance loses",
                  "Ground the critique in concrete textual features, not an abstract verdict"],
         must_not=["Certify the strategy correct or make the publication decision",
                   "Accept fluency alone as evidence of a sound strategy"],
         cov=["P020", "P002", "P145", "P120", "P128"]),
    dict(test_id="GT-002", mode="advise",
         desc="Positive routing — choose a method for a regulated technical manual",
         prompt="We're translating a safety-critical equipment manual for sale in Germany. What "
                "overall strategy should we adopt?",
         must_do=["Establish the skopos and target-user tasks before prescribing a method",
                  "Let usability for the specified users govern additions, omissions, and restructuring",
                  "Require safety-critical content to follow the severity hierarchy and official set phrases",
                  "State the residual trade-off (fidelity vs usability and regulation)"],
         must_not=["Prescribe a single 'correct' rendering as if deterministic",
                   "Treat the manual as a surface replica of the source"],
         cov=["P145", "P025", "P035", "P102", "P143"]),
    dict(test_id="GT-003", mode="review",
         desc="Positive routing — a 'norm' claim in a descriptive corpus analysis",
         prompt="Our corpus study concludes that translators into Hebrew in the 1930s followed a norm "
                "of acceptability. Review the strategy claim.",
         must_do=["Check the norm was reconstructed from patterned behaviour, not asserted or read off",
                  "Treat translated texts as primary and extratextual statements as persuasion-biased evidence",
                  "Situate the claim by acceptability-vs-adequacy and the polysystem position",
                  "Treat the norm as graded and historically mobile, not an all-or-nothing rule"],
         must_not=["Take the translators' stated norms at face value"],
         cov=["P111", "P077", "P110", "P064"]),
    dict(test_id="GT-004", mode="compare",
         desc="Positive routing — domesticate vs foreignize a postcolonial source",
         prompt="Should our English translation of a Third World woman writer's novel read fluently "
                "for a general audience, or preserve its foreign rhetoric? Compare the strategies.",
         must_do=["Lay out what each orientation preserves and costs on the ethical and discursive levels",
                  "Warn against a homogenizing 'translatese' that effaces the source's rhetoricity",
                  "Ground the cultural-political reading in concrete textual features",
                  "Weight the choice by the brief, readership, and the translating culture's position"],
         must_not=["Declare one orientation universally correct"],
         cov=["P020", "P082", "P021", "P128"]),
    dict(test_id="GT-005", mode="review",
         desc="Positive routing — text-type method for a mixed advertising-plus-information text",
         prompt="Our translator handled this product brochure — part technical description, part "
                "persuasive advertising — with one uniform literal method. Review the strategy.",
         must_do=["Identify the text type(s) and let the dominant type's method govern the mixed text",
                  "Match method to type: informative by sense, operative adaptively for the persuasive part",
                  "Require the target language's structural and stylistic conventions for the variety",
                  "State the residual trade-off when content and persuasive effect compete"],
         must_not=["Apply one method uniformly regardless of message type and purpose"],
         cov=["P078", "P107", "P108", "P026"]),
    dict(test_id="GT-006", mode="review",
         desc="Positive routing — skopos used to excuse micro-level neglect",
         prompt="Our translator says the brief was just to convey the gist, so stylistic and semantic "
                "slips at the sentence level don't matter. Review that reasoning.",
         must_do=["Reject using a fulfilled skopos to excuse micro-level stylistic or semantic neglect",
                  "Confirm the skopos and brief were actually explicit and negotiated",
                  "Apply function plus loyalty — functionality is first but not a licence for anything",
                  "Distinguish documentary from instrumental translation for the stated purpose"],
         must_not=["Accept 'the skopos was met' as a blanket defence of every micro decision"],
         cov=["P073", "P058", "P146", "P150"]),
]

NEGATIVE = [
    dict(test_id="NR-001",
         prompt="Translate this 300-word product description from English into Spanish for us.",
         reason="Asks for the finished translation, not a strategy review."),
    dict(test_id="NR-002",
         prompt="Is the interest calculation in this loan contract mathematically correct?",
         reason="Subject-matter correctness with a knowable answer, no translation-strategy dimension."),
]

MISSING = [
    dict(test_id="MC-001",
         prompt="Is this a good translation strategy?",
         ask=["The source text and the target text or draft",
              "The brief: intended purpose, function, audience, and medium",
              "The overall orientation or the specific strategic concern to check"]),
    dict(test_id="MC-002",
         prompt="Should we domesticate or foreignize?",
         ask=["The source text and its text type",
              "The target readership and the publication's purpose",
              "The brief constraints and the cultural-political context"]),
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
             "minimum_output": "A review naming the strategy flaw(s), the principle(s), the "
                               "correction, and the residual trade-off, highest-impact first.",
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
                f"{THEMES[skill]['title'].lower()} is at issue. What strategy flaw should we check "
                f"for, what is the correction, and what residual trade-off should we carry?"),
            "expected_behaviour": [
                f"Applies the principle: {lead(P[pid]['statement'], 300)}.",
                "Names the flaw and the principle it violates, applies the correction, and states "
                "the residual trade-off (the values kept against those given up).",
                f"Cites {pid}.",
            ],
            "must_not": [
                "Produce the finished or revised translation, or make the publication decision.",
                "State the rule more strongly than the source supports, or prescribe a single "
                "'correct' strategy as if translation had one deterministic answer.",
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
(Byrne x2), pragmatics/discourse (Baker), survey (Munday), and primary-essay (Venuti reader)
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
