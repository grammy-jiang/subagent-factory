"""Skill partition for technical-translation-advisor + coverage verification.

The 10 skills partition all 150 principles (disjoint union). Slugs are the
knowledge_partition.skills entries in profile.yaml; each principle lands in exactly
one skill. Run this module directly to verify coverage before generating bodies.
"""

SKILLS = {
    "analyzing-audience-brief-and-skopos": {
        "title": "Analyzing Audience, Translation Brief and Skopos",
        "desc": "Establish who will read the target text, how they will use and receive it, and the "
        "purpose (Skopos) the commission sets, from a translation brief and a document profile — "
        "before any wording decision.",
        "principles": ["P002", "P007", "P020", "P024", "P056", "P061", "P069", "P090", "P099",
                       "P108", "P109", "P121", "P129"],
    },
    "selecting-translation-strategy-and-procedures": {
        "title": "Selecting Translation Strategy and Procedures",
        "desc": "Choose an overall strategy and the local procedures (direct/oblique, equivalence "
        "level, generalising/particularising, expansion, adaptation, restructuring) from the "
        "communicative situation rather than from universal maxims.",
        "principles": ["P014", "P015", "P035", "P046", "P070", "P089", "P100", "P107", "P114",
                       "P115", "P116", "P130", "P131", "P132", "P133", "P136"],
    },
    "grounding-translation-in-reader-cognition": {
        "title": "Grounding Translation in Reader Cognition",
        "desc": "Shape the target text around how readers perceive, remember, attend, learn and solve "
        "problems: minimise processing effort and cognitive load so the text is easy to read, "
        "understand and act on.",
        "principles": ["P003", "P009", "P010", "P017", "P023", "P025", "P030", "P031", "P037",
                       "P043", "P045", "P057", "P058", "P060", "P062", "P063", "P082", "P111",
                       "P112", "P118", "P123", "P137"],
    },
    "handling-terminology-units-and-nomenclature": {
        "title": "Handling Terminology, Units and Nomenclature",
        "desc": "Handle the technical precision layer — terminology, Latin nomenclature, SI units and "
        "formulae, regulatory specification terms, mandated/regional naming, acronyms and "
        "abbreviations — with the right resources.",
        "principles": ["P071", "P079", "P093", "P094", "P098", "P101", "P103", "P104", "P122",
                       "P140", "P149", "P150"],
    },
    "applying-iconic-linkage-and-consistency": {
        "title": "Applying Iconic Linkage and Consistency",
        "desc": "Translate recurring, semantically identical information with one uniform "
        "target-language construction (iconic linkage), and scale that consistency through "
        "controlled language, style guides and translation memory where it fits.",
        "principles": ["P013", "P021", "P026", "P044", "P074", "P075", "P134"],
    },
    "matching-document-type-and-genre": {
        "title": "Matching Document Type and Genre",
        "desc": "Recognise a text's type and genre — technical vs scientific, data sheet, manual, "
        "paper, abstract, presentation, case study, reference or hybrid — and translate to its "
        "conventions and communicative purpose.",
        "principles": ["P068", "P072", "P077", "P080", "P091", "P092", "P095", "P096", "P097",
                       "P110", "P113", "P125", "P126", "P127", "P128"],
    },
    "designing-document-structure-and-presentation": {
        "title": "Designing Document Structure and Presentation",
        "desc": "Treat layout, typography, white space, structure, graphics/screenshots, the table of "
        "contents and space constraints as communicative usability factors, and build modular, "
        "navigable, task-centred guides.",
        "principles": ["P004", "P005", "P012", "P016", "P028", "P029", "P038", "P047", "P083",
                       "P106", "P124", "P147", "P148"],
    },
    "planning-usability-evaluations": {
        "title": "Planning Usability Evaluations",
        "desc": "Decide how to evaluate documentation usability: pick methods (formative/summative, "
        "analytical/empirical, absolute/comparative) from the test question, set observable "
        "criteria and metrics, and build usability in from the start.",
        "principles": ["P006", "P018", "P022", "P032", "P039", "P040", "P041", "P042", "P049",
                       "P064", "P084"],
    },
    "running-and-analyzing-usability-studies": {
        "title": "Running and Analyzing Usability Studies",
        "desc": "Run a valid usability study: recruit and protect representative participants, pilot, "
        "control confounds and contamination, choose observation methods, apply small-sample "
        "statistics and triangulate objective with subjective measures.",
        "principles": ["P019", "P027", "P033", "P034", "P050", "P051", "P052", "P053", "P054",
                       "P065", "P066", "P067", "P073", "P076", "P085", "P086", "P087", "P088",
                       "P120"],
    },
    "assuring-quality-safety-and-practice": {
        "title": "Assuring Quality, Safety and Professional Practice",
        "desc": "Hold documentation to legal, safety, accuracy and style-guide quality; treat warnings, "
        "brand names and EU-market translation as high-stakes; and revise, notify the client, and "
        "conduct professional practice with care.",
        "principles": ["P001", "P008", "P011", "P036", "P048", "P055", "P059", "P078", "P081",
                       "P102", "P105", "P117", "P119", "P135", "P138", "P139", "P141", "P142",
                       "P143", "P144", "P145", "P146"],
    },
}

REFERENCES = {
    "technical-translation-principles-index": {
        "title": "Technical Translation Principles Index",
        "desc": "Package-wide index of every promoted technical-translation principle, grouped by skill.",
    },
    "technical-translation-evidence-notes": {
        "title": "Technical Translation Evidence Notes",
        "desc": "Confidence, source spread and grounding notes for the promoted principles.",
    },
}


def verify(all_ids):
    assigned = {}
    dupes = []
    for slug, meta in SKILLS.items():
        for pid in meta["principles"]:
            if pid in assigned:
                dupes.append((pid, assigned[pid], slug))
            assigned[pid] = slug
    covered = set(assigned)
    missing = sorted(all_ids - covered)
    extra = sorted(covered - all_ids)
    return assigned, dupes, missing, extra


if __name__ == "__main__":
    import yaml
    from pathlib import Path

    base = Path(__file__).resolve().parents[2]
    d = yaml.safe_load((base / "principles" / "principles.yaml").read_text())
    all_ids = {p["principle_id"] for p in d["principles"]}
    assigned, dupes, missing, extra = verify(all_ids)
    print(f"principles={len(all_ids)} assigned={len(assigned)}")
    print(f"dupes={dupes}")
    print(f"missing (in principles, no skill)={missing}")
    print(f"extra (assigned, not a real principle)={extra}")
    for slug, meta in SKILLS.items():
        print(f"  {slug}: {len(meta['principles'])}")
