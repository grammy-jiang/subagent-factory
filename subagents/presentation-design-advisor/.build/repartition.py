"""One-shot: re-partition skill frontmatter for the r1 review fixes (F4/F10/F12) + add
a `description:` line. Bodies are re-authored separately; this only rewrites frontmatter."""

import shutil
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parent.parent
SK = BASE / "skills"

PRINCIPLES = {
    p["principle_id"]: p
    for p in yaml.safe_load((BASE / "principles" / "principles.yaml").read_text())["principles"]
}

PARTITION = {
    "assertion-evidence-slide-structure": (
        "Structure a technical content slide as a sentence assertion headline over visual evidence"
        " instead of a phrase headline over bullets: headline mechanics, when evidence may precede"
        " the assertion, and why a bulleted list fails.",
        ["P014", "P015", "P021", "P044", "P045", "P046", "P047", "P069", "P070", "P071", "P077", "P096"],
    ),
    "slide-density-and-signal-to-noise": (
        "Cut a slide down to what the speaker can actually deliver against it: words-per-minute"
        " density, splitting and sequencing, clutter and empty space, and engineered simplicity.",
        ["P012", "P018", "P019", "P025", "P026", "P033", "P073", "P080", "P081", "P084", "P097", "P101"],
    ),
    "visual-evidence-analogies-and-graphics": (
        "Choose and sequence the visual evidence a slide shows: evidence type from the assertion,"
        " replacing lists with the relationship they hold, analogies and their limits, animation,"
        " and crediting another group's work.",
        ["P001", "P002", "P034", "P042", "P078", "P091", "P100", "P102", "P103"],
    ),
    "typography-colour-and-slide-layout": (
        "Set the readable surface of a slide for the actual room: type size and typeface, boldface,"
        " background and palette verified by projecting, blank space, and software defaults.",
        ["P004", "P007", "P008", "P011", "P017", "P023", "P049", "P098", "P099"],
    ),
    "story-structure-and-the-big-idea": (
        "Settle what the presentation is about and in what order it unfolds before any slide"
        " exists: the big idea, ideation, sticky-note story order, what-is openings, the turning"
        " point, and the ending.",
        ["P005", "P035", "P041", "P059", "P060", "P064", "P087", "P116", "P118"],
    ),
    "audience-analysis-and-persona-design": (
        "Establish who the talk is for and build the design around them: audience questions and"
        " personas, audience-as-hero, jargon, mixed audiences, emotional calibration, and refusing"
        " to let the deck become the presenter's persona.",
        ["P013", "P056", "P057", "P058", "P061", "P063", "P074", "P075", "P114", "P119", "P120"],
    ),
    "persuasion-ethos-pathos-and-logos": (
        "Audit and build the persuasive case across all three appeals — evidence, the audience's"
        " emotion, and the speaker's credibility — against prior bias, contrast, reward, and the"
        " signal noise that distorts them.",
        ["P006", "P030", "P038", "P040", "P068", "P092", "P113", "P115", "P117"],
    ),
    "talk-organisation-transitions-and-emphasis": (
        "Build the architecture of the talk between opening and close: organisation, changes of"
        " direction and their signalling, an explicit memorable map, the ways audiences get lost,"
        " and deliberate emphasis.",
        ["P037", "P039", "P043", "P067", "P076", "P082", "P083", "P086", "P089", "P090"],
    ),
    "opening-closing-and-framing-slides": (
        "Design the slides that frame the talk: an orienting title slide, whether title/outline/"
        "conclusion slides earn their place, the closing sequence that invites questions, the"
        " final projected slide, and planted sound bites.",
        ["P022", "P024", "P032", "P050", "P085", "P112"],
    ),
    "rehearsal-and-memorisation": (
        "Plan how the talk is practised before the day: walking it through, practising to no notes"
        " by memorising organisation, why memorising words and reading a speech fail, and letting"
        " the visual evidence trigger what to say.",
        ["P020", "P052", "P054", "P072", "P094", "P095", "P105"],
    ),
    "in-room-delivery-and-composure": (
        "Govern what the speaker does in the room while the talk runs: confidence rather than"
        " nervousness, eye contact, taking charge of the room, varying delivery mode, holding"
        " composure through a mid-talk mishap, and judging a delivery style fairly. For composure"
        " under a hostile question, use questions-challenge-and-composure instead.",
        ["P016", "P066", "P079", "P106", "P107", "P108", "P110", "P111"],
    ),
    "questions-challenge-and-composure": (
        "Prepare for what happens after the talk and when the work is attacked: the ordered way to"
        " handle a question, three tested responses to a challenge, conceding when the challenger"
        " is right, and transparency. For general mid-talk nerves or mishaps, use"
        " in-room-delivery-and-composure instead.",
        ["P029", "P055", "P093", "P109"],
    ),
    "format-choice-and-preparation-planning": (
        "Decide whether there should be a presentation at all, in what format, and how much work"
        " it deserves: presentation versus document or meeting, length constraint, specialised"
        " formats on their conditions, preparation scheduling, and briefing an illustrator.",
        ["P009", "P010", "P027", "P031", "P051", "P062", "P065", "P088"],
    ),
    "equipment-venue-and-contingency": (
        "Remove the dependencies that fail in rooms the speaker does not control and plan for the"
        " failures that remain: local files and backups, rehearsed demonstrations, an equipment"
        " failure plan, and blanking the screen.",
        ["P003", "P028", "P053", "P104"],
    ),
}

RENAMED_FROM = {
    "rehearsal-and-memorisation": "rehearsal-and-extemporaneous-delivery",
    "in-room-delivery-and-composure": "rehearsal-and-extemporaneous-delivery",
}
DROP_DIRS = ["rehearsal-and-extemporaneous-delivery"]


def main() -> None:
    owned = set()
    for slug, (desc, pids) in PARTITION.items():
        assert not owned & set(pids), f"{slug} double-owns {owned & set(pids)}"
        owned |= set(pids)
        for pid in pids:
            assert pid in PRINCIPLES, pid
        claims = sorted({c for pid in pids for c in PRINCIPLES[pid]["derived_from_claims"]})[:16]
        d = SK / slug
        src = SK / RENAMED_FROM.get(slug, slug)
        d.mkdir(parents=True, exist_ok=True)
        body = ""
        if (src / "SKILL.md").exists():
            text = (src / "SKILL.md").read_text()
            body = text.split("\n---\n", 1)[1] if "\n---\n" in text else ""
        fm = {
            "name": slug,
            "description": desc,
            "kind": "skill",
            "status": "ready",
            "provenance": {
                "principles": pids,
                "claims": claims,
                "evidence": [],
                "source_anchors": [],
                "authored_from_digest": "PENDING",
            },
        }
        out = "---\n" + yaml.safe_dump(fm, sort_keys=False, width=100) + "---\n" + body
        (d / "SKILL.md").write_text(out)
        print("wrote", slug, len(pids), "principles")
    for stale in DROP_DIRS:
        if (SK / stale).exists():
            shutil.rmtree(SK / stale)
            print("removed", stale)
    print("unowned principles:", sorted(set(PRINCIPLES) - owned))


if __name__ == "__main__":
    main()
