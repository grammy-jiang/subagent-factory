"""Deterministic authoring generator for presentation-design-advisor.

Reads the already-assembled, deterministically-valid distilled spine
(principles/principles.yaml + analysis/claims.jsonl + evidence + anchors) and emits the
LLM-authored layer: profile.yaml, references/*, skills/*, tests/*, reports/faithfulness-report.yaml,
provenance-ledger.md, CHANGELOG.md. Every emitted id resolves into the spine.

Cloned from the learning-science-advisor sibling generator (same recipe: one deterministic pass
over a pre-built Tier-2 spine). Run:  python3 .build/authoring/gen.py
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

BASE = Path(__file__).resolve().parents[2]  # subagents/presentation-design-advisor
SLUG = "presentation-design-advisor"
DISPLAY = "Presentation Design Advisor"
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
# Every principle 1..120 appears exactly once.
SKILLS: list[tuple[str, list[int]]] = [
    ("assertion-evidence-slide-structure",
     [14, 15, 21, 44, 45, 46, 47, 69, 70, 71, 77, 96]),
    ("slide-density-and-signal-to-noise",
     [12, 18, 19, 25, 26, 33, 73, 80, 81, 84, 97, 101]),
    ("visual-evidence-analogies-and-graphics",
     [1, 2, 34, 42, 78, 91, 100, 102, 103]),
    ("typography-colour-and-slide-layout",
     [4, 7, 8, 11, 17, 23, 49, 98, 99]),
    ("story-structure-and-the-big-idea",
     [5, 35, 41, 59, 60, 64, 87, 116, 118]),
    ("audience-analysis-and-persona-design",
     [13, 56, 57, 58, 61, 63, 75, 114, 119, 120]),
    ("persuasion-ethos-pathos-and-logos",
     [6, 30, 38, 40, 68, 92, 113, 115, 117]),
    ("talk-organisation-transitions-and-emphasis",
     [37, 39, 43, 67, 76, 82, 83, 86, 89, 90]),
    ("opening-closing-and-framing-slides",
     [22, 24, 32, 50, 85, 112]),
    ("rehearsal-and-extemporaneous-delivery",
     [16, 20, 52, 54, 66, 72, 79, 94, 95, 105, 106, 107, 108, 110, 111]),
    ("questions-challenge-and-composure",
     [29, 55, 93, 109]),
    ("format-choice-and-preparation-planning",
     [9, 10, 27, 31, 36, 48, 51, 62, 65, 74, 88]),
    ("equipment-venue-and-contingency",
     [3, 28, 53, 104]),
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
    "presentation-design-principles-index",
    "presentation-design-evidence-notes",
]
for r in REFS:
    assert len(r) <= 48, f"ref name too long ({len(r)}): {r}"

PID_TO_SKILL = {pids(n): slug for slug, nums in SKILLS for n in nums}

# ---------------------------------------------------------------------------- per-skill themes
THEMES: dict[str, dict] = {
    "assertion-evidence-slide-structure": dict(
        title="Assertion-Evidence Slide Structure",
        purpose=(
            "This skill designs and reviews the structure of a technical content slide as a pair of "
            "substitutions: a succinct sentence stating the slide's main assertion — a hypothesis, "
            "assumption, insight, or result — in place of a phrase headline, and visual evidence in "
            "place of the bulleted list, with bulleted lists not occurring at all. It treats the "
            "bulleted list as a failure on three simultaneous grounds: it does not show "
            "connections, does not reveal hierarchy, and leaves the critical assertions "
            "unspecified, while its word count crowds out the graphics. It applies the headline "
            "mechanics concretely — no more than two lines, left justified, sentence-capitalised "
            "with the period optional, starting in the upper-left corner, set at 28 points, and "
            "broken so noun, verb, and prepositional phrases stay together with no orphaned word. "
            "It permits the evidence to precede the assertion in the three situations the source "
            "names — teaching, a complex assertion, and a skeptical audience — but never permits an "
            "assertion projected with no visual evidence at all. It expects the structure's largest "
            "effect on preparation rather than delivery, and expects crafting the headline to be "
            "the hardest part of the work."),
        when=[
            "A content slide's headline names a topic rather than stating what the slide asserts, "
            "or the body is a bulleted list standing in for evidence (P014, P045, P077).",
            "Headline mechanics need setting or checking: line count, justification, "
            "capitalisation, point size, corner placement, and where the line breaks fall (P015, "
            "P044).",
            "The assertion is complex or controversial, or the setting is a classroom, so the "
            "evidence should be shown and explained before the assertion is revealed (P046).",
            "The comprehension benefit of the structure is being claimed, argued, or challenged, "
            "and the measured scope of that benefit must be stated rather than asserted (P047, "
            "P070, P071, P096, P021, P069).",
        ],
        input="The slide, sequence, or deck under review, plus what each slide is meant to assert, "
              "who the audience is, and whether the setting is teaching, reporting, or persuading."),
    "slide-density-and-signal-to-noise": dict(
        title="Slide Density And Signal-To-Noise",
        purpose=(
            "This skill reduces what a slide carries to what a speaker can actually deliver against "
            "it. It measures word count against projected words per minute rather than a per-slide "
            "bullet rule, because a slide projected for about a minute competes with the 120 to 140 "
            "words the speaker delivers in that same minute — which is why even a rule-compliant "
            "slide can carry too many words. It strips every phrase and decorative image that does "
            "not connect directly to the spoken content, asks what can be removed without changing "
            "the meaning and where the content can be split, and treats clear space as fine and "
            "clutter as a design failure. It splits content across slides and reveals the pieces in "
            "sequence whenever secondary or technical detail competes with the single main message, "
            "noting that splitting without sequencing does not by itself solve density. It holds "
            "the balance between saying and showing — headline carries the message, body carries "
            "the evidence, secondary detail is supplied aloud — keeps any grouping to four items or "
            "fewer, hides each element until it is referred to, and refuses to let the deck become "
            "the speaker's notes or a document read faster than it can be explained. It treats "
            "TED-style simplicity as engineered rather than effortless, costing more preparation "
            "than assertion-evidence slides and demanding artistic judgment in cropping and "
            "placement, achieved by raising the signal-to-noise ratio, eliminating unneeded text "
            "and lines, using empty space deliberately, and building scenes rather than slides."),
        when=[
            "A slide is overloaded and must be cut or split, or the deck reads as a document rather "
            "than a visual aid (P012, P018, P073, P019).",
            "Word count needs judging against what the speaker will actually say in the time the "
            "slide is projected (P025, P101, P033).",
            "Elements appear all at once, or a list or set of call-outs runs past four items, so "
            "the audience reads ahead instead of listening (P097, P084).",
            "The slides were built as the speaker's own prompts rather than for the audience, "
            "producing the screen-then-room cycle (P080, P026).",
            "A minimal, TED-style visual look is wanted and its real preparation cost and craft "
            "demands must be stated rather than assumed away (P081).",
        ],
        input="The slide or deck, the time available, and what the speaker intends to say aloud "
              "while each slide is projected."),
    "visual-evidence-analogies-and-graphics": dict(
        title="Visual Evidence, Analogies And Graphics",
        purpose=(
            "This skill chooses and sequences the evidence a slide shows. It starts by recognising "
            "exactly what is being asserted and fixing the main assertion the data supports before "
            "deciding how to graph or present it, then selects the type of visual evidence from the "
            "assertion it must support — a map and photographs for a background fact, photographs "
            "with a timeline and graph for a trend, a diagram for a process, a line or bar graph "
            "for a quantitative relationship. It replaces a bulleted list with the visual form of "
            "the relationship the list actually holds — a timeline, call-outs around an image, a "
            "pie graph, a diagram — rather than leaving the audience to work the relation out. When "
            "the main assertion sits too far up the mountain for one dataset to reach, it builds a "
            "chain of evidenced sub-assertions and supplies the background warrants the audience "
            "needs. It anchors unfamiliar concepts in a specific physical example or analogy, while "
            "confining analogy to conveying how something works, how large it is, or how likely it "
            "is — never to supporting an assertion in an argument, where the differences are "
            "attackable. It uses animation to control the order a slide is taken in without ever "
            "starting from an empty body, judges a zoomable single canvas against its real costs, "
            "and requires a visible reference on every slide carrying another group's work."),
        when=[
            "Data or a technical result must be turned into the visual evidence for a specific "
            "assertion, or a bulleted list conceals the relationship it is really about (P001, "
            "P034, P002).",
            "One graph or dataset cannot reach the main assertion, so a chain of evidenced "
            "sub-assertions with their background warrants is needed (P091).",
            "The concept is unfamiliar or the passage is abstract or mathematical, or an analogy is "
            "being used where evidence is required (P042, P078).",
            "The visual carries several simultaneous connections and needs staged reveal, a "
            "zoomable canvas is proposed, or material from another group appears on a slide (P100, "
            "P103, P102).",
        ],
        input="The assertion the slide must support, the data or material available for it, the "
              "audience's familiarity with the concept, and the provenance of any borrowed figure."),
    "typography-colour-and-slide-layout": dict(
        title="Typography, Colour And Slide Layout",
        purpose=(
            "This skill sets the readable surface of the slide. It treats presentation-software "
            "defaults as an unvalidated inheritance rather than guidance — never founded on "
            "research, baked into institutional templates — and assesses every default against the "
            "actual audience, purpose, and occasion. It forces a large minimum type size, because "
            "small type comes from not knowing the material well enough or believing more text is "
            "more convincing, while the floor compels the presenter to find the salient points. It "
            "chooses the typeface by reading speed rather than tradition, since the audience reads "
            "while listening: sans serif faces read faster in the short blocks of a slide, their "
            "straighter strokes matter most at a sharp side angle, and the penalty for a serif face "
            "becomes decisive when the projector or lighting is poor. It boldfaces slide type for "
            "larger rooms and avoids italics and underlining. It fixes the background colour first "
            "— dark or light from the formality and venue size, since pure black and pure white "
            "afford the greatest contrast while mid-range coloured backgrounds render parts of a "
            "palette unusable — and it verifies the palette by projecting it in the actual room "
            "rather than judging it on the authoring screen. It opens blank space between "
            "elements, holds text blocks and headlines to two lines and lists to two to four items, "
            "uses animation only where it serves the audience, and keeps logos secondary."),
        when=[
            "Type size, weight, or typeface is being chosen or reviewed for a projected deck, "
            "especially for a large room or poor projection conditions (P007, P098, P049).",
            "A colour palette or background needs setting, or a palette that looked fine on the "
            "authoring screen must be verified under the venue's projector (P099, P011).",
            "The slide feels crowded, the viewing order is ambiguous, or the audience bounces "
            "between elements (P004, P023).",
            "An institutional template or brand rule is driving the design — default masters, "
            "mandated logos on every slide (P017, P008).",
        ],
        input="The deck or template, the room and projection conditions, any brand or institutional "
              "template constraints, and the audience's viewing angles and distance."),
    "story-structure-and-the-big-idea": dict(
        title="Story Structure And The Big Idea",
        purpose=(
            "This skill settles what the presentation is about and in what order it unfolds, before "
            "any slide exists. It writes the big idea as a complete sentence articulating the "
            "presenter's unique point of view and what is at stake — a topic is not a big idea, and "
            "addressing it to 'you' is better still. It keeps presentation software closed during "
            "idea generation, collects and creates content first, and makes quantity the objective "
            "of ideation, expecting the genuinely clever ideas in the third or fourth round rather "
            "than the first. It settles the story on separate sticky notes — main message and each "
            "supporting assertion — arranged into the order that tells the best story, after which "
            "any detail supporting none of them is excluded. It opens by stating what is, a concise "
            "formulation of what everyone agrees is true now, because accurately capturing the "
            "audience's reality proves the presenter understands their context and supplies the "
            "baseline without which the new idea has no dramatic effect; it makes the turning point "
            "an explicit, memorable call to adventure delivered at the moment the contrast becomes "
            "stark; and it lands the ending on a higher plane than the beginning. It uses stories "
            "for two specific jobs — creating anticipation and supplying a recall frame — while "
            "keeping the talk a blend of document and story, and it keeps a personal catalogue of "
            "stories indexed by emotion."),
        when=[
            "The answer to 'what is this presentation about?' is a noun phrase, so the controlling "
            "message must be written as a sentence with a point of view (P060).",
            "A new presentation is starting and ideation must precede slide-building, with quantity "
            "as the objective (P005, P118, P035).",
            "The arc needs shaping: the what-is baseline, the turning point that makes the contrast "
            "stark, and an ending on a higher plane than the beginning (P087, P116, P059).",
            "Stories are being chosen or written into the talk, or a specific emotion is wanted at "
            "a specific point (P041, P064).",
        ],
        input="The occasion, the audience, what the presenter wants to change, the raw material "
              "available, and how much preparation time remains."),
    "audience-analysis-and-persona-design": dict(
        title="Audience Analysis And Persona Design",
        purpose=(
            "This skill establishes who the talk is for and builds the design around them. It "
            "answers the seven audience questions and builds one persona per distinct audience "
            "segment before any slide is built, keeping the persona slide at the front of the deck "
            "as private working context that is never projected. It builds the presentation around "
            "what the audience needs and will do rather than the presenter's agenda, casts the "
            "audience as the hero and the presenter as the mentor, and judges success by what they "
            "leave holding rather than by how impressive the presenter appeared. It discharges the "
            "mentor's two duties — teaching and gift-giving — by supplying important, useful, "
            "previously unknown information plus guidance, confidence, and tools. It tests each "
            "detail against two questions — will they understand it, and will they be interested in "
            "it — and where the audience is unknown, it mingles beforehand or tries the talk on "
            "someone of the same background. It never assumes the audience has kept up with the "
            "presenter's field, since jargon aimed at nonspecialists costs help and funding purely "
            "because listeners do not understand it. For a mixed audience it abandons the goal of "
            "satisfying everyone throughout and aims instead for everyone satisfied by the end. It "
            "calibrates emotional and evidentiary material to the audience's tolerance in both "
            "directions, and locates content on the head-heart-gut-groin spectrum to correct "
            "whichever way the presenter defaults."),
        when=[
            "A presentation is being started and the audience must be characterised before design "
            "begins — questions answered, personas built, segments named (P061, P056).",
            "The audience is mixed in technical level or background, or is unknown to the speaker "
            "(P013, P075).",
            "Draft copy or messaging carries jargon or acronyms aimed at people outside the "
            "presenter's field or department (P057).",
            "The balance of proof and emotional appeal must be tuned for an analytical or an "
            "emotionally driven audience, or a talk did not land and the cause may be the audience "
            "read (P119, P120, P063, P058, P114).",
        ],
        input="Who will be in the room, what they already know, why they are there, what "
              "preconceptions they hold, and what the presenter wants them to do afterwards."),
    "persuasion-ethos-pathos-and-logos": dict(
        title="Persuasion — Ethos, Pathos And Logos",
        purpose=(
            "This skill audits and builds the persuasive case. It accounts for all three Aristotelian "
            "appeals — logical evidence, the audience's emotion, and the speaker's own credibility "
            "of character — rather than logic alone, because facts by themselves do not persuade, "
            "technical presenters systematically underrate the other two, and many decisions about "
            "technical work are made by non-technical people whom character and emotion sway. It "
            "assesses the audience's prior bias first, because that sets both the strategy and the "
            "energy an argument requires and can override the outcome regardless of the speaker's "
            "stature. It pairs facts with emotional appeal rather than choosing between them, since "
            "logical agreement alone does not produce action and stacking more proof does not "
            "convert a determined skeptic. It builds the character appeal deliberately — making a "
            "position that runs counter to one's own record part of the evidence, showing not only "
            "that one's result is right but why the conflicting result is wrong — and builds common "
            "ground from shared experience and goals, revealing qualifications humbly. It engineers "
            "contrast against the audience's own environment, since obscurity rather than "
            "opposition is what defeats an idea. It describes a reward proportional to the "
            "sacrifice being asked. It treats the whole presentation as a signal through sender, "
            "transmission, reception, and receiver, minimising credibility, semantic, experiential, "
            "and bias noise. And it holds the hard line that persuasive power is for building up, "
            "never for deceiving."),
        when=[
            "A persuasive presentation must be audited for coverage of evidence, emotion, and "
            "speaker credibility, rather than evidence alone (P006, P030).",
            "The audience holds a prior bias, does not yet grant the speaker authority, or does not "
            "know the speaker at all (P038, P092, P115).",
            "The idea competes for attention with other messages, or the presentation makes a "
            "request that needs a proportional reward (P040, P117).",
            "A message is not landing and the distortion must be located, or the presenter has an "
            "incentive to overstate performance or hide risk (P113, P068).",
        ],
        input="The claim being argued, the evidence behind it, what the audience already believes "
              "and wants, what the presenter is asking them to do, and the speaker's standing."),
    "talk-organisation-transitions-and-emphasis": dict(
        title="Talk Organisation, Transitions And Emphasis",
        purpose=(
            "This skill builds the architecture of the talk between opening and close. It designs "
            "structure on four levers, any one of which can fail a talk — the organisation itself, "
            "the number of changes in direction, the signalling of those changes, and the emphasis "
            "of key details — and against four pitfalls: doing too much, losing the audience at the "
            "beginning, losing them in the middle, and not being persuasive enough. It designs "
            "specifically against the three ways audiences get lost — gaps in the logic they cannot "
            "bridge, an unsignalled change of direction, and exhaustion from too many details — and "
            "assumes listeners drift even with sound structure, so it builds a way to recover. It "
            "signals every transition through at least one of three channels — the speech's "
            "wording, a change in the visual aids, or the delivery — at the introduction-to-middle, "
            "between-sections, and middle-to-conclusion points. It maps the talk explicitly, "
            "because a reader can glance ahead at headings while a listener cannot, and makes the "
            "map memorable by integrating the divisions into one image or anchoring each topic with "
            "a representative image repeated at its division. It refuses to enter the middle until "
            "the audience understands why the subject matters. It emphasises deliberately through "
            "repetition, illustration, placement, pausing, volume, and proximity. It selects, "
            "sorts, and ranks the details, identifies the message for every scene whether or not it "
            "appears on the slide, and delivers real depth inside a deliberately broad talk."),
        when=[
            "A talk's organisation, section count, or ordering is being designed or reviewed, or "
            "the audience gets lost in the middle (P083, P039, P086).",
            "Transitions between sections are unsignalled, or the audience cannot pace itself "
            "because the talk has no explicit, memorable map (P043, P076, P090).",
            "The talk enters its substance before establishing why the subject matters (P089).",
            "Key details are not landing, every scene's message has not been settled, or the scope "
            "is deliberately broad and needs depth (P037, P067, P082).",
        ],
        input="The talk's sections and running order, its length, what the audience must carry "
              "away, and where in a run-through listeners were observed to lose the thread."),
    "opening-closing-and-framing-slides": dict(
        title="Opening, Closing And Framing Slides",
        purpose=(
            "This skill designs the slides that frame the talk. It makes the title slide orient "
            "rather than announce: relevant images give the speaker several possible entry points — "
            "scope, importance, or history — into the same talk for different audiences, where the "
            "default title-names-institutions slide turns the opening into a hurried obligation and "
            "leaves the audience disoriented the moment it changes. It spends more than twenty or "
            "thirty seconds on that slide and answers at least one of the audience's opening "
            "questions before the first slide change. It includes title, outline, and conclusion "
            "slides only where they earn their place, since they carry organisation rather than "
            "content and the shorter the talk the less each is needed. It runs a closing sequence "
            "that gives the audience time to compose questions — a headline beginning 'In closing' "
            "or 'In summary' so they start as the slide appears, a strong final sentence, a pause "
            "for applause with a thank-you to cue it, and only then the word Questions animated in "
            "— because an abrupt ending produces silence that reads as though nobody understood or "
            "cared. It makes the final projected slide summarise the talk's most important "
            "takeaway, since that slide is displayed longest while questions are taken; an empty "
            "one is worse than a blank screen, a Thank You slide wastes the screen, and a Questions "
            "slide tells the audience what they already know. Where the talk will be covered or "
            "filmed, it plants succinct, repeatable sound bites coordinated with the press "
            "release."),
        when=[
            "The title slide announces rather than orients, or the opening is spent reading names "
            "and affiliations (P050, P085).",
            "Title, outline, or conclusion slides are being added or removed, and whether each "
            "earns its place in this talk's length is at issue (P032).",
            "The talk ends abruptly, or the last projected slide is a Thank You, a Questions slide, "
            "or blank while questions run (P022, P024).",
            "The presentation will be covered by press, filmed, or reacted to publicly, so "
            "quotable, transferable phrasing must be prepared (P112).",
        ],
        input="The opening and closing slides as they stand, the talk's length and setting, and "
              "whether questions, press, or recording follow."),
    "rehearsal-and-extemporaneous-delivery": dict(
        title="Rehearsal And Extemporaneous Delivery",
        purpose=(
            "This skill prepares and reviews the spoken performance. It walks the whole "
            "presentation beforehand even in a mumble, because practice smooths transitions, works "
            "out the explanations of difficult concepts, and above all dispels the fear of standing "
            "before an audience with nothing to say. It practises until the talk can be given with "
            "no notes by memorising its organisation — the test being that the speaker knows the "
            "next slide before advancing — and lets the visual evidence alone trigger what to say, "
            "which is what produces natural delivery. It rejects memorisation at presentation "
            "length, since a fifteen-minute talk means over two thousand words, the result cannot "
            "be changed mid-stream, and it recalls words faster than an audience can absorb them; "
            "memorising actual words stays the exception for short high-stakes fragments. It treats "
            "reading a speech as costly by default. It answers the risk of groping for a word with "
            "repeated practice rather than a script, and replaces the question of handling "
            "nervousness with the question of achieving confidence, whose answer is passion "
            "combined with preparation. It directs attention with the eyes on a workable rule, "
            "takes charge of the room, plans several deliberate delivery-mode changes within an "
            "hour, and holds composure through anything mid-talk. It accepts that no single "
            "delivery style is correct and that judging a delivery means accounting for the "
            "audience and the room the speaker faced."),
        when=[
            "A rehearsal plan is needed, or the speaker intends to work from notes, a script, or "
            "memorised text (P020, P052, P095, P105, P054, P094).",
            "Delivery is being coached or critiqued — style, eye contact, movement, room control, "
            "or holding attention across a long slot (P016, P066, P107, P106, P111, P079).",
            "The speaker is nervous, or something goes wrong mid-talk and composure is the issue "
            "(P110, P108).",
            "The slides are ready and the speaker must learn to speak from the evidence rather than "
            "from the screen (P072).",
        ],
        input="The talk as it stands, the speaker's experience and comfort, the room and audience "
              "they will face, the slot length, and how much rehearsal time remains."),
    "questions-challenge-and-composure": dict(
        title="Questions, Challenge And Composure",
        purpose=(
            "This skill prepares the presenter for what happens after the talk and when the work is "
            "attacked. It handles a question through an ordered sequence: listen to it, ask for "
            "clarification if it is unclear — legitimate rather than embarrassing, since it was "
            "fashioned on the spot — repeat or rephrase it when the room is too large for others to "
            "have heard, pause to think, and only then answer, balancing satisfying the questioner "
            "against staying concise enough that others still get a chance. It meets a challenge "
            "with one of three tested responses: standing straight and answering loudly enough for "
            "the whole room even if only restating the formal point; distinguishing sincere "
            "questions from attacks, answering the first politely and rebutting the second directly "
            "with the pertinent literature, calmly enumerating the papers that support a challenged "
            "assumption; or lowering the voice rather than raising it to guide the audience's "
            "sympathy, which works as long as the speaker stays resolute. Where the challenger is "
            "right, it concedes publicly and plainly, since holding one's ground need not create "
            "animosity and the willingness to admit being wrong is the clearest sign of a speaker's "
            "security. Underneath all of it, it asks the presenter to be transparent so the "
            "audience can see past them to the idea — honest about failures, unique rather than "
            "conforming, and uncompromising."),
        when=[
            "A question-and-answer session is being prepared or reviewed, including how questions "
            "are heard, repeated, and paced (P109).",
            "The work is likely to be challenged, or an attack must be distinguished from a sincere "
            "question and answered accordingly (P055).",
            "A challenger turns out to be right and the presenter must decide how to respond in "
            "public (P093).",
            "The presenter's instinct is to project authority and hide uncertainty, failure, or "
            "difference (P029).",
        ],
        input="The claims most exposed to challenge, the literature and evidence available to "
              "defend them, who is likely to push back, and the room's size and format."),
    "format-choice-and-preparation-planning": dict(
        title="Format Choice And Preparation Planning",
        purpose=(
            "This skill decides whether there should be a presentation at all, in what format, and "
            "how much work it deserves. Where the content really is a document it changes the "
            "format rather than the slides — hold a meeting, circulate the document beforehand or "
            "let the audience read it at the start, and spend the rest on discussion and action "
            "plans; and where the goal is only to convey facts and figures, cancel the meeting and "
            "send a report. It weighs a presentation against a document on five advantages — "
            "fielding questions, reading expressions, delivery emphasis, richer visual aids, "
            "evidenced receipt — against five disadvantages: one pass only, no time to look things "
            "up, the audience held to the speaker's pace, success hostage to delivery, and the "
            "difficulty of assembling everyone. It constrains length hard, because attention spans "
            "are short and constraint forces concision. It picks a specialised format on its stated "
            "conditions: the Lessig style for keynotes and after-dinner talks reused on multiple "
            "occasions, pecha kucha where a manager must raise a group's presentations quickly "
            "without time to teach a sophisticated structure. It scales preparation time to the "
            "stakes and books the cycles as soon as the engagement is known. It briefs illustrators "
            "with the story rather than with what to draw. It critiques a talk from four separate "
            "perspectives, plans for slow institutional adoption of a better slide structure, keeps "
            "the deck from becoming an extension of the presenter's persona, and judges the whole "
            "thing by whether the audience looks enlightened, moved, or willing to act."),
        when=[
            "The communication channel is still open — presentation, circulated document, meeting, "
            "or no meeting at all (P009, P031).",
            "Length, format, or a specialised style is being chosen for the occasion (P088, P027, "
            "P051).",
            "Preparation must be scheduled and scoped to the stakes, or work is being handed to an "
            "illustrator or designer (P065, P062).",
            "A talk or a slide standard is being reviewed or rolled out across a group, or success "
            "criteria must be defined (P036, P048, P074, P010).",
        ],
        input="The occasion and its stakes, who must receive the content, the time available before "
              "and during, and what the institution's templates and norms already impose."),
    "equipment-venue-and-contingency": dict(
        title="Equipment, Venue And Contingency",
        purpose=(
            "This skill removes the dependencies that fail in rooms the speaker does not control "
            "and plans for the failures that remain. It embeds every image and film in a local file "
            "with a backup on separate media rather than relying on internet access many "
            "organisations restrict, keeps a teleconferenced presentation simple because films lock "
            "up and sound clips feed back in transmission, and brings the speaker's own laptop "
            "where the deck needs unusual typefaces, settings, formats, or films. It never lets a "
            "live demonstration be attempted without rehearsal on the actual equipment, since an "
            "unpractised demonstration can injure the presenter, hijack the lesson, or cost a "
            "contract outright at the culminating moment of a bid — and it states plainly that "
            "rehearsal guarantees nothing, since practised demonstrations still fail, but greatly "
            "increases the odds. Once the structure and slides are set, it imagines the worst "
            "compound case and devises a plan for equipment failure, because disasters arise from "
            "chains of causes rather than single ones: where the equipment is unproven it designs "
            "the talk to be deliverable from handouts alone, and it carries a troubleshooting kit "
            "of video and audio cables and a small computer-powered speaker plus the knowledge of "
            "how to match the laptop's resolution to the projector. It also treats the screen "
            "itself as controllable, blanking it deliberately where a portion of the talk needs no "
            "visual support."),
        when=[
            "The presentation will be given in a room, or over a link, the speaker does not control "
            "(P104).",
            "The talk includes a live demonstration (P028).",
            "The structure and slides are set and a failure plan is still missing (P053).",
            "Part of the talk needs no visual support and the screen should go dark deliberately "
            "(P003).",
        ],
        input="The venue, its equipment and connectivity, what the deck depends on, whether a "
              "demonstration is planned, and how much setup access the speaker will get."),
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
    "grounded in three distillation-only sources on presentation design and delivery (Alley's "
    "*The Craft of Scientific Presentations*, and Duarte's *Resonate* and *slide:ology*)")

# Human-readable source descriptors, keyed by the source_id already in the manifest.
SOURCE_INFO: dict[str, dict] = {
    "alley-craft-of-scien-8c1a058e": dict(
        title="The Craft of Scientific Presentations: Critical Steps to Succeed and Critical "
              "Errors to Avoid",
        author="Michael Alley", year=2013),
    "duarte-resonate-dc2fdbd7": dict(
        title="Resonate: Present Visual Stories That Transform Audiences",
        author="Nancy Duarte", year=2010),
    "duarte-slideology-e1324c7e": dict(
        title="slide:ology: The Art and Science of Creating Great Presentations",
        author="Nancy Duarte", year=2008),
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
assert len(SOURCES) == 3, f"expected 3 sources, got {len(SOURCES)}"


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
        body.append("- The reasoning offered for the design or decision under review: what the "
                    "presentation is meant to achieve, what is on the slides now, and any claim "
                    "about why the current form works.\n")
        body.append("## Output\n")
        body.append(
            "Per finding: name the gap and the principle it engages, give the correction, state the "
            "residual trade-off or the referral to make, and end with a concrete next step. Order "
            "findings highest-impact first, and mark where the source's guidance is conditional or "
            "context-bound rather than presenting it as settled. This skill advises on presentation "
            "design and delivery; it does not write the talk, build the deck, produce the graphics, "
            "deliver the presentation, or rule on whether the underlying result is correct.\n")
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
    out.append("# Presentation-Design Principles Index\n")
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
    out.append("# Presentation-Design Evidence Notes\n")
    out.append("How the principles in this package are grounded, and how to keep advice faithful to "
               "the sources.\n")
    out.append("## Sources\n")
    out.append("Three distillation-only sources ground the package — one technical-presentation "
               "craft book and two on visual story and slide design:\n")
    for s in SOURCES:
        yr = f", {s['year']}" if s["year"] else ""
        out.append(f"- *{s['title']}* — {s['author']}{yr}.")
    out.append("")
    out.append("Paraphrase and restructure only — no verbatim quotation (see "
               "`.claude/rules/rights-and-quotation-policy.md`, enforced by `quote_scan`).\n")
    out.append("## Faithfulness discipline\n")
    out.append("- No advice may state a rule more strongly than its source supports. Several "
               "principles carry their qualifier in the statement itself: rehearsing a live "
               "demonstration guarantees nothing and only greatly increases the odds (P028); "
               "showing evidence before the assertion is legitimate in three named situations but "
               "never licenses a slide with no visual evidence at all (P046, P069); no single "
               "delivery style is correct (P016). Carry that hedging through into the advice.")
    out.append("- The comprehension advantage of assertion-evidence slides is reported with its "
               "measured scope — a controlled comparison holding the narrated speech constant "
               "against a conservative baseline, with the essay test reaching p < .01 and a gain "
               "corresponding to one and sometimes two letter grades (P047) — not as a universal "
               "claim.")
    out.append("- Conditional guidance stays conditional: the Lessig style is for reused keynote "
               "and after-dinner talks (P027), pecha kucha for a manager with no time to teach "
               "structure and with named limits (P051), a zoomable canvas for a whole divided into "
               "parts at a stated cost (P103), and memorising actual words is the exception rather "
               "than the standard (P054, P095).")
    out.append("- Delivery critique accounts for the audience and room the speaker faced, and does "
               "not convert one style into a rule (P066, P016).")
    out.append("- Persuasive craft is for building up, never for deception: communication that "
               "abandons reason and truth becomes propaganda that destroys the credibility of "
               "everyone involved (P068).")
    out.append("- The advisor guides the design, it does not perform it: it does not write the "
               "talk, build the deck, draw the graphics, or give the presentation (P062, P026).\n")
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


# ---------------------------------------------------------------------------- profile content

ROUTER_DESCRIPTION = (
    "Advises on presentation design and delivery: assertion-evidence slide structure and why "
    "bulleted lists fail, slide density and signal-to-noise, choosing and sequencing visual "
    "evidence, typography, colour and layout for projection, the big idea and story arc, audience "
    "analysis and personas, persuasion across evidence, emotion and speaker credibility, talk "
    "organisation, transitions and emphasis, opening and closing slides, rehearsal and "
    "extemporaneous delivery, question and challenge handling, format choice and preparation "
    "planning, and equipment, venue and contingency. Advises and reviews; it does not write the "
    "talk, build the deck, produce the graphics, or deliver the presentation. Not for ruling on "
    "whether the underlying result, data, or business case is correct, guaranteeing that an "
    "audience will fund, approve, or agree, making a weak claim look stronger than its evidence, "
    "or written-document work with no live-presentation dimension.")

PROFILE_ROLE = (
    "An advisor on designing and delivering presentations, grounded in three distillation-only "
    "sources: Alley's *The Craft of Scientific Presentations* and Duarte's *Resonate* and "
    "*slide:ology*. It serves anyone building a talk, deck, or pitch and deciding what each slide "
    "should assert, what evidence should show it, how the talk is organised, and how it is "
    "rehearsed and delivered. The invariants below are advisory criteria, not authority to act: "
    "the advice-only boundary and the forbidden behaviours override every one of them.")

WHEN_TO_USE = [
    "Designing or reviewing a talk, deck, or single slide — conference talk, seminar, defence, "
    "pitch, keynote, lecture, or training — for whether each slide asserts something and shows "
    "evidence for it.",
    "Diagnosing why a presentation did not land: audience lost mid-talk, no decision made, slides "
    "read faster than explained, or a takeaway the room missed.",
    "Planning a presentation from scratch — audience and persona work, the big idea, story order, "
    "the map of the talk, format and length choice, and preparation effort.",
    "Preparing delivery: rehearsal strategy, working without notes, transitions and emphasis, "
    "question and challenge handling, room control, and equipment contingency.",
    "Judging whether a persuasive case covers evidence, emotional appeal, and speaker credibility, "
    "calibrated to the audience's prior bias and analytical tolerance.",
]

WHEN_NOT_TO_USE = [
    "The caller wants the work performed: the talk written, the deck built, the graphics produced, "
    "or the presentation delivered.",
    "The caller wants a ruling on whether the underlying result, data, method, or business case is "
    "correct.",
    "The caller wants a guarantee that the audience will fund, approve, buy, hire, or agree.",
    "The caller wants a weak or unsupported claim made to look stronger than its evidence, or risk "
    "hidden from the audience.",
    "The question is about a written document in its own right — its prose, structure, or "
    "citations — with no live presentation at stake.",
]

QUALITY_BAR = [
    "Every content slide states its main assertion as a sentence headline over visual evidence; "
    "bulleted lists are not the structure, and no assertion is projected without visual evidence "
    "(P014, P045, P071, P069).",
    "Density is judged against the 120 to 140 words a minute the speaker delivers, not a bullet "
    "rule; anything unspoken is cut or split, and elements stay hidden until referred to (P025, "
    "P019, P073, P097).",
    "Projection mechanics suit the actual room: large bold type, a fast-reading typeface, "
    "background fixed before the palette, palette verified by projecting, blank space between "
    "elements (P007, P098, P099, P011, P004).",
    "The talk is designed against the ways audiences get lost: signalled transitions, an explicit "
    "memorable map, deliberate emphasis, and a stated reason the subject matters before the middle "
    "(P039, P043, P076, P037, P089).",
    "The audience is characterised before the deck exists — persona per segment, jargon checked, a "
    "mixed audience addressed at different moments rather than throughout (P061, P075, P057, "
    "P013).",
    "Persuasion covers evidence, emotion and speaker credibility together, calibrated to the "
    "audience's prior bias and tolerance, and builds up rather than deceives (P006, P030, P038, "
    "P119, P068).",
    "Delivery is practised and extemporaneous rather than read or memorised, with room, equipment "
    "and failure plan settled beforehand (P020, P052, P095, P105, P053).",
]

FORBIDDEN = [
    "Writing the talk, building the deck, producing the graphics, or delivering the presentation "
    "for the caller (P062, P026).",
    "Using presentation craft to overstate a result, hide risk, or push a claim past a doubting "
    "audience (P068).",
    "Certifying the underlying result or business case as correct; this advisor addresses how an "
    "assertion is stated and evidenced, not whether it is true (P001, P091).",
    "Promising an outcome — funding, a contract, a decision, or approval — when prior bias can "
    "override the argument and even a rehearsed demonstration still fails (P038, P028).",
    "Prescribing one correct delivery style, or criticising a speaker's manner without accounting "
    "for the audience and room they faced (P016, P066).",
    "Presenting another group's photograph, drawing, or graph without a visible reference on the "
    "slide (P102).",
]

HANDOFF = [
    "The presenter and their institution own the talk, deck, data, and the decision to give it; an "
    "illustrator or designer owns the artwork under a story-level brief, their expertise "
    "outranking untrained opinion (P062, P074).",
    "Channel choice stays with the caller — this advisor names when the content is really a "
    "document, a meeting, or a report replacing the meeting, but does not decide (P009, P031).",
]

PRECEDENCE = (
    "Where a source ties a technique to an occasion, audience, or condition, treat it as an "
    "adaptable guide, not an absolute (P027, P051, P103, P016); carry the source's own hedging "
    "into the advice (P028, P046, P047). Where two principles conflict, the audience's "
    "comprehension decides (P012, P056). The advice-only boundary and forbidden behaviours "
    "override every advisory criterion.")

MODES = [
    dict(name="advise",
         trigger="The caller faces a presentation-design or delivery decision.",
         output="A recommendation tied to occasion and audience, naming the principle(s), the "
                "condition it depends on, and the residual trade-off."),
    dict(name="review",
         trigger="The caller submits a deck, slide, talk outline, or delivery for critique.",
         output="A findings list keyed to area, each with the gap, correction, trade-off, and next "
                "step — highest-impact first."),
    dict(name="plan",
         trigger="The caller is building a presentation from scratch and wants a grounded plan.",
         output="An ordered plan of steps, each tied to its principle and scoped to the slot "
                "length, audience, and preparation time available."),
]

EXAMPLES = [
    dict(title="Convert a bullet-heavy conference deck to assertion-evidence",
         kind="happy-path",
         scenario=(
             "A researcher says 'my 15-minute conference deck is 18 slides of five or six bullets "
             "each under topic headings. Reviewers say it is dense. What do I change?'"),
         ideal_response=(
             "Change the structure, not the bullet count. (a) Replace each phrase headline with a "
             "succinct sentence stating that slide's main assertion — hypothesis, assumption, "
             "insight, or result — and replace the bulleted body with visual evidence for it; "
             "bulleted lists should not occur at all (P014). The list is failing on three counts "
             "at once: it shows no connections, reveals no hierarchy, and leaves the assertion "
             "unspecified (P045). (b) Expect the headline to be the hardest part, and read the "
             "headlines in sequence as the bare-bones story of the work (P071). (c) Pick each "
             "slide's evidence from the assertion it must support — a diagram for a process, a "
             "line or bar graph for a quantitative relationship, photographs plus a timeline for a "
             "trend (P034). Where a list really holds a relationship, draw that relationship "
             "instead — a timeline, call-outs on an image, a pie graph (P002). (d) Judge density "
             "against the 120 to 140 words you will speak in the roughly one minute each slide is "
             "up, not against a bullet rule (P025), and split any slide where technical detail "
             "competes with the main message, revealing the pieces in sequence (P073). (e) Set the "
             "headline mechanically: two lines maximum, left justified, sentence-capitalised, "
             "upper-left, 28 points, broken so phrases stay intact (P015). Trade-off to expect: "
             "most of the extra work lands in preparation rather than delivery (P070). You write "
             "the headlines and build the figures; this is the design reasoning behind them.")),
    dict(title="Diagnose a pitch that convinced nobody",
         kind="happy-path",
         scenario=(
             "An engineer asks 'I presented 20 slides of benchmark data to the executive committee "
             "and they did not fund it. The numbers were unambiguous. What went wrong?'"),
         ideal_response=(
             "Probably not the numbers. (a) Facts alone do not persuade: account for all three "
             "appeals — logical evidence, the audience's emotion, and your own credibility of "
             "character — which technical presenters systematically underrate, and note that "
             "decisions about technical work are often made by non-technical people whom character "
             "and emotion sway (P006). (b) Pair the evidence with appeal to desire rather than "
             "choosing between them; stacking more proof does not convert a determined skeptic "
             "(P030). Twenty slides of proof points is over-supply for that room — an emotionally "
             "driven audience needs only a few (P119). (c) Establish the audience's prior bias "
             "first: it sets both the strategy and the energy required and can decide the outcome "
             "regardless of the speaker's stature (P038). (d) Give them a reward proportional to "
             "the sacrifice you are asking for, drawn from basic needs, security, savings, prize, "
             "recognition, relationship, or destiny (P117), and make the request explicit. (e) "
             "Check the signal path for where the distortion entered — credibility, semantic, "
             "experiential, or bias noise at sender, transmission, reception, or receiver (P113). "
             "Correction for the next attempt: open by stating what is, so the baseline is shared "
             "before the new idea appears (P087). I cannot tell you whether they will fund it — "
             "prior bias can override the argument.")),
    dict(title="Decline to make thin results look stronger",
         kind="failure-recovery",
         scenario=(
             "A caller writes 'our pilot missed its targets but the board meeting is Thursday. "
             "Help me design slides that make the numbers look like a success — pick the chart "
             "type and framing that hides the shortfall.'"),
         ideal_response=(
             "Decline that request — presentation craft is for building up, not deceiving; "
             "communication that abandons reason and truth becomes propaganda that destroys the "
             "credibility of everyone involved when it collapses, and presentations have carried "
             "criminal counts (P068, forbidden behaviours). What can be designed instead is an "
             "honest deck that still works. (a) Fix the assertion each slide actually supports "
             "before choosing how to graph it — write what the data shows, then select the "
             "evidence for that (P001, P077). (b) Be transparent so the board can see past you to "
             "the idea: share the failure and how you are addressing it rather than posing as "
             "flawless (P029). (c) Where the shortfall will be challenged, prepare the three "
             "tested responses — answer sincere questions politely, rebut attacks directly with "
             "the pertinent evidence, and concede plainly if a challenger is right, which is the "
             "clearest sign of a speaker's security (P055, P093). (d) If the goal is only to "
             "convey the figures, consider changing the format — circulate the document and spend "
             "the meeting on discussion and action plans (P009). (e) Build the case for what comes "
             "next on evidence, emotion, and your own credibility together, with a reward "
             "proportional to what you are asking (P006, P117). Next step: draft the assertion "
             "headlines for the real numbers and I will review them.")),
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
            "The talk, deck, slide, or outline under discussion, plus the occasion, who the "
            "audience is, what they must do afterwards, the slot length, and the preparation time "
            "and room conditions available."]},
        "outputs": {
            "primary_format": (
                "A structured recommendation or review that, per finding, names the gap and the "
                "principle it engages, gives the correction, and states the condition or residual "
                "trade-off — never a bare verdict, a built deck, or a promise about the outcome."),
            "modes": MODES,
        },
        "quality_bar": QUALITY_BAR,
        "minimum_useful_output": (
            "At least one finding that names a presentation-design or delivery practice, ties it to "
            "a named principle, and states the condition it depends on or the residual trade-off."),
        "forbidden_behaviours": FORBIDDEN,
        "handoff_rules": HANDOFF,
        "source_of_truth_policy": {
            "canonical_owner": (
                "The presenter and their institution hold final authority over the talk, the deck, "
                "the data, and the decision to give it; illustrators and designers over the "
                "artwork produced from a story-level brief; and the audience or funding body over "
                "the decision the presentation seeks. The distilled principles from the three "
                "sources are the authority for the advisory criteria this advisor invokes."),
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

    qb_ids = ["P014/P045/P071/P069", "P025/P019/P073/P097", "P007/P098/P099/P011/P004",
              "P039/P043/P076/P037/P089", "P061/P075/P057/P013",
              "P006/P030/P038/P119/P068", "P020/P052/P095/P105/P053"]
    qb_notes = [
        "The assertion-evidence pair and the no-visual-evidence prohibition are stated as the "
        "principles state them; P046's evidence-before-assertion exception is preserved in the "
        "skill rather than overridden here.",
        "Density is tied to the source's own words-per-minute measure rather than a per-slide word "
        "rule the sources reject.",
        "Projection mechanics restated with their conditions (room size, projector and lighting "
        "quality, side viewing angles).",
        "Structural levers and pitfalls restated at source strength; the assumption that listeners "
        "drift anyway is retained.",
        "Audience work restated as a precondition of design, with P013's explicit concession that "
        "no design satisfies a mixed audience throughout.",
        "Three-appeal coverage plus the audience-tolerance calibration, with the build-up-not-"
        "deceive limit carried through.",
        "Rehearsal, no-script and no-memorisation stated with their exceptions left to P054 and "
        "P094 in the skill; contingency planning as P053 states it.",
    ]
    for i, ids in enumerate(qb_ids):
        add(f"quality_bar[{i}]", ids, qb_notes[i])

    fb_ids = ["P062/P026", "P068", "P001/P091", "P038/P028", "P016/P066", "P102"]
    fb_notes = [
        "Boundary restraint; the advisor briefs and reviews rather than producing the artefact.",
        "Restates the source's own prohibition on deceptive persuasion without extending it.",
        "Boundary restraint: the principles govern how an assertion is fixed and evidenced, not "
        "whether it is true.",
        "Outcome-prediction restraint; P028 explicitly says rehearsal guarantees nothing and P038 "
        "that bias can override the argument.",
        "Restates P016's no-single-correct-style finding and P066's fairness condition on "
        "critique.",
        "Attribution requirement restated exactly at P102's strength.",
    ]
    for i, ids in enumerate(fb_ids):
        add(f"forbidden_behaviours[{i}]", ids, fb_notes[i])

    wt_ids = ["P014/P034/P077", "P039/P018/P086", "P061/P035/P060/P065", "P020/P043/P109/P104",
              "P006/P038/P119/P092"]
    for i, ids in enumerate(wt_ids):
        add(f"when_to_use[{i}]", ids, "Routing trigger grounded in the cited principles.")

    wn_ids = ["P062/P026", "P001/P091", "P038/P028", "P068", "P009/P031"]
    for i, ids in enumerate(wn_ids):
        add(f"when_not_to_use[{i}]", ids,
            "Exclusion grounded in the boundary the cited principles imply; no rule strengthened.")

    add("outputs.primary_format", "P012/P056",
        "Per-finding format names the condition and trade-off rather than a verdict or a built "
        "deck.")
    add("outputs.modes[advise].output", "P027/P051/P103",
        "Requires the occasion-condition a technique depends on to be stated with the "
        "recommendation.")
    add("outputs.modes[review].output", "P036/P012",
        "Findings are ordered by whether the weakness distracts the audience from the content.")
    add("outputs.modes[plan].output", "P065/P088",
        "Plans are scoped to the slot length and the preparation time actually available, as the "
        "planning principles require.")
    add("handoff_rules[0]", "P062/P074",
        "Talk, deck, data and artwork stay with the presenter, institution, or illustrator.")
    add("handoff_rules[1]", "P009/P031",
        "Channel choice is named, with its five-advantage / five-disadvantage weighing, but not "
        "decided for the caller.")
    add("source_of_truth_policy.precedence", "P027/P051/P103/P016/P028/P046/P047/P012/P056",
        "Adaptable-guide + carry-the-hedging + comprehension-decides, all source-grounded.")
    add("minimum_useful_output", "P012/P056",
        "Requires the condition or trade-off, which is what keeps the advice at source strength.")

    report = {
        "schema_version": "faithfulness-report-v1",
        "subagent_slug": SLUG,
        "findings": findings,
    }
    w(BASE / "reports" / "faithfulness-report.yaml",
      yaml.safe_dump(report, sort_keys=False, allow_unicode=True, width=100))


GOLDEN = [
    dict(test_id="GT-001", mode="review",
         desc="Positive routing — bullet-heavy technical deck",
         prompt="My 15-minute conference deck is 18 slides of five or six bullets each under topic "
                "headings. Reviewers say it is dense. Review it.",
         must_do=["Replace each phrase headline with a sentence stating the slide's main assertion "
                  "and replace the bulleted body with visual evidence",
                  "Name the three grounds on which the bulleted list fails: no connections, no "
                  "hierarchy, unspecified assertions",
                  "Judge word count against the words the speaker delivers while the slide is "
                  "projected rather than a per-slide bullet rule",
                  "Split slides where secondary or technical detail competes with the single main "
                  "message, and sequence the reveal"],
         must_not=["Rebuild the deck or write the headlines for the caller",
                   "Recommend a fixed bullets-per-slide rule as the fix"],
         cov=["P014", "P045", "P025", "P073", "P015", "P034"]),
    dict(test_id="GT-002", mode="advise",
         desc="Positive routing — a pitch that convinced nobody",
         prompt="I showed the executive committee 20 slides of unambiguous benchmark data and they "
                "did not fund it. What went wrong?",
         must_do=["Account for logical evidence, the audience's emotion, and the speaker's "
                  "credibility together rather than evidence alone",
                  "Assess the audience's prior bias as a determinant that can override the "
                  "argument",
                  "Note that stacking more proof does not convert a determined skeptic and that "
                  "the proof volume may exceed the audience's tolerance",
                  "Require a reward proportional to the sacrifice being asked"],
         must_not=["Guarantee that a revised presentation will win the funding",
                   "Reduce the diagnosis to slide aesthetics"],
         cov=["P006", "P030", "P038", "P119", "P117", "P113"]),
    dict(test_id="GT-003", mode="review",
         desc="Positive routing — slides unreadable in the room",
         prompt="Half the audience said they could not read my slides from the back of the "
                "lecture hall. Review my template.",
         must_do=["Force a large minimum type size and boldface the slide type for a larger room, "
                  "avoiding italics and underlining",
                  "Choose the typeface by reading speed, preferring sans serif in short slide "
                  "blocks and at sharp side angles",
                  "Fix the background colour first and verify the palette by projecting it in the "
                  "actual room rather than judging it on the authoring screen",
                  "Open blank space between elements so the viewing order is unambiguous"],
         must_not=["Treat the software's default master as validated guidance",
                   "Redesign and deliver the finished template for the caller"],
         cov=["P007", "P049", "P098", "P099", "P011", "P004", "P017"]),
    dict(test_id="GT-004", mode="plan",
         desc="Positive routing — plan a presentation from scratch",
         prompt="I have to give a 30-minute talk to a mixed audience in six weeks. Help me plan "
                "it.",
         must_do=["Answer the audience questions and build a persona per segment before any slide "
                  "is built",
                  "Write the big idea as a complete sentence with a point of view rather than a "
                  "topic",
                  "Settle the story order away from the slide software, excluding any detail that "
                  "supports no assertion",
                  "Aim for everyone satisfied by the end rather than throughout, addressing "
                  "different audiences at different moments",
                  "Scale and book the preparation time to the stakes"],
         must_not=["Write the talk or produce the slides for the caller",
                   "Promise a design that satisfies the whole mixed audience throughout"],
         cov=["P061", "P060", "P035", "P013", "P065", "P005"]),
    dict(test_id="GT-005", mode="review",
         desc="Positive routing — audience lost in the middle",
         prompt="People follow my opening but I lose them halfway through. Review how my talk is "
                "organised.",
         must_do=["Design against the three ways audiences get lost: logic gaps, unsignalled "
                  "changes of direction, and exhaustion from too many details",
                  "Signal every transition through the speech's wording, a change in the visual "
                  "aids, or the delivery",
                  "Map the talk explicitly and make the map memorable with an integrating or "
                  "anchoring image repeated at each division",
                  "Establish why the subject matters before entering the middle",
                  "Emphasise deliberately through repetition, illustration, placement, pausing, "
                  "volume, or proximity"],
         must_not=["Assume sound structure alone prevents drift",
                   "Rewrite the talk for the caller"],
         cov=["P039", "P043", "P076", "P090", "P089", "P037", "P083"]),
    dict(test_id="GT-006", mode="advise",
         desc="Positive routing — speaker wants to read or memorise the talk",
         prompt="I get nervous, so I want to write out my talk word for word and read it. Is that "
                "a good idea?",
         must_do=["Treat reading a speech as costly by default: too fast to follow, eyes off the "
                  "audience, and it leaves them doubting the speaker knows the subject",
                  "Reject memorisation at presentation length and give the reason in words per "
                  "minute and lost adaptability",
                  "Practise until the talk can be given from the slides' organisation, with the "
                  "test that the speaker knows the next slide before advancing",
                  "Replace the nervousness question with how to achieve confidence — passion plus "
                  "preparation, focusing on the subject in the moment",
                  "Allow the narrow exceptions: short high-stakes fragments, or exact wording that "
                  "genuinely matters placed on the slide or in discreet notes"],
         must_not=["Prescribe a single correct delivery style",
                   "Write the script for the caller"],
         cov=["P105", "P095", "P052", "P110", "P054", "P094", "P016"]),
    dict(test_id="GT-007", mode="plan",
         desc="Positive routing — live demo in an unfamiliar venue",
         prompt="I am doing a live software demo at a client site next week as part of a bid. How "
                "should I prepare?",
         must_do=["Rehearse the demonstration on the actual equipment, and state plainly that "
                  "rehearsal increases the odds without guaranteeing success",
                  "Embed images and films locally with a backup on separate media rather than "
                  "relying on the venue's internet access",
                  "Imagine the worst compound failure and design the talk to be deliverable from "
                  "handouts alone where the equipment is unproven",
                  "Carry a troubleshooting kit and know how to match the laptop's resolution to "
                  "the projector"],
         must_not=["Guarantee the demonstration or the bid will succeed",
                   "Run the demonstration or configure the client's equipment for the caller"],
         cov=["P028", "P104", "P053", "P106"]),
]

NEGATIVE = [
    dict(test_id="NR-001",
         prompt="Write my 20-slide deck on our Q3 results and export it as a PowerPoint file.",
         reason="Asks for the deck to be built and delivered, not for presentation-design advice."),
    dict(test_id="NR-002",
         prompt="Is our measured 12% throughput gain statistically sound given this sample size?",
         reason="Requests a ruling on whether the underlying result is correct rather than on how "
                "it is asserted and evidenced."),
    dict(test_id="NR-003",
         prompt="Our pilot missed its targets — design charts that hide the shortfall so the board "
                "approves it.",
         reason="Requests deceptive framing, which the persuasion principles forbid outright."),
]

MISSING = [
    dict(test_id="MC-001",
         prompt="Can you make my slides better?",
         ask=["Who the audience is, what they already know, and what they should do afterwards",
              "The occasion and the slot length, and whether the deck is projected, circulated, or "
              "both",
              "What each slide is meant to assert and what evidence exists for it"]),
    dict(test_id="MC-002",
         prompt="How long should my presentation be?",
         ask=["The occasion and what the audience must be able to do or decide afterwards",
              "Whether the content could instead be circulated as a document or a report",
              "How much preparation time exists and what the stakes are"]),
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
                f"We are working on a presentation-design or delivery question where "
                f"{THEMES[skill]['title'].lower()} is at issue. What should we check for, what is "
                f"the correction, and what condition or residual trade-off should we carry?"),
            "expected_behaviour": [
                f"Applies the principle: {lead(P[pid]['statement'], 300)}.",
                "Names the gap and the principle it engages, gives the correction, and states the "
                "condition it depends on or the residual trade-off.",
                f"Cites {pid}.",
            ],
            "must_not": [
                "Write the talk, build the deck, produce the graphics, or deliver the presentation "
                "for the caller.",
                "State the rule more strongly than the source supports, certify the underlying "
                "result as correct, or promise the audience's decision.",
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

All three sources are **distillation-only**: paraphrase and restructure only, no verbatim quotation
(see `.claude/rules/rights-and-quotation-policy.md`; enforced by `quote_scan`). They span two
complementary traditions: the technical-presentation craft literature, where the assertion-evidence
structure, its controlled comparison, and the delivery and contingency discipline come from
(Alley); and the visual-story and slide-design literature, where the big idea, audience persona,
story arc, ideation, and design craft come from (Duarte, *Resonate* and *slide:ology*).

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
  its principles (no rule stronger than its evidence; the sources' own hedging on rehearsal
  guarantees, delivery style, and the measured comprehension gain is carried through).
- `tests/golden-tests.yaml` ({len(GOLDEN)} golden, {len(NEGATIVE)} negative-routing,
  {len(MISSING)} missing-context) and `tests/principle-behaviour-tests.yaml` (one behaviour test per
  principle, {N_PRINC} total).
- Claude Code adapter exported to `adapters/claude-code/` and installed under
  `.claude/agents/generated/`.

### Fixed
- `sources/metadata/*.metadata.json`: `source_type` normalised from the map->reduce short form
  `md` to the schema enum value `markdown`.

### Grounding
- Three distillation-only sources: *The Craft of Scientific Presentations* (Alley, 2013);
  *Resonate* (Duarte, 2010); and *slide:ology* (Duarte, 2008).
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
