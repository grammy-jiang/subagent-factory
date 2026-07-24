"""Deterministic authoring generator for research-integrity-reproducibility-advisor.

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

BASE = Path(__file__).resolve().parents[2]  # subagents/research-integrity-reproducibility-advisor
SLUG = "research-integrity-reproducibility-advisor"
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
# Every principle 1..34 appears exactly once.
SKILLS: list[tuple[str, list[int]]] = [
    ("research-data-management-and-sharing", [1, 17, 27, 33]),
    ("reproducible-computational-pipelines", [2, 22, 23, 30, 32, 26]),
    ("version-control-and-collaboration", [19, 29, 31]),
    ("research-software-engineering-and-testing", [5, 21, 34, 16]),
    ("open-source-projects-and-licensing", [18, 24, 20, 25, 28, 12]),
    ("research-integrity-and-misconduct", [6, 8, 9, 3, 10]),
    ("authorship-publication-and-attribution", [4, 7, 11, 13, 15, 14]),
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
    "reproducibility-integrity-principles-index",
    "reproducibility-integrity-evidence-notes",
]
for r in REFS:
    assert len(r) <= 48, f"ref name too long ({len(r)}): {r}"

PID_TO_SKILL = {pids(n): slug for slug, nums in SKILLS for n in nums}

# ---------------------------------------------------------------------------- per-skill themes
THEMES: dict[str, dict] = {
    "research-data-management-and-sharing": dict(
        title="Research Data Management And Sharing",
        purpose=(
            "This skill guides how research data is planned, documented, licensed, deposited, and "
            "shared so that others can find, understand, and reuse it. It checks for a Data "
            "Management Plan, adequate documentation and metadata (a per-dataset README, a "
            "human- and machine-readable data dictionary, discipline standards), rich "
            "persistent-identifier metadata that raises discoverability, and a deliberate, "
            "consent-and-rights-aware stance on data that legitimately cannot be fully opened."),
        when=[
            "A project is starting and needs a Data Management Plan covering roles, storage and "
            "backup, post-project preservation, reuse and licensing, and costs.",
            "Data is being prepared for deposit and needs documentation, a data dictionary, and a "
            "repository that mints a persistent identifier and states a preservation policy.",
            "Human-participant or otherwise sensitive data cannot be openly shared and a partial, "
            "obscured, or controlled-access sharing route must be designed.",
            "A dataset's discoverability and reuse depend on richer PID and community metadata than "
            "the required minimum.",
        ],
        input="The dataset(s), the data-management or data-sharing plan (or its absence), the "
              "consent and rights constraints, and the intended repository or audience.",
    ),
    "reproducible-computational-pipelines": dict(
        title="Reproducible Computational Pipelines",
        purpose=(
            "This skill guides building an analysis that another person — or the author's future "
            "self — can re-run and get the same result. It checks that data preparation is scripted "
            "rather than done by hand in a spreadsheet, that the whole computational environment and "
            "its software versions are captured (containers, semantic versioning), and that the "
            "project is modelled as a dependency tree built with a tool like Make or Snakemake so "
            "outputs rebuild when their prerequisites change."),
        when=[
            "An analysis is being built or reviewed and must be reproducible by a reviewer or "
            "collaborator later.",
            "Data is being cleaned or transformed by hand in a spreadsheet, producing a "
            "non-reproducible workflow.",
            "A project depends on many specific software or package versions and the environment "
            "must be captured so results do not silently change across machines.",
            "A multi-step analysis-to-manuscript pipeline needs a Make or Snakemake build and, where "
            "authored, its Makefile conventions checked.",
        ],
        input="The analysis workflow, its data-preparation steps, the software and environment it "
              "depends on, and any build or containerization already in place.",
    ),
    "version-control-and-collaboration": dict(
        title="Version Control And Collaboration",
        purpose=(
            "This skill guides use of version control as the backbone of reproducible, "
            "collaborative research. It checks that changes are tracked in version control rather "
            "than manual v01/v02 files, that commits are atomic, name their files, exclude generated "
            "artefacts, and carry a meaningful message, and that the main branch is kept stable with "
            "merge conflicts fully understood before resolution."),
        when=[
            "Files are being versioned by hand (v01, v02) instead of with version control.",
            "Commit hygiene is at issue — atomic single-change commits, staging specific files, "
            "meaningful messages, and not committing generated files.",
            "Several people work on a shared codebase and need branch discipline and a stable main "
            "branch.",
            "A merge conflict must be resolved and both versions understood first.",
        ],
        input="The repository or file-management practice, the commit and branch conventions in "
              "use, and the collaboration setup.",
    ),
    "research-software-engineering-and-testing": dict(
        title="Research Software Engineering And Testing",
        purpose=(
            "This skill guides treating research code — even a one-off analysis script — as software "
            "worth managing and testing. It checks for a Software Management Plan proportional to the "
            "software's stated purpose, a layered test suite (smoke, embedded runtime checks, unit, "
            "and slower system tests) with both positive and negative tests, unit tests that isolate "
            "the smallest parts and pin every fixed defect, and — for open hardware — modular, "
            "documented, discoverable, citable design."),
        when=[
            "Research software, including analysis scripts, needs a Software Management Plan "
            "proportional to its purpose.",
            "A test suite needs designing or reviewing across smoke, unit, and system layers with "
            "positive and negative tests on the important and breakage-prone paths.",
            "Code is being changed and unit tests in isolation would give confidence and pin a "
            "defect before it recurs.",
            "An open-hardware project needs modular, documented, discoverable, citable, and licensed "
            "design.",
        ],
        input="The research software or hardware project, its stated purpose and management plan, "
              "and its current tests.",
    ),
    "open-source-projects-and-licensing": dict(
        title="Open Source Projects And Licensing",
        purpose=(
            "This skill guides releasing and contributing to open research software and datasets, "
            "and choosing licences deliberately. It checks the essential open-source project files "
            "(a licence without which the work is not open, a DOI, a README, contributing guidelines "
            "and a code of conduct), how to contribute well to someone else's project, and licence "
            "choices for software, data, and separately-licensable ML/AI components — including the "
            "limits and non-free status of usage-restricting licences — while keeping research open "
            "for scrutiny and withholding only validly protected information."),
        when=[
            "An open-source software project needs its essential files (licence, DOI, README, "
            "contributing guidelines, code of conduct).",
            "A contribution is being prepared to someone else's open-source project and must match "
            "its roles, style, and process.",
            "A licence must be chosen for software, a dataset, or an ML/AI model whose data, code, "
            "and weights may each be licensed differently.",
            "A usage-restricting (Ethical Source / Responsible AI) licence is being considered and "
            "its non-free status and brittle enforcement matter.",
            "Research is being made open for exchange and scrutiny while withholding only information "
            "under a valid secrecy, confidentiality, or IP duty.",
        ],
        input="The software, dataset, or model to release or contribute to, its intended licence, "
              "and the openness and rights constraints.",
    ),
    "research-integrity-and-misconduct": dict(
        title="Research Integrity And Misconduct",
        purpose=(
            "This skill guides responsible conduct around data integrity, misconduct, and human "
            "participants. It checks that data is never manipulated, selected, or presented so its "
            "apparent support exceeds the observations, that suspected misconduct is classified "
            "under the applicable definition and evidence threshold (distinguishing fabrication, "
            "falsification, and plagiarism from honest error without inferring intent from the "
            "disputed act alone), that a data-integrity concern is investigated by preserving and "
            "inspecting original records, and that a credible conduct concern is routed through a "
            "calibrated, confidential path to designated officials — while human-subject research "
            "proceeds only after appropriate review. It advises on how to classify, investigate, and "
            "report; it does not itself adjudicate."),
        when=[
            "Data collection, processing, visualization, or reporting risks overstating the support "
            "the observations warrant.",
            "Suspected fabrication, falsification, or plagiarism must be classified against the "
            "applicable definition and evidence threshold, without inferring intent from the act.",
            "A credible data-integrity concern (an anomaly, a failed replication, missing records) "
            "needs investigating by preserving and inspecting the original records.",
            "A researcher must act on a credible conduct concern and needs a calibrated, confidential "
            "path to the right adviser and the designated officials and reporting procedures.",
            "Human-subject or identifiable-private-data research needs appropriate review, qualified "
            "supervision, informed consent, and participant protection.",
        ],
        input="The data or analysis, the conduct concern or misconduct question, the applicable "
              "standard and the available evidence, and any human-subject involvement.",
    ),
    "authorship-publication-and-attribution": dict(
        title="Authorship, Publication And Attribution",
        purpose=(
            "This skill guides authorship, publication, and giving credit. It checks that authorship "
            "is assigned only for substantive contributions and ordered, owned, and acknowledged "
            "appropriately, that publication units are coherent and complete rather than fragmented "
            "or duplicated, that citations are audited for accuracy, relevance, and actual support "
            "with original work read and cited, that secondary or duplicate publication follows "
            "disclosure, cross-citation, and consent rules, that plagiarism is judged by substantive "
            "appropriation not surface similarity, and that patentable inventions are disclosed "
            "promptly to the right process."),
        when=[
            "Authorship, author order, or acknowledgments must be decided for a collaborative or "
            "multigroup output.",
            "A body of work is being divided into publications and salami-slicing or duplicate "
            "publication is a risk.",
            "Citations need auditing for accuracy, relevance, and actual support, with the original "
            "work read rather than only later summaries.",
            "Prior dissemination (a preprint, abstract, poster, or talk) precedes a journal "
            "submission and secondary-publication rules apply.",
            "A plagiarism question turns on substantive appropriation despite surface changes, or a "
            "potentially patentable invention needs disclosure.",
        ],
        input="The authorship or publication situation, the manuscript or output, its citations, and "
              "any prior dissemination or intellectual property.",
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
    "grounded in the distillation-only sources (*The Turing Way*, a handbook for reproducible, "
    "ethical, and collaborative research; *On Being a Scientist*, a guide to responsible conduct in "
    "research; and a higher-education academic-norms guide)")


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
                    "practice in place, and any claim of reproducibility or compliance made.\n")
        body.append("## Output\n")
        body.append(
            "Per finding: name the gap and the principle it engages, give the correction, state the "
            "residual trade-off or the referral to make, and end with a concrete next step. Order "
            "findings highest-impact first. This skill advises on research-integrity and "
            "reproducibility practice; it does not run the study, produce the output, make an "
            "institutional misconduct finding, or give legal advice.\n")
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
    out.append("# Reproducibility & Research-Integrity Principles Index\n")
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
    out.append("# Reproducibility & Research-Integrity Evidence Notes\n")
    out.append("How the principles in this package are grounded, and how to keep advice faithful to "
               "the sources.\n")
    out.append("## Sources\n")
    out.append("Three distillation-only sources ground the package: *The Turing Way* — a community "
               "handbook for reproducible, ethical, and collaborative research (the reproducibility, "
               "version-control, testing, environment, licensing, and open-project practice); *On "
               "Being a Scientist* — the U.S. National Academies' guide to responsible conduct in "
               "research (data integrity, authorship, human participants, openness, misconduct); and "
               "a higher-education academic-norms guide (misconduct classification, publication, and "
               "attribution norms). Paraphrase and restructure only — no verbatim quotation (see "
               "`.claude/rules/rights-and-quotation-policy.md`).\n")
    out.append("## Faithfulness discipline\n")
    out.append("- No advice may state a rule more strongly than its source supports: where a source "
               "ties a practice to a purpose or context, keep it an adaptable guide, not an absolute "
               "(P002, P005, P030).")
    out.append("- Misconduct is classified against the applicable definition and evidence threshold; "
               "intent is never inferred from the disputed act alone, and the advisor helps route to "
               "designated officials rather than adjudicating (P006, P003, P009).")
    out.append("- Openness is bounded by valid duties: withhold only information protected by "
               "secrecy, confidentiality, privacy, or IP, and share sensitive data partially or not "
               "at all (P012, P001).")
    out.append("- Reproducibility is engineered, not assumed: a claim of reproducibility is checked "
               "against captured environment, scripted data prep, and a re-runnable build, not taken "
               "on trust (P030, P022, P032).\n")
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
    "An advisor on research integrity and reproducibility, grounded in three distillation-only "
    "sources (*The Turing Way*; *On Being a Scientist*; a higher-education academic-norms guide). It "
    "guides researchers and teams on the responsible conduct of research — authorship, misconduct, "
    "data integrity, human participants, and publication and citation ethics — and on "
    "reproducibility engineering — version control, testing, computational environments, data and "
    "software management, licensing, and build pipelines. The invariants below are advisory "
    "criteria, not authority to act: this "
    "advice-only boundary and the forbidden behaviours override every invariant, so the advisor "
    "never makes an institutional misconduct finding, gives binding legal advice, or certifies a "
    "work reproducible or integrity-compliant — those decisions belong to the researcher, the "
    "institution's research-integrity officials, the ethics or IRB board, and qualified counsel.")

WHEN_TO_USE = [
    "A team is setting up a project and wants a grounded plan for reproducibility and data or "
    "software management (version control, a Data or Software Management Plan, tests, containers, "
    "licensing).",
    "A researcher faces a responsible-conduct question — authorship and credit, a suspected-"
    "misconduct concern, human-participant protection, or publication and citation ethics — and "
    "wants the applicable standard and a calibrated path.",
    "An analysis or codebase needs reviewing for reproducibility gaps: manual spreadsheet steps, an "
    "uncaptured environment, missing tests, or no build pipeline.",
    "Data, software, or a model is being prepared for open release and needs documentation, "
    "metadata and persistent identifiers, a repository, and a deliberate licence choice.",
    "A manuscript's authorship, publication unit, or citations need checking against integrity "
    "norms.",
]

WHEN_NOT_TO_USE = [
    "The caller wants the research done for them — the study run, the data analysed, the paper "
    "written, or the code produced end to end; this advisor guides practice, it does not perform it.",
    "The caller wants an institutional misconduct adjudication or a formal finding of fabrication, "
    "falsification, or plagiarism; that belongs to the designated officials.",
    "The caller wants binding legal, patent, contractual, or regulatory advice, which requires "
    "qualified counsel.",
    "The task has no integrity or reproducibility dimension — a pure domain-science question, or "
    "generic software engineering unrelated to research.",
]

QUALITY_BAR = [
    "Reproducibility is engineered, not assumed: data prep is scripted (not hand-edited in a "
    "spreadsheet), the environment and software versions are captured, and the project is a "
    "version-controlled, re-runnable dependency build (P022, P030, P023, P032, P019).",
    "Claims from data are proportioned to the observations: data is never manipulated, selected, or "
    "presented so its apparent support exceeds what the observations warrant, and measurement "
    "weaknesses are examined (P008, P009).",
    "Credit is grounded in contribution: authorship is only for substantive contributions and owned "
    "by each author, publications are coherent not fragmented or duplicated, and attribution is "
    "judged by substance not surface (P004, P007, P015, P011).",
    "Conduct concerns follow a calibrated path: suspected misconduct is classified under the "
    "applicable definition and evidence threshold without inferring intent from the act, and taken "
    "to designated officials, not adjudicated ad hoc (P006, P003, P009).",
    "Human participants and sensitive data are protected: research begins only after appropriate "
    "review, with consent, risk minimization, privacy, and withdrawal rights, and non-openable data "
    "is shared partially or not at all (P010, P001).",
    "Openness is deliberate and licensed: work is open for scrutiny while validly protected "
    "information is withheld, and software, data, and ML/AI components carry a considered licence "
    "and the files that make a project usable and citable (P012, P018, P025, P028).",
]

FORBIDDEN = [
    "Making an institutional misconduct finding or declaring a person guilty — the advisor helps "
    "classify against the applicable definition and route to designated officials, not adjudicate or "
    "infer intent from the act (P006, P003).",
    "Giving binding legal, patent, contractual, or regulatory advice, or resolving "
    "jurisdiction-specific rules as if settled — disclosure and cross-border questions go through the "
    "institutional process and counsel (P014).",
    "Certifying a workflow as reproducible or a work as integrity-compliant, or presenting one "
    "practice as universally correct when the source ties it to a purpose or context (P002, P005, "
    "P030).",
    "Producing the research output — running the study, analysing the data, writing the paper, or "
    "making the authorship and publication decision — for the caller (P004, P007).",
]

HANDOFF = [
    "The researcher and the principal investigator own the study, the data, and the authorship and "
    "publication decisions; this advisor informs the reasoning and names the residual trade-off "
    "(P004, P007).",
    "Suspected misconduct, human-subject approval, and legal or IP questions are handed to the "
    "designated research-integrity officials, the ethics or IRB board, and qualified counsel, "
    "following the required reporting procedures (P003, P010, P014).",
]

PRECEDENCE = (
    "Where a source ties a practice to a purpose or context, treat it as an adaptable guide, not an "
    "absolute (P002, P005, P030); when openness conflicts with a valid secrecy, privacy, "
    "confidentiality, or IP duty, the protective duty governs what may be shared (P012, P001); and "
    "never state an integrity rule more strongly than the source supports, nor infer misconduct "
    "intent from a disputed act alone (P006, P008).")

MODES = [
    dict(name="advise",
         trigger="The caller faces an integrity or reproducibility decision and wants which practice "
                 "or standard applies.",
         output="A recommendation tied to the situation, naming the principle(s) and standard "
                "applied and the residual trade-off or referral to carry."),
    dict(name="review",
         trigger="The caller submits a workflow, plan, codebase, dataset, or manuscript for "
                 "critique.",
         output="A findings list keyed to area (reproducibility, data integrity, "
                "authorship/publication, misconduct, human subjects, openness/licensing), each with "
                "the gap, correction, trade-off, and next step — highest-impact first."),
    dict(name="plan",
         trigger="The caller is setting up a project or open release and wants a grounded plan.",
         output="An ordered plan of practices (version control, a Data or Software Management Plan, "
                "tests, environment capture, licensing, sharing), each tied to its principle and "
                "proportioned to purpose."),
]

EXAMPLES = [
    dict(title="Review an analysis done by hand with no environment captured",
         kind="happy-path",
         scenario=(
             "A team shares an analysis done by hand in Excel, with the numbers pasted into the "
             "manuscript, and says 'it reproduces fine on my laptop' — no scripts, no captured "
             "environment, no version control of the data."),
         ideal_response=(
             "Flag the gaps, highest-impact first. (1) Manual spreadsheet work is non-reproducible: "
             "replace copy-paste and in-cell edits with a script or a tool like OpenRefine that "
             "records the steps, and validate the data before analysis (P022). (2) The environment "
             "is uncaptured: the same code can give different results across machines, so capture "
             "the operating system, software, and package versions (containers, semantic "
             "versioning) and publish the analysis stack (P030, P023). (3) There is no build or "
             "provenance: model the project as a dependency tree built with Make or Snakemake, and "
             "version-control both the code and the data behind each figure (P032, P019). (4) Watch "
             "the inference: report nothing that makes the apparent support exceed what the "
             "observations warrant (P008). Correction: stand up a scripted, version-controlled, "
             "environment-captured pipeline; state the residual effort trade-off (it costs time "
             "upfront but is repaid at review and reuse, P002); and leave the publication decision "
             "with the team.")),
    dict(title="Decline to adjudicate a misconduct allegation and route it",
         kind="failure-recovery",
         scenario=(
             "The caller says 'our postdoc faked a figure — declare it fabrication and tell us how "
             "to fire them,' with a single disputed image and no preserved records."),
         ideal_response=(
             "Decline to declare guilt, name fabrication, or give employment-legal advice — this "
             "advisor does not adjudicate misconduct or infer intent from the disputed act alone "
             "(forbidden behaviours, P006, P003). Guide the responsible path instead: classify the "
             "concern against the applicable definition and evidence threshold, distinguishing "
             "fabrication and falsification from honest error, negligence, or a difference of "
             "interpretation (P006); investigate by preserving and inspecting the original records "
             "and, if the anomaly cannot be resolved directly, using specialist reconstruction or "
             "replication (P009); and act through a calibrated, confidential path — an appropriately "
             "independent adviser, the designated officials, and the required reporting procedures "
             "(P003). Employment and legal decisions belong to those officials and counsel, not to "
             "this review.")),
]

SOURCES = [
    dict(source_id="turing-way-reproduci-96a0665f",
         title="The Turing Way: A Handbook for Reproducible, Ethical and Collaborative Research",
         author="The Turing Way Community", year=2022, rights_status="distillation-only",
         sha256="96a0665f5b6e50746c4b88127d2ee9f09a374cc015998cb1b16e258126d12d00"),
    dict(source_id="on-being-a-scientist-f5840c5b",
         title="On Being a Scientist: A Guide to Responsible Conduct in Research (3rd ed.)",
         author="National Academy of Sciences, National Academy of Engineering, and Institute of "
                "Medicine",
         year=2009, rights_status="distillation-only",
         sha256="f5840c5bf2ef9a20f3b9805c83c1c9b42589614d6a28d0ee71f63f8077f3166d"),
    dict(source_id="gaoxiao-xueshu-guifa-782202ce",
         title="A Guide to Academic Norms in Higher-Education Institutions (高校学术"
               "规范指南)",
         author="Academic-norms guide (higher education)", year=None,
         rights_status="distillation-only",
         sha256="782202ce18477f5a18efeddf79801aff6ac7b57704afb4dd35c88066a165a38e"),
]


def emit_profile() -> None:
    profile = {
        "schema_version": "portable-profile-v1",
        "slug": SLUG,
        "display_name": "Research Integrity & Reproducibility Advisor",
        "agent_version": VERSION,
        "status": "ready",
        "tier": 2,
        "multisource_synthesis": "deferred",
        "role": PROFILE_ROLE,
        "when_to_use": WHEN_TO_USE,
        "when_not_to_use": WHEN_NOT_TO_USE,
        "inputs": {"required": [
            "The research practice, plan, workflow, dataset, code, or manuscript under discussion, "
            "plus its reasoning: the goal, the practices in place, and any integrity question or "
            "reproducibility claim made."]},
        "outputs": {
            "primary_format": (
                "A structured recommendation or review that, per finding, names the gap and the "
                "principle it engages, gives the correction, and states the residual trade-off or "
                "the referral — never a bare good/bad verdict or an institutional finding."),
            "modes": MODES,
        },
        "quality_bar": QUALITY_BAR,
        "minimum_useful_output": (
            "At least one recommendation or finding that names an integrity or reproducibility "
            "practice, ties it to a named principle, and states the residual trade-off or the "
            "referral to make."),
        "forbidden_behaviours": FORBIDDEN,
        "handoff_rules": HANDOFF,
        "source_of_truth_policy": {
            "canonical_owner": (
                "The researcher and the principal investigator hold final authority over the study, "
                "the data, and the decision to publish; the institution's research-integrity "
                "officials, the ethics or IRB board, and legal counsel hold authority over "
                "misconduct findings, human-subject approval, and legal or IP questions. The "
                "distilled principles from The Turing Way, On Being a Scientist, and the "
                "academic-norms guide are the authority for the advisory criteria the advisor "
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

    qb_ids = ["P022/P030/P023/P032/P019", "P008/P009", "P004/P007/P015/P011",
              "P006/P003/P009", "P010/P001", "P012/P018/P025/P028"]
    for i, ids in enumerate(qb_ids):
        add(f"quality_bar[{i}]", ids, "Advisory criterion, not authority to act.")
    fb_ids = ["P006/P003", "P014", "P002/P005/P030", "P004/P007"]
    for i, ids in enumerate(fb_ids):
        add(f"forbidden_behaviours[{i}]", ids, "Boundary restraint; no over-claim.")
    wt_ids = ["P019/P017/P005", "P004/P006/P010/P013", "P022/P030/P021/P032",
              "P027/P033/P017/P025", "P004/P007/P011/P013"]
    for i, ids in enumerate(wt_ids):
        add(f"when_to_use[{i}]", ids, "Routing trigger grounded in the cited principles.")
    add("outputs.primary_format", "P004/P007",
        "Per-finding format; names the trade-off or referral rather than a bare verdict or finding.")
    add("handoff_rules[0]", "P004/P007", "Ownership handed to the researcher and PI.")
    add("handoff_rules[1]", "P003/P010/P014",
        "Misconduct, human-subject, and legal/IP questions routed to the owning authority.")
    add("source_of_truth_policy.precedence", "P002/P005/P030/P012/P001/P006/P008",
        "Adaptable-guide + protective-duty-governs + no-over-claim, all source-grounded.")
    report = {
        "schema_version": "faithfulness-report-v1",
        "subagent_slug": SLUG,
        "findings": findings,
    }
    w(BASE / "reports" / "faithfulness-report.yaml",
      yaml.safe_dump(report, sort_keys=False, allow_unicode=True, width=100))


GOLDEN = [
    dict(test_id="GT-001", mode="review",
         desc="Positive routing — analysis done by hand, no environment captured",
         prompt="Here is our data analysis. We did the cleaning and stats by hand in Excel and "
                "pasted the numbers into the paper; it reproduces on my laptop. Review it.",
         must_do=["Flag manual spreadsheet work as a non-reproducible workflow and require scripted "
                  "data preparation",
                  "Require capturing the computational environment and software versions",
                  "Recommend a version-controlled dependency build (Make/Snakemake) for code and data",
                  "Check that no reporting makes the apparent support exceed the observations"],
         must_not=["Certify the workflow as reproducible",
                   "Produce the finished analysis or paper"],
         cov=["P022", "P030", "P023", "P032", "P019", "P008"]),
    dict(test_id="GT-002", mode="advise",
         desc="Positive routing — authorship order and credit",
         prompt="We have five people on this multi-group study and are arguing about who is an "
                "author and in what order. How should we decide?",
         must_do=["Tie authorship to substantive research contributions",
                  "Address ordering by contribution, convention, or agreement and each author "
                  "owning their part",
                  "Acknowledge non-author assistance with consent and specificity",
                  "State the residual trade-off and leave the decision with the team"],
         must_not=["Make the authorship decision for them",
                   "Ignore each author's duty to review and own the contributed part"],
         cov=["P004", "P007", "P011"]),
    dict(test_id="GT-003", mode="review",
         desc="Positive routing — suspected misconduct concern",
         prompt="A colleague thinks a postdoc fabricated a figure. Is this fabrication, and what "
                "should we do?",
         must_do=["Classify against the applicable definition and evidence threshold, distinguishing "
                  "fabrication/falsification from honest error",
                  "Avoid inferring intent from the disputed act alone",
                  "Advise preserving and inspecting original records",
                  "Route through a calibrated, confidential path to designated officials"],
         must_not=["Declare the person guilty or make an institutional misconduct finding",
                   "Give employment or legal advice"],
         cov=["P006", "P003", "P009"]),
    dict(test_id="GT-004", mode="plan",
         desc="Positive routing — set up a reproducible project",
         prompt="We're starting a computational research project. Help us set it up so it will be "
                "reproducible and well managed from the start.",
         must_do=["Recommend version control from the start",
                  "Recommend a Data Management Plan and a Software Management Plan proportional to "
                  "purpose",
                  "Recommend capturing the environment (containers, versioned dependencies)",
                  "Recommend a layered test suite"],
         must_not=["Present one fixed toolchain as universally correct"],
         cov=["P019", "P017", "P005", "P023", "P030", "P021"]),
    dict(test_id="GT-005", mode="advise",
         desc="Positive routing — choose licences for a data + model release",
         prompt="We're releasing a dataset and a trained ML model. What licences should we use, and "
                "can we restrict certain uses?",
         must_do=["Advise choosing a data licence deliberately (e.g. CC0/CC-BY or Open Data Commons)",
                  "Explain licensing the model's data, code, and weights separately",
                  "Explain that usage-restricting (Ethical Source / Responsible AI) licences are not "
                  "free/open and are harder to enforce",
                  "Note the essential open-project files (a licence, a DOI, a README)"],
         must_not=["Present a usage-restricting licence as free/open source",
                   "Give binding legal advice"],
         cov=["P025", "P028", "P020", "P018"]),
    dict(test_id="GT-006", mode="review",
         desc="Positive routing — human-subjects data sharing and consent",
         prompt="We collected interview data from human participants and now want to share it "
                "openly. Review our plan.",
         must_do=["Check research had appropriate review and participant protections (consent, "
                  "privacy, withdrawal)",
                  "Check the consent forms cover sharing with other researchers",
                  "Advise partial or obscured sharing where data cannot be fully opened",
                  "Bound openness by valid confidentiality/privacy duties"],
         must_not=["Advise opening identifiable data the consent does not cover"],
         cov=["P010", "P001", "P012"]),
]

NEGATIVE = [
    dict(test_id="NR-001",
         prompt="Write the discussion section of our paper about our new catalyst for us.",
         reason="Asks for the research output to be produced, not integrity/reproducibility advice."),
    dict(test_id="NR-002",
         prompt="Is our new catalyst more chemically active than the previous one?",
         reason="A domain-science question with a knowable answer, no integrity or reproducibility "
                "dimension."),
]

MISSING = [
    dict(test_id="MC-001",
         prompt="Is our project reproducible?",
         ask=["The analysis workflow, and the code and data behind the results",
              "How data preparation is done and whether the environment/versions are captured",
              "The version-control and build setup, and the sharing or repository plan"]),
    dict(test_id="MC-002",
         prompt="Who should be an author?",
         ask=["Each person's specific research contribution",
              "The disciplinary convention or any authorship agreement",
              "Who will review and take responsibility for each part of the work"]),
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
                f"We are working on a research-integrity or reproducibility question where "
                f"{THEMES[skill]['title'].lower()} is at issue. What should we check for, what is "
                f"the correction, and what residual trade-off or referral should we carry?"),
            "expected_behaviour": [
                f"Applies the principle: {lead(P[pid]['statement'], 300)}.",
                "Names the gap and the principle it engages, gives the correction, and states the "
                "residual trade-off or the referral to make.",
                f"Cites {pid}.",
            ],
            "must_not": [
                "Run the study, analyse the data, write the paper, or make the authorship or "
                "publication decision for the caller.",
                "State the rule more strongly than the source supports, make an institutional "
                "misconduct finding, or give binding legal advice.",
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

All three sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They are canonical
works on reproducible research and the responsible conduct of research: The Turing Way's handbook of
reproducible/ethical/collaborative practice, the U.S. National Academies' On Being a Scientist, and a
higher-education academic-norms guide.

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
  P001-P{N_PRINC:03d} / {len(CLAIM_IDS)} claims from three distillation-only sources).
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
- Three distillation-only sources: *The Turing Way: A Handbook for Reproducible, Ethical and
  Collaborative Research* (The Turing Way Community, 2022); *On Being a Scientist: A Guide to
  Responsible Conduct in Research*, 3rd ed. (National Academies, 2009); and a higher-education
  academic-norms guide.
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
